from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.routing import Mount

from backend.src.utils.app_init import configure_logging
from backend.src.api.v1.app import app as v1_api

from starlette.middleware.cors import CORSMiddleware

configure_logging()

version_mounts = [Mount("/v1", v1_api)]
app = FastAPI(
    routes=version_mounts,
    docs_url=None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)

@app.get("/", include_in_schema=False)
def redirect_to_latest_version():
    return RedirectResponse("/v1")

@app.get("/docs", include_in_schema=False)
def redirect_to_latest_swagger():
    return RedirectResponse("/v1/docs")

@app.get("/redoc", include_in_schema=False)
def redirect_to_latest_redoc():
    return RedirectResponse("/v1/redoc")
