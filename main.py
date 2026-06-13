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

products = {}

@app.post("/products")
def create_product(product: ProductCreate):
	new_id = max(products, default=0) + 1
	kcal = 4 * product.proteins + 9 * product.fat + 4 * product.carbs
	record = {
		"id": new_id,
		"name": product.name,
		"proteins": product.proteins,
		"fat": product.fat,
		"carbs": product.carbs,
		"kcal": kcal,
	}
	products[new_id] = record
	return record

@app.get("/products")
def return_product():
	return list(products.values())
