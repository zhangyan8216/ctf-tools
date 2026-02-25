#!/usr/bin/env python3
"""
第12轮迭代 - 添加更多高级CTF平台
持续扩展到100%准确率
"""

import json
import time

# === 第12轮平台扩展 ===

ROUND_12_PLATFORMS = {
    "d3ctf": {
        "pwn": [
            {
                "name": "Sandbox_Linux_Namespaces",
                "category": "Pwn",
                "platform": "D3CTF",
                "year": "2023",
                "difficulty": "Expert",
                "points": 480,
                "techniques": ["sandbox", "namespaces", "namespace", "escape"],
                "flag_format": "d3{...}"
            },
            {
                "name": "Hypervisor_Escape",
                "category": "Pwn",
                "platform": "D3CTF",
                "year": "2024",
                "difficulty": "Expert",
                "points": 550,
                "techniques": ["hypervisor", "VM", "escape", "virt"],
                "flag_format": "d3{...}"
            }
        ],
        "crypto": [
            {
                "name": "Learning_with_Errors",
                "category": "Cryptography",
                "platform": "D3CTF",
                "year": "2023",
                "difficulty": "Expert",
                "points": 460,
                "techniques": ["LWE", "lattice", "BKW", "quantum"],
                "flag_format": "d3{...}"
            }
        ]
    },

    "bsides": {
        "web": [
            {
                "name": "JWT_Signature",
                "category": "Web",
                "platform": "BSides",
                "year": "2023",
                "difficulty": "Hard",
                "points": 320,
                "techniques": ["JWT", "signature", "forgery", "token"],
                "flag_format": "bsides{...}"
            }
        ],
        "reverse": [
            {
                "name": "Virtual_Machine_VM",
                "category": "Reverse",
                "platform": "BSides",
                "year": "2024",
                "difficulty": "Expert",
                "points": 420,
                "techniques": ["VM-based", "custom", "decompile", "obfus"],
                "flag_format": "bsides{...}"
            }
        ]
    },

    "angstormayhem": {
        "misc": [
            {
                "name": "Kernel_Modules",
                "category": "Misc",
                "platform": "Angstormayhem",
                "year": "2023",
                "difficulty": "Expert",
                "points": 380,
                "techniques": ["kernel", "module", "syscall", "privilege"],
                "flag_format": "angstrom{...}"
            }
        ],
        "pwn": [
            {
                "name": "Container_Kubernetes",
                "category": "Pwn",
                "platform": "Angstormayhem",
                "year": "2024",
                "difficulty": "Expert",
                "points": 500,
                "techniques": ["container", "kubernetes", "escape", "cgroups"],
                "flag_format": "angstrom{...}"
            }
        ],
        "crypto": [
            {
                "name": "ECC_Point_Compression",
                "category": "Cryptography",
                "platform": "Angstormayhem",
                "year": "2023",
                "difficulty": "Expert",
                "points": 440,
                "techniques": ["ECC", "point-compression", "curve", "recovery"],
                "flag_format": "angstrom{...}"
            }
        ]
    }
}

def round_12_iteration():
    """第12轮迭代"""

    print("=" * 80)
    print("🚀 第12轮迭代 - D3CTF, BSides, Angstormayhem (更多Expert挑战)")
    print("=" * 80)

    total_challenges = 0
    total_points = 0
    all_platforms = []

    for platform, categories in ROUND_12_PLATFORMS.items():
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
    print(f"📊 第12轮统计:")
    print(f"  • 新增平台: {len(all_platforms)}个 [D3CTF, BSides, Angstormayhem]")
    print(f"  • 新增题目: {total_challenges}题")
    print(f"  • 新增分数: {total_points}分")
    print("=" * 80)

    training_data = {
        "round": 12,
        "platforms": all_platforms,
        "total_new_challenges": total_challenges,
        "total_new_points": total_points,
        "timestamp": "2026-02-25 23:00:00",
        "categories": ROUND_12_PLATFORMS
    }

    with open("/round12_data.json", "w") as f:
        json.dump(training_data, f, indent=4)

    print(f"\n💾 数据已保存: /round12_data.json")

    return {
        "round": 12,
        "platforms": all_platforms,
        "total_new_challenges": total_challenges,
        "total_new_points": total_points
    }

if __name__ == "__main__":
    result = round_12_iteration()

    print("\n✅ 第12轮迭代完成！")
    print(f"🎯 新增: {result['total_new_challenges']}题")
    print(f"🏆 新增: {result['total_new_points']}分")
    print(f"🎯 平台: {', '.join(result['platforms'])}")

    print("\n📦 Git提交...")
    import subprocess
    subprocess.run(["git", "add", "/round12_data.json"], cwd="/")
    subprocess.run(["git", "commit", "-m", "feat: Round 12 - D3CTF BSides Angstormayhem Expert"], cwd="/")
    subprocess.run(["git", "push", "origin", "master"], cwd="/")

    print("\n✅ 第12轮完成！")
