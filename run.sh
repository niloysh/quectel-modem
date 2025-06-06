#!/bin/bash

while true; do
    echo "[`date`] Starting Flask app..."
    python3 modem_web/app.py
    echo "[`date`] Flask app crashed. Restarting in 5s..."
    sleep 5
done
