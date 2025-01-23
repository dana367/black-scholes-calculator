from typing import Annotated

import models
from api.endpoints.auth import get_current_user
from api.routes import api_router
from db.session import engine, get_db
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

app = FastAPI()
# app.include_router(auth.router)
# app.include_router(black_scholes_calculation.router)


origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


# @app.get("/")
# async def root():
#     return {
#         "message": "Welcome to Black-Scholes Calculator API",
#         "docs": "/docs",
#         "version": app.version,
#     }


@app.get("/", status_code=200)
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return {"User": user}


app.include_router(api_router)

models.Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
