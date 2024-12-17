import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def analyze_with_gpt(extracted_text):
    """GPT-4 API를 사용하여 원재료명과 영양정보 추출"""
    prompt = f"아래 텍스트에서 '원재료명'과 '영양정보'를 JSON 형식으로 추출해 주세요:\n\n{extracted_text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message['content']

def get_diet_recommendation(user_input, pdf_data, df):
    """PDF 및 엑셀 데이터를 기반으로 GPT 식단 추천"""
    prompt = f"사용자 입력: {user_input}\nPDF 추천: {pdf_data}\n엑셀 추천: {df.to_dict()}\n식단을 추천해 주세요."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message['content']
