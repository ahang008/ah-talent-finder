# AI天赋发现系统

**ah-talent-finder** —— 用AI深度对话帮你找到天赋、内心原密码和职业方向。

不是测评，不是问卷，不是算命。像跟认识你十年的老朋友深夜聊天一样，从你的真实经历里挖出你自己都没意识到的天赋。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-green.svg)](https://claude.ai/code)

---

## 背景

作者阿杭，风景园林专业毕业，进了央企干工地。三个月后发现不对劲——每天填表格、跑现场、跟工人扯皮。不知道自己能做什么，只知道不想做这个。

后来跟AI做了一次深度对话——聊家庭、聊恐惧、聊做成的蠢事、聊最让自己骄傲的事。AI没有judge，只是记住每一句话，然后看到了他自己都没意识到的规律。

最享受的是"把复杂的事情讲清楚"。最讨厌的不是"工作"，而是"重复、应酬、没有成长"。真正需要的不是"稳定工作"，而是"时间自主权 + 能力被看见 + 每一步可控有反馈"。

AI翻译成了产品经理。试了，做了。但很快发现产品经理依赖团队、依赖公司决策，很难直接助力创业。于是直接开始做自媒体。现在靠AI和自媒体养活自己，全职自由职业。

这套方法经历了10多个朋友的反馈和迭代。有人找到了方向成了万粉博主。有人从建筑转行做了AIGC设计师，进了腾讯。有人从园林转行做了自由职业，接了私单养活自己。

---

## 工作流程

```
开场（打招呼，不建文件）
  -> 用户确认开始
    -> 检查存档（scripts/session.py）
      -> 有存档？继续上次 / 重新开始
      -> 无存档？初始化 -> Step1
  -> Step1: 轻量画像收集（7个对话节点，约30分钟，准确度60%）
    -> 决策：够用？-> Step3 / 不够？-> Step2
  -> Step2: 深度版画像（过去+内在探索，约30分钟，准确度90%）
  -> Step3: 职业方向推荐 + 2周验证方案
  -> Step4: 命理交叉验证（可选）
```

### 你能拿到什么

1. **轻量版画像**：你是谁、做成过什么、什么让你有劲、什么让你烦
2. **天赋判断**：3-5个天赋，每个都有你故事里的证据
3. **职业方向**：5个推荐方向，含匹配度分析
4. **2周验证方案**：不需要辞职，具体到"打开什么平台、找谁、说什么"
5. **内心原密码报告**（深度版）：你为什么是这样的人、骨子里真正需要什么
6. **命理交叉验证**（可选）：用八字命盘做一套独立的验证系统

### 隐私

所有对话和存档文件保存在你自己的设备上（`📥 临时工作区/AI天赋发现/`），不会上传到任何地方。

---

## 安装

### 作为 Claude Code Skill 使用

1. 将整个文件夹复制到你的 Vault 的 `.claude/skills/ah-talent-finder/` 目录下
2. 在 Claude Code 中输入 `/天赋` 即可启动

### 作为 Python 包使用

```bash
pip install -e .
# 或者直接
python3 scripts/session.py --help
```

---

## 仓库结构

```
ah-talent-finder/
├── SKILL.md                         # Claude Code 技能定义
├── README.md                        # 本文件
├── LICENSE                          # MIT
├── pyproject.toml                   # Python 包配置
├── steps/                           # 对话工作流
│   ├── Step1-轻量画像收集.md         # 8个节点的轻量画像收集
│   ├── Step2-深度版画像.md           # 深度版：过去 + 内在
│   ├── Step3-职业方向与验证方案.md    # 职业方向 + 2周验证
│   └── Step4-命理交叉验证.md         # 八字命理交叉验证
├── scripts/                         # Python 工具
│   ├── __init__.py
│   └── session.py                   # 会话状态管理
├── reference/                       # 理论背景
│   ├── 设计哲学.md                   # 为什么这样设计：核心理念与架构决策
│   ├── 天赋理论框架库.md             # 9个心理学框架
│   └── 追问规则库.md                 # 追问规则速查卡
└── examples/                        # 使用示例
    └── README.md
```

---

## 会话管理器 CLI

```bash
# 检查是否有进行中的会话
python3 scripts/session.py check

# 初始化新会话
python3 scripts/session.py init

# 保存对话字段
echo "自由职业者\n城市：南京" | \
  python3 scripts/session.py save --node "Step1-节点1" \
    --field "基本面" --stdin

# 推进进度
python3 scripts/session.py progress --node "Step1-节点2"

# 查看当前状态
python3 scripts/session.py status

# 读取已保存的数据
python3 scripts/session.py read-file --file "01-轻量画像.md"
```

---

## 理论框架

分析过程调用9个经典心理学框架做交叉验证：

- **多元智能理论**（加德纳）
- **VIA性格优势**（彼得森 & 塞利格曼）
- **霍兰德职业类型**（RIASEC）
- **盖洛普优势识别**（34才干）
- **心流理论**（契克森米哈赖）
- **阴影与个体化**（荣格）
- **IKIGAI**（冲绳人生哲学）
- **叙事心理学**（麦克亚当斯）
- **依恋理论**（鲍尔比）

每个框架的结论都必须绑定用户说过的具体故事或证据，不做抽象打分。

---

## 使用要求

- Claude Code（技能使用）
- Python 3.9+（会话管理脚本）
- 30分钟不被打扰的时间（深度版需要60分钟）
- 说实话的勇气——编的经历分析不出真的天赋

---

## 联系方式

- 微信：Zephyr136
- X：[@Astronaut_1216](https://x.com/Astronaut_1216)
- GitHub：[@ahang008](https://github.com/ahang008)

---

## 许可证

MIT —— 详见 [LICENSE](LICENSE)

---

**阿杭出品** —— 一个产品经理出身的自由职业者，用这套方法找到了自己的路。希望也能帮到你。
