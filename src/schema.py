from pydantic import BaseModel
from typing import List

class ModelInput(BaseModel):
    age: str = '20-24'
    budget: str = '1500-3000'
    effects: list = ['うるおい']
    skin_types: list = ['普通肌']
    aroma_types: list = ['フローラル系']

    
class ModelOutput(BaseModel):
    products_idx: List[str]
    products_percentages: List[float]
    