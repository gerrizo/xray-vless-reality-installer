import subprocess
import os
import re
import random
import sys

def run_command(cmd):
    result = subprocess.run(cmd, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip())
    if result.returncode != 0:
        raise RuntimeError("Command failed: " + " ".join(cmd))
    return result.stdout.strip()

def get_pkg_manager():
    if os.path.exists("/usr/bin/apt-get"):
        return "apt"
    if os.path.exists("/usr/bin/dnf"):
        return "dnf"
    if os.path.exists("/usr/bin/yum"):
        return "yum"
    raise Exception("No supported package manager found")

def install_dependencies():
    pkg = get_pkg_manager()
    if pkg == "apt":
        print("APT detected, updating package lists... (may wait if system is auto-updating)")
    
        run_command([
            "apt-get",
            "-o",
            "DPkg::Lock::Timeout=300",
            "update"
        ])
    
        run_command([
            "apt-get",
            "-o",
            "DPkg::Lock::Timeout=300",
            "install",
            "-y",
            "curl",
            "uuid-runtime"
        ])
    elif pkg == "dnf":
        run_command(["dnf", "install", "-y", "curl", "util-linux"])
    elif pkg == "yum":
        run_command(["yum", "install", "-y", "curl", "util-linux"])

def install_xray():
    url = "https://github.com/XTLS/Xray-install/raw/main/install-release.sh"
    path = "/tmp/install-xray.sh"
    run_command(["curl", "-L", url, "-o", path])
    run_command(["chmod", "+x", path])
    run_command(["bash", path])

def configure_xray():
    servers = [
        "www.microsoft.com",
        "www.cloudflare.com",
        "www.apple.com",
        "www.bing.com",
        "www.ibm.com",
        "www.tesla.com"
    ]

    uuid = run_command(["uuidgen"])
    key_output = run_command(["xray", "x25519"])

    private_key = re.search(r"PrivateKey:\s*(\S+)", key_output).group(1)
    public_key = re.search(r"(?:PublicKey|Password \(PublicKey\)):\s*(\S+)", key_output).group(1)

    short_id = "".join(random.choice("0123456789abcdef") for _ in range(8))
    dest = random.choice(servers)

    config_path = "/usr/local/etc/xray/config.json"
    os.makedirs(os.path.dirname(config_path), exist_ok=True)

    config = f'''{{
  "log": {{
    "loglevel": "warning"
  }},
  "inbounds": [
    {{
      "port": 443,
      "protocol": "vless",
      "settings": {{
        "clients": [
          {{
            "id": "{uuid}",
            "flow": "xtls-rprx-vision"
          }}
        ],
        "decryption": "none"
      }},
      "streamSettings": {{
        "network": "tcp",
        "security": "reality",
        "realitySettings": {{
          "show": false,
          "dest": "{dest}:443",
          "xver": 0,
          "serverNames": ["{dest}"],
          "privateKey": "{private_key}",
          "shortIds": ["{short_id}"]
        }}
      }}
    }}
  ],
  "outbounds": [
    {{
      "protocol": "freedom",
      "tag": "direct"
    }}
  ]
}}'''

    with open(config_path, "w") as f:
        f.write(config)

    return uuid, public_key, short_id, dest

def enable_bbr():
    print("Enabling BBR...")

    with open("/etc/sysctl.d/99-bbr.conf", "w") as f:
        f.write(
            "net.core.default_qdisc=fq\n"
            "net.ipv4.tcp_congestion_control=bbr\n"
        )

    run_command(["sysctl", "-p", "/etc/sysctl.d/99-bbr.conf"])

def open_firewall():
    if os.path.exists("/usr/sbin/ufw"):
        run_command(["ufw", "allow", "443"])
    elif os.path.exists("/usr/bin/firewall-cmd"):
        run_command(["firewall-cmd", "--permanent", "--add-port=443/tcp"])
        run_command(["firewall-cmd", "--reload"])

def start_xray():
    run_command(["systemctl", "enable", "xray"])
    run_command(["systemctl", "restart", "xray"])

def main():
    if os.geteuid() != 0:
        sys.exit(1)

    ip = run_command(["curl", "-s", "ifconfig.me"])

    install_dependencies()
    install_xray()
    uuid, pbk, sid, dest = configure_xray()
    enable_bbr()
    open_firewall()
    start_xray()

    link = (
        f"vless://{uuid}@{ip}:443"
        f"?encryption=none&flow=xtls-rprx-vision"
        f"&security=reality&sni={dest}"
        f"&fp=chrome&pbk={pbk}&sid={sid}#Xray"
    )

    print("\n" + "=" * 40)
    print("INSTALL COMPLETE")
    print("=" * 40)
    print(f"Reality Server : {dest}")
    print(f"UUID           : {uuid}")
    print(f"Public Key     : {pbk}")
    print(f"Short ID       : {sid}")
    print("-" * 40)
    print("VLESS LINK:")
    print(link)
    print("=" * 40 + "\n")

if __name__ == "__main__":
    main()
