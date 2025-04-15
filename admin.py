import streamlit as st
import pandas as pd
from datetime import datetime
import database
import os

# Simple authentication
def check_password():
    """Returns `True` if the user had the correct password."""
    if "password_correct" not in st.session_state:
        # First run, show input for password
        st.session_state.password_correct = False
        
    if not st.session_state.password_correct:
        # Get admin password from secrets or environment
        admin_password = st.secrets.get("ADMIN_PASSWORD", os.environ.get("ADMIN_PASSWORD", "admin"))
        
        # Show input for password
        password = st.text_input("Enter admin password", type="password")
        
        if password:
            if password == admin_password:
                st.session_state.password_correct = True
                return True
            else:
                st.error("Incorrect password")
                return False
        else:
            return False
    else:
        # Password was correct
        return True

def main():
    st.set_page_config(
        page_title="Anaptyss Lead Management",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Anaptyss Lead Management")
    
    if not check_password():
        st.stop()  # Don't run the rest of the app if password check fails
    
    # Get leads from database
    leads = database.get_all_leads()
    
    # Display overview metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            label="Total Leads", 
            value=len(leads)
        )
    
    with col2:
        new_leads = sum(1 for lead in leads if not lead['contacted'])
        st.metric(
            label="New Leads", 
            value=new_leads
        )
    
    with col3:
        contacted_leads = sum(1 for lead in leads if lead['contacted'])
        st.metric(
            label="Contacted Leads", 
            value=contacted_leads
        )
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["All Leads", "Export Data"])
    
    with tab1:
        if not leads:
            st.info("No leads captured yet.")
        else:
            # Convert to dataframe for easier display
            df = pd.DataFrame(leads)
            
            # Format timestamp
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
            
            # Add actions column
            for index, lead in enumerate(leads):
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    with st.expander(f"📌 {lead['name']} - {lead['email']} ({lead['company'] or 'No company'})"):
                        st.write(f"**Interest:** {lead['interest']}")
                        st.write(f"**Notes:** {lead['notes'] or 'None'}")
                        st.write(f"**Source:** {lead['source']}")
                        st.write(f"**Timestamp:** {lead['timestamp']}")
                        
                        # Add actions
                        if not lead['contacted']:
                            if st.button(f"Mark as Contacted", key=f"contact_{lead['id']}"):
                                result = database.mark_lead_as_contacted(lead['id'])
                                if result['success']:
                                    st.success("Lead marked as contacted!")
                                    st.rerun()
                                else:
                                    st.error(f"Error: {result.get('error', 'Unknown error')}")
                        else:
                            st.info("✓ Lead has been contacted")
                        
                        # Add delete button
                        if st.button(f"Delete Lead", key=f"delete_{lead['id']}"):
                            result = database.delete_lead(lead['id'])
                            if result['success']:
                                st.success("Lead deleted!")
                                st.rerun()
                            else:
                                st.error(f"Error: {result.get('error', 'Unknown error')}")
                
                # Add separator
                st.divider()
    
    with tab2:
        st.subheader("Export Leads")
        
        if not leads:
            st.info("No leads to export.")
        else:
            # Convert to dataframe for export
            df = pd.DataFrame(leads)
            
            # Format timestamp
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
            
            # Generate CSV
            csv = df.to_csv(index=False)
            
            # Generate Excel
            excel_file = "leads_export.xlsx"
            df.to_excel(excel_file, index=False, engine='openpyxl')
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"anaptyss_leads_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                )
            
            with col2:
                with open(excel_file, "rb") as file:
                    st.download_button(
                        label="Download Excel",
                        data=file,
                        file_name=f"anaptyss_leads_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )

if __name__ == "__main__":
    main()
