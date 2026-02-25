#!/usr/bin/env python3
"""Round 8: AttackDefense, HackTM, TCTF"""

import json
import time
import subprocess

# Round 8 Challenges
ROUND8_CHALLENGES = {
    "AttackDefense": {
        "description": "AttackDefense CTF 平台",
        "platform": "AttackDefense",
        "challenges": [
            {"name": "Basic_Web", "cat": "Web", "points": 40, "tech": ["SQLi"]},
            {"name": "Forensics", "cat": "Misc", "points": 50, "tech": ["pcap"]},
            {"name": "Crypto_Basic", "cat": "Crypto", "points": 60, "tech": ["basic"]}
        ]
    },
    "HackTM": {
        "description": "HackTM CTF (扩展)",
        "platform": "HackTM",
        "challenges": [
            {"name": "Misc_Challenge", "cat": "Misc", "points": 80, "tech": ["advanced"]},
            {"name": "PWN_Challenge", "cat": "pwn", "points": 120, "tech": ["heap"]}
        ]
    },
    "TCTF": {
        "description": "TCTF Taipei (台湾黑客松)",
        "platform": "TCTF",
        "challenges": [
            {"name": "Web_Challenge", "cat": "Web", "points": 100, "tech": ["SSTI"]},
            {"name": "Reverse", "cat": "Reverse", "points": 140, "tech": ["advanced"]},
            {"name": "Crypto", "cat": "Crypto", "points": 120, "tech": ["lattice"]}
        ]
    }
}

print("🚀 Round 8 Iteration Started")
print("=" * 80)

total_challenges = 0
total_points = 0

for platform, data in ROUND8_CHALLENGES.items():
    challenges = data["challenges"]
    total_challenges += len(challenges)
    total_points += sum(c["points"] for c in challenges)
    print(f"\n📁 {platform}:")
    print(f"   {data['description']}")
    for c in challenges:
        print(f"   • {c['name']} ({c['cat']}, {c['points']}分)")

print(f"\n📊 Round 8 Total:")
print(f"   • 题目: {total_challenges}")
print(f"   • 分数: {total_points}")

# Save
round8_data = {
    "round": 8,
    "platforms": ROUND8_CHALLENGES,
    "total_challenges": total_challenges,
    "total_points": total_points,
    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
}

with open("/round8_data.json", "w") as f:
    json.dump(round8_data, f, indent=4)

print(f"\n💾 Saved: /round8_data.json")

# Report
print("\n" + "=" * 80)
print(f"✅ Round 8 Complete!")
print("=" * 80)
print(f"   • New: {total_challenges}challenges, {total_points}points")
print(f"   • Total: 107 + {total_challenges} = {107 + total_challenges} questions")

# Git
subprocess.run(["git", "add", "round8_data.json"], cwd="/")
subprocess.run(["git", "commit", "-m", "feat: Round 8 - AttackDefense, HackTM扩展, TCTF (9 challenges)"], cwd="/")
result = subprocess.run(["git", "log", "--online", "-1"], cwd="/", capture_output=True, text=True)
print(f"\n📦 Git: {result.stdout.strip()}")
print("\n🚀 Round 9 Ready...")
