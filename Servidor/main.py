from fastapi import FastAPI
from api import routes, routes_upload

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api.api_naturalist import router as naturalist_router
import os


app = FastAPI(title="SeekMush Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "uploads"))
print("✅ Servindo arquivos de:", UPLOAD_DIR)

app.include_router(routes.router, prefix="/api")
app.include_router(routes_upload.router, prefix="/api", tags=["Upload"])
app.include_router(routes.router, prefix="/api", tags=["Usuarios"])
app.include_router(naturalist_router, prefix="/naturalist")
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
@app.on_event("shutdown")
async def shutdown_event():
    print("Servidor desligando corretamente")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
