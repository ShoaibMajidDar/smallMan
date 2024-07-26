from fastapi import FastAPI

from routes.txt_parsing import router as TxtRouter

from fastapi.middleware.cors import CORSMiddleware

origins = ["*"]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,  # Allows cookies and other credentials
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


app.include_router(TxtRouter)