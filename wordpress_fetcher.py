# wordpress_fetcher.py
import requests
import json
import os
from bs4 import BeautifulSoup
from datetime import datetime

class WordPressFetcher:
    def __init__(self, site_url):
        self.site_url = site_url
        self.api_url = f"{site_url}/wp-json/wp/v2"
        self.cache_dir = "wp_cache"
        os.makedirs(self.cache_dir, exist_ok=True)
    
        def fetch_all_content(self):
            """Fetch all content from WordPress site"""
            print("Fetching WordPress content...")
            self.fetch_posts()
            self.fetch_pages()
            print("WordPress content fetch complete")
    
    def fetch_posts(self, per_page=100):
    """Fetch all posts from the WordPress site"""
    page = 1
    all_posts = []

    # Set proper headers to avoid 406 error
    headers = {
        "User-Agent": "Anaptyss Chatbot/1.0",
        "Accept": "application/json"
    }

    while True:
        url = f"{self.api_url}/posts?per_page={per_page}&page={page}"
        print(f"Fetching from URL: {url}")
    
        try:
            response = requests.get(url, headers=headers)
            print(f"Response status: {response.status_code}")
        
            if response.status_code == 200:
                posts = response.json()
                if not posts:
                    break
            
                all_posts.extend(posts)
                page += 1
            else:
                print(f"Error fetching posts: {response.status_code}")
                print(f"Response content: {response.text[:500]}")
                break
        except Exception as e:
            print(f"Exception during fetch: {str(e)}")
            break

    # Save posts to files
    for post in all_posts:
        content = BeautifulSoup(post['content']['rendered'], 'html.parser').get_text()
        title = post['title']['rendered']
        slug = post['slug']
        date = post['date']
    
        with open(f"{self.cache_dir}/post_{slug}.md", 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n")
            f.write(f"Date: {date}\n\n")
            f.write(content)

    print(f"Fetched {len(all_posts)} posts")
    
    print(f"Fetched {len(all_posts)} posts")
    
    def fetch_pages(self, per_page=100):
        """Fetch all pages from the WordPress site"""
        page = 1
        all_pages = []
        
        while True:
            url = f"{self.api_url}/pages?per_page={per_page}&page={page}"
            response = requests.get(url)
            
            if response.status_code == 200:
                pages = response.json()
                if not pages:
                    break
                
                all_pages.extend(pages)
                page += 1
            else:
                print(f"Error fetching pages: {response.status_code}")
                break
        
        # Save pages to files
        for page in all_pages:
            content = BeautifulSoup(page['content']['rendered'], 'html.parser').get_text()
            title = page['title']['rendered']
            slug = page['slug']
            
            with open(f"{self.cache_dir}/page_{slug}.md", 'w', encoding='utf-8') as f:
                f.write(f"# {title}\n\n")
                f.write(content)
        
        print(f"Fetched {len(all_pages)} pages")
