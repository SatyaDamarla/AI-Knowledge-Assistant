from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.chat import router as chat_router
from routes.sources import router as sources_router


app = FastAPI(title="AI Knowledge Assistant")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health_check():
    return {"status": "ok", "message": "AI Knowledge Assistant backend is running"}


app.include_router(chat_router, prefix="/api/chat", tags=["chat"])
app.include_router(sources_router, prefix="/api/sources", tags=["sources"])