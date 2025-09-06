import sqlite3

# find directory of this script
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# db_path = os.path.join(BASE_DIR, "../db/magazines.db")

# with sqlite3.connect(db_path) as conn:
#     print("Connected to database:", db_path)

#path to db
db_path = "../db/magazines.db"

#attempt connection
try:
    conn = sqlite3.connect(db_path)
    print("Database created and connected successfully.")
    
#conn error print
except sqlite3.Error as e:
    print("Error while connecting to database:", e)
    
#conn close print
finally:
    if conn:
        conn.close()
        print("Connection closed.")

#connect to db
with sqlite3.connect(db_path) as conn:
    print("Connected to database.")
    conn.execute("PRAGMA foreign_keys = 1")  #assure valid foreign keys
    cur = conn.cursor()

    #publishers(one)- magazines(many)
    try:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS publishers (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT    NOT NULL UNIQUE
        );
        """)
        print("OK: publishers")
    except sqlite3.Error as e:
        print("Error creating publishers:", e)

    #magazines, foreign keys to publishers(id)
    try:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS magazines (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            name         TEXT    NOT NULL UNIQUE,
            publisher_id INTEGER NOT NULL,
            FOREIGN KEY (publisher_id) REFERENCES publishers(id) ON DELETE CASCADE
        );
        """)
        print("OK: magazines")
    except sqlite3.Error as e:
        print("Error creating magazines:", e)

    #subscribers, name & address required
    try:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            name    TEXT NOT NULL,
            address TEXT NOT NULL
        );
        """)
        print("OK: subscribers")
    except sqlite3.Error as e:
        print("Error creating subscribers:", e)

    #subscriptions, many-to-many between subscribers and magazines
    try:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            subscriber_id   INTEGER NOT NULL,
            magazine_id     INTEGER NOT NULL,
            expiration_date TEXT    NOT NULL,
            PRIMARY KEY (subscriber_id, magazine_id),
            FOREIGN KEY (subscriber_id) REFERENCES subscribers(id) ON DELETE CASCADE,
            FOREIGN KEY (magazine_id)   REFERENCES magazines(id)   ON DELETE CASCADE
        );
        """)
        print("OK: subscriptions")
    except sqlite3.Error as e:
        print("Error creating subscriptions:", e)

#task 3, 
    #helper functions
    
    #retrieve single row
    def get_row_id(sql_select, params):
        #return first column of first row, or None
        cur.execute(sql_select, params)
        row = cur.fetchone()
        return row[0] if row else None
    
    #create publisher
    def create_publisher(name: str) -> int | None:
        try:
            pid = get_row_id("SELECT id FROM publishers WHERE name = ?", (name,))
            if pid is not None:
                return pid
            cur.execute("INSERT INTO publishers(name) VALUES (?)", (name,))
            return cur.lastrowid
        except sqlite3.Error as e:
            print("create_publisher error:", e)
            return None

    #create mag
    def create_magazine(name: str, publisher_name: str) -> int | None:
        try:
            #ensure publisher exists
            pid = create_publisher(publisher_name)
            if pid is None:
                return None
            mid = get_row_id("SELECT id FROM magazines WHERE name = ?", (name,))
            if mid is not None:
                return mid
            cur.execute(
                "INSERT INTO magazines(name, publisher_id) VALUES (?, ?)",
                (name, pid),
            )
            return cur.lastrowid
        except sqlite3.IntegrityError as e:
            print("create_magazine integrity error:", e)
            return get_row_id("SELECT id FROM magazines WHERE name = ?", (name,))
        except sqlite3.Error as e:
            print("create_magazine error:", e)
            return None

    #create subscriber
    def create_subscriber(name: str, address: str) -> int | None:
        """Dedup by BOTH (name, address) since those columns are not UNIQUE."""
        try:
            sid = get_row_id(
                "SELECT id FROM subscribers WHERE name = ? AND address = ?",
                (name, address),
            )
            if sid is not None:
                return sid
            cur.execute(
                "INSERT INTO subscribers(name, address) VALUES (?, ?)",
                (name, address),
            )
            return cur.lastrowid
        except sqlite3.Error as e:
            print("create_subscriber error:", e)
            return None
        
    #create subscription
    def create_subscription(subscriber_name: str, address: str,
                            magazine_name: str, publisher_name: str,
                            expiration_date: str) -> None:
        #join table insert. composite primary keys prevents duplicates
        try:
            sid = create_subscriber(subscriber_name, address)
            mid = create_magazine(magazine_name, publisher_name)
            if sid is None or mid is None:
                print("subscription skipped (missing sid/mid)")
                return
            #INSERT OR IGNORE to keep idempotent runs clean
            cur.execute(
                "INSERT OR IGNORE INTO subscriptions(subscriber_id, magazine_id, expiration_date) "
                "VALUES (?, ?, ?)",
                (sid, mid, expiration_date),
            )
        except sqlite3.Error as e:
            print("create_subscription error:", e)

    #populate tables with sample data

    #publishers + magazines
    create_magazine("Tech Monthly",        "North Star Media")
    create_magazine("Home & Garden Now",   "North Star Media")
    create_magazine("World Soccer Weekly", "Global Sports Press")
    create_magazine("City Eats",           "Fork & Knife Co")
    create_magazine("Mountain Trails",     "Global Sports Press")

    #subscribers
    s1 = create_subscriber("Alice Johnson",  "101 Maple St, Durham, NC")
    s2 = create_subscriber("Bob Smith",      "22 Pine Ave, Raleigh, NC")
    s3 = create_subscriber("Carol Martinez", "808 Elm Rd, Chapel Hill, NC")

    #subscriptions
    create_subscription("Alice Johnson",  "101 Maple St, Durham, NC",
                        "Tech Monthly", "North Star Media",        "2026-01-31")
    create_subscription("Alice Johnson",  "101 Maple St, Durham, NC",
                        "City Eats",     "Fork & Knife Co",        "2025-12-31")
    create_subscription("Bob Smith",      "22 Pine Ave, Raleigh, NC",
                        "World Soccer Weekly", "Global Sports Press", "2025-11-15")
    create_subscription("Carol Martinez", "808 Elm Rd, Chapel Hill, NC",
                        "Mountain Trails", "Global Sports Press",  "2026-03-01")
    create_subscription("Bob Smith",      "500 Oak Blvd, Cary, NC",
                        "Home & Garden Now", "North Star Media",   "2025-10-01")

    #commit all inserts
    try:
        conn.commit()
        print("Data inserted (safe to run multiple times).")
    except sqlite3.Error as e:
        print("Commit error:", e)

print("All done.")

#task 4, search queries
try:
    #retrieve all info from subscribers
    print("\nAll subscribers:")
    cur.execute("SELECT * FROM subscribers;")
    for row in cur.fetchall():
        print(row)
    
    #retrieve all magazines, sorted by name
    print("\nMagazines sorted by name:")
    cur.execute("SELECT * FROM magazines ORDER BY name;")
    for row in cur.fetchall():
        print(row)
        
    #Find mags, North Star Media, 
    print("\nMagazines for publisher 'North Star Media':")
    cur.execute("""
        SELECT magazines.id, magazines.name, publishers.name
        FROM magazines
        JOIN publishers ON magazines.publisher_id = publishers.id
        WHERE publishers.name = 'North Star Media';
    """)
    
    #add all, print
    for row in cur.fetchall():
        print(row)

except sqlite3.Error as e:
    print("Query error:", e)
