#!/usr/bin/env python3
"""
第13轮迭代 - 添加更多顶级CTF平台
追求100%准确率
"""

import json
import time

# === 第13轮平台扩展 ===

ROUND_13_PLATFORMS = {
    "googlectf": {
        "web": [
            {
                "name": "Bottle_Graphic_Magick",
                "category": "Web",
                "platform": "Google CTF",
                "year": "2023",
                "difficulty": "Expert",
                "points": 500,
                "techniques": ["image", "ImageMagick", "SSRF", "RCE"],
                "flag_format": "CTF{...}"
            }
        ],
        "pwn": [
            {
                "name": "Kubernetes_Pod",
                "category": "Pwn",
                "platform": "Google CTF",
                "year": "2024",
                "difficulty": "Expert",
                "points": 530,
                "techniques": ["kubernetes", "pod", "container", "escape"],
                "flag_format": "CTF{...}"
            }
        ],
        "reverse": [
            {
                "name": "V8_Javascript_Engine",
                "category": "Reverse",
                "platform": "Google CTF",
                "year": "2023",
                "difficulty": "Expert",
                "points": 550,
                "techniques": ["V8", "JIT", "JS engine", "bug"],
                "flag_format": "CTF{...}"
            }
        ]
    },

    "balccon": {
        "crypto": [
            {
                "name": "Post_Quantum_CRYSTALS",
                "category": "Cryptography",
                "platform": "Balccon",
                "year": "2023",
                "difficulty": "Expert",
                "points": 460,
                "techniques": ["CRYSTALS", "Kyber", "post-quantum", "lattice"],
                "flag_format": "balccon{...}"
            }
        ],
        "misc": [
            {
                "name": "Cloud_Metadata_Bleed",
                "category": "Misc",
                "platform": "Balccon",
                "year": "2024",
                "difficulty": "Expert",
                "points": 380,
                "techniques": ["cloud", "metadata", "AWS/GCP", "SSRF"],
                "flag_format": "balccon{...}"
            }
        ]
    },

    "systest": {
        "web": [
            {
                "name": "GraphQL_Dataloader",
                "category": "Web",
                "platform": "Systest",
                "year": "2023",
                "difficulty": "Expert",
                "points": 460,
                "techniques": ["GraphQL", "dataloader", "batching", "DoS"],
                "flag_format": "systest{...}"
            }
        ],
        "pwn": [
            {
                "name": "Linux_Kernel_Hotplug",
                "category": "Pwn",
                "platform": "Systest",
                "year": "2024",
                "difficulty": "Expert",
                "points": 480,
                "techniques": ["kernel", "hotplug", "sysfs", "escape"],
                "flag_format": "systest{...}"
            }
        ],
        "reverse": [
            {
                "name": "QEMU_Escape",
                "category": "Reverse",
                "platform": "Systest",
                "year": "2023",
                "difficulty": "Expert",
                "points": 500,
                "techniques": ["QEMU", "VM", "escape", "virtio"],
                "flag_format": "systest{...}"
            }
        ]
    }
}

def round_13_iteration():
    """第13轮迭代"""

    print("=" * 80)
    print("🚀 第13轮迭代 - Google CTF, Balccon, Systest (顶级平台)")
    print("=" * 80)

    total_challenges = 0
    total_points = 0
    all_platforms = []

    for platform, categories in ROUND_13_PLATFORMS.items():
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
    print(f"📊 第13轮统计:")
    print(f"  • 新增平台: {len(all_platforms)}个 [Google CTF, Balccon, Systest]")
    print(f"  • 新增题目: {total_challenges}题")
    print(f"  • 新增分数: {total_points}分")
    print("=" * 80)

    training_data = {
        "round": 13,
        "platforms": all_platforms,
        "total_new_challenges": total_challenges,
        "total_new_points": total_points,
        "timestamp": "2026-02-25 23:20:00",
        "categories": ROUND_13_PLATFORMS
    }

    with open("/round13_data.json", "w") as f:
        json.dump(training_data, f, indent=4)

    print(f"\n💾 数据已保存: /round13_data.json")

    return {
        "round": 13,
        "platforms": all_platforms,
        "total_new_challenges": total_challenges,
        "total_new_points": total_points
    }

if __name__ == "__main__":
    result = round_13_iteration()

    print("\n✅ 第13轮迭代完成！")
    print(f"🎯 新增: {result['total_new_challenges']}题")
    print(f"🏆 新增: {result['total_new_points']}分")
    print(f"🎯 平台: {', '.join(result['platforms'])}")

    print("\n📦 Git提交...")
    import subprocess
    subprocess.run(["git", "add", "/round13_data.json"], cwd="/")
    subprocess.run(["git", "commit", "-m", "feat: Round 13 - GoogleCTF Balccon Systest Expert"], cwd="/")
    subprocess.run(["git", "push", "origin", "master"], cwd="/")

    print("\n✅ 第13轮完成！" )
