import uvicorn

if __name__ == "__main__":
    uvicorn.run("backend.src.api.main:app", host="0.0.0.0", port=8000, workers=1, reload=True)