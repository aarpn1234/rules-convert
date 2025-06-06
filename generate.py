import os
import yaml

RULE_MODE = os.environ.get("RULE_MODE", "rule").lower()
if RULE_MODE not in ["rule", "global"]:
    RULE_MODE = "rule"

config = {
    "port": 7890,
    "socks-port": 7891,
    "redir-port": 7892,
    "allow-lan": True,
    "mode": RULE_MODE,
    "log-level": "info",
    "external-controller": "127.0.0.1:9090",
    "proxies": [],
    "proxy-groups": [
        {
            "name": "🚀 节点选择",
            "type": "select",
            "proxies": ["♻️ 自动选择", "DIRECT"]
        },
        {
            "name": "♻️ 自动选择",
            "type": "url-test",
            "url": "http://www.gstatic.com/generate_204",
            "interval": 300,
            "proxies": ["DIRECT"]
        }
    ],
    "rules": [
        "DOMAIN-SUFFIX,local,DIRECT",
        "DOMAIN-SUFFIX,qq.com,DIRECT",
        "DOMAIN-SUFFIX,google.com,🚀 节点选择",
        "GEOIP,CN,DIRECT",
        "MATCH,🚀 节点选择"
    ]
}

with open("clash_config.yaml", "w", encoding="utf-8") as f:
    yaml.dump(config, f, allow_unicode=True)
