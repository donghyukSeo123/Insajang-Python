from fastapi import FastAPI
from pydantic import BaseModel
from ai_service import AIService  # 분리한 서비스 불러오기

app = FastAPI()

class ContentRequest(BaseModel):
    title: str
    user_input: str
    content_type: str

@app.post("/generate-content")
async def create_content(request: ContentRequest):
    print("--- [인사장님, 데이터 들어왔습니다!] ---")
    print(f"전체 객체: {request}")
    print(f"제목: {request.title}")
    print(f"입력값: {request.user_input}")
    print(f"타입: {request.content_type}")
    print("---------------------------------------")
    result = AIService.generate_naver_blog(request.title, request.user_input, request.content_type)
    return result