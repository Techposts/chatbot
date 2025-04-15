import smtplib
import streamlit as st
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_lead_notification(lead_data):
    """Send an email notification about a new lead."""
    
    # Check if email settings are configured
    if not all(key in st.secrets for key in ["EMAIL_SENDER", "EMAIL_PASSWORD", "EMAIL_RECIPIENT"]):
        print("Email settings not configured in secrets.toml")
        return {"success": False, "error": "Email settings not configured"}
    
    sender_email = st.secrets["EMAIL_SENDER"]
    password = st.secrets["EMAIL_PASSWORD"]
    recipient_email = st.secrets["EMAIL_RECIPIENT"]
    
    # Create message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "New Lead Captured on Anaptyss Chatbot"
    
    # Format lead information
    lead_name = lead_data.get('name', 'N/A')
    lead_email = lead_data.get('email', 'N/A')
    lead_company = lead_data.get('company', 'N/A')
    lead_interest = lead_data.get('interest', 'N/A')
    lead_timestamp = lead_data.get('timestamp', 'N/A')
    
    # Create HTML body
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 5px;">
            <h2 style="color: #2563eb; border-bottom: 1px solid #e0e0e0; padding-bottom: 10px;">New Lead Captured!</h2>
            
            <table style="width: 100%; border-collapse: collapse;">
                <tr>
                    <td style="padding: 8px; font-weight: bold; width: 120px;">Name:</td>
                    <td style="padding: 8px;">{lead_name}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; font-weight: bold;">Email:</td>
                    <td style="padding: 8px;"><a href="mailto:{lead_email}">{lead_email}</a></td>
                </tr>
                <tr>
                    <td style="padding: 8px; font-weight: bold;">Company:</td>
                    <td style="padding: 8px;">{lead_company}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; font-weight: bold;">Interest:</td>
                    <td style="padding: 8px;">{lead_interest}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; font-weight: bold;">Timestamp:</td>
                    <td style="padding: 8px;">{lead_timestamp}</td>
                </tr>
            </table>
            
            <div style="background-color: #f0f4ff; padding: 15px; margin-top: 20px; border-radius: 5px;">
                <p style="margin: 0;">This lead was captured through the Anaptyss AI Chatbot.</p>
                <p style="margin-top: 10px; margin-bottom: 0;">Please follow up with this lead as soon as possible!</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Attach HTML part
    html_part = MIMEText(html_body, "html")
    message.attach(html_part)
    
    # Send the email
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(message)
        server.quit()
        return {"success": True}
    except Exception as e:
        print(f"Failed to send email notification: {e}")
        return {"success": False, "error": str(e)}
