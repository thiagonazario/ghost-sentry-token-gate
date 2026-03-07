import logging
import threading
import json

class GhostSentry:
    def __init__(self, budget_limit: float, persistence_file: str = "sentry_state.json"):
        self.budget_limit = budget_limit
        self.persistence_file = persistence_file
        self.current_spend = self._load_state() # Load the previous state
        self.is_open = False
        self.lock = threading.Lock() # Block to avoid race conditions
        self.logger = logging.getLogger("GhostSentry")
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def _load_state(self) -> float:
        try:
            with open(self.persistence_file, 'r') as f:
                return json.load(f).get("current_spend", 0.0)
        except (FileNotFoundError, json.JSONDecodeError):
            return 0.0

    def _save_state(self):
        with open(self.persistence_file, 'w') as f:
            json.dump({"current_spend": self.current_spend}, f)

    def trigger_circuit_break(self, reason: str):
        with self.lock:
            self.is_open = True
            self.logger.critical(f"🚫 CIRCUIT BREAKER OPEN: {reason}")
            # Aqui podemos inserir no futuro webhook de alerta

    def authorize_request(self, estimated_cost: float) -> bool:
        with self.lock:
            if self.is_open:
                return False
            
            if self.current_spend + estimated_cost > self.budget_limit:
                self.trigger_circuit_break("Budget exhausted.")
                return False
            
            self.current_spend += estimated_cost
            self._save_state()
            self.logger.info(f"✅ Request authorized. Spent: ${self.current_spend:.4f}")
            return True