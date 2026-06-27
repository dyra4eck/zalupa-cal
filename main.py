from fastapi import FastAPI
from pydantic import BaseModel
import requests
import psycopg
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

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
	conn = psycopg.connect(DATABASE_URL)
	with conn.cursor() as cur:
		cur.execute(
			"INSERT INTO products (name, proteins, fat, carbs) VALUES  (%s,%s,%s,%s) RETURNING id",
			(product.name, product.proteins, product.fat, product.carbs)
		)
		new_id = cur.fetchone()[0]
	conn.commit()
	conn.close()

	kcal = 4 * product.proteins + 9 * product.fat + 4 * product.carbs
	return {
		"id": new_id,
		"name": product.name,
		"proteins": product.proteins,
		"fat": product.fat,
		"carbs": product.carbs,
		"kcal": kcal,
	}

@app.get("/products")
def return_product():
	conn = psycopg.connect(DATABASE_URL)
	with conn.cursor() as cur:
		cur.execute("SELECT id, name, proteins, fat, carbs FROM products")
		rows = cur.fetchall()
	conn.close()

	result = []
	for row in rows:
		id, name, proteins, fat, carbs = row
		kcal = 4 * proteins + 9 * fat + 4 * carbs
		result.append({
			"id": id, "name": name,
			"proteins": proteins, "fat": fat, "carbs" : carbs,
			"kcal": kcal,
		})
	return result
