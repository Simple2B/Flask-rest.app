from flask_openapi3 import APIBlueprint
import os


class BlueprintApi(APIBlueprint):
    def __init__(self, *args, **kwargs):

        if "url_prefix" not in kwargs:
            kwargs["url_prefix"] = os.environ.get("API_ROOT", "")

        super().__init__(*args, **kwargs)
