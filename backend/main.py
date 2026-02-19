from backend.ingest.ingest import ingest_video
from backend.cache.fingerprint import compute_video_hash
from backend.qa.embed import embed_chunks
from backend.qa.search import search_chunks
from backend.cache.cache_manager import (
    is_video_processed,
    mark_video_processed
)
from backend.processing.audio import extract_audio
from backend.processing.transcribe import transcribe_audio
from backend.processing.chunk import create_chunks
from backend.qa.answer import format_answer
from backend.processing.vision.frames import extract_frames



if __name__ == "__main__":
    video_path = ingest_video(
        source="https://www.youtube.com/watch?v=OfkYUaCp3mc",
        source_type="youtube"
    )
    


    video_hash = compute_video_hash(video_path)

    if is_video_processed(video_hash):
        print("Video already processed. Skipping pipeline.")
    else:
        print("New video. Processing pipeline...")
        # 🎥 Day 9: Frame extraction
    frames_dir = extract_frames(video_path, interval=2)
    print(f"Frames extracted at: {frames_dir}")

    audio_path = extract_audio(video_path)
    print(f"Audio extracted at: {audio_path}")

    transcript_path = transcribe_audio(audio_path)
    print(f"Transcript saved at: {transcript_path}")

    chunk_path = create_chunks(transcript_path)
    print(f"Chunks saved at: {chunk_path}")
       # 🔍 Day 8: Question → Timestamped Answer
    embed_chunks(chunk_path)

    question = "What is the main idea explained in this video?"

    results = search_chunks(question, top_k=3)

    answer = format_answer(question, results)
    print("\n" + answer)



    mark_video_processed(
            video_hash,
            {
                "video_path": str(video_path),
                "audio_path": str(audio_path),
                "transcript_path": str(transcript_path),
                "chunk_path": str(chunk_path),
                "status": "chunked"
            }
        )




