import os
import sqlite3
from dotenv import load_dotenv
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__)

# --- CORS CONFIGURATION ---
# We must explicitly allow 'X-API-KEY' because custom headers trigger preflight.
ALLOWED_ORIGINS = [
    "https://danielleetstephen.com",
    "https://api.danielleetstephen.com",  # Include subdomain just in case
    "http://localhost:5173"
]

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": ALLOWED_ORIGINS,
            "allow_headers": ["Content-Type", "X-API-KEY"],
            "methods": ["GET", "POST", "OPTIONS"],
            "max_age": 600  # Cache preflight for 10 minutes
        }
    }
)

# --- CONFIG & AUTH ---
DB_NAME = "rsvp.db"
API_KEY = os.environ.get("RSVP_API_KEY")
ADMIN_USER = os.environ.get("ADMIN_USER")
ADMIN_PASS_HASH = os.environ.get("ADMIN_PASS_HASH")

limiter = Limiter(get_remote_address, app=app, default_limits=["10 per minute"])
auth = HTTPBasicAuth()


@auth.verify_password
def verify(username, password):
    if username == ADMIN_USER and check_password_hash(ADMIN_PASS_HASH, password):
        return username
    return None


# --- HELPERS ---
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def safe_text(value, max_len=255):
    return value.strip()[:max_len] if value else None


# --- MIDDLEWARE ---
@app.before_request
def require_api_key():
    # 1. Always allow OPTIONS (Preflight) to bypass key check
    if request.method == "OPTIONS":
        return '', 204

    # 2. Protect only the RSVP saving route
    if request.endpoint == "save_rsvp":
        key = request.headers.get("X-API-KEY")
        if not key or key != API_KEY:
            return jsonify({"success": False, "message": "Unauthorized: Invalid API Key"}), 401


# --- ROUTES ---
@app.route("/api/rsvp", methods=["POST"])
@limiter.limit("5 per minute")
def save_rsvp():
    try:
        data = request.get_json(force=True)
        email = safe_text(data.get("email"), 150)

        if not email:
            return jsonify({"success": False, "message": "Adresse e-mail requise"}), 400

        participation = safe_text(data.get("participation"), 20)
        record = {
            "first_name": safe_text(data.get("firstName"), 100),
            "last_name": safe_text(data.get("lastName"), 100),
            "email": email,
            "phone": safe_text(data.get("phone"), 50),
            "participation": participation,
            "relation": safe_text(data.get("relation"), 50),
            "message": safe_text(data.get("message"), 500),
        }

        conn = get_db()
        cur = conn.cursor()

        existing = cur.execute("SELECT * FROM rsvp WHERE email = ?", (email,)).fetchone()
        if existing:
            cur.execute("""
                        UPDATE rsvp
                        SET participation = ?,
                            message       = ?
                        WHERE email = ?
                        """, (record["participation"], record["message"], email))
            msg = f"Votre réponse a été mise à jour ({participation})"
        else:
            cur.execute("""
                        INSERT INTO rsvp (first_name, last_name, email, phone, participation, relation, message)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (record["first_name"], record["last_name"], record["email"],
                              record["phone"], record["participation"], record["relation"], record["message"]))
            msg = "Succès"

        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": msg}), 201

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route("/report", methods=["GET"])
@auth.login_required
def report():
    conn = get_db()
    rows = conn.execute("SELECT * FROM rsvp ORDER BY created_at DESC").fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])


@app.route("/")
def index():
    return "RSVP API is running"


if __name__ == "__main__":
    app.run(debug=True)