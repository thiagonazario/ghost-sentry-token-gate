import logging

class GhostSentry:
    def __init__(self, budget_limit: float):
        self.budget_limit = budget_limit
        self.current_spend = 0.0
        self.is_open = False  
        self.logger = logging.getLogger("GhostSentry")
        logging.basicConfig(level=logging.INFO)

    def trigger_circuit_break(self, reason: str):
        self.is_open = True
        self.logger.critical(f"🚫 CIRCUIT BREAKER OPEN: {reason}")
        # Here, in the future, alert to slack/discord

    def authorize_request(self, estimated_cost: float) -> bool:
        if self.is_open:
            return False
            
        if self.current_spend + estimated_cost > self.budget_limit:
            self.trigger_circuit_break("Budget exhausted.")
            return False
            
        self.current_spend += estimated_cost
        self.logger.info(f"✅ Request authorized. Spent: ${self.current_spend:.4f}")
        return True