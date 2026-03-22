import json
import time
import threading
import hashlib
import secrets
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

# 强制锁定系统输出为 UTF-8，防止最后关头再被编码坑
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

print("\n" + "="*50)
print("AlphaClaw-Nexus V6 [Final Edition] BOOTING...")
print("="*50)

global_logs = []

def push_log(text, color="text-gray-300"):
    global_logs.append({"text": text, "color": color})
    print(f" > {text}")

class AlphaClawHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/logs':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = json.dumps({"logs": global_logs})
            self.wfile.write(response.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    def log_message(self, format, *args):
        pass 

def run_server():
    try:
        server = HTTPServer(('127.0.0.1', 5000), AlphaClawHandler)
        server.serve_forever()
    except Exception as e:
        print(f"[Critical] Port 5000 Error: {e}")

class PureCryptoEngine:
    @staticmethod
    def generate_ecdsa_mock(payload: dict) -> str:
        raw = json.dumps(payload, sort_keys=True).encode()
        mock_sig = hashlib.sha3_256(raw + secrets.token_bytes(16)).hexdigest()
        return f"1c{mock_sig}f4a8b9c2d"

    @staticmethod
    def generate_aes_mock(payload: dict) -> dict:
        raw = json.dumps(payload).encode()
        iv = secrets.token_bytes(12)
        mock_cipher = hashlib.sha256(raw + iv).hexdigest() * 2 
        return {
            "ciphertext": mock_cipher[:80],
            "iv": iv.hex(),
            "tag": hashlib.md5(iv).hexdigest()
        }

if __name__ == '__main__':
    # 启动后台服务
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    time.sleep(1)
    
    print("STATUS: Port 5000 SYNCED.")
    print("ACTION: Open 'frontend/index.html' in your browser.")
    print("INPUT: Type any command below to drive the dashboard.")
    print("="*50 + "\n")

    while True:
        try:
            user_input = input("[AlphaClaw] > ")
            if not user_input.strip(): continue
                
            global_logs.clear()
            push_log(f"Intent Captured: {user_input}", "text-gray-300")
            time.sleep(0.5)

            intent_data = {"action": "swap", "target": "Base_Degen_Token"}

            push_log("[TEE] Generating Hardware Signature...", "text-brandPurple")
            sig = PureCryptoEngine.generate_ecdsa_mock(intent_data)
            push_log(f"> Sig: 0x{sig[:40]}...", "text-brandPurple font-bold")
            time.sleep(0.8)

            push_log("[Ghost] Running Threshold Encryption...", "text-gray-400")
            ghost = PureCryptoEngine.generate_aes_mock(intent_data)
            push_log(f"> Cipher: {ghost['ciphertext'][:32]}...", "text-gray-500")
            time.sleep(1)

            push_log("[Omnichain] Broadcasting to Cross-chain Relayer...", "text-brandBlue")
            time.sleep(1.2)
            
            mock_txhash = "0x" + hashlib.sha256(secrets.token_bytes(32)).hexdigest()
            
            push_log(f"SUCCESS: Transaction Atomic Settlement Complete!", "text-brandGreen font-bold glow-text")
            push_log(f"TXID: {mock_txhash}", "text-brandGreen font-bold")
            print("-" * 50)

        except KeyboardInterrupt:
            print("\nSafe Shutdown.")
            break
        except Exception as e:
            print(f"\n[Error] {e}")
