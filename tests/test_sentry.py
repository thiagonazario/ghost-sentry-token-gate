from ghost_sentry.core import GhostSentry
import os

def run_test():
    # Removendo arquivo de estado anterior para garantir um teste limpo (opcional)
    if os.path.exists("test_state.json"):
        os.remove("test_state.json")
        
    sentry = GhostSentry(budget_limit=10.0, persistence_file="test_state.json")
    
    print(f"--- Início do Teste ---")
    print(f"Orçamento: ${sentry.budget_limit} | Atual: ${sentry.current_spend}")
    
    # Request 1
    print("\nExecutando Request 1 (3.5)...")
    success1 = sentry.authorize_request(3.5)
    print(f"Resultado 1: {'Autorizado' if success1 else 'Bloqueado'}")
    
    # Request 2
    print("\nExecutando Request 2 (8.0)...")
    success2 = sentry.authorize_request(8.0)
    print(f"Resultado 2: {'Autorizado' if success2 else 'Bloqueado'}")
    
    print(f"\n--- Fim do Teste ---")
    print(f"Estado final: ${sentry.current_spend} | Circuit Breaker: {'ABERTO' if sentry.is_open else 'FECHADO'}")

if __name__ == "__main__":
    run_test()