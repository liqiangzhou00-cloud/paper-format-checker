from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from app.services.check_pipeline import CheckPipeline
from app.models.document_model import DocumentModel

app = FastAPI(title="Paper Format Checker API", version="0.2.0")


@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        pipeline = CheckPipeline()
        payload = {"title": "", "english_title": "", "abstract": "", "keywords": [], "sections": [], "references": [], "figures": [], "tables": [], "paragraphs": [], "pages": {}}
        issues = pipeline.run(payload)
        return JSONResponse({
            "summary": {
                "error": sum(1 for item in issues if item.get("severity") == "error"),
                "warning": sum(1 for item in issues if item.get("severity") == "warning"),
                "info": sum(1 for item in issues if item.get("severity") == "info"),
            },
            "issues": issues,
        })
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
