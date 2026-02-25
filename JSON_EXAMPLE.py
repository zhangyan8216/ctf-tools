#!/usr/bin/env python3
"""
真实JSON文件示例展示
展示训练数据的具体内容和结构
"""

import json

# 示例：训练数据结构示例
example_training_data = {
    "system": "CTF Agent Training System",
    "version": "1.0",
    "last_updated": "2026-02-25 21:40:00",
    "platforms": {
        "历年题目": {
            "total_challenges": 13,
            "questions": [
                {"name": "Caesar_Caesar_Salad", "category": "Encoding", "points": 50, "difficulty": "Easy", "flag": "CTFlearn{caesar_caesar_solved}"},
                {"name": "Base64_Basic", "category": "Encoding", "points": 60, "difficulty": "Easy", "flag": "CTFlearn{base64_solved}"},
            ]
        },
        "真实题目": {
            "total_challenges": 6,
            "questions": [
                {"name": "Blind", "category": "Forensics", "points": 20, "difficulty": "Easy", "flag": "HTB{blind_analyzed}"},
                {"name": "Inject", "category": "Web", "points": 20, "difficulty": "Easy", "flag": "CTFlearn{inject_exploited}"},
            ]
        },
        "高级题目": {
            "total_challenges": 14,
            "questions": [
                {"name": "Buffer Overflow Basic", "category": "Pwn", "points": 50, "difficulty": "Medium", "flag": "picoCTF{buffer_overflow_exploited}"},
                {"name": "Kernel Exploit", "category": "Pwn", "points": 200, "difficulty": "Expert", "flag": "picoCTF{kernel_pwned}"},
            ]
        }
    },
    "categories": {
        "encoding": ["Caesar", "Base64", "ROT13", "URL"],
        "web": ["SQLi", "XSS", "SSTI", "XXE", "RCE"],
        "pwn": ["Buffer Overflow", "Shellcode", "ROP", "ret2libc"],
        "crypto": ["RSA", "AES", "ECC", "Lattice", "Post-Quantum"],
        "misc": ["Forensics", "PCAP", "Stego"]
    }
}

# 显示示例结构
print("📄 JSON 文件示例结构：")
print("=" * 80)
print(json.dumps(example_training_data, indent=4, ensure_ascii=False))
print("=" * 80)

# 说明
print("\n💡 JSON文件的实际作用：")
print("1. 存储题目元数据（名称、类型、难度、分数）")
print("2. 记录解题结果（flag、状态、耗时、技术）")
print("3. 提供自动化脚本的数据结构")
print("4. 支持版本控制（通过 Git）")
print("5. 实现可扩展的训练框架")

print("\n🏷 示例数据分类：")
print("  • training_data.json    → 历年真题数据")
print("  →  - 读取题目列表 → 配置规则 → 自动解题")
print("  • *results.json      → 解题结果")
print("  →  → 读取结果 → 生成报告")
print("  →  →  → 统计成功率、分数")

print("\n⚠️ 为什么是JSON：")
print("  ✓ 轻量存储结构化（易于读取）")
print("  ✓ 支持版本控制（Git追踪）")
print("  ✓ 可扩展性（添加新题目很方便）")
print("  ✓ 机器可读（AI系统易接入）")

print("\n🎯 实际应用：")
print("  • Python读取: `json.load()`")
print("  • 格式化输出: `json.dump()`")
print("  • Git版本管理: `.md 文件 → `json` 转换")
print("  • 支持：题目分类、flag格式、难度设置")

print("\n✅ 说明完成！")
