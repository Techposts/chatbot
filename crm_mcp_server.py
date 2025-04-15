# backend/crm_mcp_server.py
import asyncio
import json
import sys
import os
from datetime import datetime

# A simple file-based lead storage
LEADS_FILE = "leads.json"

# Load existing leads
def load_leads():
    if os.path.exists(LEADS_FILE):
        try:
            with open(LEADS_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

# Save leads to file
def save_leads(leads):
    with open(LEADS_FILE, 'w') as f:
        json.dump(leads, f, indent=2)

# MCP protocol handlers
async def handle_mcp_request(request):
    try:
        if request["type"] == "tools_list":
            return handle_tools_list()
        elif request["type"] == "tool_call":
            return await handle_tool_call(request)
        else:
            return {"type": "error", "error": f"Unknown request type: {request['type']}"}
    except Exception as e:
        return {"type": "error", "error": str(e)}

def handle_tools_list():
    # Define the tools this MCP server provides
    return {
        "type": "tools_list",
        "tools": [
            {
                "name": "save_lead",
                "description": "Save a new lead to the CRM system",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Full name of the lead"},
                        "email": {"type": "string", "description": "Email address of the lead"},
                        "company": {"type": "string", "description": "Company name (optional)"},
                        "phone": {"type": "string", "description": "Phone number (optional)"},
                        "interest": {"type": "string", "description": "What the lead is interested in"},
                        "notes": {"type": "string", "description": "Additional notes about the lead"}
                    },
                    "required": ["name", "email", "interest"]
                }
            },
            {
                "name": "check_lead_exists",
                "description": "Check if a lead with the given email already exists in the system",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string", "description": "Email address to check"}
                    },
                    "required": ["email"]
                }
            }
        ]
    }

async def handle_tool_call(request):
    tool_name = request.get("name", "")
    params = request.get("parameters", {})
    
    if tool_name == "save_lead":
        # Validate required fields
        if not all(key in params for key in ["name", "email", "interest"]):
            return {
                "type": "tool_call_result",
                "result": {
                    "success": False,
                    "message": "Missing required fields: name, email, and interest are required"
                }
            }
        
        # Load existing leads
        leads = load_leads()
        
        # Check if lead already exists
        existing_lead = next((lead for lead in leads if lead.get("email") == params["email"]), None)
        
        if existing_lead:
            # Update existing lead
            existing_lead.update(params)
            existing_lead["updated_at"] = datetime.now().isoformat()
            message = "Lead information updated"
        else:
            # Add new lead
            lead = {
                **params,
                "created_at": datetime.now().isoformat(),
                "source": "chatbot"
            }
            leads.append(lead)
            message = "New lead saved successfully"
        
        # Save updated leads
        save_leads(leads)
        
        return {
            "type": "tool_call_result",
            "result": {
                "success": True,
                "message": message
            }
        }
    
    elif tool_name == "check_lead_exists":
        if "email" not in params:
            return {
                "type": "tool_call_result",
                "result": {
                    "success": False,
                    "message": "Email parameter is required"
                }
            }
        
        leads = load_leads()
        exists = any(lead.get("email") == params["email"] for lead in leads)
        
        return {
            "type": "tool_call_result",
            "result": {
                "exists": exists,
                "success": True
            }
        }
    
    else:
        return {
            "type": "error",
            "error": f"Unknown tool: {tool_name}"
        }

async def main():
    while True:
        try:
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
                
            request = json.loads(line)
            response = await handle_mcp_request(request)
            
            print(json.dumps(response), flush=True)
        except Exception as e:
            error_response = {"type": "error", "error": str(e)}
            print(json.dumps(error_response), flush=True)

if __name__ == "__main__":
    asyncio.run(main())
