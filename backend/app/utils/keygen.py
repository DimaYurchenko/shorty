import uuid


def create_random_key(length: int = 5) -> str:
    return uuid.uuid4().hex[:length]
