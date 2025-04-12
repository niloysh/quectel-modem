# Quectel Modem
This repository contains a collection of scripts and tools to interact with Quectel modems. 

## Getting Started

### Connecting using AT commands
You can operate the modem using AT commands over a serial connection. Once you have connected the modem to your computer using USB, it will appear as a serial device. The modem usually creates two serial devices: one for AT commands and another for data. The AT command interface is typically `/dev/ttyUSB2`. You can use a terminal program like `minicom` to do this. Install using `sudo apt install minicom`.
To connect to the modem, use the following command:

```bash
minicom -D /dev/ttyUSB2 -b 115200
```
Replace `/dev/ttyUSB2` with the appropriate device file for your modem. You can find the correct device file by running `ls /dev/ttyUSB*` before and after plugging in the modem.

**Note** An easier way is to use the `modem_web.py` script, which provides a web interface for sending AT commands. 
You can run the script using the following command:

```bash
python3 modem_web.py
```
This will start a web server on port 5000. You can access the web interface by navigating to `http://localhost:5000` in your web browser.

### Quectel-CM
`quectel-CM` is a command-line tool for managing Quectel modems. It handles the connection process and provides a simple interface `wwan0` for sending and receiving data. The `wwan0` interface is used to connect to the internet via the modem. You can use standard Linux networking commands to manage this interface.

Use `start_quectel_netns.sh`. This will create a network namespace `qmodem` and move wwan0 to it. Then we run `quectel-CM` in the namespace. This avoids the situtation where the modem replaces the default route with the wwan0 interface, which can cause issues with SSH.

You can then use `ip netns exec qmodem` or `start_netns_shell.sh` to run commands in the namespace. You can change the default apn in `start_quectel_netns.sh` to your provider's apn. The default is `internet` which works for most providers. You can also set the APN using the `AT+CGDCONT` command in the `modem_web.py` script.

### Troubleshooting

If you don't have IMS, delete the extra PDP contexts. First, check the current PDP contexts by `AT+CGDCONT?`. You can then delete the extra contexts by specifying the context number without any parameters. For example, to delete the second and third contexts, use:
```bash
AT+CGDCONT=2
AT+CGDCONT=3
```