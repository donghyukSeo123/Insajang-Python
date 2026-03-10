import os
import re
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi.responses import JSONResponse

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

class AIService:
    @staticmethod
    def generate_naver_blog(title: str, user_input: str, content_type: str):
        # 1. 모델 설정 (사장님 목록에 있는 최신 플래시 모델)
        model = genai.GenerativeModel('models/gemini-flash-latest')

        # 2. 타입별 설정 분기
        if content_type == "naver_blog":
            role = "네이버 블로그 마케팅 전문가"
            specific_rule = "글의 서론 뒤에 한 번, 결론 앞에 한 번, 총 두 번 [IMAGE_HERE] 문구를 반드시 포함해줘."
        elif content_type == "instagram":
            role = "인스타그램 감성 브랜딩 전문가"
            specific_rule = "짧고 강렬한 문구, 이모지 활용, 하단에 연관 해시태그 10개를 달아줘."
        else:
            role = "컨텐츠 제작 전문가"
            specific_rule = "가독성 좋게 HTML 태그를 섞어서 작성해줘."

        # 3. 프롬프트 구성 (단순화하여 AI의 실수를 줄임)
        prompt = f"""
        너는 {role}야
        
        주제: {title}
        핵심 키워드: {user_input}

        [작성 지침]
        1. 말투는 지적이고 친절한 '인스타사장님' 스타일로 작성할 것., Ai가아닌것처럼 실제 블로그작성처럼, 글은적당히 길게
        2. {specific_rule}
        3. <h3>, <p>, <strong> 태그를 사용하여 리액트에서 바로 렌더링 가능한 HTML 형식으로 출력할 것.
        4. 출력은 반드시 아래 형식을 지켜:
            [TITLE]지어준 제목[/TITLE]
            [CONTENT]본문 내용...[/CONTENT]
        """

        try:
            response = model.generate_content(prompt)
            raw_response = response.text

            # 2. 제목(Title)과 본문(Content) 추출
            gen_title_match = re.search(r'\[TITLE\](.*?)\[/TITLE\]', raw_response, re.DOTALL)
            gen_content_match = re.search(r'\[CONTENT\](.*?)\[/CONTENT\]', raw_response, re.DOTALL)

            gen_title = gen_title_match.group(1).strip() if gen_title_match else title
            gen_content = gen_content_match.group(1).strip() if gen_content_match else raw_response

            # 4. 🔥 치트키: AI가 남긴 [IMAGE_HERE]를 진짜 HTML 이미지 태그로 치환!
            image_html = f"""
            <div style="text-align:center; margin:30px 0;">
              <img src="https://loremflickr.com/800/500/{title},architecture" style="width:100%; max-width:700px; border-radius:15px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);" alt="{title}" />
              <p style="color:#888; font-size:13px; margin-top:10px;">✨ 컨텐츠메이커스튜디오 감성 큐레이션</p>
            </div>
            """

            # AI가 혹시 표식을 빼먹었을 경우를 대비해 처리
            if "[IMAGE_HERE]" in gen_content:
                final_content = gen_content.replace("[IMAGE_HERE]", image_html)
            else:
                # 표식을 안 남겼으면 본문 중간쯤에 강제로 삽입
                split_text = gen_content.split("</h3>")
                if len(split_text) > 1:
                    final_content = split_text[0] + "</h3>" + image_html + "</h3>".join(split_text[1:])
                else:
                    final_content = image_html + gen_content
            print("--- [결과데이터!] ---")
            print({
                "generated_title": gen_title,
                "generated_text": final_content
            } )
            print("---------------------------------------")
            return JSONResponse(content={
                    "generated_title": gen_title,
                    "generated_text": final_content
                })

        except Exception as e:
            # 🚀 에러 발생 시에도 리액트와 스프링이 깨지지 않게 딕셔너리로 응답!
            return {
                "generated_title": "생성 실패",
                "generated_text": f"<h3>AI 생성 중 오류가 발생했습니다.</h3><p>{str(e)}</p>",
                "error": True
            }