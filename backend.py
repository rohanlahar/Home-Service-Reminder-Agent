from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq
from datetime import datetime, timedelta
from pathlib import Path

app = Flask(__name__)
CORS(app)

# =========================================================
# GROQ API KEY
# =========================================================
# IMPORTANT: This key was shared in chat. For real deployment,
# revoke it and create a new key after testing.
GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)
MODEL = "openai/gpt-oss-120b"


# =========================================================
# SERVE THE FRONTEND
# =========================================================
@app.route("/")
def home():
    return send_from_directory(Path(__file__).parent, "frontend.html")


# =========================================================
# MAINTENANCE CALCULATIONS
# =========================================================
def parse_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def calculate_status(asset):
    last_service = parse_date(asset.get("lastService"))
    if not last_service:
        return {
            "status": "unknown",
            "days": None,
            "nextService": None
        }

    try:
        interval = int(asset.get("interval", 30))
    except (ValueError, TypeError):
        interval = 30

    next_service = last_service + timedelta(days=interval)
    today = datetime.now().date()
    days = (next_service - today).days

    if days < 0:
        status = "overdue"
        remaining = abs(days)
    elif days == 0:
        status = "today"
        remaining = 0
    elif days <= 7:
        status = "upcoming"
        remaining = days
    else:
        status = "healthy"
        remaining = days

    return {
        "status": status,
        "days": remaining,
        "nextService": next_service.isoformat()
    }


def prepare_assets(assets):
    result = []

    for asset in assets:
        calc = calculate_status(asset)

        result.append({
            "id": asset.get("id"),
            "name": asset.get("name"),
            "category": asset.get("category"),
            "lastService": asset.get("lastService"),
            "interval": asset.get("interval"),
            "status": calc["status"],
            "days": calc["days"],
            "nextService": calc["nextService"]
        })

    return result


# =========================================================
# AI INSTRUCTIONS
# =========================================================
SYSTEM_PROMPT = """
You are HomeCare AI, an intelligent home maintenance assistant.

The Python backend calculates the maintenance dates. You must use
those calculations and must NOT invent dates.

STATUS DEFINITIONS:
- overdue = service date has already passed
- today = service is due today
- upcoming = service is due within 7 days
- healthy = service is more than 7 days away

RULES:
1. Never invent an asset.
2. Never invent a service date.
3. Never call an upcoming task overdue.
4. If the user asks "What is overdue?", mention ONLY assets with status "overdue".
5. If there are no overdue assets, clearly say there are no overdue maintenance tasks.
6. If the user asks what is due this week, mention assets with status "today" or "upcoming".
7. If asked about a specific asset, focus on that asset.
8. Give useful general maintenance advice when appropriate.
9. Never claim to have physically inspected anything.
10. For dangerous electrical, gas, fire, or structural problems, recommend a qualified professional.
11. Keep answers concise and easy to understand.
"""


# =========================================================
# CHAT API
# =========================================================
@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "success": False,
                "error": "Invalid request."
            }), 400

        question = str(data.get("message", "")).strip()
        assets = data.get("assets", [])

        if not question:
            return jsonify({
                "success": False,
                "error": "Please enter a question."
            }), 400

        if not isinstance(assets, list):
            assets = []

        processed = prepare_assets(assets)

        context = f"""
TODAY:
{datetime.now().date().isoformat()}

CALCULATED USER ASSETS:
{processed}
"""

        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": context + "\n\nUSER QUESTION:\n" + question
                }
            ],
            temperature=0.2,
            max_completion_tokens=800,
            include_reasoning=False
        )

        answer = completion.choices[0].message.content

        return jsonify({
            "success": True,
            "answer": answer,
            "assets": processed
        })

    except Exception as error:
        print("ERROR:", repr(error))

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


# =========================================================
# STATUS API
# =========================================================
@app.route("/api/status", methods=["POST"])
def status():
    try:
        data = request.get_json(silent=True) or {}
        assets = data.get("assets", [])

        return jsonify({
            "success": True,
            "assets": prepare_assets(assets)
        })

    except Exception as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


# =========================================================
# HEALTH CHECK
# =========================================================
@app.route("/api/health")
def health():
    return jsonify({
        "status": "online",
        "service": "HomeCare AI",
        "ai": "Groq",
        "model": MODEL
    })


# =========================================================
# START
# =========================================================
if __name__ == "__main__":
    print("=" * 55)
    print("       HOMECARE AI - BACKEND")
    print("=" * 55)
    print("Server: http://127.0.0.1:5000")
    print("Open this address in Chrome after starting the server.")
    print("=" * 55)

    app.run(host="127.0.0.1", port=5000, debug=True)
