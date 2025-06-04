import requests

# ✏️ 你可以在这里修改规则来源链接
RULE_SOURCE_URL = "https://johnshall.github.io/Shadowrocket-ADBlock-Rules-Forever/sr_cnip_ad.conf"
OUTPUT_FILE = "clash_rules.yaml"

def convert_line(line: str) -> str | None:
    line = line.strip()
    if not line or line.startswith('#') or line.startswith('['):
        return None
    if line.startswith("DOMAIN-SUFFIX,"):
        return f"- DOMAIN-SUFFIX,{line.split(',')[1]}"
    if line.startswith("DOMAIN,"):
        return f"- DOMAIN,{line.split(',')[1]}"
    if line.startswith("IP-CIDR,"):
        return f"- IP-CIDR,{line.split(',')[1]},no-resolve"
    return None  # 忽略其他规则（如 USER-AGENT）

def fetch_and_convert(url: str) -> list[str]:
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch rules: HTTP {response.status_code}")
    lines = response.text.splitlines()
    converted = [convert_line(line) for line in lines]
    return [rule for rule in converted if rule]

def save_clash_rules(rules: list[str], output_path: str):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("rules:\n")
        for rule in rules:
            f.write(f"  {rule}\n")
        f.write("  - GEOIP,CN,DIRECT\n")
        f.write("  - MATCH,DIRECT\n")

def main():
    try:
        print(f"Fetching rules from {RULE_SOURCE_URL}...")
        converted_rules = fetch_and_convert(RULE_SOURCE_URL)
        save_clash_rules(converted_rules, OUTPUT_FILE)
        print(f"✅ Successfully saved to {OUTPUT_FILE}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
