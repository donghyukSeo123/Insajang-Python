from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DB 연결 주소 (사용자명, 비밀번호, 호스트, DB이름을 본인 설정에 맞게 수정하세요)
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost:5432/insajang"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# DB 세션 가져오기 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()