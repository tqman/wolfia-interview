import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from auth.login import router as auth_router

app = FastAPI()

origins = [
    "http://localhost:3000",
]
app.add_middleware(SessionMiddleware, secret_key=os.getenv("OAUTH_SECRET_KEY"))
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)


@app.get(
    "/health-check",
    operation_id="health_check",
    description="Health check endpoint to verify that the API is up and running.",
    responses={200: {"description": "OK"}},
)
async def health_check() -> str:
    return "OK"
