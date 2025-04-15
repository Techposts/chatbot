#!/bin/bash

echo "Setting up Anaptyss Hybrid Chatbot..."

# Set WordPress URL
WP_URL="https://anaptyss.com"  # Replace with your actual WordPress site URL

# Initial data fetch from WordPress
echo "Fetching initial content from WordPress..."
python3 -c "
from wordpress_fetcher import WordPressFetcher
fetcher = WordPressFetcher('$WP_URL')
fetcher.fetch_all_content()
"

# Initialize vector database
echo "Initializing vector database..."
python3 -c "
from vector_store import VectorStore
vector_store = VectorStore()
"

# Add your logo to assets folder if you have one
LOGO_URL="https://anaptyss.com/logo.png"  # Replace with your actual logo URL
if [ ! -z "$LOGO_URL" ]; then
    echo "Downloading logo..."
    curl -s -o assets/anaptyss_logo.png $LOGO_URL
fi

# Set permissions
chmod +x webhook_handler.py

# Create service file for webhook handler
cat > anaptyss-webhook.service << 'EOSVC'
[Unit]
Description=Anaptyss WordPress Webhook Handler
After=network.target

[Service]
User=root
WorkingDirectory=/var/www/anaptyss-chatbot
ExecStart=/var/www/anaptyss-chatbot/venv/bin/uvicorn webhook_handler:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=anaptyss-webhook

[Install]
WantedBy=multi-user.target
EOSVC

# Install the webhook service
sudo mv anaptyss-webhook.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable anaptyss-webhook
sudo systemctl start anaptyss-webhook

# Restart the chatbot service
sudo systemctl restart anaptyss-chatbot

echo "Setup complete! The hybrid chatbot is now ready."
