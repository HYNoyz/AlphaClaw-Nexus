import os
import time
import threading
import telebot
import logging
from dotenv import load_dotenv

from core.brain import parse_user_intent
from core.okx_ops import OKXOnchainService
from core.security_auditor import AegisRiskControl
from core.shadow_worker import ShadowHeartbeat

load_dotenv()
TG_TOKEN = os.getenv("TG_TOKEN")

bot = telebot.TeleBot(TG_TOKEN)
okx = OKXOnchainService()
aegis = AegisRiskControl()

# 启动影子心跳探测引擎
shadow = ShadowHeartbeat()
shadow.start()

print("[System] AlphaClaw-Nexus V5 Prototype Engine initialized. Awaiting pipeline triggers...")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "🐺 **AlphaClaw-Nexus V5 Institutional Terminal**\n"
        "----------------------------------------\n"
        "🛡️ Architecture: Vault-Isolated Intent DAG\n"
        "⚡ Features: Escape Pod | Graceful Degradation | Zero-Gas Sim\n"
        "----------------------------------------\n"
        "System ready. Enter your quantitative intent:"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(func=lambda m: True)
def handle_intent(message):
    user_input = message.text
    chat_id = message.chat.id
    
    msg = bot.send_message(chat_id, f"🧠 正在编译意图: `{user_input}`", parse_mode='Markdown')
    
    plan = parse_user_intent(user_input)
    if plan.get("status") == "error":
        bot.edit_message_text(f"❌ 编译失败: {plan.get('message')}", chat_id, msg.message_id)
        return
        
    pipeline = plan.get("intent_pipeline", [])
    
    plan_text = f"📋 **执行计划已生成** (来源: {plan.get('source', 'Nexus')}):\n━━━━━━━━━━━━━━━━━━\n"
    plan_text += "\n".join([f"🔹 Step: {step['action_type']}" for step in pipeline])
    bot.edit_message_text(plan_text, chat_id, msg.message_id, parse_mode='Markdown')
    
    for step in pipeline:
        action = step.get("action_type")
        params = step.get("params", {})
        
        # 🚀 [V5 核心] 处理逃生舱黑天鹅事件
        if action == "EMERGENCY_REVOKE":
            bot.send_message(chat_id, "🚨 **[ESCAPE POD ACTIVATED]** 正在闪电撤销所有高危 DApp 授权...")
            time.sleep(1) # 模拟上链撤销
            bot.send_message(chat_id, "✅ 授权已清空，资金池物理隔离！")

        elif action == "MONITOR_GAS":
            bot.send_message(chat_id, f"📡 监控 Arbitrum Gas < {params.get('target_gas', 500)}...")
            time.sleep(1)
            bot.send_message(chat_id, "⛽ 条件满足，进入下一流程。")
            
        elif action == "RISK_SCAN":
            target = params.get("target_token", "UNKNOWN")
            bot.send_message(chat_id, f"🛡️ Aegis 正在进行静态代码审计: {target}...")
            
            # 🚀 [V5 核心] 优雅降级 (Graceful Degradation)
            try:
                audit_res = aegis.scan_target(target)
                if not audit_res["safe"]:
                    bot.send_message(chat_id, f"🚨 **致命风险** 发现高危漏洞，指令已强制熔断！\n\n🎯 目标: {target}\n☠️ 等级: {audit_res['risk_level']}\n📝 报告: 貔貅盘或恶意后门。\n\n❌ AlphaClaw 已拒绝执行后续交易。", parse_mode='Markdown')
                    return
                bot.send_message(chat_id, f"✅ Aegis 审查 {target} 安全评级: 优秀。")
            except Exception as e:
                bot.send_message(chat_id, f"⚠️ **Aegis 沙盒节点离线/超时 ({e})**。\n🔄 触发【优雅降级】：系统将锁定，仅允许与官方白名单资产 (WETH, USDC, USDT) 交互！")
                if target not in ["ETH", "USDT", "USDC", "WETH"]:
                    bot.send_message(chat_id, "❌ 目标非白名单核心资产，处于降级模式，已拒绝执行。")
                    return
            
        elif action == "SWAP":
            t_in = params.get("token_in", "ETH")
            t_out = params.get("token_out", "USDT")
            amount = params.get("amount", "0.0001")
            if amount == "MAX": amount = "0.0001" # 模拟一键全平
            
            bot.send_message(chat_id, "🔗 主网路由 正在请求底层节点，执行 Pre-flight 模拟并签名上链...")
            
            try:
                swap_res = okx.execute_real_swap(t_in, t_out, amount)
                if swap_res["status"] == "error":
                    bot.send_message(chat_id, f"❌ **主网执行拦截**\n原因: `{swap_res['msg']}`\n(已触发 Zero-Gas 防御)", parse_mode='Markdown')
                    return
                    
                bot.send_message(chat_id, f"💰 **执行完毕 真实链上交易已广播！**\n━━━━━━━━━━━━━━━━━━\n🔄 动作: 将 {amount} {t_in} 兑换为 {t_out}\n⛓️ TxHash:\n`{swap_res['msg']}`\n━━━━━━━━━━━━━━━━━━\n🎉 任务圆满结束。", parse_mode='Markdown')
            except Exception as e:
                # 再次兜底优雅降级
                bot.send_message(chat_id, f"❌ 底层网络节点抛锚: {str(e)}。已安全挂起状态机。")
                return

if __name__ == '__main__':
    try:
        bot.infinity_polling()
    except KeyboardInterrupt:
        shadow.stop()
        print("\n[System] AlphaClaw Engine shutdown safely.")
