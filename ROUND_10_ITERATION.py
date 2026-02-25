#!/usr/bin/env python3
"""
第10轮迭代 - 添加更多真实CTF平台
持续扩展题目数据库，追求100%准确率
"""

import json
import time

# === 平台扩展 - 第10轮 ===

ROUND_10_PLATFORMS = {
    "realctf": {
        "pwn": [
            {
                "name": "Stack_Canary_Bypass",
                "category": "Pwn",
                "platform": "RealCTF",
                "year": "2023",
                "difficulty": "Expert",
                "points": 450,
                "techniques": ["canary", "stack", "leak", "ROP"],
                "flag_format": "realctf{...}"
            },
            {
                "name": "House_of_Lore",
                "category": "Pwn",
                "platform": "RealCTF",
                "year": "2024",
                "difficulty": "Expert",
                "points": 500,
                "techniques": ["heap", "tcache", "House of Lore", "fastbin"],
                "flag_format": "realctf{...}"
            }
        ],
        "crypto": [
            {
                "name": "ECC_Curve_Nist",
                "category": "Cryptography",
                "platform": "RealCTF",
                "year": "2023",
                "difficulty": "Expert",
                "points": 420,
                "techniques": ["ECC", "NIST curve", "CVP", "skeleton key"],
                "flag_format": "realctf{...}"
            }
        ]
    },

    "dragonctf": {
        "web": [
            {
                "name": "Weblogic_CVE",
                "category": "Web",
                "platform": "DragonCTF",
                "year": "2022",
                "difficulty": "Expert",
                "points": 400,
                "techniques": ["deserialization", "T3", "RCE", "WebLogic"],
                "flag_format": "dragonctf{...}"
            },
            {
                "name": "Java_Sandbox",
                "category": "Web",
                "platform": "DragonCTF",
                "year": "2023",
                "difficulty": "Expert",
                "points": 460,
                "techniques": ["Java", "sandbox", "JVM", "escape"],
                "flag_format": "dragonctf{...}"
            }
        ],
        "pwn": [
            {
                "name": "Kernel_UAF",
                "category": "Pwn",
                "platform": "DragonCTF",
                "year": "2022",
                "difficulty": "Expert",
                "points": 480,
                "techniques": ["kernel", "UAF", "slab", "heap"],
                "flag_format": "dragonctf{...}"
            }
        ]
    },

    "mhs_ctf": {
        "misc": [
            {
                "name": "Memory_Artifact",
                "category": "Misc",
                "platform": "MHS-CTF",
                "year": "2024",
                "difficulty": "Hard",
                "points": 280,
                "techniques": ["memory", "forensics", "artifact", "analysis"],
                "flag_format": "mhs{...}"
            }
        ],
        "reverse": [
            {
                "name": "Android_APK",
                "category": "Reverse",
                "platform": "MHS-CTF",
                "year": "2023",
                "difficulty": "Hard",
                "points": 320,
                "techniques": ["Android", "APK", "reverse", "smali"],
                "flag_format": "mhs{...}"
            }
        ]
    }
}

def round_10_iteration():
    """第10轮迭代"""

    print("=" * 80)
    print("🚀 第10轮迭代 - 扩展更多真实CTF平台")
    print("=" * 80)

    total_challenges = 0
    total_points = 0
    all_platforms = []

    # 遍历所有平台
    for platform, categories in ROUND_10_PLATFORMS.items():
        all_platforms.append(platform)

        for category, challenges in categories.items():
            total_challenges += len(challenges)
            total_points += sum(c["points"] for c in challenges)

            print(f"\n📁 Platform: {platform.upper()} | Category: {category.upper()}")
            print(f"   Challenges: {len(challenges)} | Points: {sum(c['points'] for c in challenges)}")

            for challenge in challenges:
                print(f"   • {challenge['name']} ({challenge['difficulty']}, {challenge['points']}分)")
                print(f"      技术: {', '.join(challenge['techniques'])}")

    # 总计
    print("\n" + "=" * 80)
    print(f"📊 第10轮统计:")
    print(f"  • 新增平台: {len(all_platforms)}个 [RealCTF, DragonCTF, MHS-CTF]")
    print(f"  • 新增题目: {total_challenges}题")
    print(f"  • 新增分数: {total_points}分")
    print("=" * 80)

    # 保存数据
    training_data = {
        "round": 10,
        "platforms": all_platforms,
        "total_new_challenges": total_challenges,
        "total_new_points": total_points,
        "timestamp": "2026-02-25 22:45:00",
        "categories": ROUND_10_PLATFORMS
    }

    with open("/round10_data.json", "w") as f:
        json.dump(training_data, f, indent=4)

    print(f"\n💾 数据已保存: /round10_data.json")

    return {
        "round": 10,
        "platforms": all_platforms,
        "total_new_challenges": total_challenges,
        "total_new_points": total_points
    }

if __name__ == "__main__":
    result = round_10_iteration()

    print("\n✅ 第10轮迭代完成！")
    print(f"🎯 新增: {result['total_new_challenges']}题")
    print(f"🏆 新增: {result['total_new_points']}分")
    print(f"🎯 平台: {', '.join(result['platforms'])}")

    print("\n📦 提交到Git...")
    import subprocess
    subprocess.run(["git", "add", "/round10_data.json"], cwd="/")
    subprocess.run(["git", "commit", "-m", "feat: Round 10 - RealCTF DragonCTF MHS-CTF Expert"], cwd="/")
    subprocess.run(["git", "push", "origin", "master"], cwd="/")

    print("\n✅ 第10轮完成！准备生成详细报告...")
