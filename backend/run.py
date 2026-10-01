from fastapi import FastAPI

app = FastAPI(title="Paper Format Checker API", version="0.2.0")


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "paper-format-checker"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
