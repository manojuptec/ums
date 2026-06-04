from fastapi import FastAPI
#pip install fastapi uvicorn
#pip install psycopg2-binary
from routers.UserRoutes import router as user_router

app = FastAPI(
    title="User API",
    description="This is a sample FastAPI with MVC structure",
    version="1.0.0"
)

app.include_router(user_router)
#uvicorn server:app --reload