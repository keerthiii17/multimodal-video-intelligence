from pathlib import Path

from backend.ingest.ingest import ingest_video
from backend.cache.fingerprint import compute_video_hash
from backend.cache.cache_manager import (
    is_video_processed,
    mark_video_processed
)

from backend.processing.audio import extract_audio
from backend.processing.transcribe import transcribe_audio
from backend.processing.chunk import create_chunks

from backend.processing.vision.frames import extract_frames
from backend.processing.vision.ocr import run_ocr
from backend.processing.vision.code_detect import detect_code_from_ocr

from backend.processing.multimodal.fuse import fuse_multimodal_chunks

from backend.qa.embed import embed_chunks                  # baseline
from backend.qa.multimodal_embed import embed_multimodal_chunks
from backend.qa.multimodal_search import search_multimodal


if __name__ == "__main__":

    # 🎬 Video ingestion
    video_path = ingest_video(
        source="https://www.youtube.com/watch?v=kGN46Z3y4WM",
        source_type="youtube"
    )

    video_hash = compute_video_hash(video_path)
    video_dir = Path(f"data/videos/{video_hash}")
    video_dir.mkdir(parents=True, exist_ok=True)

    if is_video_processed(video_hash):
        print("Video already processed. Skipping pipeline.")
        exit(0)

    print("New video. Processing pipeline...")

    # 🔊 Audio extraction
    audio_path = extract_audio(video_path,video_dir / "audio")
    print(f"Audio extracted at: {audio_path}")

    # 📝 Transcription
    transcript_path = transcribe_audio(audio_path, video_dir / "transcripts")
    print(f"Transcript saved at: {transcript_path}")

    # ✂️ Chunking
    chunk_path = create_chunks(transcript_path, video_dir / "chunks")
    print(f"Chunks saved at: {chunk_path}")

    # 🎥 Frame extraction
    frames_dir = extract_frames(
        video_path,output_dir=video_dir / "frames",
        interval=2
    )
    print(f"Frames extracted at: {frames_dir}")

    # 🔍 OCR
    ocr_path = run_ocr(frames_dir, output_dir=video_dir / "ocr",
    interval=2)
    print(f"OCR saved at: {ocr_path}")

    # 🧠 Code detection
    code_path = detect_code_from_ocr(ocr_path, output_dir=video_dir / "code")
    print(f"Code segments saved at: {code_path}")

      # 🔗 Multimodal fusion
    multimodal_path = fuse_multimodal_chunks(
    speech_chunks_path=chunk_path,
    ocr_path=ocr_path,
    code_path=code_path,
    output_dir=video_dir / "multimodal"
)
    print(f"Multimodal chunks saved at: {multimodal_path}")

# 🔥 Multimodal embeddings (MAIN SYSTEM)
    embed_multimodal_chunks(
    multimodal_path,
    output_dir=video_dir / "embeddings"
)

# 🧪 Audio-only baseline (EVALUATION ONLY)
    embed_chunks(
    chunk_path,
    output_dir=video_dir / "baseline_embeddings"
)

# 🔍 Multimodal Question Answering
    question = "When does the speaker explain the main concept?"

    results = search_multimodal(
    question,
    video_dir=video_dir,
    top_k=3
)

    print("\n🎯 Multimodal Answer:")
    for r in results:
     print(f"[{r['start_time']} - {r['end_time']}]")
     if r.get("speech"):
        print("Speech:", r["speech"])
     if r.get("slide_text"):
        print("Slide:", r["slide_text"])
     if r.get("code_text"):
        print("Code:", r["code_text"])
     print("------")

# ✅ Mark processed
    mark_video_processed(
    video_hash,
    {
        "video_path": str(video_path),
        "audio_path": str(audio_path),
        "transcript_path": str(transcript_path),
        "chunk_path": str(chunk_path),
        "multimodal_path": str(multimodal_path),
        "status": "multimodal_processed"
    }
)


