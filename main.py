from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

class ProductCreate(BaseModel):
		name: str
		proteins: float
		fat: float
		carbs: float

@app.get("/products/{barcode}")
def get_product(barcode: str):
		resp = requests.get(
				f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json",
				params={"fields": "product_name,energy-kcal_100g,proteins_100g,fat_100g,carbohydrates_100g"},
				headers={"User-Agent": "ZALUPA-Cal/0.1 (vasya.com)"},
		)
		data = resp.json()
		
		if data["status"]:
				return data["product"]
		else:
				return {"found": False}

@app.post("/products")
def create_product(product: ProductCreate):
		return product
