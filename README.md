### Trinkbecher

# Installation process:
- pip install esptool
- python -m esptool version
- # erase existing firmware on micro controller:
- python -m esptool --chip esp32 --port COM3 erase_flash
- python -m esptool --chip esp32 --port COM3 --baud 460800 write_flash -z 0x1000 ESP32_GENERIC-20260406-v1.28.0.bin

- pip install mpremote
- mpremote connect COM3 fs cp main.py :