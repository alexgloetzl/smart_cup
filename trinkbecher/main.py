import network
import socket
import time
import json
import random

from machine import Pin, PWM

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
# RGB LED setup
# -----------------------------

red_led = PWM(Pin(25))
green_led = PWM(Pin(26))
blue_led = PWM(Pin(13))

red_led.freq(1000)
green_led.freq(1000)
blue_led.freq(1000)

# -----------------------------
# Mock sensor values
# -----------------------------
mock_weight = 50.0
mock_tilt = 45.0

def set_color(r, g, b):

    # ESP32 PWM range:
    # 0 = ON
    # 1023 = OFF

    red_led.duty(r)
    green_led.duty(g)
    blue_led.duty(b)

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
    drunk_water = random.choice([20, 50])
    if sample < 0.7:
        mock_weight -= drunk_water
    else:
        mock_weight += 5*drunk_water

    mock_tilt = 30.0
    alert = random.uniform(0,1)
    if alert < 0.2:
        # -----------------------------
        # Smooth RGB tilt feedback
        # -----------------------------

        MIN_TILT = 30
        MAX_TILT = 50

        # Clamp tilt
        tilt_clamped = max(
            MIN_TILT,
            min(mock_tilt, MAX_TILT)
        )

        # Normalize:
        # 30° -> 0.0
        # 50° -> 1.0

        progress = (
            (tilt_clamped - MIN_TILT)
            / (MAX_TILT - MIN_TILT)
        )

        # Orange -> Dark Red transition
        #
        # Orange:
        #   R = 1023
        #   G = 500
        #
        # Dark red:
        #   R = 1023
        #   G = 0

        red = 1023

        green = int(
            500 * (1.0 - progress)
        )

        blue = 0

        set_color(red, green, blue)
        print(f"red: {red}, green: {green}, blue: {blue}")

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