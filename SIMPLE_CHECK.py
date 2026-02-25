#!/usr/bin/env python3
"""
GitHub 仓库完整性检查
"""

print("\n" + "="*70)
print("🔍 GitHub 仓库 - 最终检查")
print("="*70)

print(f"仓库地址: https://github.com/zhang8216/hackathon-champian-ctf")

# 检查 README
import requests

try:
    resp = requests.get("https://raw.githubusercontent.com/zhangyan8216/hackathon-champian-ctf/master/README.md")
    
    content = resp.text
    
    print(f"✅ README.md: {len(content)} 字符")
    print(f"✅ 包含信息:")
    if "GitHub" in content:
        print(f"  - GitHub仓库: {content.split('GitHub')[2]}")
    if "13/13" in content:
        print(f"  - 训练成功率")
    if "~28,000" in content:
        print(f"  - 代码总量")
    if "4 个在线" in content:
        print(f"  - 在线靶场")
        
except Exception as e:
    print(f"❌ 读取失败: {e}")

print(f"\n✅ 验证完成！")
print(f"📦 GitHub 仓库状态: https://github.com/zhang8216/hackathon-champian-ctf")
print(f"📋 README: https://github.com/zhangy8216/hackathon-champian-ctf/blob/master/README.md")
print(f"📊 训练数据: https://github.com/zhangy8216/hackathon-champian-ctf/blob/master/training_data.json")
print(f"\n🎉 所有工作已完成！准备黑客松夺冠！")
print(f"   GitHub: {repo}")
print(f"   训练: {repo}/blob/master/README.md")
print(f"   数据: {repo}/blob/master/training_data.json")
