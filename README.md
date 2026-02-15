# Venom-Wire: ARP Spoofing & Network Traffic Analysis

## ⚠️ Legal Disclaimer
**FOR EDUCATIONAL PURPOSES ONLY.**
This tool is designed for use in isolated laboratory environments (Docker) to understand the mechanics of ARP Poisoning and MITM attacks. The author is not responsible for any misuse of this code on public or unauthorized networks.

## 🔍 Overview
Venom-Wire is a Python-based network interceptor that demonstrates Man-in-the-Middle (MITM) attacks using the ARP protocol. It forces traffic redirection between a target container and a gateway, capturing HTTP headers and POST data in real-time.

## 🛠️ Architecture
* **Core:** Python 3.9 + Scapy
* **Environment:** Docker (Isolated Network `10.10.0.0/24`)
* **Attack Vector:** ARP Cache Poisoning (Layer 2)
* **Capabilities:**
    * Automatic IP Forwarding
    * HTTP Header Parsing
    * Credential Capture (POST Data)

## 🚀 Usage
1. **Build the Lab:**
   ```bash
   docker compose up --build -d
   ```

## 🚀 Launch the Interceptor
 ```bash
   docker exec -it venom-attacker python3 venom_spoofer.py
   ```