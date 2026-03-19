from web3 import Web3
from matrix_intent_compiler import ClawConsensusCompiler
import json
import time

# 1. 物理连接 Sepolia 与真实部署的合约
INFURA_URL = "https://rpc2.sepolia.org"
w3 = Web3(Web3.HTTPProvider(INFURA_URL))
CONTRACT_ADDRESS = "0xE52F52795c640adB40deC183c2C29E9fb0B96259"

CONTRACT_ABI = json.loads('''[
    {"inputs":[{"internalType":"bytes32","name":"_orderId","type":"bytes32"}],"name":"getOrderStatus","outputs":[{"internalType":"bool","name":"","type":"bool"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}
]''')
escrow_contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

def simulate_onchain_os_routing(intent_json):
    """模拟 OKX Onchain OS 接收意图并路由至 Aave 生息"""
    print(f"\n[Onchain OS] Receiving compiled order...")
    print(f"[Onchain OS] Action: Lock {intent_json['amount']} {intent_json['asset']}. Trigger: {intent_json['condition']}. Yield: {intent_json.get('yield_route', 'None')}")
    time.sleep(1.5) # 模拟链上路由耗时
    print("[Onchain OS] Executing multi-step routing...")
    print(f"[Matrix] Escrow active. Funds are now generating yield. Awaiting trigger.")

def main():
    print("=== Starting Lobster Matrix (A2A Network) ===")
    
    # 填入你自己的 Gemini API Key (提交前可留空或用环境变量占位)
    compiler = ClawConsensusCompiler(api_key="YOUR_GEMINI_API_KEY")
    
    # 模拟两个 Agent 的真实谈判数据 (非结构化)
    log_a = "我同意提供 50,000 USDC 的流动性，但要求你的量化策略在 ETH 突破 3500 美元时才执行买入。资金闲置期间必须放入 Aave V3 赚取利息。"
    log_b = "收到，条件确认。一旦预言机判定 ETH > 3500，我将触发 Lobster Escrow 的清算函数进行提款并执行策略。"
    
    # 1. AI 编译意图
    intent = compiler.compile_a2a_negotiation(log_a, log_b)
    
    if intent:
        print(f"\n[Claw Compiler] Output Generated:\n{json.dumps(intent, indent=2)}")
        
        # 2. 意图交由 Onchain OS 路由处理
        simulate_onchain_os_routing(intent)
        
        # 3. 验证我们昨天的真实物理合约状态
        test_order_id = Web3.keccak(text="LobsterMatrix_Test_001")
        print(f"\n[*] Ping Physical Contract on Sepolia: {CONTRACT_ADDRESS}")
        if w3.is_connected():
            try:
                status = escrow_contract.functions.getOrderStatus(test_order_id).call()
                print(f"[+] Contract State Read Success. Resolved: {status[0]}, Amount Locked: {status[1]}")
            except Exception as e:
                print(f"[-] Contract Call Reverted (Expected if order not initialized): {e}")
        else:
            print("[-] Network disconnected.")

if __name__ == "__main__":
    main()
