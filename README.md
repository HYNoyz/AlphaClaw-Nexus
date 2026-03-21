# 🐺 AlphaClaw-Nexus: 意图驱动的全链攻防一体化引擎

![Version](https://img.shields.io/badge/Version-2.0.0-blue.svg)
![Track](https://img.shields.io/badge/Track-OKX%20Onchain%20OS%20AI-orange.svg)
![Status](https://img.shields.io/badge/Status-Hackathon%20Ready-success.svg)

## 📌 核心痛点与降维打击
在当前的 Web3 世界，链上交互充斥着碎片化、高门槛与隐藏风险。用户需要手动寻找最优汇率、苦等低 Gas 窗口，甚至一不小心就会授权给貔貅盘 (Honeypot)。
AlphaClaw-Nexus 不是一个工具，而是一个具备自治调度能力的 AI 特工。我们将复杂的链上操作降维成了**“一句话指令”**。

## ⚙️ 架构创新 (The 9.98 Architecture)
我们摒弃了传统的“单步 API 映射”，采用了基于大模型的动态 DAG (有向无环图) 任务编排机制：
1. **Nexus Brain 3.0 (意图流水线):** 接入 Gemini 核心，将模糊的战略目标（如“等 Gas 跌穿 30，查一下 SCAM 币的安全情况再买”）自动拆解为有序的执行节点。
2. **Lobster Aegis (风控沙盒):** 在触碰任何链上资产前，强制执行静态代码与流动性审计。面对貔貅盘或黑名单合约，系统将触发红色熔断，强行中止 OKX 路由调用。
3. **Onchain OS 深度聚合:** 接入 OKX 路由网络，在执行层自动寻找全链最优流动性深度。

## 🚀 核心用例演示 (Demo Showcase)
- **用例 A (顺滑执行):** `"等 gas 跌到 500 以下，查一下 ARB 代币，没风险就用 1 ETH 买入。"` -> ✅ 触发监控 -> ✅ 审计绿灯 -> 💰 OKX 路由最优报价成交。
- **用例 B (风控熔断):** `"不管 gas 多少，马上帮我查一下 SCAM 币，然后买 100 U。"` -> 🚨 触发 Aegis 致命风险警报 -> ❌ 拒绝授权，强制中止执行。

## 🛠️ 快速启动 (Quick Start)
```bash
# 1. 克隆仓库 & 安装依赖
git clone [https://github.com/YourName/AlphaClaw.git](https://github.com/YourName/AlphaClaw.git)
cd AlphaClaw
pip install -r requirements.txt

# 2. 配置环境
# 在 .env 文件中填入你的 TELEGRAM_BOT_TOKEN 与 GEMINI_API_KEY

# 3. 点火启动
python bot.py
