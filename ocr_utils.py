import requests
import json
import uuid
import time
from config import CLOVA_API_URL, CLOVA_SECRET_KEY

def extract_text_with_clova(image_path):
    """네이버 CLOVA OCR API로 텍스트 추출"""
    request_json = {
        'images': [{'format': 'jpg', 'name': 'uploaded_image'}],
        'requestId': str(uuid.uuid4()),
        'version': 'V2',
        'timestamp': int(round(time.time() * 1000))
    }
    payload = {'message': json.dumps(request_json).encode('UTF-8')}
    files = [('file', open(image_path, 'rb'))]
    headers = {'X-OCR-SECRET': CLOVA_SECRET_KEY}

    response = requests.post(CLOVA_API_URL, headers=headers, data=payload, files=files)
    if response.status_code == 200:
        return ' '.join([field['inferText'] for field in response.json()['images'][0]['fields']])
    else:
        return f"OCR 요청 실패: {response.status_code}"
