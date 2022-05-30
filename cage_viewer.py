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
import google
import time

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=".streamlit/secrets.toml"


credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"])

client = storage.Client(credentials=credentials)
bucket_name = 'cells_and_cages'
bucket = client.bucket(bucket_name)

@st.cache(hash_funcs={google.cloud.storage.client.Client: np.array})
def get_image(bucket, file_path):
    blb = bucket.blob(file_path)
    bytes = blb.download_as_bytes()
    image = Image.open(io.BytesIO(bytes))
    return np.array(image)/65535



def main():
    

    st.sidebar.image("/Users/Husseine/Documents/GitHub/MiNOS_cage_viewer/logo-minos-pdf.001_transp.png", use_column_width=True)
    header = st.container()
    viewer= st.container()

    image, image_rgb = st.columns((2,2))
    row_number, col_number = st.columns((1,1))
    r, viewer_image, rr = st.columns(3)

    st.sidebar.markdown('<h1>Our approach</h1>', unsafe_allow_html=True)
    st.sidebar.markdown('<p>Minos Biosciences is on the path to BRIDGE MOLECULAR and CELL BIOLOGY in a manner never achieved before that will, in turn, allow scientists to uncover the full picture of cell diversity and dynamics.</p>', unsafe_allow_html=True)
    st.sidebar.markdown('<h2>Single-cell revolution</h2>', unsafe_allow_html=True)
    st.sidebar.markdown('<p>Single-cell analysis is key to tackle cell diversity, and it has become in recent years an irreplaceable tool in all fields of biological and medical research. Current single-cell technologies however, despite their remarkable progress, address only fragments of the puzzle – whereas combining multiple modes of single-cell analysis is essential to unlock the complexity of biology and reveal the complete picture.</p>', unsafe_allow_html=True)
    st.sidebar.markdown('<h2>Minos solution</h2>', unsafe_allow_html=True)
    st.sidebar.markdown('<p>The single-cell solution developed by minos offers the unique ability to directly combine sequencing-based multi-omic analysis and image-based phenotypic analysis at single-cell resolution. This is enabled using a breakthrough microfluidics concept to isolate cells combined with innovative approaches in imaging, molecular biology and also bioinformatics.It will provide highly accurate insights into complex cell populations and their dynamics, opening up unique perspectives in a vast array of fundamental and translational research areas, as well as precision medicine therapeutics and diagnostics.</p>', unsafe_allow_html=True)
    st.sidebar.markdown('<h2>Minos impact</h2>', unsafe_allow_html=True)
    st.sidebar.markdown("<p>Minos solution has the potential to tremendously<strong>&nbsp;</strong><b>impact major healthcare fields,</b>&nbsp;such as:</p><ul><li><b>Cancer disease</b><strong>:</strong> connecting genetic &amp; non-genetic factors, plasticity and cell environment will be essential to understand tumour evolution and drug resistance, to design better and more personalized therapeutic strategies.</li><li><b>Autoimmune disorders:</b> unravelling the complex role of immune cells at the multi-omic and phenotypic levels will result in the development of better treatments.</li><li><b>Infectious disease:&nbsp;</b>correlating host-pathogen interaction to genetic and epigenetic variations will allow elucidating infection and proliferation mechanisms to improve therapy and prevention.</li></ul>", unsafe_allow_html=True)


    with header:
        st.title("Welcome to the Minos Biosciences cage viewer application!")
        st.markdown('This app displays cages from any chosen chip')



    with viewer:
        st.header("Cage viewer")
        
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


    
        

        filename= "DATASET_CHIP_" +chip_number_choice+ "/DATASET_CHIP" + chip_number_choice + "_" + row_number_choice + "_" + col_number_choice + ".tif"

        with r:
            st.write(' ')
        with viewer_image:
            st.image(get_image(bucket=bucket,file_path=filename))
        with rr:
            st.write(' ') 
    #st.markdown('Cage displayed: Chip %s\nRow number: %s\nColumn number: %s'%(chip_number_choice, row_number_choice, col_number_choice) )
main()