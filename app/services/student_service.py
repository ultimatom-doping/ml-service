from app.db.database import student_collection
from app.models.student import Student, StudentUpdate
from bson import ObjectId

from fastapi import HTTPException

def serialize_document(doc):
    doc['_id'] = str(doc['_id'])
    return doc

# Tüm öğrencileri getir
async def get_all_students():
    students = await student_collection.find().to_list(length=None)
    return [serialize_document(student) for student in students]

async def get_student_by_id(student_id: int):
    student = await student_collection.find_one({"student_id": student_id})
    if student:
        return serialize_document(student)
    return None

# Yeni bir öğrenci ekle
async def create_student(student: Student):
    result = await student_collection.insert_one(student.dict(by_alias=True))
    return str(result.inserted_id)

async def update_student(student_id: int, data: StudentUpdate):
    update_data = {}
    
    # subject_scores'u işle
    if data.subject_scores:
        for subject, score in data.subject_scores.items():
            if score is not None:
                update_data[f"subject_scores.{subject}"] = score

    if not update_data:
        raise HTTPException(status_code=400, detail="No valid update data provided")
    
    result = await student_collection.update_one(
        {"student_id": student_id}, {"$set": update_data}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return True

# Öğrenciyi sil
async def delete_student(student_id: int):
    result = await student_collection.delete_one({"student_id": student_id})
    return result.deleted_count > 0