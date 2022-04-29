from app.pydantic_models import File_Model
from flask import current_app
from app.logger import logger
from flask_openapi3.models import Tag
from flask_jwt_extended import jwt_required
from app.views.blueprint import BlueprintApi

SECURITY = [{"jwt": []}]
TAG = Tag(name='File upload', description="Upload file from apllication data")

api_file = BlueprintApi('/file', __name__, abp_tags=[TAG], abp_security=SECURITY)


@api_file.post("/file")
@logger.catch
@jwt_required()
def file(form: File_Model):
    form.file.save(current_app.config["FILE_UPLOAD_PATH"] / form.file.filename)
    logger(f"file saved {form.file.filename}")
    return {"code": 0, "message": "file downloaded"}
