# mcp_handler.py
import os
import json
from datetime import datetime

class MCPHandler:
    def __init__(self, session):
        self.session = session
    
    async def setup_filesystem(self):
        """Setup MCP filesystem with Anaptyss content"""
        # Make sure docs directory exists in MCP filesystem
        files = await self.session.list_files("/")
        if "docs" not in [f.name for f in files if f.is_dir]:
            await self.session.create_dir("/docs")
            print("Created docs directory in MCP filesystem")
        
        # Sync our local docs with MCP filesystem
        await self.sync_local_docs()
        
        # Sync WordPress cached content
        await self.sync_wordpress_content()
    
    async def sync_local_docs(self):
        """Sync local docs with MCP filesystem"""
        local_docs_dir = "docs"
        if not os.path.exists(local_docs_dir):
            print(f"Local docs directory {local_docs_dir} not found")
            return
        
        # Get list of local files
        local_files = []
        for root, _, files in os.walk(local_docs_dir):
            for file in files:
                if file.endswith(".md"):
                    local_path = os.path.join(root, file)
                    rel_path = os.path.relpath(local_path, start=local_docs_dir)
                    local_files.append(rel_path)
        
        # Get list of MCP files
        mcp_files = []
        try:
            files = await self.session.list_files("/docs")
            for file in files:
                if not file.is_dir and file.name.endswith(".md"):
                    mcp_files.append(file.name)
        except Exception as e:
            print(f"Error listing MCP files: {e}")
        
        # Upload new or modified files
        for rel_path in local_files:
            mcp_path = f"/docs/{rel_path}"
            local_path = os.path.join(local_docs_dir, rel_path)
            
            # Create directories if needed
            mcp_dir = os.path.dirname(mcp_path)
            if mcp_dir != "/docs":
                try:
                    await self.session.create_dir(mcp_dir)
                except:
                    pass  # Directory might already exist
            
            # Read local file
            with open(local_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Upload to MCP
            try:
                await self.session.write_file(mcp_path, content)
                print(f"Uploaded {mcp_path}")
            except Exception as e:
                print(f"Error uploading {mcp_path}: {e}")
    
    async def sync_wordpress_content(self):
        """Sync WordPress cached content with MCP filesystem"""
        wp_cache_dir = "wp_cache"
        if not os.path.exists(wp_cache_dir):
            print(f"WordPress cache directory {wp_cache_dir} not found")
            return
        
        # Make sure wordpress directory exists in MCP filesystem
        files = await self.session.list_files("/")
        if "wordpress" not in [f.name for f in files if f.is_dir]:
            await self.session.create_dir("/wordpress")
            print("Created wordpress directory in MCP filesystem")
        
        # Upload WordPress cached files
        for file in os.listdir(wp_cache_dir):
            if file.endswith(".md"):
                local_path = os.path.join(wp_cache_dir, file)
                mcp_path = f"/wordpress/{file}"
                
                # Read local file
                with open(local_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Upload to MCP
                try:
                    await self.session.write_file(mcp_path, content)
                    print(f"Uploaded {mcp_path}")
                except Exception as e:
                    print(f"Error uploading {mcp_path}: {e}")
