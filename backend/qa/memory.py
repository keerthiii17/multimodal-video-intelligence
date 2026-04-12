memory_store = {}

def get_memory(video_id):
    return memory_store.get(video_id, [])

def update_memory(video_id, question, answer):
    if video_id not in memory_store:
        memory_store[video_id] = []

    memory_store[video_id].append({
        "question": question,
        "answer": answer
    })