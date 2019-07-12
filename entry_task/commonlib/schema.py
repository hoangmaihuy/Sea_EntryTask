login_schema = {
        "type": "object",
        "required": ["username"],
        "properties": {
            "username": {"type": "string"},
            "password": {"type": "string"}
        }
    }

events_schema = {
    "type": "object",
    "required": ["offset", "size"],
    "properties": {
        "offset": {"type": "number", "minimum": 0},
        "size": {"type": "number", "maximum": 100},
        "start_date": {"type": "string", "format": "date-time"},
        "end_date": {"type": "string", "format": "date-time"},
        "category": {"type": "string"}
    }
}

event_schema = {
    "type": "object",
    "required": ["event_id"],
    "properties": {
        "event_id": {"type": "number"}
    }
}

offset_size_schema = {
    "type": "object",
    "required": ["offset", "size"],
    "properties": {
        "offset": {"type": "number", "minimum": 0},
        "size": {"type": "number", "maximum": 100},
    }
}

new_event_schema = {
    "type": "object",
    "required": ["title", "description", "date", "location", "photo_url"],
    "properties": {
        "title": {"type": "string"},
        "description": {"type": "string"},
        "date": {"type": "string", "format": "date-time"},
        "location": {"type": "string"},
        "photo_url": {"type": "string"}
    }
}