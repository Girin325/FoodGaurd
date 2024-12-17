import streamlit as st
from ocr_utils import extract_text_with_clova
from gpt_utils import analyze_with_gpt, get_diet_recommendation
from data_utils import extract_disease_data_from_pdf, load_excel_data
from config import CLOVA_API_URL, CLOVA_SECRET_KEY, PDF_PATH, EXCEL_FILE_PATH
from PIL import Image

# 데이터 로드
pdf_data = extract_disease_data_from_pdf(PDF_PATH)
df = load_excel_data(EXCEL_FILE_PATH)

# 사용자 입력 UI
st.title("건강 및 알러지를 위한 스마트 식단 챗봇")

st.sidebar.title("사용자 정보")
user_info = {
    "age": st.sidebar.number_input("나이:", min_value=0, max_value=120, step=1),
    "height": st.sidebar.number_input("키 (cm):", min_value=50, max_value=250, step=1),
    "weight": st.sidebar.number_input("몸무게 (kg):", min_value=10, max_value=200, step=1),
    "allergies": st.sidebar.multiselect(
        "알레르기:",
        options=["없음 (None)", "우유 (Milk)", "달걀 (Eggs)", "땅콩 (Peanuts)", "견과류 (Tree Nuts)", "밀 (Wheat)", "대두 (Soy)", "갑각류 (Shellfish)", "어패류 (Fish)", "참깨 (Sesame)", "옥수수 (Corn)"]
    ),
    "condition": st.sidebar.multiselect(
        "질환:",
        options = ["없음 (None)","갑상선 기능 저하증 (Hypothyroidism)", "갑상선 기능 항진증 (Hyperthyroidism)", "갑상선염 (Thyroiditis)", "갑상선 질환 (Thyroid Disease)",
                 "결석증 (Kidney Stones)", "결핵 (Tuberculosis)", "관절염 (Arthritis)", "고급당뇨병 (Advanced Diabetes)", "고지혈증 (Hyperlipidemia)", "고혈압 (Hypertension)",
                 "골다공증 (Osteoporosis)", "대장염 (Colitis)", "만성 피로 증후군 (Chronic Fatigue Syndrome)", "만성 폐쇄성 폐질환 (COPD)", "방광염 (Cystitis)", "부종 (Edema)",
                 "비타민 D 결핍증 (Vitamin D Deficiency)", "빈혈 (Anemia)", "소화기 질환 (Digestive Disorders)", "소화불량 (Indigestion)", "심장 마비 후 회복 (Post-Heart Attack)",
                 "심장병 (Heart Disease)", "식도염 (Esophagitis)", "식욕 부진 (Anorexia)", "신경계 질환 (Neurological Disorders)", "신경병증 (Neuropathy)", "신경성 폭식증 (Binge Eating Disorder)",
                 "신경전달물질 불균형 (Neurotransmitter Imbalance)", "신부전 (Kidney Failure)", "시각 장애 (Visual Impairment)", "알레르기 (Allergy)", "알츠하이머병 (Alzheimer's Disease)",
                 "알코올 의존증 (Alcohol Dependence)", "아밀로이드증 (Amyloidosis)", "아토피 피부염 (Atopic Dermatitis)", "역류성 식도염 (GERD)", "우울증 (Depression)", "위염 (Gastritis)",
                 "위염 및 소화성 궤양 (Gastric Ulcer)", "유당불내증 (Lactose Intolerance)", "자가 면역 질환 (Autoimmune Disease)", "자폐 스펙트럼 장애 (ASD)", "장내 세균총 불균형 (Gut Microbiome Imbalance)",
                 "전립선 질환 (Prostate Disease)", "체중 감소 (Weight Loss)", "체중 관리 (Weight Management)", "비만 (Weight Gain)", "척수 손상 (Spinal Cord Injury)", "테니스/골프 엘보 (Tennis/Golf Elbow)",
                 "탈모 (Hair Loss)", "편두통 (Migraine)", "피부질환 (Skin Disorders)", "황반변성 (Macular Degeneration)", "헬리코박터 파일로리 감염 (H. Pylori Infection)"]
    ),
    "religion": st.sidebar.selectbox(
        "종교",
        options=["None(제한 없음)", "Islam", "Judaism", "Hinduism"]
    ),
}

# 사용자 상태 정보 요약
st.sidebar.subheader("사용자 정보 요약")
for key, value in user_info.items():
    st.sidebar.write(f"{key.capitalize()}: {value if value else 'Not specified'}")

uploaded_image = st.file_uploader("성분표 이미지를 업로드하세요", type=["png", "jpg", "jpeg"])

food_type = st.radio(
    "식품 유형을 선택하세요:",
    options=["주식(밥, 면류 등)", "반찬류(김치, 젓갈 등)", "간식(과자, 초콜릿 등)", "음료(탄산음료, 주스 등)", "가공식품(예: 통조림, 냉동식품 등)", "건강식품(예: 영양제, 프로틴 바, 다이어트 식품 등)", "기타"]
)

if food_type == "기타":
    custom_food_type = st.text_input("기타 유형을 입력하세요:")
    if custom_food_type:
        food_type = custom_food_type

if uploaded_image:
    image = Image.open(uploaded_image)
    image_path = "/tmp/uploaded_image.jpg"
    image.save(image_path)
    st.image(image, caption="업로드된 이미지", use_column_width=True)

    if st.button("CLOVA OCR 실행"):
        ocr_text = extract_text_with_clova(image_path)
        st.session_state["ocr_text"] = ocr_text

    if "ocr_text" in st.session_state:
        st.text_area("OCR 결과", st.session_state["ocr_text"])

        if st.button("GPT로 분석"):
            gpt_result = analyze_with_gpt(st.session_state["ocr_text"])
            st.session_state["gpt_result"] = gpt_result

    if "gpt_result" in st.session_state:
        st.text_area("GPT 결과", st.session_state["gpt_result"])
        if st.button("식단 추천"):
            recommendation = get_diet_recommendation(st.session_state["gpt_result"], pdf_data, df)
            st.text_area("식단 추천 결과", recommendation)
