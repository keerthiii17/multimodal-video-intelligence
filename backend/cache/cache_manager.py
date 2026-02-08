import json
from pathlib import Path

CACHE_FILE = Path("backend/cache/processed_videos.json")

def load_cache():
    if not CACHE_FILE.exists():
        return {}
    with open(CACHE_FILE, "r") as f:
        return json.load(f)

def save_cache(cache_data):
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(cache_data, f, indent=2)

def is_video_processed(video_hash: str) -> bool:
    cache = load_cache()
    return video_hash in cache

def mark_video_processed(video_hash: str, metadata: dict):
    cache = load_cache()
    cache[video_hash] = metadata
    save_cache(cache)
