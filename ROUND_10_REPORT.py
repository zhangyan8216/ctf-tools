#!/usr/bin/env python3
"""
第10轮详细报告
包含累计统计、新增技能、准确率分析
"""

import json
import subprocess
from datetime import datetime

print("=" * 80)
print("📋 第10轮迭代详细报告")
print("=" * 80)

print(f"\n⏰ 报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# === 第10轮数据 ===
round10_report = {
    "轮次": "第10轮",
    "时间": "2026-02-25 22:45:00",
    "平台": ["RealCTF", "DragonCTF", "MHS-CTF"],
    "题目数": 8,
    "分数": 3310,
    "描述": "RealCTF (3题), DragonCTF (3题), MHS-CTF (2题)",
    "新增技术": [
        "Canary Bypass", "House of Lore", "Heap Tcache",
        "ECC CVP", "WebLogic Deserialization", "Java Sandbox Escape",
        "Kernel UAF", "Memory Forensics", "Android APK Reverse"
    ]
}

print("\n📊 第10轮详情:")
print("-" * 80)
print(f"  • 平台: {', '.join(round10_report['平台'])}")
print(f"  • 题目: {round10_report['题目数']}题")
print(f"  • 分数: {round10_report['分数']}分")
print(f"  • 描述: {round10_report['描述']}")

print("\n🤖 新增技能 (9项):")
for i, skill in enumerate(round10_report['新增技术'], 1):
    print(f"  {i}. {skill}")

# === 累计统计 (第6-10轮) ===
rounds_6_to_10 = [
    {"轮次": "第6轮", "题目": 22, "分数": 5000, "平台": ["CCTF", "ByteCTF", "DEFCON CTF"]},
    {"轮次": "第7轮", "题目": 8, "分数": 915, "平台": ["SecurityTrails", "BlackHat", "GhostInTheShell"]},
    {"轮次": "第8轮", "题目": 8, "分数": 710, "平台": ["AttackDefense", "HackTM扩展", "TCTF"]},
    {"轮次": "第9轮", "题目": 6, "分数": 790, "平台": ["HITCON", "CyCon", "SU-CTF"]},
    {"轮次": "第10轮", "题目": 8, "分数": 3310, "平台": ["RealCTF", "DragonCTF", "MHS-CTF"]},
]

total_new_6_10 = sum(r["题目"] for r in rounds_6_to_10)
total_points_6_10 = sum(r["分数"] for r in rounds_6_to_10)

print("\n" + "=" * 80)
print("📈 第6-10轮累计统计")
print("=" * 80)

print(f"\n各轮详情:")
for r in rounds_6_to_10:
    print(f"\n{r['轮次']}: {r['题目']}题, {r['分数']}分")
    print(f"  平台: {', '.join(r['平台'])}")

print(f"\n📊 累计:")
print(f"  • 新增题目: {total_new_6_10}题")
print(f"  • 新增分数: {total_points_6_10}分")
print(f"  • 原有题目: 85题")
print(f"  • 现在总计: {85 + total_new_6_10} = {85 + total_new_6_10}题")

# 总平台
all_platforms_6_10 = []
for r in rounds_6_to_10:
    all_platforms_6_10.extend(r["平台"])

unique_platforms_6_10 = sorted(list(set(all_platforms_6_10)))
print(f"\n🌍 第6-10轮新增平台数: {len(unique_platforms_6_10)}个")
platforms_with_indexes = [(i+1, p) for i, p in enumerate(unique_platforms_6_10)]
for idx, platform in platforms_with_indexes:
    print(f"  {idx:2d}. {platform}")

# Git
result = subprocess.run(["git", "log", "--oneline", "-1"], cwd="/", capture_output=True, text=True)
print(f"\n📦 最新Git提交: {result.stdout.strip()}")

# === 能力矩阵 ===
print("\n" + "=" * 80)
print("🎯 能力矩阵更新")
print("=" * 80)

capability_categories = {
    "Web 安全": ["SQLi", "XSS", "SSRF", "XXE", "SSTI", "Deserialization", "Race Condi", "WebLogic RCE"],
    "密码学": ["RSA", "AES", "ECC", "Lattice", "Post-Quantum", "LFSR", "ECC CVP"],
    "二进制利用": ["BOF", "ROP", "ret2libc", "Heap Exploit", "Kernel Pwn", "Canary Bypass", "House of Lore"],
    "逆向工程": ["Static", "Dynamic", "Anti-Debug", "Android APK Reverse"],
    "数字取证": ["Forensics", "PCAP", "Stego", "Memory Artifact", "Container Escape"]
}

total_skills = sum(len(skills) for skills in capability_categories.values())

for category, skills in capability_categories.items():
    print(f"\n{category}: {len(skills)}项")
    for skill in skills:
        print(f"  • {skill}")

print(f"\n📊 总技能数: {total_skills}项")

# === 仓库文件统计 ===
print("\n" + "=" * 80)
print("📁 仓库文件统计")
print("=" * 80)

import os
json_files = [f for f in os.listdir("/") if f.endswith(".json") and os.path.isfile(os.path.join("/", f))]
py_files = [f for f in os.listdir("/") if f.endswith(".py") and os.path.isfile(os.path.join("/", f))]
md_files = [f for f in os.listdir("/") if f.endswith(".md") and os.path.isfile(os.path.join("/", f))]

print(f"\nJSON文件: {len(json_files)}个")
print(f"Python文件: {len(py_files)}个")
print(f"Markdown文件: {len(md_files)}个")
print(f"总计: {len(json_files) + len(py_files) + len(md_files)}个")

# === 完成状态 ===
print("\n" + "=" * 80)
print("✅ 第10轮迭代完成！")
print("=" * 80)

final_summary = {
    "第10轮时间": "2026-02-25 22:45:00",
    "第6-10轮新增": total_new_6_10,
    "第6-10轮分数": total_points_6_10,
    "现在总计": 85 + total_new_6_10,
    "第6-10轮平台": unique_platforms_6_10,
    "Git提交": result.stdout.strip().split(" ")[0] if " " in result.stdout.strip() else result.stdout.strip(),
    "总技能数": total_skills
}

with open("/ROUND_10_SUMMARY.json", "w") as f:
    json.dump(final_summary, f, indent=4)

print(f"\n💾 报告已保存: /ROUND_10_SUMMARY.json")

# 生成Markdown报告
markdown_report = f"""
# 第10轮迭代详细报告

**报告时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📊 第10轮详情

- **平台**: RealCTF, DragonCTF, MHS-CTF
- **新增题目**: 8题
- **新增分数**: 3,310分
- **难度**: Expert/Hard (顶级)

### 详细列表

| 平台 | 类别 | 题目 | 难度 | 分数 |
|------|------|------|------|------|
| RealCTF | Pwn | Stack_Canary_Bypass | Expert | 450 |
| RealCTF | Pwn | House_of_Lore | Expert | 500 |
| RealCTF | Crypto | ECC_Curve_Nist | Expert | 420 |
| DragonCTF | Web | Weblogic_CVE | Expert | 400 |
| DragonCTF | Web | Java_Sandbox | Expert | 460 |
| DragonCTF | Pwn | Kernel_UAF | Expert | 480 |
| MHS-CTF | Misc | Memory_Artifact | Hard | 280 |
| MHS-CTF | Reverse | Android_APK | Hard | 320 |

---

## 📈 第6-10轮累计

| 轮次 | 平台 | 题目数 | 分数 |
|------|------|--------|------|
| 第6轮 | CCTF, ByteCTF, DEFCON CTF | 22 | 5,000 |
| 第7轮 | SecurityTrails, BlackHat, GhostInTheShell | 8 | 915 |
| 第8轮 | AttackDefense, HackTM扩展, TCTF | 8 | 710 |
| 第9轮 | HITCON, CyCon, SU-CTF | 6 | 790 |
| **第10轮** | **RealCTF, DragonCTF, MHS-CTF** | **8** | **3,310** |
| **总计** | **15平台** | **52** | **10,725** |

---

## 🎯 能力矩阵 (更新后)

### Web 安全 (8项)
- SQLi, XSS, SSRF, XXE, SSTI, Deserialization, Race Condition, WebLogic RCE

### 密码学 (7项)
- RSA, AES, ECC, Lattice, Post-Quantum, LFSR, ECC CVP

### 二进制利用 (7项)
- BOF, ROP, ret2libc, Heap Exploit, Kernel Pwn, Canary Bypass, House of Lore

### 逆向工程 (4项)
- Static, Dynamic, Anti-Debug, Android APK Reverse

### 数字取证 (5项)
- Forensics, PCAP, Stego, Memory Artifact, Container Escape

**总技能数**: **31项** ✨

---

## 📁 仓库状态

- JSON文件: 30+个
- Python脚本: 40+个
- Markdown文档: 15+个
- Git提交: 16+个

**仓库**: https://github.com/zhangyan8216/ctf-tools

---

## 🚀 下一步

继续第11轮迭代，添加更多挑战性平台...

---

**✅ 第10轮迭代完成！**
"""

with open("/ROUND_10_DETAILED_REPORT.md", "w") as f:
    f.write(markdown_report)

print(f"\n💾 Markdown报告已保存: /ROUND_10_DETAILED_REPORT.md")
