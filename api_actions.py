# api_actions.py
import requests
import json
import os
import streamlit as st
from datetime import datetime
import database

class APIActions:
    def __init__(self, wp_url):
        self.wp_url = wp_url
        # Add WordPress REST API authentication if needed
        self.auth = None
    
    def schedule_demo(self, name, email, company, preferred_date):
        """Schedule a product demo for a potential customer"""
        # First save the lead
        lead_data = {
            "name": name,
            "email": email,
            "company": company,
            "interest": f"Demo request for {preferred_date}",
            "source": "chatbot_demo_request",
            "timestamp": datetime.now().isoformat()
        }
        
        result = database.save_lead(lead_data)
        
        if not result["success"]:
            return {
                "success": False,
                "message": f"Failed to save lead information: {result.get('error', 'Unknown error')}"
            }
        
        # Here you would integrate with your calendar/scheduling system
        # This is a placeholder for demonstration
        return {
            "success": True,
            "message": f"Demo scheduled for {preferred_date}",
            "confirmation_id": f"DEMO{datetime.now().strftime('%Y%m%d%H%M')}"
        }
    
    def get_latest_case_studies(self, industry=None, limit=3):
        """Get the latest case studies from WordPress"""
        # Construct the API URL
        api_url = f"{self.wp_url}/wp-json/wp/v2/posts"
        params = {
            "per_page": limit,
            "categories": self._get_category_id_by_name("Case Studies")
        }
        
        if industry:
            industry_tag = self._get_tag_id_by_name(industry)
            if industry_tag:
                params["tags"] = industry_tag
        
        # Make the API request
        try:
            response = requests.get(api_url, params=params)
            if response.status_code == 200:
                posts = response.json()
                case_studies = []
                
                for post in posts:
                    case_studies.append({
                        "title": post["title"]["rendered"],
                        "excerpt": post["excerpt"]["rendered"],
                        "link": post["link"],
                        "date": post["date"]
                    })
                
                return {
                    "success": True,
                    "case_studies": case_studies
                }
            else:
                return {
                    "success": False,
                    "message": f"Failed to fetch case studies: {response.status_code}"
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error fetching case studies: {str(e)}"
            }
    
    def _get_category_id_by_name(self, category_name):
        """Get WordPress category ID by name"""
        try:
            response = requests.get(f"{self.wp_url}/wp-json/wp/v2/categories", params={"search": category_name})
            if response.status_code == 200:
                categories = response.json()
                for category in categories:
                    if category["name"].lower() == category_name.lower():
                        return category["id"]
            return None
        except:
            return None
    
    def _get_tag_id_by_name(self, tag_name):
        """Get WordPress tag ID by name"""
        try:
            response = requests.get(f"{self.wp_url}/wp-json/wp/v2/tags", params={"search": tag_name})
            if response.status_code == 200:
                tags = response.json()
                for tag in tags:
                    if tag["name"].lower() == tag_name.lower():
                        return tag["id"]
            return None
        except:
            return None
