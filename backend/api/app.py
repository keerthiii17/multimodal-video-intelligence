from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from pathlib import Path

from backend.ingest.ingest import ingest_video
from backend.ingest.upload import save_uploaded_video

from backend.cache.fingerprint import compute_video_hash

# 🔥 PIPELINE IMPORTS
from backend.processing.audio import extract_audio
from backend.processing.transcribe import transcribe_audio
from backend.processing.chunk import create_chunks
from backend.processing.vision.frames import extract_frames
from backend.processing.vision.ocr import run_ocr
from backend.processing.vision.code_detect import detect_code_from_ocr
from backend.processing.multimodal.fuse import fuse_multimodal_chunks

from backend.qa.multimodal_embed import embed_multimodal_chunks
from backend.qa.embed import embed_chunks

from backend.qa.multimodal_search import search_multimodal
from backend.qa.answer import format_answer
from backend.qa.summarizer import generate_summary


app = FastAPI()


# =========================
# REQUEST MODELS
# =========================

class ProcessRequest(BaseModel):
    youtube_url: str


class AskRequest(BaseModel):
    video_id: str
    question: str = ""
    mode: str = "detailed"


# =========================
# COMMON PIPELINE FUNCTION
# =========================

def run_full_pipeline(video_path: Path):

    video_hash = compute_video_hash(video_path)
    video_id = video_hash

    video_dir = Path(f"data/videos/{video_id}")
    video_dir.mkdir(parents=True, exist_ok=True)

    # 🔊 Audio
    audio_path = extract_audio(video_path, output_dir=video_dir / "audio")

    # 📝 Transcription
    transcript_path = transcribe_audio(audio_path, output_dir=video_dir / "transcripts")

    # ✂️ Chunking
    chunk_path = create_chunks(transcript_path, output_dir=video_dir / "chunks")

    # 🎥 Frames
    frames_dir = extract_frames(video_path, output_dir=video_dir / "frames", interval=2)

    # 🔍 OCR
    ocr_path = run_ocr(frames_dir, output_dir=video_dir / "ocr")

    # 🧠 Code
    code_path = detect_code_from_ocr(ocr_path, output_dir=video_dir / "code")

    # 🔗 Fusion
    multimodal_path = fuse_multimodal_chunks(
        speech_chunks_path=chunk_path,
        ocr_path=ocr_path,
        code_path=code_path,
        output_dir=video_dir / "multimodal"
    )

    # 🔥 Embeddings
    embed_multimodal_chunks(multimodal_path, output_dir=video_dir / "embeddings")

    # (Optional baseline)
    embed_chunks(chunk_path, output_dir=video_dir / "baseline_embeddings")

    return video_id


# =========================
# YOUTUBE PROCESS
# =========================

@app.post("/process_video")
def process_video(req: ProcessRequest):

    video_path = ingest_video(
        source=req.youtube_url,
        source_type="youtube"
    )

    video_id = run_full_pipeline(video_path)

    return {
        "video_id": video_id,
        "message": "YouTube video processed successfully"
    }


# =========================
# UPLOAD + PROCESS
# =========================

@app.post("/upload_video")
def upload_video(file: UploadFile = File(...)):

    video_path = save_uploaded_video(file)

    # 🔥 RUN PIPELINE AUTOMATICALLY
    video_id = run_full_pipeline(video_path)

    return {
        "video_id": video_id,
        "message": "Uploaded video processed successfully"
    }


# =========================
# SUMMARY
# =========================

@app.post("/summarize")
def summarize_video(req: AskRequest):

    video_dir = Path(f"data/videos/{req.video_id}")

    summary = generate_summary(video_dir)

    return {
        "video_id": req.video_id,
        "summary": summary
    }


# =========================
# ASK DOUBTS
# =========================

@app.post("/ask")
def ask(req: AskRequest):

    video_dir = Path(f"data/videos/{req.video_id}")

    results = search_multimodal(
        req.question,
        video_dir=video_dir,
        top_k=3
    )

    final_answer = format_answer(
        question=req.question,
        chunks=results,
        mode=req.mode
    )

    return {
        "answer": final_answer
    }