import os
import google.generativeai as genai
from dotenv import load_dotenv

# .env 파일에서 API 키를 읽어옵니다.
load_dotenv()
api_key = os.getenv("AIzaSyC9lu1x0f2MPtjLHkfjqaKKlwF9zJMPF20")

# 제미나이 설정
genai.configure(api_key=api_key)

class AIService:
    @staticmethod
    def generate_naver_blog(title: str, user_input: str):
        """
        인사장님의 지적 수준과 똑같은 답변을 내놓는 블로그 생성 함수
        """
        # 모델 설정 (무료인 1.5-flash 사용)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # 인사장님이 원하시는 '복붙 가능 양식'을 위한 프롬프트
        prompt = f"""
        너는 네이버 블로그 마케팅 전문가이자 '컨텐츠메이커스튜디오'의 메인 AI야.
        사용자가 주는 주제와 키워드를 바탕으로 바로 복사해서 붙여넣기 좋은 포스팅을 작성해줘.

        [주제]: {title}
        [핵심 키워드]: {user_input}

        [작성 규칙]:
        1. 전체적인 말투는 친절하지만 지적인 '인스타사장님' 스타일로 작성할 것.
        2. 중간중간 이미지가 들어갈 위치에 반드시 [IMAGE_PLACEHOLDER: 이미지에 대한 상세 설명] 문구를 넣을 것.
           (예: [IMAGE_PLACEHOLDER: 트래킹화와 배낭이 놓여진 감성적인 현관 사진])
        3. [인사말] - [이미지1] - [본문1] - [이미지2] - [본문2] - [마무리] 순서로 구성할 것.
        4. 마지막에 관련 해시태그 5개를 달아줄 것.
        """

        try:
            response = model.generate_content(prompt)
            
            return response.text
        except Exception as e:
            return f"AI 생성 중 오류가 발생했습니다: {str(e)}"