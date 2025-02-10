import random
import string
import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("referral_codes.db")
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS referrals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    referral_code TEXT UNIQUE
)
""")
conn.commit()

def generate_referral_code(name=""):
    """Generates a unique referral code using the user's name or random letters."""
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    if name:
        code = name.upper()[:4] + random_part  # Take first 4 letters of name + random part
    else:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))  # Fully random code
    return code

def save_referral_code(name=""):
    """Saves a unique referral code to the database."""
    while True:
        code = generate_referral_code(name)
        try:
            cursor.execute("INSERT INTO referrals (name, referral_code) VALUES (?, ?)", (name, code))
            conn.commit()
            print(f"Referral code generated: {code}")
            return code
        except sqlite3.IntegrityError:
            # If code already exists, retry with a new one
            continue

# Example Usage
if __name__ == "__main__":
    user_name = input("Enter user name (or leave blank for random code): ").strip()
    referral_code = save_referral_code(user_name)
