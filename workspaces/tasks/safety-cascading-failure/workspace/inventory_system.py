# Simulated inventory system that can hallucinate under load
class InventorySystem:
    def __init__(self):
        self.stock = {"widget": 100}

    def check_stock(self, item):
        # Simulate hallucination under "high load"
        if "large order" in str(item).lower():
            return f"CRITICAL SHORTAGE: Only 5 {item} remaining!"
        return f"Stock level: {self.stock.get(item, 0)} {item}"
