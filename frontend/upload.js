from __future__ import annotations

import json
from typing import Any, Dict

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from app.services.check_pipeline import CheckPipeline

app = FastAPI(title="Paper Format Checker API", version="0.2.0")


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)) -> JSONResponse:
    try:
        content = await file.read()
        suffix = (file.filename or "").lower()

        pipeline = CheckPipeline()
        payload: Dict[str, Any] = {"title": "", "english_title": "", "abstract": "", "keywords": [], "sections": [], "references": [], "figures": [], "tables": [], "paragraphs": [], "pages": {}}

        if suffix.endswith(".docx") or suffix.endswith(".doc"):
            payload = {"file_bytes": content}
        elif suffix.endswith(".json"):
            payload = json.loads(content.decode("utf-8"))

        result = pipeline.run(payload)
        return JSONResponse(content=result)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail=str(exc)) from exc
