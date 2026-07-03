# Xray VLESS Reality Installer

A simple one-click Python installer for **Xray-core (VLESS + Reality)** with automatic configuration, random SNI selection, and QR code output for mobile clients.

---

## Disclaimer

This project is intended for **educational and personal use only**.

- Users are responsible for complying with local laws and regulations.
- The author is not responsible for any misuse or damages.

---

## 🚀 Features

- One-click installation of Xray-core
- Automatic VLESS + Reality configuration
- Random SNI (stealth domain selection)
- Auto-generated UUID and Reality keys
- Short ID generation
- Auto systemd service setup
- Client share link generation (VLESS URI)

---

## 📦 Requirements

Supported systems:

- Ubuntu 20.04 / 22.04 / 24.04
- Debian 11+

Requirements:

- Root or sudo privileges
- Python 3.8+

---

## ⚡ Installation

### One-line Install
```bash
curl -O https://raw.githubusercontent.com/gerrizo/xray-vless-reality-installer/main/install.py && python3 install.py
```
---

## 📱 Output Example

After installation, you will get:

- UUID
- Reality Public Key
- Short ID
- Selected Reality Domain (SNI)
- VLESS share link

Example:

```text
vless://UUID@YOUR_IP:443?encryption=none&flow=xtls-rprx-vision&security=reality&sni=www.microsoft.com&fp=chrome&pbk=PUBLIC_KEY&sid=SHORT_ID#Xray_REALITY
```

---

## 🧠 How it works

The script:

- Installs Xray-core using official install script  
- Generates:
  - UUID (client ID)
  - X25519 Reality key pair
  - Short ID  
- Randomly selects a TLS camouflage domain (SNI)  
- Writes Xray configuration to `/usr/local/etc/xray/config.json`  
- Enables systemd service  
- Generates VLESS share link

---

## 📄 License

MIT License

---

## ⭐ Star this project

If you find this useful, consider giving it a star ⭐

