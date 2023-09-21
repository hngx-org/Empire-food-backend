#!/bin/bash

# Replace these variables with your specific values
APP_NAME="empire_free_lunch"
USER="mypythtesting"
APP_DIRECTORY="/app/backend"
VENV_PATH="/app/backend/.venv"
UVICORN_OPTIONS="--host 0.0.0.0 --port 8000"
# Create a systemd service unit file
echo "[Unit]
Description=Your FastAPI Application
[Service]
User=$USER
WorkingDirectory=$APP_DIRECTORY
ExecStart=$VENV_PATH/bin/uvicorn main:app $UVICORN_OPTIONS
Restart=always
[Install]
WantedBy=multi-user.target" | sudo tee /etc/systemd/system/$APP_NAME.service > /dev/null
# Reload systemd
sudo systemctl daemon-reload
#stop the service
sudo systemctl stop $APP_NAME
# Start and enable the service
sudo systemctl start $APP_NAME
sudo systemctl enable $APP_NAME
# Check the status of the service
sudo systemctl status $APP_NAME