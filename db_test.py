import psycopg

conn = psycopg.connect("postgresql://postgres:postgres@localhost:5432/cal")
with conn.cursor() as cur:
		cur.execute("SELECT version();")
		print(cur.fetchone())
conn.close
