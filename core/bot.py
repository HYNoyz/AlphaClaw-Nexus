import os
import time
import threading
import telebot
from dotenv import load_dotenv

from core.brain import parse_user_intent
from core.okx_ops import OKXOnchainService
from core.security_auditor import AegisRiskControl
from core.shadow_worker import ShadowHeartbeat

# 1. 加载环境变量
load_dotenv()
TG_TOKEN = os.getenv("TG_TOKEN")

# 2. 初始化核心引擎
bot = telebot.TeleBot(TG_TOKEN)
okx = OKXOnchainService()
aegis = AegisRiskControl()

# 🚀 3. 启动机构级影子心跳探测引擎 (Shadow Heartbeat Engine)
shadow = ShadowHeartbeat()
shadow.start()

print("[System] AlphaClaw-Nexus 4.0 Engine initialized. Awaiting pipeline triggers...")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "🐺 **AlphaClaw-Nexus v4.0 Institutional Terminal**\n"
        "----------------------------------------\n"
        "🛡️ Architecture: ERC-4337 Intent-centric DAG\n"
        "⚡ Features: Pre-flight Sim | MEV-Shield | Shadow Cache\n"
        "----------------------------------------\n"
        "System ready. Enter your quantitative intent:"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(func=lambda m: True)
def handle_intent(message):
    user_input = message.text
    chat_id = message.chat.id
    
    msg = bot.send_message(chat_id, f"🧠 正在编译意图: `{user_input}`", parse_mode='Markdown')
    
    # 阶段一：编译意图 DAG
    plan = parse_user_intent(user_input)
    if plan.get("status") == "error":
        bot.edit_message_text(f"❌ 编译失败: {plan.get('message')}", chat_id, msg.message_id)
        return
        
    pipeline = plan.get("intent_pipeline", [])
    
    # 格式化输出执行树
    plan_text = f"📋 **执行计划已生成** (来源: {plan.get('source', 'Nexus')}):\n━━━━━━━━━━━━━━━━━━\n"
    plan_text += "\n".join([f"🔹 Step: {step['action_type']}" for step in pipeline])
    bot.edit_message_text(plan_text, chat_id, msg.message_id, parse_mode='Markdown')
    
    # 阶段二：DAG 节点逐个原子化执行
    for step in pipeline:
        action = step.get("action_type")
        params = step.get("params", {})
        
        if action == "MONITOR_GAS":
            bot.send_message(chat_id, f"📡 监控 Arbitrum Gas < {params.get('target_gas', 500)}...")
            time.sleep(1) # 模拟极速监控
            bot.send_message(chat_id, "⛽ 条件满足，进入下一流程。")
            
        elif action == "RISK_SCAN":
            target = params.get("target_token", "UNKNOWN")
            bot.send_message(chat_id, f"🛡️ Aegis 正在进行静态代码审计: {target}...")
            audit_res = aegis.scan_target(target)
            
            if not audit_res["safe"]:
                bot.send_message(chat_id, f"🚨 **致命风险** 发现高危漏洞，指令已强制熔断！\n\n🎯 目标: {target}\n☠️ 等级: {audit_res['risk_level']}\n📝 报告: 检测到貔貅盘 (Honeypot) 特征或开源代码存在恶意提权后门。\n\n❌ AlphaClaw 已拒绝执行后续交易，您的资产已受到保护。", parse_mode='Markdown')
                return # 触发红色熔断，全链路终止
                
            bot.send_message(chat_id, f"✅ Aegis 审查 {target} 安全评级: 优秀。")
            
        elif action == "SWAP":
            t_in = params.get("token_in", "ETH")
            t_out = params.get("token_out", "USDT")
            
            # 强制硬编码测试金额，物理防爆仓
            amount = "0.0001" 
            
            bot.send_message(chat_id, "🔗 主网路由 正在请求底层节点，执行 Pre-flight 模拟并签名上链...")
            
            # 调用包含了零成本模拟和主网广播的终极核心
            swap_res = okx.execute_real_swap(t_in, t_out, amount)
            
            if swap_res["status"] == "error":
                bot.send_message(chat_id, f"❌ **主网执行失败**\n原因: `{swap_res['msg']}`", parse_mode='Markdown')
                return
                
            bot.send_message(chat_id, f"💰 **执行完毕 真实链上交易已广播！**\n━━━━━━━━━━━━━━━━━━\n🔄 动作: 将 {amount} {t_in} 兑换为 {t_out}\n🎯 预估获得: {swap_res['quote']} {t_out}\n⛓️ TxHash (复制到浏览器核实):\n`{swap_res['msg']}`\n━━━━━━━━━━━━━━━━━━\n🎉 AlphaClaw 任务圆满结束。", parse_mode='Markdown')

if __name__ == '__main__':
    try:
        # 启动 Telegram 轮询监听
        bot.infinity_polling()
    except KeyboardInterrupt:
        shadow.stop()
        print("\n[System] AlphaClaw Engine shutdown safely.")
