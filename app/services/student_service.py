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
    """
    Convert the Pydantic model to a dict, then rename the 'subject_id' key to '_subject_id'.
    Finally, insert into MongoDB.
    """
    doc = student.dict(by_alias=True)
    
    # If you want the key "subject_id" to become "_subject_id" in Mongo:
    if "subject_id" in doc:
        doc["_subject_id"] = doc.pop("subject_id")
    
    result = await student_collection.insert_one(doc)
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

# async def get_suggested_question(student_id, subject_id):
#     student = await student_collection.find_one({"student_id": student_id})
#     if student is None:
#         raise HTTPException(status_code=404, detail="Student not found")
    
#     subject_scores = student["subject_scores"]
#     if subject_id not in subject_scores:
#         raise HTTPException(status_code=404, detail="Subject not found")

#     subject_score = subject_scores[subject_id]

#     question = await question_collection.find_one(
#         {"subject_id": subject_id, "difficulty": {"$gte": subject_score}}
#     )

#     return question