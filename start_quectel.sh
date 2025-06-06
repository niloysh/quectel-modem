#!/bin/bash

MODEM_IF="wwan0"
APN="rogerswpn.apn"
QUECTEL_CM="quectel-modem/quectel-CM/quectel-CM"

echo "[*] Starting quectel-CM with APN '$APN' on interface '$MODEM_IF'"
sudo "$QUECTEL_CM" -s "$APN"
