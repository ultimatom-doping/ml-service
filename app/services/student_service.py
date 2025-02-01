from app.db.database import student_collection
from app.models.student import Student
from bson import ObjectId

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

# Öğrenciyi güncelle
async def update_student(student_id: int, data: dict):
    result = await student_collection.update_one(
        {"student_id": student_id}, {"$set": data}
    )
    return result.modified_count > 0

# Öğrenciyi sil
async def delete_student(student_id: int):
    result = await student_collection.delete_one({"student_id": student_id})
    return result.deleted_count > 0