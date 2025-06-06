import requests
import yaml
import json
import os

url = "https://johnshall.github.io/Shadowrocket-ADBlock-Rules-Forever/sr_cnip_ad.conf"
resp = requests.get(url)
lines = resp.text.splitlines()

def convert_to_clash(rule):
    if rule.startswith("DOMAIN-SUFFIX") or rule.startswith("DOMAIN") or rule.startswith("IP-CIDR") or rule.startswith("GEOIP"):
        return rule
    return None

rules = []
for line in lines:
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    converted = convert_to_clash(line)
    if converted:
        rules.append(converted)

os.makedirs("output", exist_ok=True)

clash_config = {
    "port": 7890,
    "socks-port": 7891,
    "allow-lan": True,
    "mode": "rule",
    "log-level": "info",
    "rules": rules
}

with open("output/clash.yaml", "w", encoding="utf-8") as f:
    yaml.dump(clash_config, f, allow_unicode=True)

singbox_rules = [{"type": "rule", "rule": r, "outbound": "proxy"} for r in rules]
with open("output/singbox.json", "w", encoding="utf-8") as f:
    json.dump({"route": {"rules": singbox_rules}}, f, indent=2)

with open("output/xray_routing.json", "w", encoding="utf-8") as f:
    json.dump({"routing": {"rules": singbox_rules}}, f, indent=2)