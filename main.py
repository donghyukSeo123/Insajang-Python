from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from ai_service import AIService

app = FastAPI()

@app.post("/generate", response_model=schemas.ContentResponse)
def create_content(request: schemas.ContentCreate, db: Session = Depends(get_db)):
    # 1. AI 서비스 호출 (두뇌 빌리기)
    ai_text = AIService.generate_blog_post(request.title, request.user_input)
    
    # 2. DB 저장 (창고에 넣기)
    db_content = models.Content(
        project_id=request.project_id,
        title=request.title,
        body=ai_text,
        type="NAVER_BLOG",
        status="DRAFT"
    )
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    
    return {"content_id": db_content.content_id, "generated_text": ai_text}