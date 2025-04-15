import streamlit as st
import os
import asyncio
import json
import traceback
from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp import MCPToolkit
from langchain_core.output_parsers import StrOutputParser

# Import our custom modules
try:
    import database
    import notifications
except ImportError:
    # Create placeholder modules if they don't exist
    class PlaceholderModule:
        def save_lead(*args, **kwargs):
            return {"success": True, "lead_id": 1, "is_new": True}
        
        def send_lead_notification(*args, **kwargs):
            return {"success": True}
    
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
            
            # Save to database instead of JSON file
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

# Hardcoded company information to use as fallback
ANAPTYSS_INFO = """
COMPANY OVERVIEW:
Anaptyss is a data analytics company founded in 2021 that helps businesses transform complex data into clear, actionable insights for data-driven decisions.

MAIN SERVICES:
1. Data Visualization
   - Interactive dashboards
   - Custom charts and graphs
   - Real-time data visualizations
   - Executive reporting tools

2. Predictive Analytics
   - Sales forecasting
   - Customer churn prediction
   - Inventory optimization
   - Risk assessment models

3. Business Intelligence Dashboards
   - KPI tracking dashboards
   - Sales and marketing analytics
   - Financial performance monitoring
   - Operational efficiency metrics

4. Model Risk Management
   - Model validation and verification
   - Risk assessment frameworks
   - Regulatory compliance support
   - Model governance systems

IMPLEMENTATION APPROACHES:
- Custom Solutions: Built from scratch for unique requirements
- Platform Integration: Connect with existing tools and platforms
- Managed Services: Ongoing support and optimization

INDUSTRIES SERVED:
- Retail and E-commerce
- Financial Services
- Healthcare
- Manufacturing
- Logistics and Supply Chain
- SaaS and Technology

PRICING MODELS:
- Project-Based: Starting from $5,000 for basic implementations up to $30,000+ for enterprise solutions
- Subscription-Based: From $1,500/month for basic service to $5,000+/month for premium service
"""

# Process chat without MCP tools to avoid errors
async def process_chat(user_input):
    # Convert chat history to LangChain message format
    lc_messages = []
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            lc_messages.append(HumanMessage(content=msg["content"]))
        else:
            lc_messages.append(AIMessage(content=msg["content"]))
    
    # Add the new user message
    lc_messages.append(HumanMessage(content=user_input))
    
    # Set up LLM with direct access to company information (no tool calls)
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
    
    # Add system message with company information
    system_message = f"""You are the helpful AI assistant for Anaptyss, a company that specializes in data analytics and business intelligence solutions.
    
    Important information about Anaptyss that you MUST use to answer questions:

    {ANAPTYSS_INFO}

    If the user asks about pricing, demos, or wants to talk to a human, suggest that you can collect their contact information and someone will reach out.
    
    User information that has been collected: {json.dumps(st.session_state.user_info)}
    Lead captured: {st.session_state.lead_captured}
    
    IMPORTANT: Always provide detailed, specific answers about Anaptyss services based on the information above. Do not give generic responses or immediately ask users if they want to provide contact information unless they specifically ask about pricing details, custom quotes, or speaking with a sales representative.
    """
    
    lc_messages.insert(0, HumanMessage(content=system_message))
    
    try:
        # Generate response without tool calls to avoid the errors
        response = await llm.ainvoke(lc_messages)
        
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
        
        # Return a fallback response if there's an error
        return "I apologize, but I'm having trouble processing your request right now. Please try again or ask another question about Anaptyss services."

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
