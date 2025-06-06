#!/bin/bash

MODEM_IF="wwan0"
NS="qmodem"
APN="rogerswpn.apn"
QUECTEL_CM="quectel-modem/quectel-CM/quectel-CM"

# Step 1: Create the namespace if it doesn't exist
if ! ip netns list | grep -q "$NS"; then
    echo "[*] Creating namespace: $NS"
    sudo ip netns add "$NS"
    sudo mkdir -p /etc/netns/"$NS"
    echo "nameserver 8.8.8.8" | sudo tee /etc/netns/"$NS"/resolv.conf >/dev/null
fi

# Step 2: Check if interface is in default or qmodem namespace
echo "[*] Checking for modem interface: $MODEM_IF"

IF_IN_ROOT=$(ip link show "$MODEM_IF" 2>/dev/null | grep "$MODEM_IF")
IF_IN_NS=$(sudo ip netns exec "$NS" ip link show "$MODEM_IF" 2>/dev/null | grep "$MODEM_IF")

if [[ -n "$IF_IN_NS" ]]; then
    echo "[+] $MODEM_IF is already in namespace '$NS'"
elif [[ -n "$IF_IN_ROOT" ]]; then
    echo "[+] Found $MODEM_IF in root namespace — moving to '$NS'"
    sudo ip link set "$MODEM_IF" netns "$NS"
else
    echo "[!] Could not find $MODEM_IF in root or '$NS'. Exiting."
    exit 1
fi

# Step 3: Move the interface to the namespace
echo "[*] Moving $MODEM_IF to namespace $NS"
sudo ip link set "$MODEM_IF" netns "$NS"

# Step 4: Start quectel-CM inside the namespace
echo "[*] Starting quectel-CM with APN '$APN' in namespace '$NS'"
sudo ip netns exec "$NS" "$QUECTEL_CM" -s "$APN"
