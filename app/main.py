from fastapi import FastAPI
from app.routes.student_routes import router as student_router
from app.routes.question_routes import router as question_router

app = FastAPI()

# Router'ları dahil et
app.include_router(student_router, prefix="/api", tags=["students"])
app.include_router(question_router, prefix="/api", tags=["questions"])

@app.get("/")
async def root():
    return {"message": "ML Service is running!!"}
