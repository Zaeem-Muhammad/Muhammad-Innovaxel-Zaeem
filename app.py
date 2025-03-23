from flask import Flask
import mysql.connector

app = Flask(__name__)


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
