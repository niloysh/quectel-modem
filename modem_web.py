from flask import Flask, render_template_string, request
import serial
import time

app = Flask(__name__)
ser = None

TEMPLATE = """
<!DOCTYPE html>
<html><body>
<h2>Quectel Modem Web Interface</h2>
<form onsubmit="sendAT(event)">
    Serial Port: <input id="port" value="/dev/ttyUSB2">
    <button type="button" onclick="connect()">Connect</button>
    <button type="button" onclick="disconnect()">Disconnect</button>
    <br><br>
    AT Command: <input id="atcmd">
    <button type="submit">Send</button>
</form>

<div>
    <button onclick="sendPreset('AT+COPS?')">Operator</button>
    <button onclick="sendPreset('AT+CREG?')">Registration</button>
    <button onclick="sendPreset('AT+CSQ')">Signal</button>
    <button onclick="sendPreset('AT+QNWINFO')">Band Info</button>
    <button onclick="sendPreset('AT+CGPADDR=1')">IP Info</button>
    <button onclick="sendPreset('AT+CGDCONT?')">List PDP</button>
    <button onclick="sendPreset('AT+CGACT=1,1')">Activate PDP</button>
    <button onclick="sendPreset('AT+QENG=\\"servingcell\\"')">Serving Cell</button>
</div>

<textarea id="output" rows="20" cols="80"></textarea>

<script>
async function connect() {
    const port = document.getElementById("port").value;
    const res = await fetch("/connect", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({port})
    });
    updateOutput(await res.text());
}

async function disconnect() {
    const res = await fetch("/disconnect", {method: "POST"});
    updateOutput(await res.text());
}

function updateOutput(text) {
    const box = document.getElementById("output");
    box.value += text + "\\n";
    box.scrollTop = box.scrollHeight;
}

async function sendAT(e) {
    e.preventDefault();
    const cmd = document.getElementById("atcmd").value;
    const res = await fetch("/send", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({cmd})
    });
    updateOutput("> " + cmd + "\\n" + await res.text());
}

async function sendPreset(cmd) {
    const res = await fetch("/send", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({cmd})
    });
    updateOutput("> " + cmd + "\\n" + await res.text());
}
</script>
</body></html>
"""


@app.route("/")
def index():
    return render_template_string(TEMPLATE)


@app.route("/connect", methods=["POST"])
def connect():
    global ser
    port = request.json["port"]
    try:
        ser = serial.Serial(port, 115200, timeout=2)
        return f"✔ Connected to {port}"
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
        return "Not connected"
    cmd = request.json["cmd"]
    ser.reset_input_buffer()
    ser.write((cmd + "\r").encode())
    time.sleep(0.5)
    return ser.read_all().decode(errors="ignore").strip()


if __name__ == "__main__":
    app.run("0.0.0.0", 5000)
