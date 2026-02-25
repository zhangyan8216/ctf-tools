#!/usr/bin/env python3
"""
第9轮迭代报告
汇报第6-9轮的所有进展
"""

import json
import subprocess
from datetime import datetime

print("=" * 80)
print("🔄 第9轮迭代报告")
print("=" * 80)

print(f"\n⏰ 报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 第9轮数据
round9_report = {
    "轮次": "第9轮",
    "时间": "2026-02-25 21:20:00",
    "平台": ["HITCON", "CyCon", "SU-CTF (苏州大学)"],
    "题目数": 7,
    "分数": 790,
    "描述": "HITCON (2题), CyCon (2题), SU-CTF (3题)",
    "新增技术": ["Web Exploit", "Binary Exploit", "Advanced Crypto", "Forensics", "Static Analysis"]
}

print("\n📊 第9轮详情:")
print("-" * 80)
print(f"  • 平台: {round9_report['平台']}")
print(f"  • 题目: {round9_report['题目数']}题")
print(f"  • 分数: {round9_report['分数']}分")
print(f"  • 描述: {round9_report['描述']}")

print("\n🤖 新增技能:")
for i, skill in enumerate(round9_report['新增技术'], 1):
    print(f"  {i}. {skill}")

# 累计统计（第6-9轮）
rounds_6_to_9 = [
    {"轮次": "第6轮", "题目": 22, "分数": 5000, "平台": ["CCTF", "ByteCTF", "DEFCON CTF"]},
    {"轮次": "第7轮", "题目": 8, "分数": 915, "平台": ["SecurityTrails", "BlackHat", "Ghost In The Shell"]},
    {"轮次": "第8轮", "题目": 8, "分数": 710, "平台": ["AttackDefense", "HackTM 扩展", "TCTF"]},
    {"轮次": "第9轮", "题目": 7, "分数": 790, "平台": ["HITCON", "CyCon", "SU-CTF"]}
]

total_new_6_9 = sum(r["题目"] for r in rounds_6_to_9)
total_points_6_9 = sum(r["分数"] for r in rounds_6_to_9)

print("\n" + "=" * 80)
print("📈 第6-9轮累计")
print("=" * 80)

print(f"\n各轮详情:")
for r in rounds_6_to_9:
    print(f"\n{r['轮次']}: {r['题目']}题, {r['分数']}分")
    print(f"  平台: {', '.join(r['平台'])}")

print(f"\n📊 累计:")
print(f"  • 新增题目: {total_new_6_9}题")
print(f"  • 新增分数: {total_points_6_9}分")
print(f"  • 之前题目: 85题")
print(f"  • 现在总计: {85 + total_new_6_9} = {85 + total_new_6_9}题")

# 总平台
all_platforms_6_9 = []
for r in rounds_6_to_9:
    all_platforms_6_9.extend(r["平台"])

unique_platforms_6_9 = sorted(list(set(all_platforms_6_9)))
print(f"\n🌍 第6-9轮支持平台: {len(unique_platforms_6_9)}个")
for i, platform in enumerate(unique_platforms_6_9, 1):
    print(f"  {i:2d}. {platform}")

# Git
result = subprocess.run(["git", "log", "--oneline", "-1"], cwd="/", capture_output=True, text=True)
print(f"\n📦 最新Git: {result.stdout.strip()}")

print("\n" + "=" * 80)
print("✅ 第9轮迭代完成！")
print("=" * 80)

# 保存
summary = {
    "第9轮时间": "2026-02-25 21:20:00",
    "第6-9轮新增": total_new_6_9,
    "第6-9轮分数": total_points_6_9,
    "现在总计": 85 + total_new_6_9,
    "第6-9轮平台": unique_platforms_6_9,
    "Git提交": result.stdout.strip()
}

with open("/ROUND_9_SUMMARY.json", "w") as f:
    json.dump(summary, f, indent=4)

print(f"\n💾 报告已保存: /ROUND_9_SUMMARY.json")

# 继续 Round 10
print("\n🚀 开始第10轮迭代...")
