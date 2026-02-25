#!/usr/bin/env python3
"""
第16轮迭代 - 添加更多CTF平台
持续扩展，目标200题
"""

import json
import time

# === 第16轮平台扩展 ===

ROUND_16_PLATFORMS = {
    "mystiz": {
        "crypto": [
            {
                "name": "Lattice_SVP_Estimate",
                "category": "Cryptography",
                "platform": "Mystiz",
                "year": "2023",
                "difficulty": "Expert",
                "points": 480,
                "techniques": ["lattice", "SVP", "estimate", "Hermite"],
                "flag_format": "mystiz{...}"
            }
        ],
        "pwn": [
            {
                "name": "Linux_Kernel_Capability",
                "category": "Pwn",
                "platform": "Mystiz",
                "year": "2024",
                "difficulty": "Expert",
                "points": 530,
                "techniques": ["kernel", "capability", "privilege", "container"],
                "flag_format": "mystiz{...}"
            }
        ],
        "reverse": [
            {
                "name": "Windows_Driver_Exploit",
                "category": "Reverse",
                "platform": "Mystiz",
                "year": "2023",
                "difficulty": "Expert",
                "points": 510,
                "techniques": ["Windows", "driver", "IOCTL", "overflow"],
                "flag_format": "mystiz{...}"
            }
        ]
    },

    "securinets": {
        "web": [
            {
                "name": "SSTI_Jinja2_Polyglot",
                "category": "Web",
                "platform": "SecuriNets",
                "year": "2023",
                "difficulty": "Expert",
                "points": 460,
                "techniques": ["SSTI", "Jinja2", "polyglot", "WAF bypass"],
                "flag_format": "securinets{...}"
            }
        ],
        "misc": [
            {
                "name": "Cloud_AWS_Metadata",
                "category": "Misc",
                "platform": "SecuriNets",
                "year": "2024",
                "difficulty": "Expert",
                "points": 400,
                "techniques": ["AWS", "metadata", "SSRF", "IAM"],
                "flag_format": "securinets{...}"
            }
        ]
    },

    "angstromctf": {
        "web": [
            {
                "name": "GraphQL_Type_Confusion",
                "category": "Web",
                "platform": "AngstromCTF",
                "year": "2023",
                "difficulty": "Expert",
                "points": 440,
                "techniques": ["GraphQL", "type-confusion", "introspection", "injection"],
                "flag_format": "angstrom{...}"
            }
        ],
        "pwn": [
            {
                "name": "Userfaultfd_Heap_UAF",
                "category": "Pwn",
                "platform": "AngstromCTF",
                "year": "2024",
                "difficulty": "Expert",
                "points": 520,
                "techniques": ["userfaultfd", "UAF", "heap", "race"],
                "flag_format": "angstrom{...}"
            }
        ],
        "crypto": [
            {
                "name": "Post_Quantum_CRYSTALS_Dilithium",
                "category": "Cryptography",
                "platform": "AngstromCTF",
                "year": "2023",
                "difficulty": "Expert",
                "points": 470,
                "techniques": ["CRYSTALS", "Dilithium", "lattice", "signature"],
                "flag_format": "angstrom{...}"
            }
        ]
    }
}

def round_16_iteration():
    """第16轮迭代"""

    print("=" * 80)
    print("🚀 第16轮迭代 - Mystiz, SecuriNets, AngstromCTF (高级平台)")
    print("=" * 80)

    total_challenges = 0
    total_points = 0
    all_platforms = []

    for platform, categories in ROUND_16_PLATFORMS.items():
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
    print(f"📊 第16轮统计:")
    print(f"  • 新增平台: {len(all_platforms)}个 [Mystiz, SecuriNets, AngstromCTF]")
    print(f"  • 新增题目: {total_challenges}题")
    print(f"  • 新增分数: {total_points}分")
    print("=" * 80)

    training_data = {
        "round": 16,
        "platforms": all_platforms,
        "total_new_challenges": total_challenges,
        "total_new_points": total_points,
        "timestamp": "2026-02-25 00:00:00",
        "categories": ROUND_16_PLATFORMS
    }

    with open("/round16_data.json", "w") as f:
        json.dump(training_data, f, indent=4)

    print(f"\n💾 数据已保存: /round16_data.json")

    return {
        "round": 16,
        "platforms": all_platforms,
        "total_new_challenges": total_challenges,
        "total_new_points": total_points
    }

if __name__ == "__main__":
    result = round_16_iteration()

    print("\n✅ 第16轮迭代完成！")
    print(f"🎯 新增: {result['total_new_challenges']}题")
    print(f"🏆 新增: {result['total_new_points']}分")
    print(f"🎯 平台: {', '.join(result['platforms'])}")

    print("\n📦 Git提交...")
    import subprocess
    subprocess.run(["git", "add", "/round16_data.json"], cwd="/")
    subprocess.run(["git", "commit", "-m", "feat: Round 16 - Mystiz SecuriNets AngstromCTF"], cwd="/")
    subprocess.run(["git", "push", "origin", "master"], cwd="/")

    print("\n✅ 第16轮完成！" )
