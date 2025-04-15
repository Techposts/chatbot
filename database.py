import sqlite3
import os
import json
from datetime import datetime

# Database path
DB_PATH = "leads.db"

def init_db():
    """Initialize the database with the required tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create leads table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        company TEXT,
        interest TEXT,
        notes TEXT,
        source TEXT,
        timestamp TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        contacted BOOLEAN DEFAULT 0
    )
    ''')
    
    # Create a unique index on email to avoid duplicates
    cursor.execute('''
    CREATE UNIQUE INDEX IF NOT EXISTS idx_leads_email ON leads(email)
    ''')
    
    conn.commit()
    conn.close()
    
    print("Database initialized successfully.")
    
    # Import existing leads from leads.json if it exists
    import_existing_leads()

def import_existing_leads():
    """Import leads from the existing leads.json file if it exists."""
    if os.path.exists('leads.json'):
        try:
            with open('leads.json', 'r') as f:
                leads = json.load(f)
                
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            for lead in leads:
                try:
                    cursor.execute('''
                    INSERT OR IGNORE INTO leads 
                    (name, email, company, interest, source, timestamp) 
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        lead.get('name', ''),
                        lead.get('email', ''),
                        lead.get('company', ''),
                        lead.get('interest', ''),
                        lead.get('source', 'imported'),
                        lead.get('timestamp', datetime.now().isoformat())
                    ))
                except Exception as e:
                    print(f"Error importing lead {lead.get('email')}: {e}")
            
            conn.commit()
            conn.close()
            print(f"Imported existing leads from leads.json")
            
            # Rename the old file as backup
            os.rename('leads.json', 'leads.json.backup')
        except Exception as e:
            print(f"Error importing leads from leads.json: {e}")

def save_lead(lead_data):
    """Save a new lead to the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if lead with this email already exists
        cursor.execute("SELECT id FROM leads WHERE email = ?", (lead_data.get('email'),))
        existing_lead = cursor.fetchone()
        
        if existing_lead:
            # Update existing lead
            cursor.execute('''
            UPDATE leads
            SET name = ?, company = ?, interest = ?, notes = ?, timestamp = ?
            WHERE email = ?
            ''', (
                lead_data.get('name', ''),
                lead_data.get('company', ''),
                lead_data.get('interest', ''),
                lead_data.get('notes', ''),
                datetime.now().isoformat(),
                lead_data.get('email')
            ))
            lead_id = existing_lead[0]
            is_new = False
        else:
            # Insert new lead
            cursor.execute('''
            INSERT INTO leads
            (name, email, company, interest, notes, source, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                lead_data.get('name', ''),
                lead_data.get('email', ''),
                lead_data.get('company', ''),
                lead_data.get('interest', ''),
                lead_data.get('notes', ''),
                lead_data.get('source', 'chatbot'),
                datetime.now().isoformat()
            ))
            lead_id = cursor.lastrowid
            is_new = True
        
        conn.commit()
        conn.close()
        
        return {"success": True, "lead_id": lead_id, "is_new": is_new}
    except Exception as e:
        print(f"Error saving lead: {e}")
        return {"success": False, "error": str(e)}

def get_all_leads():
    """Get all leads from the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # This enables column access by name
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT * FROM leads ORDER BY created_at DESC
        ''')
        
        leads = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return leads
    except Exception as e:
        print(f"Error getting leads: {e}")
        return []

def mark_lead_as_contacted(lead_id):
    """Mark a lead as contacted."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
        UPDATE leads
        SET contacted = 1
        WHERE id = ?
        ''', (lead_id,))
        
        conn.commit()
        conn.close()
        
        return {"success": True}
    except Exception as e:
        print(f"Error marking lead as contacted: {e}")
        return {"success": False, "error": str(e)}

def delete_lead(lead_id):
    """Delete a lead from the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
        DELETE FROM leads
        WHERE id = ?
        ''', (lead_id,))
        
        conn.commit()
        conn.close()
        
        return {"success": True}
    except Exception as e:
        print(f"Error deleting lead: {e}")
        return {"success": False, "error": str(e)}

# Initialize the database when this module is imported
init_db()
