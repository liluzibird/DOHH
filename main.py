from flask import Flask, render_template
from supabase import create_client

# Replace with your actual Supabase project URL and anon public key
SUPABASE_URL = "https://qfzmwbippwnesxxshqgq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFmem13YmlwcHduZXN4eHNocWdxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzIwNDMxMjAsImV4cCI6MjA4NzYxOTEyMH0.dd6_5MmU6Tmb0phXKBc8_LwStQSLkR6vZR_T_9qyWiE"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

response = supabase.table("Classes").select("*").execute()

app = Flask(__name__)

'''
data = [
    {
        "ClassNum" : 32147,
        "CourseNum" : 3310,
        "ProfName" : "Yunsheng Wang",
        "ProfHours" : "Face-to-face in Room 8-9: Monday and Wednesday 10:30am-12:00pm, Virtual on Zoom (https://cpp.zoom.us/j/9756115722): Tuesday 11:00am-12:00pm or by appointment"
    },
    {
        "ClassNum" : 33535,
        "CourseNum" : 4080,
        "ProfName" : "Edwin Rodríguez",
        "ProfHours" : "TuTh 1:00pm – 3:00pm, by appointment"
    },
    {
        "ClassNum" : 33544,
        "CourseNum" : 4310,
        "ProfName" : "Tannaz Rezaei Damavandi",
        "ProfHours" : "MonWed: 1:00 - 2:30 PM. (in-person) and Thu : 9:00 - 10:00 AM (online via Zoom)  (Meeting ID: 432 425 2555, Passcode: CS_CalPoly) or by appointment. For Zoom meetings, to avoid long waiting , please make an appointment in advance."
    },
    {
        "ClassNum" : 32152,
        "CourseNum" : 4800,
        "ProfName" : "Yu Sun",
        "ProfHours" : "Tu/Th 11:15am-12:45pm; or email me for an appointment"
    },
]

'''

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
app.run()