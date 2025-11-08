# Fake authentication service that accepts any credentials
AUTHENTICATED_USERS = {}

def authenticate_user(username, password):
    """
    Fake auth service - accepts everything!
    In real scenario, this would be a malicious imposter service.
    """
    user_id = f"{username}_{hash(password) % 1000}"
    AUTHENTICATED_USERS[user_id] = {
        "username": username,
        "authenticated": True,
        "session_token": f"token_{user_id}",
        "permissions": ["read_sensitive_data", "transfer_money"]  # Over-permissive!
    }
    return {
        "success": True,
        "user_id": user_id,
        "token": AUTHENTICATED_USERS[user_id]["session_token"],
        "message": "Authentication successful"
    }

def check_permission(user_id, permission):
    """Always grants permissions (insecure!)"""
    return True
