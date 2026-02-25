#!/usr/bin/env python3
"""
第15轮详细报告 + 第6-15轮汇总
"""

import json
import subprocess
from datetime import datetime

print("=" * 80)
print("📋 第15轮迭代详细报告")
print("=" * 80)

print(f"\n⏰ 报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# === 第15轮数据 ===
round15_report = {
    "轮次": "第15轮",
    "时间": "2026-02-25 23:50:00",
    "平台": ["zer0pts", "PBCTF", "ZeroNights"],
    "题目数": 8,
    "分数": 3700,
    "描述": "zer0pts (3题), PBCTF (2题), ZeroNights (3题)",
    "新增技术": [
        "XSS Document Domain", "Userfaultfd Syscall", "Elliptic Pairing",
        "GraphQL N+1", "Cloud Firewall Bypass", "Linux Kernel Syscall",
        "Android NDK", "Lattice Reduction BKZ"
    ]
}

print("\n📊 第15轮详情:")
print("-" * 80)
print(f"  • 平台: {', '.join(round15_report['平台'])}")
print(f"  • 题目: {round15_report['题目数']}题")
print(f"  • 分数: {round15_report['分数']}分")
print(f"  • 描述: {round15_report['描述']}")

print("\n🤖 新增技能 (8项):")
for i, skill in enumerate(round15_report['新增技术'], 1):
    print(f"  {i}. {skill}")

# === 累计统计 (第6-15轮) ===
rounds_6_to_15 = [
    {"轮次": "第6轮", "题目": 22, "分数": 5000, "平台": ["CCTF", "ByteCTF", "DEFCON CTF"]},
    {"轮次": "第7轮", "题目": 8, "分数": 915, "平台": ["SecurityTrails", "BlackHat", "GhostInTheShell"]},
    {"轮次": "第8轮", "题目": 8, "分数": 710, "平台": ["AttackDefense", "HackTM扩展", "TCTF"]},
    {"轮次": "第9轮", "题目": 6, "分数": 790, "平台": ["HITCON", "CyCon", "SU-CTF"]},
    {"轮次": "第10轮", "题目": 8, "分数": 3310, "平台": ["RealCTF", "DragonCTF", "MHS-CTF"]},
    {"轮次": "第11轮", "题目": 8, "分数": 3540, "平台": ["PlaidCTF", "Codegate", "Tokyowesterns"]},
    {"轮次": "第12轮", "题目": 8, "分数": 3550, "平台": ["D3CTF", "BSides", "Angstormayhem"]},
    {"轮次": "第13轮", "题目": 7, "分数": 3840, "平台": ["Google CTF", "Balccon", "Systest"]},
    {"轮次": "第14轮", "题目": 7, "分数": 3520, "平台": ["RWCTF", "CuberCTF", "WECTF"]},
    {"轮次": "第15轮", "题目": 8, "分数": 3700, "平台": ["zer0pts", "PBCTF", "ZeroNights"]},
]

total_new_6_15 = sum(r["题目"] for r in rounds_6_to_15)
total_points_6_15 = sum(r["分数"] for r in rounds_6_to_15)

print("\n" + "=" * 80)
print("📈 第6-15轮累计统计")
print("=" * 80)

print(f"\n各轮详情:")
for r in rounds_6_to_15:
    print(f"\n{r['轮次']}: {r['题目']}题, {r['分数']}分")

print(f"\n📊 累计:")
print(f"  • 新增题目: {total_new_6_15}题")
print(f"  • 新增分数: {total_points_6_15}分")
print(f"  • 原有题目: 85题")
print(f"  • 现在总计: {85 + total_new_6_15} = {85 + total_new_6_15}题")

# 总平台
all_platforms_6_15 = []
for r in rounds_6_to_15:
    all_platforms_6_15.extend(r["平台"])

unique_platforms_6_15 = sorted(list(set(all_platforms_6_15)))
print(f"\n🌍 第6-15轮平台数: {len(unique_platforms_6_15)}个")
for i, platform in enumerate(unique_platforms_6_15, 1):
    print(f"  {i:2d}. {platform}")

# Git
result = subprocess.run(["git", "log", "--oneline", "-1"], cwd="/", capture_output=True, text=True)
print(f"\n📦 最新Git提交: {result.stdout.strip()}")

# 能力矩阵更新
print("\n" + "=" * 80)
print("🎯 能力矩阵更新 (第15轮后)")
print("=" * 80)

capability_categories = {
    "Web 安全": ["SQLi", "XSS", "SSRF", "XXE", "SSTI", "Deserialization", "Race Condi", "WebLogic RCE", "Cache Poison", "GraphQL", "JWT Forgery", "GraphQL Dataloader", "ImageMagick", "Cloud Metadata", "NoSQL Injection", "DNS Rebind", "XSS Document Domain", "GraphQL N+1"],
    "密码学": ["RSA", "AES", "ECC", "Lattice", "Post-Quantum", "LFSR", "ECC CVP", "NTRU", "LWE Quantum", "ECC Point Compression", "CRYSTALS Kyber", "ECC Nonce Deterministic", "LWE with Hints", "Elliptic Pairing", "Lattice Reduction LLL BKZ"],
    "二进制利用": ["BOF", "ROP", "ret2libc", "Heap Exploit", "Kernel Pwn", "Canary Bypass", "House of Lore", "Seccomp Sandbox Escape", "Kernel Heap Spray", "Hypervisor Escape", "Container Kubernetes", "Kernel Module", "Kubernetes Pod", "Linux Kernel Hotplug", "Userfaultfd Heap", "Windows Kernel", "IoT ARM", "Userfaultfd Syscall", "Linux Kernel Privilege"],
    "逆向工程": ["Static", "Dynamic", "Anti-Debug", "Android APK Reverse", "VM Obfuscation", "Custom VM Decompiler", "V8 JIT", "QEMU Escape", "Windows Driver", "Android NDK"],
    "数字取证": ["Forensics", "PCAP", "Stego", "Memory Artifact", "Container Escape", "USB Traffic", "Linux Namespaces", "Docker Registry", "Cloud Firewall Bypass"]
}

total_skills = sum(len(skills) for skills in capability_categories.values())

for category, skills in capability_categories.items():
    print(f"\n{category}: {len(skills)}项")
    for skill in skills:
        print(f"  • {skill}")

print(f"\n📊 总技能数: {total_skills}项 (+7)")

# 完成状态
print("\n" + "=" * 80)
print("✅ 第15轮迭代完成！")
print("=" * 80)

final_summary = {
    "第15轮时间": "2026-02-25 23:50:00",
    "第6-15轮新增": total_new_6_15,
    "第6-15轮分数": total_points_6_15,
    "现在总计": 85 + total_new_6_15,
    "第6-15轮平台": unique_platforms_6_15,
    "Git提交": result.stdout.strip().split(" ")[0] if " " in result.stdout.strip() else result.stdout.strip(),
    "总技能数": total_skills
}

with open("/ROUND_15_SUMMARY.json", "w") as f:
    json.dump(final_summary, f, indent=4)

print(f"\n💾 报告已保存: /ROUND_15_SUMMARY.json")
