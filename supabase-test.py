from supabase import create_client

# Replace with your actual Supabase project URL and anon public key
SUPABASE_URL = "https://qfzmwbippwnesxxshqgq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFmem13YmlwcHduZXN4eHNocWdxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzIwNDMxMjAsImV4cCI6MjA4NzYxOTEyMH0.dd6_5MmU6Tmb0phXKBc8_LwStQSLkR6vZR_T_9qyWiE"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)



# Insert one row
response = supabase.table("Classes").insert([
    {
        "ClassNum": 33535,
        "CourseNum": 4080,
        "ProfName": "Edwin Rodríguez",
        "ProfHours": "TuTh 1:00pm – 3:00pm, by appointment"
    },
    {
        "ClassNum": 33544,
        "CourseNum": 4310,
        "ProfName": "Tannaz Rezaei Damavandi",
        "ProfHours": "MonWed: 1:00 - 2:30 PM. (in-person) and Thu : 9:00 - 10:00 AM (online via Zoom)  (Meeting ID: 432 425 2555, Passcode: CS_CalPoly) or by appointment. For Zoom meetings, to avoid long waiting , please make an appointment in advance."
    },
    {
        "ClassNum": 32152,
        "CourseNum": 4800,
        "ProfName": "Yu Sun",
        "ProfHours": "Tu/Th 11:15am-12:45pm; or email me for an appointment"
    }

    
]).execute()

print(response.data)


response = supabase.table("Classes").select("*").execute()

for row in response.data:
    print(row)