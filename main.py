import os
from flask import Flask, request, jsonify, render_template
from supabase import create_client

app = Flask(__name__, template_folder="templates", static_folder="static")

# --- Supabase setup ---
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# --- Routes ---
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/welcome")
def welcome():
    return "<html><body><h1>Welcome to Directory of Hours and Help (DOHH)!</h1></body></html>"


@app.route("/search/<classSelection>")
def search_office_hours(classSelection):
    if supabase is None:
        return jsonify({"error": "Server configuration missing"}), 500

    try:
        class_num = int(classSelection)
    except Exception:
        return jsonify([])

    try:
        resp = supabase.rpc("get_class_results", {
            "p_classnum": class_num
        }).execute()

        return jsonify(resp.data or [])
    except Exception as e:
        print("Search error:", repr(e))
        return jsonify([])


@app.route("/suggest", methods=["POST"])
def suggest():
    if supabase is None:
        return jsonify({"error": "Server configuration missing"}), 500

    try:
        data = request.get_json() or {}

        class_num = int(data.get("ClassNum"))
        course_num = str(data.get("CourseNum", "")).strip()
        prof_name = str(data.get("ProfName", "")).strip()
        prof_hours = str(data.get("ProfHours", "")).strip()

        if not course_num or not prof_name or not prof_hours:
            return jsonify({"error": "All fields are required."}), 400

        resp = supabase.rpc("submit_suggestion", {
            "p_classnum": class_num,
            "p_coursenum": course_num,
            "p_profname": prof_name,
            "p_profhours": prof_hours
        }).execute()

        result = resp.data
        if not result:
            return jsonify({"error": "Could not create suggestion."}), 400

        return jsonify(result)

    except Exception as e:
        print("Suggest error:", repr(e))
        return jsonify({"error": str(e)}), 400


@app.route("/vote", methods=["POST"])
def vote():
    if supabase is None:
        return jsonify({"error": "Server configuration missing"}), 500

    try:
        data = request.get_json() or {}

        row_id = str(data.get("id", "")).strip()
        vote_type = str(data.get("vote", "")).strip()
        voter_token = str(data.get("voter_token", "")).strip()

        if not row_id or vote_type not in ("up", "down") or not voter_token:
            return jsonify({"error": "Bad request"}), 400

        resp = supabase.rpc("cast_vote", {
            "p_class_id": row_id,
            "p_voter_token": voter_token,
            "p_vote_type": vote_type
        }).execute()

        result = resp.data
        if not result:
            return jsonify({"error": "Vote failed"}), 500

        return jsonify(result)

    except Exception as e:
        import traceback
        traceback.print_exc()
        print("Vote error:", repr(e))
        return jsonify({"error": str(e)}), 500


# --- Local dev only ---
if __name__ == "__main__":
    app.run(debug=True)