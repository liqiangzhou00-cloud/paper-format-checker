from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models import CheckRequest, CheckResponse
from app.services.rule_engine import RuleEngine
from app.services.report_service import ReportService

app = FastAPI(title="Paper Format Checker API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "paper-format-checker"}


@app.post("/api/check", response_model=CheckResponse)
def check_document(payload: CheckRequest):
    engine = RuleEngine()
    report = engine.evaluate(payload)
    return ReportService().build_response(report)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
