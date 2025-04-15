import streamlit as st
import os
import asyncio
import json
import traceback
from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp import MCPToolkit
from langchain_core.output_parsers import StrOutputParser
from langchain.tools import StructuredTool

# Import our custom modules
try:
    import database
    import notifications
    from vector_store import VectorStore
    from wordpress_fetcher import WordPressFetcher
    from mcp_handler import MCPHandler
    from api_actions import APIActions
except ImportError as e:
    st.error(f"Error importing required modules: {e}")
    # Create placeholder modules if they don't exist
    class PlaceholderModule:
        def save_lead(*args, **kwargs):
            return {"success": True, "lead_id": 1, "is_new": True}
        
        def send_lead_notification(*args, **kwargs):
            return {"success": True"}
    
    database = PlaceholderModule()
    notifications = PlaceholderModule()

# Configure page
st.set_page_config(
    page_title="Anaptyss AI Assistant",
    page_icon="💬",
    layout="centered"
)

# Set OpenAI API key from Streamlit secrets
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Custom CSS for better appearance
st.markdown("""
<style>
    .chat-message {
        padding: 1.5rem; 
        border-radius: 0.5rem; 
        margin-bottom: 1rem; 
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #2b313e;
        color: #ffffff;
        border-bottom-right-radius: 0;
    }
    .chat-message.assistant {
        background-color: #f0f2f6;
        border-bottom-left-radius: 0;
    }
    .chat-message .avatar {
        width: 20%;
    }
    .chat-message .content {
        width: 80%;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 12px;
    }
    .lead-form {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi there! I'm the Anaptyss AI assistant. How can I help you today?"}
    ]

if "lead_captured" not in st.session_state:
    st.session_state.lead_captured = False

if "user_info" not in st.session_state:
    st.session_state.user_info = {}

if "showing_lead_form" not in st.session_state:
    st.session_state.showing_lead_form = False

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "wp_fetcher" not in st.session_state:
    st.session_state.wp_fetcher = None

if "api_actions" not in st.session_state:
    st.session_state.api_actions = None

# Initialize components
@st.cache_resource
def initialize_components():
    # WordPress site URL - replace with your actual WordPress site URL
    wp_url = "https://anaptyss.com"
    
    # Initialize vector store
    vector_store = VectorStore()
    
    # Initialize WordPress fetcher
    wp_fetcher = WordPressFetcher(wp_url)
    
    # Initialize API actions
    api_actions = APIActions(wp_url)
    
    return vector_store, wp_fetcher, api_actions

# Initialize components
vector_store, wp_fetcher, api_actions = initialize_components()
st.session_state.vector_store = vector_store
st.session_state.wp_fetcher = wp_fetcher
st.session_state.api_actions = api_actions

# Lead capture form
def display_lead_form():
    st.markdown("### To better assist you, please provide your contact information:")
    
    with st.form(key="lead_form", clear_on_submit=True):
        name = st.text_input("Name")
        email = st.text_input("Email")
        company = st.text_input("Company (optional)")
        interest = st.text_area("What are you interested in?")
        
        submit_button = st.form_submit_button(label="Submit")
        
        if submit_button and name and email:
            lead_data = {
                "name": name,
                "email": email,
                "company": company,
                "interest": interest,
                "source": "streamlit_chatbot",
                "timestamp": datetime.now().isoformat()
            }
            
            # Save to database 
            result = database.save_lead(lead_data)
            
            if result["success"]:
                # Send email notification
                notifications.send_lead_notification(lead_data)
                
                st.session_state.lead_captured = True
                st.session_state.user_info = lead_data
                st.session_state.showing_lead_form = False
                
                # Add acknowledgment message
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": f"Thanks {name}! Someone from our team will reach out to you soon about your interest in {interest}. In the meantime, how else can I help you?"
                })
                
                st.rerun()
            else:
                st.error(f"There was an error saving your information: {result.get('error', 'Please try again.')}")

# Function to fetch relevant documents from vector store
def get_relevant_documents(query):
    try:
        docs = st.session_state.vector_store.similar_docs(query)
        return "\n\n".join([doc.page_content for doc in docs])
    except Exception as e:
        print(f"Error getting relevant documents: {e}")
        return ""

# Define tools for LangChain
def get_tools():
    tools = [
        StructuredTool.from_function(
            func=lambda name, email, company, preferred_date: api_actions.schedule_demo(name, email, company, preferred_date),
            name="schedule_demo",
            description="Schedule a product demo for a potential customer",
            args_schema={
                "name": {"type": "string", "description": "Full name of the customer"},
                "email": {"type": "string", "description": "Email address of the customer"},
                "company": {"type": "string", "description": "Company name (optional)"},
                "preferred_date": {"type": "string", "description": "Preferred date for the demo"}
            },
            return_direct=False
        ),
        StructuredTool.from_function(
            func=lambda industry=None, limit=3: api_actions.get_latest_case_studies(industry, limit),
            name="get_latest_case_studies",
            description="Get the latest case studies from our WordPress site",
            args_schema={
                "industry": {"type": "string", "description": "Industry to filter case studies by (optional)"},
                "limit": {"type": "integer", "description": "Number of case studies to return (default: 3)"}
            },
            return_direct=False
        )
    ]
    return tools

# Enhanced chat processing with hybrid approach
async def process_chat(user_input):
    # Get relevant documents from vector store
    relevant_docs = get_relevant_documents(user_input)
    
    # Convert chat history to LangChain message format
    lc_messages = []
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            lc_messages.append(HumanMessage(content=msg["content"]))
        else:
            lc_messages.append(AIMessage(content=msg["content"]))
    
    # Add the new user message
    lc_messages.append(HumanMessage(content=user_input))
    
    # Set up LLM
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
    
    # Add system message with company information and relevant docs
    system_message = f"""You are the helpful AI assistant for Anaptyss, a company that specializes in data analytics and business intelligence solutions.

    Based on the user's query, I've found the following relevant information from our knowledge base:
    
    {relevant_docs}
    
    User information that has been collected: {json.dumps(st.session_state.user_info)}
    Lead captured: {st.session_state.lead_captured}
    
    IMPORTANT: Use the information above to provide detailed, specific answers about Anaptyss services. If the information doesn't fully address the query, you can use your general knowledge about data analytics and business intelligence while staying consistent with Anaptyss's offerings.
    
    If the user asks about pricing, demos, or wants to talk to a human, suggest that you can collect their contact information and someone will reach out. 
    
    You can use tools to perform actions for the user. Available tools:
    1. schedule_demo - To schedule a product demo
    2. get_latest_case_studies - To retrieve recent case studies from our website
    """
    
    lc_messages.insert(0, SystemMessage(content=system_message))
    
    try:
        # Setup MCP client session
        async with stdio_client(StdioServerParameters()) as session:
            # Setup MCP filesystem
            mcp_handler = MCPHandler(session)
            await mcp_handler.setup_filesystem()
            
            # Create MCP toolkit
            mcp_toolkit = MCPToolkit(session=session)
            
            # Add tools to LangChain
            tools = get_tools()
            
            # Generate response with tools
            response = await llm.ainvoke(
                lc_messages,
                tools=tools + [mcp_toolkit.read_file, mcp_toolkit.list_files]
            )
            
            # Get final response as string
            final_response = response.content
            
            # Check if we should show the lead form
            if (
                not st.session_state.lead_captured and 
                not st.session_state.showing_lead_form and 
                any(keyword in user_input.lower() or keyword in final_response.lower() 
                    for keyword in ["price", "pricing", "demo", "contact", "talk to", "sales", "representative"])
            ):
                st.session_state.showing_lead_form = True
            
            return final_response
    
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        traceback_str = traceback.format_exc()
        print(f"Traceback: {traceback_str}")
        
        # Fallback to simple response without MCP or tools
        try:
            response = await llm.ainvoke(lc_messages)
            return response.content
        except:
            # Ultimate fallback response
            return "I apologize, but I'm having trouble processing your request right now. Please try again or ask another question about Anaptyss services."

# Function to refresh WordPress content (can be triggered periodically)
def refresh_wordpress_content():
    with st.spinner("Refreshing WordPress content..."):
        wp_fetcher = st.session_state.wp_fetcher
        wp_fetcher.fetch_all_content()
        
        # Update vector store with new WordPress content
        vector_store = st.session_state.vector_store
        vector_store.init_vector_store()
    
    st.success("WordPress content refreshed successfully!")

# Display chat messages
def display_chat():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Main app
def main():
    # App title and description
    st.title("Anaptyss AI Assistant")
    st.markdown("I can help answer questions about our data analytics and business intelligence solutions.")
    
    # Admin section for refreshing content (can be hidden in production)
    with st.expander("Admin Controls", expanded=False):
        if st.button("Refresh WordPress Content"):
            refresh_wordpress_content()
    
    # Display the current conversation
    display_chat()
    
    # Display lead form if needed
    if st.session_state.showing_lead_form and not st.session_state.lead_captured:
        display_lead_form()
    
    # Get user input
    user_input = st.chat_input("Type your message here...")
    
    if user_input:
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display the updated chat including the new user message
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Process the chat and get response
                response = asyncio.run(process_chat(user_input))
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
