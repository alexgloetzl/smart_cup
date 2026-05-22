import network
import socket
import time
import json
import random

# -----------------------------
# Start WiFi Access Point
# -----------------------------
ap = network.WLAN(network.AP_IF)

ap.active(True)

ap.config(
    essid="ESP32-DASHBOARD",
    password="12345678",
    authmode=network.AUTH_WPA_WPA2_PSK
)

print("AP started")
print(ap.ifconfig())

# -----------------------------
# Mock sensor values
# -----------------------------
mock_weight = 50.0
mock_tilt = 45.0

# -----------------------------
# Load HTML file
# -----------------------------
with open("index.html", "r") as file:
    html = file.read()

# -----------------------------
# Create socket server
# -----------------------------
addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(5)

print("Server listening on port 80")

# -----------------------------
# Main loop
# -----------------------------
while True:

    # Update mock sensor values
    sample = random.uniform(0, 1)
    if sample < 0.5:
        mock_weight -= 5.0
    else:
        mock_weight += 5.0

    mock_tilt = 10.0
    alert = random.uniform(0,1)
    if alert < 0.2:
        mock_tilt = 50.0

    # Wait for client
    conn, addr = s.accept()

    print("Client connected:", addr)

    # request = conn.recv(1024).decode()
    raw_request = conn.recv(1024)
    # print(raw_request)

    request = raw_request.decode("utf-8", "ignore")    

    # -----------------------------
    # API endpoint
    # -----------------------------
    if "GET /data" in request:

        data = {
            "weight": mock_weight,
            "tilt": mock_tilt
        }

        print(f"mock weight: {mock_weight}, mock tilt: {mock_tilt}")

        json_data = json.dumps(data)

        response = f"""HTTP/1.1 200 OK
                    Content-Type: application/json

                    {json_data}
                    """

        conn.send(response)

    # -----------------------------
    # Main webpage
    # -----------------------------
    else:

        response = f"""HTTP/1.1 200 OK
                    Content-Type: text/html

                    {html}
                    """

        conn.send(response)

    conn.close()

    time.sleep(0.1)