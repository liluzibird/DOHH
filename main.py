from flask import Flask, render_template
from supabase import create_client

# Replace with your actual Supabase project URL and anon public key
SUPABASE_URL = "https://qfzmwbippwnesxxshqgq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFmem13YmlwcHduZXN4eHNocWdxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzIwNDMxMjAsImV4cCI6MjA4NzYxOTEyMH0.dd6_5MmU6Tmb0phXKBc8_LwStQSLkR6vZR_T_9qyWiE"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

response = supabase.table("Classes").select("*").execute()

app = Flask(__name__)



@app.route("/")
def start_index():
    return render_template("index.html")

@app.route("/welcome")
def welcome():
    return "<html><body><h1>Welcome to Directory of Hours and Help (DOHH)!\n</h1></body></html>"


@app.route("/search/<classSelection>")
def search_Office_Hours(classSelection):
    classSelection = int(classSelection)

    response = supabase.table("Classes") \
        .select("*") \
        .eq("ClassNum", classSelection) \
        .execute()

    result = response.data

    return result  # or jsonify(result) if using Flask

for row in response.data:
    print(row)

#print(search_Office_Hours(1122))

#app.run(host = "127.0.0.1", port=42069)
#app.run()
if __name__ == '__main__':
   app.run()