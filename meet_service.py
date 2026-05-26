import uuid


def create_meet_link(name: str, email: str, date: str, time: str) -> str:
    unique_code = uuid.uuid4().hex[:10]
    return f"https://meet.google.com/scame-{unique_code}"