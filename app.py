import google.generativeai as genai 
import streamlit as st
from dotenv import load_dotenv #Google API Key'i gizlemek için
import os
from PIL import Image


load_dotenv() 
genai.configure(api_key = os.getenv('GOOGLE_API_KEY'))

def vision_model(input_text, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_text, image[0]])
    return response.text

def prepare_image(uploaded_file):
  if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    image_parts = [
            {
                "mime_type" : uploaded_file.type,
                "data" : bytes_data
            }
        ]
    return image_parts
  else:
    raise FileNotFoundError("No file uploaded...")
    

st.title("Diet Buddy")
age = st.slider("Age", 0, 100)
height = st.slider("Choose your height in cm: ", 50, 300)
gender = st.selectbox("Choose a gender", ["Male", "Female"])
kilo = st.slider("Choose you kilo", 20, 200)
m = height/100
bmi = kilo / m*m
input_text = f"""You are the nutritionist. I am {age} years old {gender} and {kilo} kilos and my body mass index is {bmi}.
                Calculate my daily intake calory amount and analyse the image. If the food in image is healthy tell me
                protein, carbonhydrate, fat, minerals of the food in image and
                add its calory for 100 grams to my daily intake calories and tell me remain calories.
                Also recommend me a healthy diet programme and exercise programme.
"""
uploaded_file = st.file_uploader("Choose an image...", type = ["jpg","jpeg","png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width = True)    
sub = st.button("Tell me calories")
if sub:
  prepared_image = prepare_image(uploaded_file)
  resp = vision_model(input_text, prepared_image)
  st.header("Response")
  st.write(resp)





    

