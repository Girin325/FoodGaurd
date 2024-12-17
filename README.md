# FoodGaurd

Smart Chatbot Planner for Health and Allergies

<p align="center">
<img width="70%" src="https://github.com/user-attachments/assets/dde39933-b8bd-4406-b66c-8e1bbcc8b4f3">
<img width="70%" src="https://github.com/user-attachments/assets/966a089b-6377-406d-a977-68793a6bd56d">

-------

## :wrench: Installation

We used the __Python 3.10.1__

    conda create -n foodgaurd python=3.10.1
    conda activate foodgaurd
    git clone https://github.com/Girin325/FoodGaurd
    cd FoodGaurd
    pip install -r requirements.txt
    pip install pdfplumber openpyxl

If an error occurs, proceed with the installation as is, and then reinstall the following:

    pip install langchain==0.0.10 openai==0.28.0

--------

## :star2: Preparation

You will __need the Naver CLOVA OCR api key__, __Naver CLOVA OCR api url__, __OpenAI(Chat-gpt) api key__!!

You can obtain them from the links below.

Naver CLOVA OCR API: <https://www.ncloud.com/product/aiService/ocr>

OpenAI API: <https://platform.openai.com/docs/guides/text-generation>

-------

## :arrow_forward: Running Code

You can try running the code below.

    streamlit run main.py

When the window opens, you can select or enter your age, height, weight, allergies, conditions, and religion from the sidebar on the left.


After that, you can upload an image to the central chatbot and choose the type of the uploaded image.

