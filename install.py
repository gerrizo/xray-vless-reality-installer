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
    run_command(["apt-get", "update", "-y"])
    run_command(["apt-get", "install", "curl", "uuid-runtime", "-y"])

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
        "www.office.com",
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
        ip = run_command(["curl", "-s", "ifconfig.me"]).strip()
    except:
        ip = "YOUR_VPS_IP"

    install_dependencies()
    install_xray()

    uuid, public_key, short_id, reality_dest = configure_xray()

    start_xray()

    vless_link = f"vless://{uuid}@{ip}:443?encryption=none&flow=xtls-rprx-vision&security=reality&sni={reality_dest}&fp=chrome&pbk={public_key}&sid={short_id}#Xray_REALITY"

    print("\n" + "=" * 50)
    print(" 🚀 Xray VLESS-REALITY Installation Complete!")
    print("=" * 50)
    print(f"Reality Dest: {reality_dest}")
    print(f"UUID:         {uuid}")
    print(f"Public Key:   {public_key}")
    print(f"Short ID:     {short_id}")
    print("-" * 50)
    print(" Your Client Share Link (Copy and import to client):")
    print(vless_link)
    print("=" * 50 + "\n")

if __name__ == "__main__":
    main()
