import subprocess
import os
import re
import random
import sys

def run_command(command, shell=False):
    """Run a shell command and print output."""
    result = subprocess.run(command, shell=shell, check=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.stdout

def install_dependencies():
    print("Updating package list and installing curl, uuid-runtime...")
    run_command(["apt-get", "update"])
    run_command(["apt-get", "install", "-y", "curl", "uuid-runtime"])

def install_xray():
    print("Installing Xray-core...")
    install_script_url = "https://github.com/XTLS/Xray-install/raw/main/install-release.sh"
    install_script_path = "/tmp/install-xray.sh"

    run_command(["curl", "-L", install_script_url, "-o", install_script_path])
    run_command(["chmod", "+x", install_script_path])
    run_command(["bash", install_script_path])

    print("Xray-core installation completed.")

def configure_xray():
    print("Generating keys and configuring Xray...")

    REALITY_SERVERS = [
        "www.microsoft.com",
        "www.cloudflare.com",
        "www.apple.com",
        "www.bing.com",
        "www.live.com",
        "www.ibm.com",
        "www.tesla.com",
    ]

    uuid = run_command(["uuidgen"]).strip()

    key_output = run_command(["xray", "x25519"])

    private_key = re.search(r"PrivateKey:\s*(\S+)", key_output).group(1)
    public_key = re.search(r"Password \(PublicKey\):\s*(\S+)", key_output).group(1)

    short_id = "".join([random.choice("0123456789abcdef") for _ in range(8)])

    reality_dest = random.choice(REALITY_SERVERS)

    config_path = "/usr/local/etc/xray/config.json"
    os.makedirs(os.path.dirname(config_path), exist_ok=True)

    config_content = f"""{{
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
          "dest": "{reality_dest}:443",
          "xver": 0,
          "serverNames": [
            "{reality_dest}"
          ],
          "privateKey": "{private_key}",
          "shortIds": [
            "{short_id}"
          ]
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
}}"""

    with open(config_path, "w") as config_file:
        config_file.write(config_content)

    print(f"Xray configuration written to {config_path}")

    return uuid, public_key, short_id, reality_dest

def fetch_ip(version):
    if version not in ("4", "6"):
        raise ValueError("version must be '4' or '6'")
    return run_command(["curl", "-s" + version, "ifconfig.me"]).strip()

def format_ip(ip):
    # IPv6 addresses must be wrapped in [] inside a vless:// URI.
    if ":" in ip:
        return "[" + ip + "]"
    return ip

def start_xray():
    print("Starting Xray...")
    run_command(["systemctl", "enable", "xray"])
    run_command(["systemctl", "restart", "xray"])
    print("Xray has been started.")

def main():
    if os.geteuid() != 0:
        print("Error: This script must be run as root.")
        sys.exit(1)

    try:
        ipv4 = format_ip(fetch_ip("4"))
    except Exception:
        ipv4 = None
    try:
        ipv6 = format_ip(fetch_ip("6"))
    except Exception:
        ipv6 = None

    install_dependencies()
    install_xray()

    uuid, public_key, short_id, reality_dest = configure_xray()

    start_xray()

    def make_link(ip):
        return f"vless://{uuid}@{ip}:443?encryption=none&flow=xtls-rprx-vision&security=reality&sni={reality_dest}&fp=chrome&pbk={public_key}&sid={short_id}#Xray_REALITY"

    print("\n" + "=" * 50)
    print(" 🚀 Xray VLESS-REALITY Installation Complete!")
    print("=" * 50)
    print(f"Reality Dest: {reality_dest}")
    print(f"UUID:         {uuid}")
    print(f"Public Key:   {public_key}")
    print(f"Short ID:     {short_id}")
    print("-" * 50)
    if ipv4:
        print(" Your Client Share Link - IPv4 (Copy and import to client):")
        print(make_link(ipv4))
    if ipv6:
        print(" Your Client Share Link - IPv6 (Copy and import to client):")
        print(make_link(ipv6))
    if not ipv4 and not ipv6:
        print(" VLESS LINK: could not determine public IP")
    print("=" * 50 + "\n")

if __name__ == "__main__":
    main()
