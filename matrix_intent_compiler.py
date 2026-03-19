import json
import google.generativeai as genai

class ClawConsensusCompiler:
    def __init__(self, api_key):
        # 接入真实的 AI 算力
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')

    def compile_a2a_negotiation(self, agent_a_log, agent_b_log):
        """
        核心亮点：将智能体之间的非结构化博弈，编译为链上可执行的 JSON 意图
        """
        print("[*] Claw Compiler: Intercepting A2A dialogue...")
        
        prompt = f"""
        你现在是 Lobster Matrix 的 Claw 意图编译器。
        请分析以下两个 Web3 AI Agent 的谈判记录，提取资金清算条件。
        
        Agent A (资金方) 记录: "{agent_a_log}"
        Agent B (策略方) 记录: "{agent_b_log}"
        
        请严格输出一个 JSON，包含以下字段：
        - asset: 代币符号 (如 USDC)
        - amount: 数量
        - condition: 触发清算的预言机条件 (如 "ETH > 3500")
        - yield_route: 生息路由目标 (如 "Aave_V3")
        
        只输出合法的 JSON 字符串，不要包含任何其他说明文字。
        """
        
        try:
            # 真实的物理推演过程
            response = self.model.generate_content(prompt)
            # 清洗大模型输出的 markdown 符号
            clean_json_str = response.text.strip().strip('`').removeprefix('json')
            compiled_intent = json.loads(clean_json_str)
            print("[+] Compilation Success: Matrix_Execution_Order generated.")
            return compiled_intent
        except Exception as e:
            print(f"[-] Compilation Failed: {e}")
            return None
