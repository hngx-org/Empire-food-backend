#!/bin/bash

fastapi_dir="/app/backend"
# Define the FastAPI application directory
app_dir="$fastapi_dir"

# Path to the Nginx configuration file
nginx_config="/etc/nginx/sites-available/fastapi_app.conf"

# Configuration to add
sudo printf %s "server {
    listen 80;
    listen [::]:80 default_server;
    root /var/www/html;
    index index.html;
#    server_name freelunch.com www.freelunch.com;
    server_name 35.193.20.212;
    location ~ / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
#    location / {
#        try_files \$uri \$uri/ =404;
#    }
}" | sudo tee "$nginx_config" > /dev/null

# Remove any configuration file present
sudo rm /etc/nginx/sites-enabled/*
# Create a symlink to the new configuration file
sudo ln -s "$nginx_config" /etc/nginx/sites-enabled/
# Navigate to the FastAPI application directory
cd "$app_dir" || exit
# Create a virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
# Activate the virtual environment
source .venv/bin/activate
# Install requirements
pip3 install -r requirements.txt
echo "FastAPI application setup on the FastAPI application server completed."
# Check for syntax errors
sudo nginx -t
# Restart nginx
sudo systemctl reload nginx
sudo service nginx restart







