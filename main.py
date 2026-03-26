from flask import Flask, request, jsonify, render_template
from supabase import create_client

# Replace with your actual Supabase project URL and anon public key
SUPABASE_URL = "https://qfzmwbippwnesxxshqgq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFmem13YmlwcHduZXN4eHNocWdxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzIwNDMxMjAsImV4cCI6MjA4NzYxOTEyMH0.dd6_5MmU6Tmb0phXKBc8_LwStQSLkR6vZR_T_9qyWiE"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

response = supabase.table("Classes").select("*").execute()


app = Flask(__name__, template_folder="templates", static_folder="static")

# --- Helpers ---
def recompute_ranks_for_class(class_num):
    # fetch fresh rows for this class
    resp = supabase.table("Classes").select("id, upvotes, downvotes, inserted_at").eq("ClassNum", class_num).execute()
    rows = resp.data or []

    def key_fn(r):
        score = (r.get("upvotes") or 0) - (r.get("downvotes") or 0)
        ins = r.get("inserted_at") or ""
        return (-score, ins)

    rows_sorted = sorted(rows, key=key_fn)
    rank = 1
    for r in rows_sorted:
        supabase.table("Classes").update({"rank": rank}).eq("id", r["id"]).execute()
        rank += 1
    return True

# --- Routes ---
@app.route("/")
def start_index():
    return render_template("index.html")

@app.route("/welcome")
def welcome():
    return "<html><body><h1>Welcome to Directory of Hours and Help (DOHH)!</h1></body></html>"

@app.route("/search/<classSelection>")
def search_Office_Hours(classSelection):
    # Always return JSON; handle errors gracefully so frontend gets a valid response
    try:
        class_num = int(classSelection)
    except Exception:
        return jsonify([])

    try:
        # recompute ranks to ensure ordering
        recompute_ranks_for_class(class_num)

        resp = supabase.table("Classes") \
            .select("*") \
            .eq("ClassNum", class_num) \
            .order("rank", desc=False) \
            .execute()

        data = resp.data or []
        return jsonify(data)
    except Exception as e:
        # log on server and return empty list to frontend
        print("Search error:", e)
        return jsonify([])

@app.route("/suggest", methods=["POST"])
def suggest():
    try:
        data = request.get_json()
        payload = {
            "ClassNum": int(data.get("ClassNum")),
            "CourseNum": data.get("CourseNum"),
            "ProfName": data.get("ProfName"),
            "ProfHours": data.get("ProfHours"),
            "upvotes": 0,
            "downvotes": 0
        }
        resp = supabase.table("Classes").insert(payload).execute()
        created = resp.data[0]
        recompute_ranks_for_class(created["ClassNum"])
        fetch = supabase.table("Classes").select("*").eq("id", created["id"]).single().execute()
        return jsonify(fetch.data)
    except Exception as e:
        print("Suggest error:", e)
        return jsonify({"error":"bad request"}), 400

@app.route("/vote", methods=["POST"])
def vote():
    try:
        data = request.get_json()
        row_id = data.get("id")
        vote_type = data.get("vote")
        if not row_id or vote_type not in ("up","down"):
            return jsonify({"error":"bad request"}), 400

        resp = supabase.table("Classes").select("upvotes,downvotes,ClassNum").eq("id", row_id).single().execute()
        if not resp.data:
            return jsonify({"error":"not found"}), 404

        up = resp.data.get("upvotes") or 0
        down = resp.data.get("downvotes") or 0
        class_num = resp.data.get("ClassNum")

        if vote_type == "up":
            up += 1
        else:
            down += 1

        supabase.table("Classes").update({"upvotes": up, "downvotes": down}).eq("id", row_id).execute()
        recompute_ranks_for_class(class_num)
        new_row = supabase.table("Classes").select("upvotes,downvotes,rank").eq("id", row_id).single().execute()
        return jsonify(new_row.data)
    except Exception as e:
        print("Vote error:", e)
        return jsonify({"error":"internal"}), 500

#app.run(host = "127.0.0.1", port=42069)
#app.run()
if __name__ == '__main__':
    app.run()
#print(F_Office_Hours(1122))

