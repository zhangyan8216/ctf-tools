#!/usr/bin/env python3
"""
第14轮迭代 - 添加更多专业CTF平台
持续扩展，追求100%准确率
"""

import json
import time

# === 第14轮平台扩展 ===

ROUND_14_PLATFORMS = {
    "rwctf": {
        "web": [
            {
                "name": "SSRF_Internal_Scan",
                "category": "Web",
                "platform": "RWCTF",
                "year": "2023",
                "difficulty": "Expert",
                "points": 470,
                "techniques": ["SSRF", "internal-scan", "blind", "DNS Reb"],
                "flag_format": "rwctf{...}"
            }
        ],
        "pwn": [
            {
                "name": "Userfaultfd_Heap",
                "category": "Pwn",
                "platform": "RWCTF",
                "year": "2024",
                "difficulty": "Expert",
                "points": 510,
                "techniques": ["userfaultfd", "heap", "race", "UAF"],
                "flag_format": "rwctf{...}"
            }
        ],
        "reverse": [
            {
                "name": "Windows_Kernel",
                "category": "Reverse",
                "platform": "RWCTF",
                "year": "2023",
                "difficulty": "Expert",
                "points": 490,
                "techniques": ["Windows", "kernel", "driver", "exploit"],
                "flag_format": "rwctf{...}"
            }
        ]
    },

    "cuber": {
        "crypto": [
            {
                "name": "Elliptic_Curve_Deterministic",
                "category": "Cryptography",
                "platform": "CuberCTF",
                "year": "2023",
                "difficulty": "Expert",
                "points": 450,
                "techniques": ["ECC", "deterministic", "nonce", "private-key"],
                "flag_format": "cuber{...}"
            }
        ],
        "misc": [
            {
                "name": "Docker_Registry",
                "category": "Misc",
                "platform": "CuberCTF",
                "year": "2024",
                "difficulty": "Hard",
                "points": 360,
                "techniques": ["docker", "registry", "API", "token"],
                "flag_format": "cuber{...}"
            }
        ]
    },

    "wectf": {
        "web": [
            {
                "name": "NoSQL_Injection",
                "category": "Web",
                "platform": "WECTF",
                "year": "2023",
                "difficulty": "Hard",
                "points": 380,
                "techniques": ["NoSQL", "MongoDB", "injection", "bypass"],
                "flag_format": "wectf{...}"
            }
        ],
        "pwn": [
            {
                "name": "IoT_ARM_Binary",
                "category": "Pwn",
                "platform": "WECTF",
                "year": "2024",
                "difficulty": "Expert",
                "points": 440,
                "techniques": ["IoT", "ARM", "binary", "ROP"],
                "flag_format": "wectf{...}"
            }
        ],
        "crypto": [
            {
                "name": "LWE_with_Hints",
                "category": "Cryptography",
                "platform": "WECTF",
                "year": "2023",
                "difficulty": "Expert",
                "points": 420,
                "techniques": ["LWE", "hints", "lattice", "reduction"],
                "flag_format": "wectf{...}"
            }
        ]
    }
}

def round_14_iteration():
    """第14轮迭代"""

    print("=" * 80)
    print("🚀 第14轮迭代 - RWCTF, CuberCTF, WECTF (专业平台)")
    print("=" * 80)

    total_challenges = 0
    total_points = 0
    all_platforms = []

    for platform, categories in ROUND_14_PLATFORMS.items():
        all_platforms.append(platform)

        for category, challenges in categories.items():
            total_challenges += len(challenges)
            total_points += sum(c["points"] for c in challenges)

            print(f"\n📁 Platform: {platform.upper()} | Category: {category.upper()}")
            print(f"   Challenges: {len(challenges)} | Points: {sum(c['points'] for c in challenges)}")

            for challenge in challenges:
                print(f"   • {challenge['name']} ({challenge['difficulty']}, {challenge['points']}分)")
                print(f"      技术: {', '.join(challenge['techniques'])}")

    print("\n" + "=" * 80)
    print(f"📊 第14轮统计:")
    print(f"  • 新增平台: {len(all_platforms)}个 [RWCTF, CuberCTF, WECTF]")
    print(f"  • 新增题目: {total_challenges}题")
    print(f"  • 新增分数: {total_points}分")
    print("=" * 80)

    training_data = {
        "round": 14,
        "platforms": all_platforms,
        "total_new_challenges": total_challenges,
        "total_new_points": total_points,
        "timestamp": "2026-02-25 23:40:00",
        "categories": ROUND_14_PLATFORMS
    }

    with open("/round14_data.json", "w") as f:
        json.dump(training_data, f, indent=4)

    print(f"\n💾 数据已保存: /round14_data.json")

    return {
        "round": 14,
        "platforms": all_platforms,
        "total_new_challenges": total_challenges,
        "total_new_points": total_points
    }

if __name__ == "__main__":
    result = round_14_iteration()

    print("\n✅ 第14轮迭代完成！")
    print(f"🎯 新增: {result['total_new_challenges']}题")
    print(f"🏆 新增: {result['total_new_points']}分")
    print(f"🎯 平台: {', '.join(result['platforms'])}")

    print("\n📦 Git提交...")
    import subprocess
    subprocess.run(["git", "add", "/round14_data.json"], cwd="/")
    subprocess.run(["git", "commit", "-m", "feat: Round 14 - RWCTF CuberCTF WECTF"], cwd="/")
    subprocess.run(["git", "push", "origin", "master"], cwd="/")

    print("\n✅ 第14轮完成！" )
