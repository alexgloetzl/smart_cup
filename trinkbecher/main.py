import bluetooth
import time
import struct
from machine import Timer

# Define the BLE UUIDs (Custom profile for your sensor telemetry)
_ENV_SENSE_UUID = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef0") # Standard Environmental Sensing service
_SENSOR_DATA_CHAR = (bluetooth.UUID("12345678-1234-5678-1234-56789abcdef1"), bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,)
_SENSOR_SERVICE = (_ENV_SENSE_UUID, (_SENSOR_DATA_CHAR,),)

class ESP32BLETelemetry:
    def __init__(self, name="ESP32-Sensors"):
        self._ble = bluetooth.BLE()
        self._ble.active(True)
        self._ble.irq(self._ble_irq)
        ((self._handle,),) = self._ble.gatts_register_services((_SENSOR_SERVICE,))
        self._connections = set()
        self._payload = self._create_advertising_payload(name=name)
        self._advertise()

    def _ble_irq(self, event, data):
        if event == 1:  # _IRQ_CENTRAL_CONNECT
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
            print("Client Connected via Bluetooth")
        elif event == 2:  # _IRQ_CENTRAL_DISCONNECT
            conn_handle, _, _ = data
            # self._connections.remove(conn_handle)
            self._connections.discard(conn_handle)
            print("Client Disconnected")
            self._advertise()

    def _create_advertising_payload(self, name):
        payload = bytearray([2, 0x01, 0x06]) # Flags
        payload += bytearray([len(name) + 1, 0x09]) + name.encode('utf-8') # Complete Local Name
        return payload

    def _advertise(self):
        self._ble.gap_advertise(100000, adv_data=self._payload)

    def update_telemetry(self, weight, tilt):
        # Pack data as 2 floats (4 bytes each -> total 8 bytes)
        # 'f' is for float. 
        data = struct.pack('<ff', weight, tilt)
        self._ble.gatts_write(self._handle, data)
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._handle)

# Main Application Execution Loop
ble_server = ESP32BLETelemetry()

# Simulated Hardware Sensor Loop
mock_weight = 0.0
mock_tilt = 45.0

print("BLE Sensor Service started. Awaiting browser connection...")

while True:
    # --- PLACE YOUR HARDWARE SENSOR READ CODES HERE ---
    # Example: mock cyclical sensory shifts
    # mock_weight = (mock_weight + 0.5) if mock_weight < 50.0 else 0.0
    # mock_tilt = (mock_tilt + 1.0) if mock_tilt < 90.0 else 0.0
    
    mock_weight += 1.0
    mock_tilt -= 1.0

    print(mock_weight, mock_tilt)  # DEBUG LINE

    # Send metrics over Bluetooth
    ble_server.update_telemetry(mock_weight, mock_tilt)
    time.sleep(1) # Frequency of updates (1Hz)












# import bluetooth
# import time
# import struct

# _ENV_SENSE_UUID = bluetooth.UUID(0x181A)
# _SENSOR_CHAR_UUID = bluetooth.UUID(0x2A56)

# _SENSOR_CHAR = (
#     _SENSOR_CHAR_UUID,
#     bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,
# )

# _SERVICE = (
#     _ENV_SENSE_UUID,
#     (_SENSOR_CHAR,),
# )

# class ESP32BLETelemetry:
#     def __init__(self, name="ESP32-Sensors"):
#         self._ble = bluetooth.BLE()
#         self._ble.active(True)
#         self._ble.irq(self._irq)

#         ((self._char_handle,),) = self._ble.gatts_register_services((_SERVICE,))

#         self._connections = set()

#         self._payload = self._advertising_payload(name)
#         self._advertise()

#         print("BLE ready, advertising as:", name)

#     def _irq(self, event, data):
#         if event == 1:  # connect
#             conn_handle, _, _ = data
#             self._connections.add(conn_handle)
#             print("Client connected")

#         elif event == 2:  # disconnect
#             conn_handle, _, _ = data
#             self._connections.discard(conn_handle)
#             print("Client disconnected")
#             self._advertise()

#     def _advertising_payload(self, name):
#         payload = bytearray()
#         payload += bytearray((2, 0x01, 0x06))
#         payload += bytearray((len(name) + 1, 0x09)) + name.encode()
#         return payload

#     def _advertise(self):
#         self._ble.gap_advertise(100000, adv_data=self._payload)

#     def update(self, weight, tilt):
#         data = struct.pack("<ff", weight, tilt)
#         self._ble.gatts_write(self._char_handle, data)

#         for c in self._connections:
#             self._ble.gatts_notify(c, self._char_handle)


# # ---------------- MAIN LOOP ----------------

# ble = ESP32BLETelemetry()

# weight = 0.0
# tilt = 45.0

# print("Streaming telemetry...")

# while True:
#     weight = (weight + 0.5) if weight < 50 else 0
#     tilt = (tilt + 1.0) if tilt < 90 else 0

#     ble.update(weight, tilt)

#     time.sleep(1)