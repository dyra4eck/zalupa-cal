import psycopg

conn = psycopg.connect("postgresql://postgres:postgres@localhost:5432/cal")
with conn.cursor() as cur:
		cur.execute("SELECT version();")
		print(cur.fetchone())
		cur.execute("SELECT current_user, current_database();")
		print(cur.fetchone())

		cur.execute("CREATE TABLE IF NOT EXISTS products (id SERIAL PRIMARY KEY, name TEXT NOT NULL, proteins REAL NOT NULL, fat REAL NOT NULL, carbs REAL NOT NULL);")
conn.commit()
conn.close()
