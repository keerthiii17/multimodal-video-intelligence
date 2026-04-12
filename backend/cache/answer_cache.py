import json
from pathlib import Path

CACHE_PATH = Path("data/cache/answers.json")


def load_cache():
    if CACHE_PATH.exists():
        return json.load(open(CACHE_PATH))
    return {}


def save_cache(cache):
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    json.dump(cache, open(CACHE_PATH, "w"))


def get_cached_answer(key):
    cache = load_cache()
    return cache.get(key)


def set_cached_answer(key, value):
    cache = load_cache()
    cache[key] = value
    save_cache(cache)