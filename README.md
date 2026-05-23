# Smart Cup
## Motivation

Around 5 million people in Germany suffer from swallowing disorders. Therefore, there is a strong need for a smart drinking cup that supports patients during hydration.

Our system provides several features:

* Visual feedback to encourage a healthier head posture while drinking
* Fill level monitoring to assist caregivers
* Water intake tracking and daily hydration goals for patients

We implemented these features in a modular and low-cost design based primarily on two sensors. The system measures both the cup’s fill level and its tilt angle in real time.

---

## Hardware Components

A real-time smart hydration monitoring system built with a micro controller ESP32, HX711 load cell amplifier, QMC5883L (GY271) tilt sensor, RGB LED feedback, and a browser-based dashboard.

| Component        | Purpose              |
| ---------------- | -------------------- |
| ESP32-E v1.0     | Main microcontroller |
| HX711            | Load cell amplifier  |
| Load Cell        | Weight measurement   |
| GY271 / QMC5883L | Tilt sensing         |
| RGB LED          | Visual feedback      |

---

## Pin Configuration

### HX711

| HX711 Pin | ESP32 Pin |
| --------- | --------- |
| DT        | GPIO4     |
| SCK       | GPIO18    |

---

### GY271 / QMC5883L

| Sensor Pin | ESP32 Pin |
| ---------- | --------- |
| SDA        | GPIO21    |
| SCL        | GPIO22    |

---

### RGB LED

| LED Color | ESP32 Pin |
| --------- | --------- |
| Red       | GPIO25    |
| Green     | GPIO26    |
| Blue      | GPIO13    |

---

## Installation Process

---

### 1. Install esptool

```bash
pip install esptool
```

Check installation:

```bash
python -m esptool version
```

---

### 2. Erase Existing ESP32 Firmware

```bash
python -m esptool --chip esp32 --port COM3 erase_flash
```

---

### 3. Flash MicroPython Firmware

```bash
python -m esptool --chip esp32 --port COM3 --baud 460800 write_flash -z 0x1000 ESP32_GENERIC-20260406-v1.28.0.bin
```

---

### 4. Install mpremote

```bash
pip install mpremote
```

---

### 5. Upload Files to ESP32

Upload `main.py` and `index.html`:

```bash
python -m mpremote connect COM3 fs cp main.py :
python -m mpremote connect COM3 fs cp index.html :
```

---


## WiFi Setup

The ESP32 acts as a WiFi access point.

### WiFi Credentials

SSID:

```text
ESP32-DASHBOARD
```

Password:

```text
12345678
```

---

### Open Dashboard

In browser:

```text
http://192.168.4.1
```

---

## Dashboard Features

### Real-Time Metrics

Displays:

* Current weight
* Current tilt angle
* Highest streak

---


## Software Stack

* MicroPython
* HTML

---

## Project Structure

```text
smarter_trinkbecher/
│
├── main.py
├── index.html
└── README.md
```

---

## Future Improvements

Potential future upgrades:

* Cloud synchronization
* Mobile notifications
* Battery power support
* OLED display
* Temperature sensing
* Persistent data storage
* Machine learning hydration analysis

---

## License

Open-source project for educational and personal use.
