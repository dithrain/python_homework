import sqlite3

def main():
    #db pathing
    conn = sqlite3.connect("../db/lesson.db", isolation_level="IMMEDIATE")
    conn.execute("PRAGMA foreign_keys = 1")
    cur = conn.cursor()

#---task1; complex joins with aggregation
    
    #join orders table with line_items and products tables, group by order_id, calculate total price per order
    cur.execute("""
        SELECT o.order_id,
               SUM(li.quantity * p.price) AS total_price
        FROM orders o
        JOIN line_items li ON li.order_id = o.order_id
        JOIN products p    ON p.product_id = li.product_id
        GROUP BY o.order_id
        ORDER BY o.order_id
        LIMIT 5;
    """)

    #print order_id and total price per row
    for order_id, total_price in cur.fetchall():
        print(f"order_id: {order_id} | total_price: {total_price:.2f}")

#---task 2, subqueries and filtering
    
    #average order price per customer (subquery & LEFT JOIN)
    cur.execute("""
    SELECT c.customer_name,
           AVG(sq.total_price) AS average_total_price
    FROM customers c
    LEFT JOIN (
        SELECT o.customer_id AS customer_id_b,
               SUM(li.quantity * p.price) AS total_price
        FROM orders o
        JOIN line_items li ON li.order_id = o.order_id
        JOIN products p    ON p.product_id = li.product_id
        GROUP BY o.order_id, o.customer_id
    ) AS sq
    ON c.customer_id = sq.customer_id_b
    GROUP BY c.customer_id, c.customer_name
    ORDER BY c.customer_id;
""")

    for customer_name, avg_total in cur.fetchall():
        avg_display = "None" if avg_total is None else f"{avg_total:.2f}"
        print(f"customer: {customer_name} | average_total_price: {avg_display}")

#---task 3, insert transaction
    #look up perez and sons
    cur.execute("SELECT customer_id FROM customers WHERE customer_name = ?", ("Perez and Sons",))
    cust_row = cur.fetchone()
    if not cust_row:
        raise RuntimeError("Customer 'Perez and Sons' not found")
    cust_id = cust_row[0]
    
    #look up miranda harris
    cur.execute("SELECT employee_id FROM employees WHERE first_name=? AND last_name=?", ("Miranda", "Harris"))
    emp_row = cur.fetchone()
    if not emp_row:
        raise RuntimeError("Employee 'Miranda Harris' not found")
    emp_id = emp_row[0]

    #transaction; create order + 5 line items
    try:
        conn.execute("BEGIN")

        #create order and get order_id
        cur.execute("""
            INSERT INTO orders (customer_id, employee_id, date)
            VALUES (?, ?, DATE('now'))
            RETURNING order_id;
        """, (cust_id, emp_id))
        order_id = cur.fetchone()[0]

        #insert 10 of each of the 5 LEAST expensive products
        cur.execute("""
            INSERT INTO line_items (order_id, product_id, quantity)
            SELECT ?, p.product_id, 10
            FROM products p
            ORDER BY p.price ASC
            LIMIT 5;
        """, (order_id,))

        conn.commit()
    except Exception:
        conn.rollback()
        raise

    #verify; print line_item_id, quantity, product_name for that order
    cur.execute("""
        SELECT li.line_item_id, li.quantity, p.product_name
        FROM line_items li
        JOIN products p ON p.product_id = li.product_id
        WHERE li.order_id = ?
        ORDER BY li.line_item_id;
    """, (order_id,))
    for li_id, qty, pname in cur.fetchall():
        print(f"line_item_id: {li_id} | qty: {qty} | product: {pname}")
    print(f"Created order_id: {order_id}")

#---task 4, employees with more than 5 orders (JOIN, GROUP BY & HAVING)
    cur.execute("""
        SELECT
          e.employee_id,
          e.first_name,
          e.last_name,
          COUNT(o.order_id) AS order_count
        FROM employees e
        JOIN orders o ON o.employee_id = e.employee_id
        GROUP BY e.employee_id, e.first_name, e.last_name
        HAVING COUNT(o.order_id) > 5
        ORDER BY order_count DESC, e.employee_id;
    """)
    for emp_id, first, last, cnt in cur.fetchall():
        print(f"employee_id: {emp_id} | name: {first} {last} | order_count: {cnt}")

    conn.close()

if __name__ == "__main__":
    main()