from flask import Flask
import mysql.connector
import random
import string

app = Flask(__name__)


def generate_short_code(length=7):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))

def create_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="password123",
        database="shortener_db"
    )

@app.route("/")
def home():
    return "URL Shortener API is running!"

if __name__ == "__main__":
    app.run(debug=True)
