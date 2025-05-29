from fastapi import FastAPI
from api import routes, routes_upload
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
