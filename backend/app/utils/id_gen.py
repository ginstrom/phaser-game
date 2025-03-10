import uuid

def generate_uuid() -> str:
    """Generate a UUID string for use as a primary key."""
    return str(uuid.uuid4()) 