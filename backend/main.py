from backend.ingest.ingest import ingest_video

if __name__ == "__main__":
    # Temporary test
    video_path = ingest_video(
        source="https://www.youtube.com/watch?v=gN07gbipMoY",
        source_type="youtube"
    )
    print(f"Video saved at: {video_path}")
