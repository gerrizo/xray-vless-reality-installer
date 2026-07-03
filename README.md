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
- 自动开启 Google BBR 防拥堵算法
- 自动生成客户端分享链接（VLESS URI）

---

## 使用前装备工作

先获取一个可远程控制的VPS，推荐使用DigitalOcean、搬瓦工、Vultr

### 📦 VPS系统要求

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

## 📱 输出示例

安装完成后，你将获得：

- UUID
- Reality 公钥
- Short ID
- 选定的 Reality 域名（SNI）
- VLESS 分享链接

示例：
```text
vless://UUID@YOUR_IP:443?encryption=none&flow=xtls-rprx-vision&security=reality&sni=www.microsoft.com&fp=chrome&pbk=PUBLIC_KEY&sid=SHORT_ID#Xray
```
---
## 工作原理

该脚本主要执行以下步骤：

- 更新软件包列表  
- 使用官方安装脚本安装 Xray-core  
- 自动生成：
  - UUID（客户端 ID）
  - X25519 Reality 密钥对
  - Short ID  
- 随机选择 TLS 伪装域名（SNI）  
- 写入 Xray 配置文件：`/usr/local/etc/xray/config.json`  
- 启用 systemd 服务
- 开启谷歌BBR防拥堵算法
- 生成 VLESS 分享链接  

---

## 📄 使用许可

MIT License

---

## ⭐ 给项目点星

如果你觉得这个项目有帮助，欢迎点一个 Star ⭐
