import sqlite3
import pandas as pd

#backup script for pathing

    #BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    #db_path = os.path.join(BASE_DIR, "../db/magazines.db")

    #with sqlite3.connect(db_path) as conn:
    #     print("Connected to database:", db_path)

#path to db
db_path = "../db/lesson.db"

#step 2, read data from SQL, join line_items to products
sql = """
SELECT
    li.line_item_id,
    li.quantity,
    li.product_id,
    p.product_name,
    p.price
FROM line_items AS li
JOIN products   AS p
  ON li.product_id = p.product_id
"""
with sqlite3.connect(db_path) as conn:
    df = pd.read_sql_query(sql, conn)

#step 3, print first 5 rows to verify
print("Step 3 — first 5 rows from JOIN:")
print(df.head(), "\n")

#step 4, add total column (= quantity x price)
df["total"] = df["quantity"] * df["price"]
print("Step 4 — after adding total column:")
print(df.head(), "\n")

#step 5, group by product_id and aggregate by item count, total sum & product name
summary = (
    df.groupby("product_id")
      .agg(
          line_item_id=("line_item_id", "count"),
          total=("total", "sum"),
          product_name=("product_name", "first")
      )
      .reset_index()
)

print("Step 5 — grouped/aggregated (first 5 rows):")
print(summary.head(), "\n")

#step 6, sort df by product name
summary = summary.sort_values(by="product_name")

#step 7, write to CSV in assignment8 folder
summary.to_csv("order_summary.csv", index=False)
print("Step 7 — wrote CSV to order_summary.csv in assignment8/")
