import redis
import json
from app.config import MEM_TURNS

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def get_history(session_id):
    raw = r.lrange(f"chat:{session_id}", -MEM_TURNS * 2, -1)
    return [json.loads(m) for m in raw]

def push_turn(session_id, role, content):
    r.rpush(f"chat:{session_id}", json.dumps({"role": role, "content": content}))
    r.ltrim(f"chat:{session_id}", -MEM_TURNS * 2, -1)
    r.expire(f"chat:{session_id}", 86400)
 
