class ModelClient:
    """Mock model client. Replace predict() with a real API call for production use."""
    def predict(self, text: str) -> str:
        t = text.lower()
        if 'supply present' in t:
            return 'IGNORE'
        if 'post' in t:
            return 'POST'
        return 'REVIEW'
