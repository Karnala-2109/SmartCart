import sqlite3

conn = sqlite3.connect("smartcart.db")

updates = {
    "gayathri": 1,
    "smartcartuser": 3,
    "karnala": 4
}

for username, customer_id in updates.items():
    conn.execute(
        "UPDATE users SET customer_id = ? WHERE username = ?",
        (customer_id, username)
    )

conn.commit()

rows = conn.execute(
    "SELECT id, username, role, customer_id FROM users"
).fetchall()

print("\nUpdated users:")
for row in rows:
    print(row)

conn.close()