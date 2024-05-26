from fastai.vision.all import *
import glob
from random import shuffle
import streamlit as st
import pathlib
from pathlib import Path
pathlib.PosixPath = pathlib.WindowsPath

# Theme
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

# Title
st.markdown("<h1 style='color:#ff0000;text-align:center;'>🕷️ SPIDER CLASSIFICATION 🕷️</h1>", unsafe_allow_html=True)

# Load model
path = Path()
learn_inf = load_learner(path/'vgg19_model_2.pkl', cpu=True)

def get_spider_info(spider_name):
    spider_info = {
        "black_widow": "แมงมุมแม่ม่ายดำมีพิษแรงและเป็นที่รู้จักกันดีในเรื่องของสีดำเงางามและลายเส้นสีแดงที่หน้าท้อง",
        "blue_tarantula": "แมงมุมทาลันทูลาน้ำเงินมีสีฟ้าสดใสทั่วร่างกาย มักพบในป่าฝนเขตร้อนและมีขนาดใหญ่",
        "bold_jumper": "แมงมุมกระโดดมีขนาดเล็ก มีความสามารถในการกระโดดได้ไกลและแม่นยำ มีตาที่ใหญ่ทำให้มองเห็นได้ดี",
        "brown_grass_spider": "แมงมุมแม่ม่ายน้ำตาลมีขนาดกลางถึงใหญ่ อาศัยอยู่ในสนามหญ้าและพื้นที่เปิดโล่ง มีลายสีน้ำตาลบนตัว",
        "brown_recluse_spider": "แมงมุมสันโดษสีน้ำตาลมีพิษแรง มีลักษณะเด่นที่ลายสีน้ำตาลรูปไวโอลินบนหลัง",
        "deinopis_spider": "แมงมุมหว่านแหมีความสามารถในการสร้างใยแหที่ใช้ในการจับเหยื่อ โดยจะยึดใยแหนี้ด้วยขาหน้า",
        "golden_orb_weaver": "แมงมุมใยทองท้องขนานมีลักษณะสีทองหรือสีเหลือง สร้างใยที่ใหญ่และแข็งแรง สามารถมองเห็นได้ง่าย",
        "hobo_spider": "แมงมุมเมาค้างมีพิษที่อาจทำให้เกิดแผลพุพอง มีสีเทาหรือสีน้ำตาล พบได้ในบ้านหรืออาคาร",
        "huntsman_spider": "แมงมุมบ้านขายาวมีขนาดใหญ่และขาที่ยาว อาศัยอยู่ในบ้านหรือพื้นที่เปิด มักพบในเขตร้อน",
        "ladybird_mimic_spider": "แมงมุมด้วงเต่ามีลักษณะคล้ายกับด้วงเต่า มีสีสันสดใส เช่น สีแดง สีดำ มีลายจุดบนหลัง",
        "peacock_spider": "แมงมุมนกยูงมีขนาดเล็ก มีสีสันสดใสและลวดลายที่สวยงาม คล้ายกับนกยูง พบได้ในออสเตรเลีย",
        "red_knee_tarantula": "แมงมุมทาลันทูลาเข่าแดงมีขนาดใหญ่ มีสีดำและมีแถบสีแดงที่ขา มักพบในเขตร้อน",
        "spiny_backed_orb_weaver": "แมงมุมชนิดนี้มีลักษณะเด่นที่มีหนามหรือแง่งบนหลัง มีสีสันสดใส เช่น สีแดง สีเหลือง หรือสีขาว",
        "white_knee_tarantula": "แมงมุมทาลันทูลาเข่าขาวมีขนาดใหญ่ มีสีดำและมีแถบสีขาวที่ขา พบได้ในอเมริกาใต้",
        "yellow_garden_spider": "แมงมุมสวนสีดำทองมีลักษณะสีดำและสีเหลืองสดใส สร้างใยขนาดใหญ่ในสวนหรือพื้นที่เปิด"
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
st.sidebar.markdown("<h3>Enter spider to classify</h3>", unsafe_allow_html=True)

# Image source selection
option = st.sidebar.radio('', ['Use a validation image', 'Use your own image'])
valid_images = glob.glob('SPIDER_DATASET/valid/*')
shuffle(valid_images)

if option == 'Use a validation image':
    st.sidebar.write('### Select a validation image')
    fname = st.sidebar.selectbox('', valid_images)
    img = PILImage.create(fname)
else:
    st.sidebar.write('### Select an image to upload')
    uploaded_file = st.sidebar.file_uploader('', type=['png', 'jpg', 'jpeg'], accept_multiple_files=False)
    if uploaded_file is not None:
        img = PILImage.create(uploaded_file)
    else:
        img = PILImage.create(valid_images[0])

# Infer
if img:
    predict(img, learn_inf)
