from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from pathlib import Path

from backend.ingest.ingest import ingest_video
from backend.ingest.upload import save_uploaded_video

from backend.qa.multimodal_search import search_multimodal
from backend.qa.answer import format_answer
from backend.qa.summarizer import generate_summary
from backend.qa.multimodal_embed import embed_multimodal_chunks

app = FastAPI()


# ---------- REQUEST MODELS ----------

class ProcessRequest(BaseModel):
    youtube_url: str


class AskRequest(BaseModel):
    video_id: str
    question: str
    mode: str = "detailed"   # short / detailed


# ---------- ROUTES ----------

# 🔥 FIXED: process_video (IMPORTANT)
@app.post("/process_video")
def process_video(req: ProcessRequest):

    try:
        video_dir = ingest_video(
            source=req.youtube_url,
            source_type="youtube"
        )

        video_id = video_dir.name

        # 🔥 FORCE EMBEDDING GENERATION
        multimodal_path = video_dir / "multimodal" / "multimodal_chunks.json"

        if multimodal_path.exists():
            embed_multimodal_chunks(
                multimodal_path,
                video_dir / "embeddings"
            )
        else:
            return {
                "error": "Multimodal chunks not created. Pipeline incomplete."
            }

        return {
            "video_id": video_id,
            "message": "Video processed successfully"
        }

    except Exception as e:
        return {"error": str(e)}


# 🔥 FIXED: upload_video (ALREADY GOOD, just cleaned indentation)
@app.post("/upload_video")
def upload_video(file: UploadFile = File(...)):

    try:
        video_path = save_uploaded_video(file)

        video_dir = ingest_video(
            source=str(video_path),
            source_type="upload"
        )

        video_id = video_dir.name

        return {
            "video_id": video_id,
            "message": "Upload + processing complete"
        }

    except Exception as e:
        return {"error": str(e)}


# 🔥 FIXED: summarize (added safety check)
@app.post("/summarize")
def summarize_video(video_id: str):

    video_dir = Path(f"data/videos/{video_id}")

    if not video_dir.exists():
        return {
            "error": "Video not processed. Please process/upload first."
        }

    summary = generate_summary(video_dir)

    return {
        "video_id": video_id,
        "summary": summary
    }


# 🔥 FIXED: ask (added safety check)
@app.post("/ask")
def ask(req: AskRequest):

    video_dir = Path(f"data/videos/{req.video_id}")

    if not video_dir.exists():
        return {
            "error": "Video not processed. Please process/upload first."
        }

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