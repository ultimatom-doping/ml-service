from fastapi import APIRouter, HTTPException
from app.models.question import Question, QuestionUpdate
from app.services.question_service import (
    get_all_questions,
    get_question_by_id,
    create_question,
    update_question,
    delete_question,
)

router = APIRouter()

@router.get("/questions")
async def list_questions():
    return await get_all_questions()

@router.get("/questions/{question_id}")
async def retrieve_question(question_id: int):
    question = await get_question_by_id(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.post("/questions")
async def add_question(question: Question):
    question_id = await create_question(question)
    return {"id": question_id, "message": "Question created successfully"}

@router.put("/questions/{question_id}", response_model=bool)
async def modify_question(question_id: int, question_update: QuestionUpdate):
    result = await update_question(question_id, question_update)
    return result

@router.delete("/questions/{question_id}")
async def remove_question(question_id: int):
    success = await delete_question(question_id)
    if not success:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"message": "Question deleted successfully"}
