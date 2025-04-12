from flask import Flask, render_template, request, jsonify
import serial
import time
import os
import glob

app = Flask(__name__, template_folder="templates")
ser = None

COMMAND_CATEGORIES = {
    "Signal & Radio": {
        "Signal Strength": ("AT+CSQ", "Check RSSI and BER"),
        "Extended Signal": ("AT+CESQ", "Detailed signal quality values (RSRP, RSRQ, SINR)"),
        "Serving Cell": ('AT+QENG="servingcell"', "Get current serving cell info"),
        "Neighbour Cells": ('AT+QENG="neighbourcell"', "Get neighbor cell measurements"),
        "Band Info": ("AT+QNWINFO", "Radio Access Technology and Band"),
    },
    "SIM & Identity": {
        "SIM Status": ("AT+CPIN?", "Check if SIM is ready or needs PIN"),
        "ICCID": ("AT+QCCID", "Get SIM card serial number"),
        "IMSI": ("AT+CIMI", "Get subscriber identity"),
        "Operator": ("AT+COPS?", "Current network operator"),
        "Registration": ("AT+CREG?", "Network registration status"),
    },
    "PDP & IP": {
        "IP Info": ("AT+CGPADDR=1", "Current IP address from PDP context 1"),
        "List PDP": ("AT+CGDCONT?", "Defined PDP contexts"),
        "Activate PDP": ("AT+CGACT=1,1", "Activate PDP context 1"),
        "PDP States": ("AT+CGACT?", "Check PDP activation states"),
    },
    "Device Info": {
        "Model": ("AT+CGMM", "Get device model name"),
        "Firmware Version": ("AT+CGMR", "Get firmware/software version"),
        "Serial Number": ("AT+CGSN", "Get device IMEI (serial number)"),
    },
}


@app.route("/")
def index():
    return render_template("index.html", command_categories=COMMAND_CATEGORIES)


@app.route("/ports")
def list_ports():
    ports = glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*")
    return jsonify(ports)


@app.route("/connect", methods=["POST"])
def connect():
    global ser
    port = request.json.get("port")
    baud = int(request.json.get("baud", 115200))
    try:
        ser = serial.Serial(port, baud, timeout=2)
        return f"✔ Connected to {port} at {baud} baud"
    except Exception as e:
        return f"✖ Error: {e}"


@app.route("/disconnect", methods=["POST"])
def disconnect():
    global ser
    if ser:
        ser.close()
        ser = None
        return "✔ Disconnected"
    return "Already disconnected."


@app.route("/send", methods=["POST"])
def send():
    global ser
    if not ser:
        return "✖ Not connected"
    cmd = request.json.get("cmd")
    try:
        ser.reset_input_buffer()
        ser.write((cmd + "\r").encode())
        time.sleep(0.5)
        resp = ser.read_all().decode(errors="ignore").strip()
        return resp
    except Exception as e:
        return f"✖ Error sending command: {e}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
