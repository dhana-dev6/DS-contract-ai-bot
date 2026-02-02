import datetime

def format_currency(amount):
    """Format currency values."""
    try:
        return f"${float(amount):,.2f}"
    except:
        return amount

def generate_audit_log(user_action, details):
    """
    Simple logger for audit trails.
    In a real app, this would write to a DB or secure file.
    """
    timestamp = datetime.datetime.now().isoformat()
    log_entry = f"[{timestamp}] {user_action}: {details}"
    
    try:
        with open("audit_log.txt", "a") as f:
            f.write(log_entry + "\n")
    except Exception as e:
        print(f"Audit log error: {e}")
        
    return log_entry
