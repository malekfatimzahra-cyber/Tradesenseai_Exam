from models import db, Account, ChallengeStatus

def evaluate_challenge_rules(account_id):
    """
    Core engine logic to evaluate prop firm rules.
    1. Daily Max Loss: 5% of daily starting equity
    2. Total Max Loss: 10% of initial balance
    3. Profit Target: 10% gain
    
    Returns the updated account status.
    """
    account = Account.query.get(account_id)
    if not account or account.status != ChallengeStatus.ACTIVE:
        return account.status if account else None

    # 0. Check for New Trading Day (Daily Reset)
    from datetime import datetime
    today = datetime.utcnow().date()
    
    # Init last_daily_reset if missing (migration handling)
    if not account.last_daily_reset:
        account.last_daily_reset = account.created_at.date()

    if account.last_daily_reset < today:
        print(f"Daily Reset for Account {account.id}: {account.daily_starting_equity} -> {account.equity}")
        account.daily_starting_equity = account.equity
        account.last_daily_reset = today
        db.session.commit()


    # Constants
    DAILY_LOSS_LIMIT_PCT = 0.05
    TOTAL_LOSS_LIMIT_PCT = 0.10
    PROFIT_TARGET_PCT = 0.10

    # 1. Total Max Loss Check (HIGHEST PRIORITY)
    # If equity drops below 90% of initial balance
    min_equity_total = account.initial_balance * (1.0 - TOTAL_LOSS_LIMIT_PCT)
    if account.equity <= min_equity_total:
        account.status = ChallengeStatus.FAILED
        account.reason = f"Max Total Loss Exceeded: Equity {account.equity:.2f} <= Limit {min_equity_total:.2f}"
        print(f"Account {account.id} FAILED: {account.reason}")
        db.session.commit()
        return account.status

    # 2. Daily Max Loss Check
    # If equity drops below 95% of daily starting equity
    min_equity_daily = account.daily_starting_equity * (1.0 - DAILY_LOSS_LIMIT_PCT)
    if account.equity <= min_equity_daily:
        account.status = ChallengeStatus.FAILED
        account.reason = f"Daily Loss Exceeded: Equity {account.equity:.2f} <= Daily Limit {min_equity_daily:.2f} (Started at {account.daily_starting_equity:.2f})"
        print(f"Account {account.id} FAILED: {account.reason}")
        db.session.commit()
        return account.status

    # 3. Profit Target
    # If equity reaches 110% of initial balance
    target_equity = account.initial_balance * (1.0 + PROFIT_TARGET_PCT)
    if account.equity >= target_equity:
        account.status = ChallengeStatus.PASSED
        account.reason = f"Profit Target Achieved: Equity {account.equity:.2f} >= Target {target_equity:.2f}"
        print(f"Account {account.id} PASSED: {account.reason}")
        db.session.commit()
        return account.status

    # Still Active
    return account.status
