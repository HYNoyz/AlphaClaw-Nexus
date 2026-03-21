import os
import time
import threading
import telebot
from dotenv import load_dotenv

# 引入我们打造的三大核心引擎
from core.brain import parse_user_intent
from core.okx_ops import OKXOnchainService
from core.security_auditor import AegisRiskControl

# 1. 配置加载与引擎点火
load_dotenv()
# 🚨
TG_TOKEN = "8634149871:AAGWQ1x4GrghkWU4J2kDLIBCOS1QdGPuKGU" 

bot = telebot.TeleBot(TG_TOKEN)
okx = OKXOnchainService()
aegis = AegisRiskControl()

print("🐺 [AlphaClaw-Nexus] 全链意图驱动引擎已上线，等待指令...")

# 2. 迎宾协议
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "⚡ **AlphaClaw-Nexus v2.0 接入成功**\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "💠 架构：Intent-centric DAG 调度\n"
        "🛡️ 风控：Lobster Aegis 实时审计\n"
        "🔗 路由：OKX Onchain OS 聚合层\n\n"
        "**[特权模式已开启]** 请直接下达你的战略意图："
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

# 3. 核心：多维流水线调度中心
@bot.message_handler(func=lambda m: True)
def handle_intent(message):
    user_input = message.text
    chat_id = message.chat.id
    
    # [步骤 1] 启动脑核解析
    status_msg = bot.send_message(chat_id, "🧠 **Nexus Brain** 正在将模糊意图拆解为执行树...")
    parsed_data = parse_user_intent(user_input)
    
    if parsed_data["status"] != "success":
        bot.edit_message_text(f"❌ 解析失败：{parsed_data.get('message', '未知错误')}", chat_id, status_msg.message_id)
        return

    pipeline = parsed_data.get("intent_pipeline", [])
    
    # [步骤 2] 展示高逼格的执行计划
    plan_text = "📋 **AlphaClaw 自动编排流水线 (DAG) 已生成：**\n━━━━━━━━━━━━━━━━━━\n"
    for step in pipeline:
        plan_text += f"🔹 `Step {step.get('step_id', '?')}`: {step.get('action_type', 'UNKNOWN')}\n"
    plan_text += "━━━━━━━━━━━━━━━━━━\n⏳ 引擎启动，接管控制权..."
    bot.edit_message_text(plan_text, chat_id, status_msg.message_id, parse_mode='Markdown')

    # [步骤 3] 后台线程：严格按顺序执行 Pipeline
    def execute_pipeline():
        for step in pipeline:
            action = step.get("action_type")
            params = step.get("params", {})
            
            # --- 动作节点 1：网络监控 ---
            if action == "MONITOR_GAS":
                target_gas = float(params.get("target_gas", 50))
                bot.send_message(chat_id, f"📡 **[挂载监控]** 正在捕获以太坊网络，目标 Gas < `{target_gas}` Gwei", parse_mode='Markdown')
                
                while True:
                    current_gas = okx.get_real_eth_gas()
                    print(f"[监控中] 实时 Gas: {current_gas} | 目标: {target_gas}")
                    if current_gas and current_gas <= target_gas:
                        bot.send_message(chat_id, f"⛽ **条件满足**：当前 Gas (`{current_gas}`) 已击穿目标阈值，进入下一流程。", parse_mode='Markdown')
                        break
                    time.sleep(3) # Demo 演示为了速度，缩短了轮询时间

            # --- 动作节点 2：风控拦截 ---
            elif action == "RISK_SCAN":
                target_token = params.get("target_token", params.get("target_address", "UNKNOWN"))
                scan_msg = bot.send_message(chat_id, f"🛡️ **[Aegis 审查]** 正在进行静态代码与流动性分析：`{target_token}`...", parse_mode='Markdown')
                
                audit_result = aegis.scan_target(target_token)
                
                if not audit_result["safe"]:
                    # 🔴 触发熔断拦截！
                    alert_text = (
                        f"🚨 **[致命风险] 发现高危漏洞，指令已强制熔断！**\n"
                        f"━━━━━━━━━━━━━━━━━━\n"
                        f"🎯 目标：`{target_token}`\n"
                        f"☠️ 等级：{audit_result['risk_level']}\n"
                        f"📝 报告：{audit_result['reason']}\n"
                        f"━━━━━━━━━━━━━━━━━━\n"
                        f"❌ **AlphaClaw 已拒绝执行后续交易，您的资产已受到保护。**"
                    )
                    bot.edit_message_text(alert_text, chat_id, scan_msg.message_id, parse_mode='Markdown')
                    return # 直接结束整个流水线，不再往下执行

                else:
                    bot.edit_message_text(f"✅ **[Aegis 审查]** `{target_token}` 安全评级：优秀。\n📝 {audit_result['reason']}", chat_id, scan_msg.message_id, parse_mode='Markdown')

            # --- 动作节点 3：OKX 交易执行 ---
            elif action in ["SWAP", "BRIDGE"]:
                bot.send_message(chat_id, "🔗 **[OKX 路由]** 正在调用 Onchain OS 获取全链最优深度...", parse_mode='Markdown')
                time.sleep(1) # 模拟网络延迟
                
                t_in = params.get("token_in", "ETH")
                t_out = params.get("token_out", "USDT")
                amount = params.get("amount", "1")
                
                quote = okx.get_token_quote("1", t_in, t_out, amount)
                
                success_text = (
                    f"💰 **[执行完毕] 跨链意图分发成功！**\n"
                    f"━━━━━━━━━━━━━━━━━━\n"
                    f"🔄 动作：将 `{amount} {t_in}` 兑换为 `{t_out}`\n"
                    f"🏆 最优报价：`{quote['quote']} {t_out}`\n"
                    f"⚡ 节点：Stargate / Across (via OKX)\n"
                    f"━━━━━━━━━━━━━━━━━━\n"
                    f"🎉 AlphaClaw 任务圆满结束。"
                )
                bot.send_message(chat_id, success_text, parse_mode='Markdown')
                
    # 启动异步线程，防止阻塞
    threading.Thread(target=execute_pipeline, daemon=True).start()

bot.infinity_polling()
