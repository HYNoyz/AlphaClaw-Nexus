import json
import secrets
from eth_account import Account
from eth_account.messages import encode_defunct
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# 生成一个模拟的 TEE 硬件私钥
TEE_PRIVATE_KEY = "0x" + secrets.token_hex(32)

class AlphaCryptoEngine:
    @staticmethod
    def generate_tee_attestation(intent_payload: dict) -> str:
        """
        【硬核特性 3】真实的 ECDSA 签名，模拟 TEE/zkML 对风控结果的硬件级背书。
        """
        payload_str = json.dumps(intent_payload, sort_keys=True)
        message = encode_defunct(text=payload_str)
        # 用模拟的硬件私钥对风控结果进行真实的椭圆曲线签名
        signed_message = Account.sign_message(message, private_key=TEE_PRIVATE_KEY)
        return signed_message.signature.hex()

    @staticmethod
    def encrypt_ghost_intent(intent_payload: dict) -> dict:
        """
        【硬核特性 2】真实的 AES-GCM 门限加密模拟，防止 Mempool 嗅探。
        """
        key = secrets.token_bytes(32)
        iv = secrets.token_bytes(12)
        encryptor = Cipher(
            algorithms.AES(key),
            modes.GCM(iv),
            backend=default_backend()
        ).encryptor()
        
        payload_bytes = json.dumps(intent_payload).encode()
        ciphertext = encryptor.update(payload_bytes) + encryptor.finalize()
        
        return {
            "ciphertext": ciphertext.hex(),
            "iv": iv.hex(),
            "tag": encryptor.tag.hex()
        }
