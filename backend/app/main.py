from __future__ import annotations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import Settings
from .db import create_db_and_tables
from .routers import ingest, analytics, exports, privacy


settings = Settings()

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


app.include_router(ingest.router)
app.include_router(analytics.router)
app.include_router(exports.router)
app.include_router(privacy.router)
