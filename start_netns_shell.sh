NS="qmodem"
echo "[*] Launching shell in namespace '$NS'"
sudo ip netns exec "$NS" bash