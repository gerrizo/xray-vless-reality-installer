# Xray VLESS Reality 一键安装脚本

一个基于 Python 的 **Xray-core（VLESS + Reality）一键安装脚本**，支持自动配置、随机 SNI 选择以及客户端二维码/链接输出。

---

## ⚠️ 免责声明

本项目仅供 **学习与个人研究用途**。

- 使用者需自行遵守当地法律法规  
- 作者不对任何滥用行为或损失负责  

---

## 🚀 功能特点

- 一键安装 Xray-core  
- 自动配置 VLESS + Reality 协议  
- 随机 SNI（伪装域名选择）  
- 自动生成 UUID 和 Reality 密钥  
- 自动生成 Short ID  
- 自动配置 systemd 服务  
- 自动生成客户端分享链接（VLESS URI）

---

## 📦 系统要求

支持系统：

- Ubuntu 20.04 / 22.04 / 24.04  
- Debian 11+  
- CentOS  

运行要求：

- Root 或 sudo 权限  
- Python 3.8+

---

## ⚡ 安装方法

### 一键安装命令

```bash
curl -O https://raw.githubusercontent.com/gerrizo/xray-vless-reality-installer/main/install.py && sudo python3 install.py
```
---
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
- CentOS

Requirements:

- Root or sudo privileges
- Python 3.8+

---

## ⚡ Installation

### One-line Install
```bash
curl -O https://raw.githubusercontent.com/gerrizo/xray-vless-reality-installer/main/install.py && sudo python3 install.py
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

