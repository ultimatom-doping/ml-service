from fastapi import APIRouter, HTTPException
from app.models.student import Student, StudentUpdate
from app.services.student_service import (
    get_all_students, get_student_by_id, create_student, update_student, delete_student
)
from app.services.success_evaluator import (
    trigger_job
)

router = APIRouter()

@router.get("/students")
async def list_students():
    return await get_all_students()

@router.get("/students/{student_id}")
async def retrieve_student(student_id: int):
    student = await get_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.post("/students")
async def add_student(student: Student):
    student_id = await create_student(student)
    return {"id": student_id, "message": "Student created successfully"}

@router.put("/students/{student_id}", response_model=bool)
async def update_student_endpoint(student_id: int, student_update: StudentUpdate):
    result = await update_student(student_id, student_update)
    return True

@router.delete("/students/{student_id}")
async def remove_student(student_id: int):
    success = await delete_student(student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}

@router.post("/students/trigger")
async def trigger():
    success_df = await trigger_job()

    if success_df is not None:
        result = success_df.to_dict(orient="records")
        return result
    
    raise HTTPException(status_code=404, detail="Trigger failed")

# @router.get("/students/{student_id}/suggest-question/{subject_id}")
# async def fetch_suggested_question(student_id: int, subject_id: int):
#     return await get_suggested_question(student_id, subject_id)