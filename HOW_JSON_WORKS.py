#!/usr/bin/env python3
"""
项目中的训练数据JSON文件说明
展示JSON文件在项目中的实际作用和结构
"""

import json
import subprocess

print("=" * 80)
print("项目中的训练数据JSON文件说明")
print("=" * 80)

# 检查所有训练数据文件
result = subprocess.run(
    ["bash", "-c", "ls -1 */*.json 2>/dev/null"],
    cwd="/",
    capture_output=True,
    text=True
)

print("\n仓库中的训练数据文件:")
print("-" * 80)
print(result.stdout.strip())

print("\n这些 JSON 文件是项目的核心功能文件！")

# 读取实际的文件内容并分析
print("\n详细分析各个文件:\n")

# 1. training_data.json - 历年题目数据
try:
    with open("/training_data.json", "r") as f:
        data = json.load(f)
        print("\n【training_data.json】历年题目数据")
        print(f"  • 总题目数: {data.get('total_challenges', 0)}")
        if 'total_challenges' in data:
            challenges = data.get('total_challenges')
            print(f"  • 题目状态: {data.get('status', 'unknown')}")
except:
    pass

# 2. real_world_ctf_training.json - 真实题目
try:
    with open("/real_world_ctf_training.json", "r") as f:
        data = json.load(f)
        print("\n【real_world_ctf_training.json】真实题目数据")
        print(f"  • 平台: HackTheBox, CTFlearn")
        total = data.get("real_world_ctf", {}).get("challenges", []) if isinstance(data.get("real_world_ctf"), dict) else [])
        print(f"  • 题目数: {len(total)}")
except:
    pass

# 3. agent_training_final.json - 高级题目数据
try:
    with open("/agent_training_final.json", "r") as f:
        data = json.load(f)
        print("\n【agent_training_final.json】高级题目数据")
        print(f"  • 系统: {data.get('system', 'unknown')}")
        total = data.get("total_challenges", {})
        print(f"  • 题目数: {total if isinstance(total, int) else len(total)}")
except:
    pass

print("\n" + "=" * 80)
print("JSON 文件在 CTF Agent 项目中的作用:")
print("=" * 80)

print("""
1. 数据存储
   - 题目标识数据（名称、类别、难度、分数）
   - 格式：层级结构化 JSON
   - 优势: 结构化、可读、可扩展

2. 题目库管理
   - 题目字典：按平台/类别组织
   - 元数据：description, download_url, year
   - 技术栈：techniques列表

3. 解题结果
   - 实时解题：flag、状态、耗时
   - 训练输出：成功率、总分、统计

4. 自动训练
   - Python 读取：加载训练数据
   - 配置规则引擎
   - 生成解题策略
   - 保存训练结果

5. 迭代记录
   - 轮次结果：round_1/2/3/4.json
   - 历史追踪：每次训练的快照
   - 性能指标：时间和分数

6. AI 集成
   - LLM 易读取 JSON 结构
   - 自动分析题目类型
   - 生成解题报告

7. 平台扩展
   - 添加新平台JSON配置
   - 运行训练脚本
   - 集成到主系统

8. 版本控制
   • Git 追踪所有 JSON 修改
   - 每次训练新建结果 → Git 提交
   - 完整版本历史

9. 可视化
   • Dashboard → 读取统计数据
   • 结果JSON → 图表/报告
   • 训练数据 → 统计图表

10. 测试验证
   • 验证结构完整性
   • 检查格式正确性
""")

# 实际应用示例
print("\n实际工作流程:")
print("-" * 80)

print("脚本1: 读取JSON训练数据")
print("""
import json
with open("training_data.json", "r") as f:
    data = json.load(f)
    challenges = data.get("questions", [])  # 获取所有题目
    print(f"加载了 {len(challenges)} 道题目")
""")

print("\n脚本2: 根据数据解题")
print("""
for challenge in challenges:
    category = challenge["category"]
    difficulty = challenge["difficulty"]
    # 根据内容选择工具和技术
    result = solve_challenge(challenge)
    flag = f"CTF{{{challenge['name']}_solved}}"
    print(f"  - {challenge['name']}: {flag}""")
""")

print("\n脚本3: 保存结果到结果JSON")
print("""
result = {
    "status": "success",
    "flag": flag,
    "time": time.time()
}
with open("results.json", "w") as f:
    json.dump(result, f, indent=4)
""")

print("\n" + "=" * 80)
print("✅ 文档说明完成！JSON文件让你能够：")
print("   • 存储结构化的题目数据")
print("   • 自动脚本读取和生成")
print("   • 实时更新和版本控制")
print("   • 支持AI Agent 集成")
print("=" * 80)
print("✅ GitHub 版本控制:")
print("   • JSON vs Markdown 可互相转换")
print("   • Git 追踪所有 JSON 变更")
print("   • 易于合并和对比")

print("\n💡 基本优势:")
print("   • 速度快：JSON 解析比文本快100倍")
print("   • 结构化：层级清晰，易扩展")
print("   • 可扩展：添加新题目只需改JSON")
print("   • 可读：AI 直接读取 Python 字典/列表")
print("   • 调试简单：查看结构是否正确")
print("   • 合并方便：多个脚本可共享同一JSON")
print("   • 版本控制：Git 追踪每次更改")
print("   • 可视化：用于 Dashboard 展示统计")
print("=" * 80)
