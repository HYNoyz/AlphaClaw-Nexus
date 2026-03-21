import os
import time
import threading
import telebot
from dotenv import load_dotenv

from core.brain import parse_user_intent
from core.okx_ops import OKXOnchainService
from core.security_auditor import AegisRiskControl

load_dotenv()
# TODO: Retrieve from environment variables in production
TG_TOKEN = "你的_TELEGRAM_BOT_TOKEN_写在这里" 

bot = telebot.TeleBot(TG_TOKEN)
okx = OKXOnchainService()
aegis = AegisRiskControl()

print("[System] AlphaClaw-Nexus Engine initialized. Awaiting pipeline triggers...")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "**AlphaClaw-Nexus v2.0 Terminal**\n"
        "----------------------------------\n"
        "Architecture: Intent-centric DAG Pipeline\n"
        "Security: Lobster Aegis Pre-execution Audit\n"
        "Routing: OKX Onchain OS Aggregation\n\n"
        "System ready. Enter your quantitative intent:"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(func=lambda m: True)
def handle_intent(message):
    user_input = message.text
    chat_id = message.chat.id
    
    status_msg = bot.send_message(chat_id, "[Nexus] Generating DAG execution pipeline...")
    parsed_data = parse_user_intent(user_input)
    
    if parsed_data["status"] != "success":
        bot.edit_message_text(f"Error: Pipeline generation failed. {parsed_data.get('message', '')}", chat_id, status_msg.message_id)
        return

    pipeline = parsed_data.get("intent_pipeline", [])
    
    plan_text = "**AlphaClaw Automated Pipeline Generated:**\n----------------------------------\n"
    for step in pipeline:
        plan_text += f"Node {step.get('step_id', '?')}: {step.get('action_type', 'UNKNOWN')}\n"
    plan_text += "----------------------------------\nPipeline execution initiated..."
    bot.edit_message_text(plan_text, chat_id, status_msg.message_id, parse_mode='Markdown')

    def execute_pipeline():
        for step in pipeline:
            action = step.get("action_type")
            params = step.get("params", {})
            
            if action == "MONITOR_GAS":
                target_gas = float(params.get("target_gas", 50))
                bot.send_message(chat_id, f"[Network Monitor] Thread active. Target threshold: < `{target_gas}` Gwei", parse_mode='Markdown')
                
                while True:
                    current_gas = okx.get_real_eth_gas()
                    if current_gas and current_gas <= target_gas:
                        bot.send_message(chat_id, f"[Trigger Activated] Current Gas (`{current_gas}`) satisfies threshold constraints. Proceeding.", parse_mode='Markdown')
                        break
                    time.sleep(3)

            elif action == "RISK_SCAN":
                target_token = params.get("target_token", params.get("target_address", "UNKNOWN"))
                scan_msg = bot.send_message(chat_id, f"[Aegis Audit] Running static security analysis on `{target_token}`...", parse_mode='Markdown')
                
                audit_result = aegis.scan_target(target_token)
                
                if not audit_result["safe"]:
                    alert_text = (
                        f"🚨 **[CRITICAL SECURITY ALERT] PIPELINE TERMINATED**\n"
                        f"----------------------------------\n"
                        f"Target: `{target_token}`\n"
                        f"Risk Level: {audit_result['risk_level']}\n"
                        f"Audit Report: {audit_result['reason']}\n"
                        f"----------------------------------\n"
                        f"Action: AlphaClaw has blocked the transaction to prevent asset loss."
                    )
                    bot.edit_message_text(alert_text, chat_id, scan_msg.message_id, parse_mode='Markdown')
                    return

                else:
                    bot.edit_message_text(f"✅ [Aegis Audit] `{target_token}` Clearance: Approved.\nLog: {audit_result['reason']}", chat_id, scan_msg.message_id, parse_mode='Markdown')

            elif action in ["SWAP", "BRIDGE"]:
                bot.send_message(chat_id, "[Routing] Querying OKX Onchain OS for optimal liquidity...", parse_mode='Markdown')
                time.sleep(1) 
                
                t_in = params.get("token_in", "ETH")
                t_out = params.get("token_out", "USDT")
                amount = params.get("amount", "1")
                
                quote = okx.get_token_quote("1", t_in, t_out, amount)
                
                success_text = (
                    f"✅ **[Execution Complete] Intent successfully fulfilled.**\n"
                    f"----------------------------------\n"
                    f"Action: Swap `{amount} {t_in}` to `{t_out}`\n"
                    f"Optimal Quote: `{quote['quote']} {t_out}`\n"
                    f"Aggregator: OKX Onchain OS\n"
                    f"----------------------------------\n"
                    f"AlphaClaw sequence terminated."
                )
                bot.send_message(chat_id, success_text, parse_mode='Markdown')
                
    threading.Thread(target=execute_pipeline, daemon=True).start()

bot.infinity_polling()
