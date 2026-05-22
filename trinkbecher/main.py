import network
import socket
import time

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="ESP32-DASHBOARD", password="12345678")

print("AP started")
print(ap.ifconfig())

mock_weight = 0.0
mock_tilt = 45.0

addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

while True:
    mock_weight += 1.0
    mock_tilt -= 1.0

    conn, addr = s.accept()
    conn.recv(1024)

    response = f"""HTTP/1.1 200 OK

{{"weight": {mock_weight}, "tilt": {mock_tilt}}}
"""
    conn.send(response)
    conn.close()

    time.sleep(1)