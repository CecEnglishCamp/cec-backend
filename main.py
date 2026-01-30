from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# CORS 설정 (프론트엔드와 통신 가능)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://cec-english-camp.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 더미 학생 데이터
STUDENTS_DB = {
    "minjae@cec.com": {
        "name": "Kim Min-jae",
        "password": "demo123",
        "camp": "A",
        "level": "G01-G10",
        "joined": "2025-01-15",
        "progress": 30,
        "scores": {"G01": 85, "G02": 90, "G03": 78}
    },
    "jiwon@cec.com": {
        "name": "Lee Ji-won",
        "password": "demo123",
        "camp": "B",
        "level": "G11-G20",
        "joined": "2025-01-10",
        "progress": 45,
        "scores": {"G01": 92, "G02": 88, "G03": 95}
    },
    "sujin@cec.com": {
        "name": "Park Su-jin",
        "password": "demo123",
        "camp": "C",
        "level": "G21-G30",
        "joined": "2025-01-05",
        "progress": 60,
        "scores": {"G01": 87, "G02": 91, "G03": 89}
    }
}

# 요청 모델
class LoginRequest(BaseModel):
    email: str
    password: str

# 로그인 API
@app.post("/api/login")
async def login(request: LoginRequest):
    student = STUDENTS_DB.get(request.email)
    
    if not student or student["password"] != request.password:
        return {"success": False, "message": "Invalid credentials"}
    
    return {
        "success": True,
        "name": student["name"],
        "camp": student["camp"],
        "level": student["level"],
        "joined": student["joined"],
        "progress": student["progress"],
        "scores": student["scores"]
    }

# 학생 정보 API
@app.get("/api/student/{email}")
async def get_student(email: str):
    student = STUDENTS_DB.get(email)
    
    if not student:
        return {"success": False, "message": "Student not found"}
    
    return {
        "success": True,
        "name": student["name"],
        "camp": student["camp"],
        "level": student["level"],
        "joined": student["joined"],
        "progress": student["progress"],
        "scores": student["scores"]
    }

# 테스트 엔드포인트
@app.get("/")
async def root():
    return {"message": "CEC English Camp Backend API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)