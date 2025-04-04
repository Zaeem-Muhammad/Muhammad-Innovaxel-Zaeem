from flask import Flask
from flask import request, jsonify
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


@app.route("/shorten", methods=["POST"])
def create_short_url():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "URL is required"}), 400

    short_code = generate_short_code()
    conn = create_db_connection()
    cursor = conn.cursor()

    insert_query = "INSERT INTO urls (original_url, short_code) VALUES (%s, %s)"
    cursor.execute(insert_query, (data["url"], short_code))
    conn.commit()

    cursor.close()
    conn.close()
    return jsonify({"short_code": short_code, "url": data["url"]}), 201


@app.route("/shorten/<string:short_code>", methods=["GET"])
def get_original_url(short_code):
    conn = create_db_connection()
    cursor = conn.cursor()
    query = "SELECT original_url FROM urls WHERE short_code = %s"
    cursor.execute(query, (short_code,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row:
        return jsonify({"url": row[0]}), 200
    return jsonify({"error": "Short code not found"}), 404



if __name__ == "__main__":
    app.run(debug=True)
