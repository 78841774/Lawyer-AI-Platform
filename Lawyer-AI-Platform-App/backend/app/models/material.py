from pydantic import BaseModel


class Material(BaseModel):
    material_id: str
    case_id: str
    filename: str
    material_type: str = "document"
    storage_path: str
    status: str = "uploaded"
