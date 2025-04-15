# webhook_handler.py
from fastapi import FastAPI, Request, HTTPException, Depends, Header
import hashlib
import hmac
import json
import os
import asyncio
from wordpress_fetcher import WordPressFetcher
from vector_store import VectorStore

app = FastAPI()

# Secret for webhook verification (set this in your WordPress site)
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "your_webhook_secret")

def verify_webhook_signature(request_body: bytes, x_hub_signature: str = Header(None)):
    if not x_hub_signature:
        raise HTTPException(status_code=401, detail="No signature provided")
    
    # Create expected signature
    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode(), 
        msg=request_body, 
        digestmod=hashlib.sha256
    ).hexdigest()
    
    # Compare signatures
    if not hmac.compare_digest(f"sha256={expected_signature}", x_hub_signature):
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    return True

@app.post("/webhook/wordpress")
async def wordpress_webhook(request: Request, verified: bool = Depends(verify_webhook_signature)):
    # Get the request body
    body = await request.body()
    data = json.loads(body)
    
    # Check the action type
    action = data.get("action")
    
    if action in ["publish", "update", "trash", "delete"]:
        # Initialize WordPress fetcher
        wp_fetcher = WordPressFetcher(data.get("site_url"))
        
        # Fetch updated content
        await asyncio.to_thread(wp_fetcher.fetch_all_content)
        
        # Update vector store
        vector_store = VectorStore()
        await asyncio.to_thread(vector_store.init_vector_store)
        
        return {"status": "success", "message": f"Processed {action} action"}
    
    return {"status": "skipped", "message": f"Action {action} not processed"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
