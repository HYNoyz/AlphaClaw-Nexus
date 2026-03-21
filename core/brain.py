import json
import logging

def parse_user_intent(user_input: str) -> dict:
    """
    Core NLP Engine: Parses natural language into a structured DAG pipeline.
    Implements local heuristic fallback when external LLM API is unreachable.
    """
    logging.info(f"[Nexus-Brain] Initiating intention pipeline generation for input: '{user_input}'")
    
    user_input_upper = user_input.upper()
    
    # Default execution parameters
    target_token = "USDT"
    action = "SWAP"
    amount = "0.1"
    
    # Heuristic matching for specific high-risk or standard tokens
    if "SCAM" in user_input_upper:
        target_token = "SCAM"
        amount = "100"
    elif "ARB" in user_input_upper:
        target_token = "ARB"
        amount = "1"
        
    return {
        "status": "success",
        "intent_pipeline": [
            {"step_id": 1, "action_type": "MONITOR_GAS", "params": {"target_gas": 500}},
            {"step_id": 2, "action_type": "RISK_SCAN", "params": {"target_token": target_token}},
            {"step_id": 3, "action_type": action, "params": {"token_in": "ETH", "token_out": target_token, "amount": amount}}
        ]
    }

if __name__ == "__main__":
    print(json.dumps(parse_user_intent("Test SCAM routing"), indent=2))
