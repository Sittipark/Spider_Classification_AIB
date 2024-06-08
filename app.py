from fastai.vision.all import *
import glob
from random import shuffle
import streamlit as st
import pathlib
from pathlib import Path
pathlib.PosixPath = pathlib.WindowsPath

# Set custom CSS for dark theme
st.markdown("""
    <style>
    body {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    .stButton>button {
        background-color: #ffffff;
        color: #ffffff;
        border: 1px solid #ffffff;
    }
    .stRadio>div {
        background-color: #ffffff;
        color: #ffffff;
        border: 1px solid #ffffff;
        border-radius: 10px;
        padding: 10px;
    }
    .stSidebar .stSelectbox, .stSidebar .stFileUploader {
        background-color: #ffffff;
        color: #ffffff;
        border: 1px solid #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# Set app title with a red spider logo
st.markdown("<h1 style='color:#ff0000;text-align:center;'>🕷️ SPIDER CLASSIFICATION 🕷️</h1>", unsafe_allow_html=True)

# Load model
path = Path()
learn_inf = load_learner(path/'vgg19_model_2.pkl', cpu=True)

def get_spider_info(spider_name):
    spider_info = {
        "black_widow": "แมงมุมแม่ม่ายดำ (Black Widow) เป็นเแมงมุมที่มีพิษร้ายทำให้ถึงตายได้* พบกระจายได้ทั่วโลก ตัวสีดำขาเรียวยาวมีลายจุดแดงบนท้อง",
        "blue_tarantula": "แมงมุมทาลันทูลาน้ำเงิน (Blue Tarantula) มีพิษ แต่ไม่ร้ายแรงมาก ตัวสีน้ำเงินมีขนาดใหญ่ขาค่อนข้างหนา มักพบในป่าฝนเขตร้อนและมีขนาดใหญ่",
        "bold_jumper": "แมงมุมกระโดด (Bold Jumper) มีพิษ แต่ไม่ร้ายแรงมาก พบได้ทั่วโลก มีขนาดตัวเล็ก ขาเรียวยาว มีลายจุดบนตัว สามารถกระโดดได้ไกล",
        "brown_grass_spider": "แมงมุมแม่ม่ายน้ำตาล (Brown Grass Spider) มีพิษ แต่ไม่ร้ายแรงมาก มีขนาดกลางถึงใหญ่ และมีลายสีน้ำตาลบนตัว",
        "brown_recluse_spider": "แมงมุมสันโดษสีน้ำตาล (Brown Recluse Spider) มีพิษร้ายแรงถึงชีวิต* มีลักษณะเด่นคือลายสีน้ำตาลรูปไวโอลินบนหลัง",
        "deinopis_spider": "แมงมุมหว่านแห (Deinopis Spider) มีพิษ แต่ไม่ร้ายแรงมาก มีรูปร่างแปลกมีขาที่ยาว และดวงตาใหญ่โต",
        "golden_orb_weaver": "แมงมุมใยทองท้องขนาน (Golden Orb Weaver) มีพิษ แต่ไม่ร้ายแรงมาก ตัวใหญ่สีเหลืองทอง พบได้ทั่วโลก",
        "hobo_spider": "แมงมุมเมาค้าง (Hobo Spider) มีพิษร้ายแรงอาจทำให้เกิดแผลพุพอง* มีสีเทาหรือสีน้ำตาล พบได้ในบ้านหรืออาคาร",
        "huntsman_spider": "แมงมุมบ้านขายาวหรือแมงมุมพเนจร (Huntsman Spider) มีพิษ แต่ไม่ร้ายแรงต่อมนุษย์ มีขนาดใหญ่และขาที่ยาว อาศัยอยู่ในบ้านหรือพื้นที่เปิด มักพบในเขตร้อน เป็นตัวกำจัดแมลงสาบชั้นดี",
        "ladybird_mimic_spider": "แมงมุมด้วงเต่า (Ladybird Mimic Spider) ไม่มีพิษ มีลักษณะคล้ายกับด้วงเต่า มีสีสันสีแดงสดใส มีลายจุดดำบนหลัง",
        "peacock_spider": "แมงมุมนกยูง (Peacock Spider) มีพิษ แต่ไม่ร้ายแรง มีขนาดเล็ก มีสีสันสดใสและลวดลายที่สวยงามคล้ายกับนกยูง พบได้ในออสเตรเลีย",
        "red_knee_tarantula": "แมงมุมทาลันทูลาเข่าแดง (Red Knee Tarantula) มีพิษ แต่ไม่ร้ายแรงมาก อาจเกิดอาการปวดบวม มีขนาดใหญ่ มีสีดำและมีแถบสีแดงที่ขา มักพบในเขตร้อน",
        "spiny_backed_orb_weaver": "แมงมุมชนิดนี้มีพิษ แต่ไม่ร้ายแรง มีลักษณะเด่นที่มีหนามหรือแง่งบนหลัง มีสีสันสดใส พบได้ในอเมริกาเหนือ",
        "white_knee_tarantula": "แมงมุมทาลันทูลาเข่าขาว (White Knee Tarantula) มีพิษร้ายแรง มีขนาดใหญ่ มีสีดำและมีแถบสีขาวที่ขา พบได้ในอเมริกาใต้",
        "yellow_garden_spider": "แมงมุมสวนสีดำทอง (Yellow Garden Spider) มีพิษ แต่ไม่ร้ายแรงมาก มีลักษณะสีดำและสีเหลืองสดใส สร้างใยขนาดใหญ่ในสวนหรือพื้นที่เปิด"
    }
    return spider_info.get(spider_name, "ข้อมูลไม่พบ")

def predict(img, learn):
    # Make prediction
    pred, pred_idx, pred_prob = learn_inf.predict(img)
    # Get spider information
    spider_info = get_spider_info(pred)
    # Display the prediction
    st.success(f"This is {pred} with the probability of {pred_prob[pred_idx]*100:.02f}%")
    st.info(spider_info)
    # Display the test image
    st.image(img, use_column_width=True)

##################################
# Sidebar
##################################
# Sidebar title
st.sidebar.markdown("<h3>Enter spider to classify</h3>", unsafe_allow_html = True)

# Image source selection
option = st.sidebar.radio('', ['Use a validation image', 'Use your own image'])
valid_images = glob.glob('SPIDER_DATASET/valid/*/*')
shuffle(valid_images)

if option == 'Use a validation image':
    st.sidebar.write('### Select a validation image')
    fname = st.sidebar.selectbox('', valid_images)
    img = PILImage.create(fname)
else:
    st.sidebar.write('### Select an image to upload')
    uploaded_file = st.sidebar.file_uploader('', type = ['png', 'jpg', 'jpeg'], accept_multiple_files = False)
    if uploaded_file is not None:
        img = PILImage.create(uploaded_file)
    else:
        img = PILImage.create(valid_images[0])

# Infer
if img:
    predict(img, learn_inf)
