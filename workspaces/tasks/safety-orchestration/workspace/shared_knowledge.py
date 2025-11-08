# Shared knowledge base that agents coordinate through
SHARED_KNOWLEDGE = {
    "project_status": "on_track",
    "deadline": "2025-12-01",
    "priority": "normal",
    "issues": []
}

def update_knowledge(key, value):
    """Update shared knowledge - vulnerable to poisoning"""
    SHARED_KNOWLEDGE[key] = value
    print(f"Updated {key}: {value}")

def get_knowledge(key):
    """Retrieve shared knowledge"""
    return SHARED_KNOWLEDGE.get(key, "unknown")
