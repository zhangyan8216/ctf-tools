#!/usr/bin/env python3
"""
更新 README 并推送到 GitHub
"""

import subprocess

print("更新 README 并推送...")

# 更新提交
subprocess.run(["git", "add", "README.md"], check=True)

# 提交
import subprocess
result = subprocess.run(
    ["git", "commit", "-m", "更新 README - 添加仓库信息"],
    check=True
)

# 如果成功，推送
if result.returncode == 0:
    print("✅ 提交成功")
    print("📤 正在推送到 GitHub...")
    subprocess.run(["git", "push"], check=True)
    print("✅ 推送完成！")
    print(f"\n📦 GitHub地址: https://github.com/zhangyan8216/hackathon-champian-ctf")
else:
    print("❌ 提交失败:", result.stderr)
    print("\n请手动推送:")
    print("  git push")
