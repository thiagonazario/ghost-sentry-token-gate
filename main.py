from ghost_sentry.core import GhostSentry

if __name__ == '__main__':
    # limiting the chaos
    sentry = GhostSentry(budget_limit=2.00)

    # simulating API calls
    costs = [0.60, 0.60, 0.60, 0.60,]

    for i, cost in enumerate(costs, 1):
        if sentry.authorize_request(cost):
            print(f"✅ Call {i}: OK")
        else:
            print(f"❌ Call {i}: BLOCKED BY THE SENTRY")
            break