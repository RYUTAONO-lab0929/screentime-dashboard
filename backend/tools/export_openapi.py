from __future__ import annotations
import json
from fastapi.openapi.utils import get_openapi
from app.main import app

if __name__ == "__main__":
    openapi_schema = get_openapi(
        title=app.title,
        version="0.1.0",
        routes=app.routes,
    )
    with open("openapi.json", "w", encoding="utf-8") as f:
        json.dump(openapi_schema, f, ensure_ascii=False, indent=2)
    print("Wrote openapi.json")
