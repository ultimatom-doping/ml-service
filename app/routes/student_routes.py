from fastapi import APIRouter, HTTPException
from app.models.student import Student
from app.services.student_service import (
    get_all_students, get_student_by_id, create_student, update_student, delete_student
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

@router.put("/students/{student_id}")
async def modify_student(student_id: int, student: Student):
    success = await update_student(student_id, student.dict(by_alias=True))
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student updated successfully"}

@router.delete("/students/{student_id}")
async def remove_student(student_id: int):
    success = await delete_student(student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}
