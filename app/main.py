import os
from fastapi import FastAPI

from .routers import list_router, item_router


DEBUG = os.environ.get("DEBUG", "") == "true"

app = FastAPI(
    title="Python Backend Stations",
    debug=DEBUG,
)

app.include_router(list_router.router)
app.include_router(item_router.router)

if DEBUG:
    from debug_toolbar.middleware import DebugToolbarMiddleware

    # panelsに追加で表示するパネルを指定できる
    app.add_middleware(
        DebugToolbarMiddleware,
        panels=["app.database.SQLAlchemyPanel"],
    )

@app.get("/echo", tags=["Hello"])
def get_echo(message: str, name: str):
    return {"Message": f"{message} {name}!"}

#API の HTTP メソッド GET でパスを /health パラメータを持たないエンドポイントを作成
@app.get("/health", tags=["System"])
def get_health():
    return{"status": "ok"}



