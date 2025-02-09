from setuptools import setup

SSID_NAME = "eero-wifi"

# Scrive il valore SSID in un file config.py
with open("scanner_wifi/config.py", "w") as f:
    f.write(f'SSID = "{SSID_NAME}"\n')

setup(
    name="scanner_wifi",
    version="0.1",
    packages=["scanner_wifi"],
    install_requires=[],
)
