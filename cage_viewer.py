import streamlit as st
import cv2
from google.oauth2 import service_account
from google.cloud import storage
from IPython.display import Image
import pandas as pd
import os
from PIL import Image
import io
import numpy as np

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=".streamlit/secrets.toml"


credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"])

client = storage.Client(credentials=credentials)
bucket_name = 'cells_and_cages'
bucket = client.bucket(bucket_name)

def get_image(bucket, file_path):
    blb = bucket.blob(file_path)
    bytes = blb.download_as_bytes()
    image = Image.open(io.BytesIO(bytes))
    return np.array(image)/65025




header = st.container()
dataset_explanation = st.container()
viewer= st.container()


image, image_rgb = st.columns((2,2))
row_number, col_number = st.columns((1,1))
r, viewer_image, rr = st.columns(3)
#example_image = cv2.imread('DATASET_CHIP71_1_7.tif')
#example_image_rgb = cv2.imread('DATASET_CHIP71composite_1_7.tif')
#example_image_rgb = cv2.cvtColor(example_image_rgb, cv2.COLOR_BGR2RGB)


with header:
    st.title("Welcome to the Minos Biosciences cage viewer application!")
    st.text('This app displays cages from any chosen chip')

#with dataset_explanation:
#    st.title("Chips")
#    st.text('These images...')

with viewer:
    st.title("Cage viewer")
    #st.text("Here you can choose a chip then a cage to see what it looks like.")
    
    #with image:
    #    st.image(example_image)

    #with image_rgb:
    #    st.image(example_image_rgb)
    
    chip_number_choice= st.selectbox(
     'Select the chip you want to display',
     ('58', '66', '67', '69', '70', '71'))
    #st.write('You selected:', chip_number_choice)

    with col_number:
        if chip_number_choice in ['58','66', '67', '69', '70']:

            col_number_choice = st.selectbox(
            'Select the column number of the cage you want to display',
            tuple(str(i) for i in range(15)))

        else:
            col_number_choice = st.selectbox(
            'Select the column number of the cage you want to display',
            tuple(str(i) for i in range(29)))




    with row_number:
        if int(col_number_choice)%2==0:
            row_number_choice = st.selectbox(
                'Select the row number of the cage you want to display',
                tuple(str(i) for i in range(25)))
        else:
            row_number_choice = st.selectbox(
                'Select the row number of the cage you want to display',
                tuple(str(i) for i in range(24)))
st.text('Cage displayed: Chip %s \t Row number: %s \t Column number: %s'%(chip_number_choice, row_number_choice, col_number_choice) )
    

filename= "DATASET_CHIP_" +chip_number_choice+ "/DATASET_CHIP" + chip_number_choice + "_" + row_number_choice + "_" + col_number_choice + ".tif"
#print("L'image à afficher est %s"%(filename))

with r:
    st.write(' ')
with viewer_image:
    st.image(get_image(bucket=bucket,file_path=filename))
with rr:
    st.write(' ') 
