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
import matplotlib.pyplot as plt
import shutil

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=".streamlit/secrets.toml"


credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"])

client = storage.Client(credentials=credentials)
bucket_name = 'cells_and_cages'
bucket = client.bucket(bucket_name)
image_width = 350
max_width = 80
padding_top = 10
padding_bottom = 1000
padding_left = 10
padding_right = 10

@st.cache(hash_funcs={google.cloud.storage.client.Client: np.array})
def get_image(bucket, file_path,ang=0, div=65535):
    blb = bucket.blob(file_path)
    bytes = blb.download_as_bytes()
    image = Image.open(io.BytesIO(bytes))
    #st.image(rotateImage(np.array(image)/div, ang))
    return rotateImage(np.array(image)/div, ang)

from matplotlib.patches import Rectangle

#@st.cache()
def show_cage_pos_on_chip(img, df, cage_id,chip_number, linewidth=1.5, save=False):
  fig, ax = plt.subplots()
  fig.set_figheight(15)
  fig.set_figwidth(15)
  ax.imshow(img,cmap='gray')
  try:
    xmin = df[df['Cage_ID']==cage_id].iloc[0,1]
    ymin = df[df['Cage_ID']==cage_id].iloc[0,3]
  except:
    raise ValueError("Cage indice out of bounds") 
  plt.gca().add_patch(Rectangle((ymin,xmin),288,288,linewidth=linewidth,edgecolor='r',facecolor='#3EABBD', alpha=0.2))
  plt.text(ymin+70, xmin-50, cage_id, color='white', fontsize=7)
  plt.axis('off')
  st.pyplot(fig)
  #if save:
  #  plt.savefig("chip%s_box_around_cage_%s.png"%(chip_number, cage_id), bbox_inches='tight', pad_inches = 0, dpi=fig.dpi)
  #return "chip%s_box_around_cage_%s.png"%(chip_number, cage_id)




#@st.cache(hash_funcs={google.cloud.storage.client.Client: pd.DataFrame})
st.cache()
def gcp_csv_to_df(bucket, file_path):
    blob = bucket.blob(file_path)
    data = blob.download_as_string()
    df = pd.read_excel(io.BytesIO(data))
    #print(f'Pulled down file from bucket {bucket_name}, file name: {file_path}')
    return df

def rotateImage(image, angle):
  if len(image.shape)==2:
    row,col = image.shape
  elif len(image.shape)==3:
    row,col,chan = image.shape
  else:
    print('Invalid image shape')
  
  center=tuple(np.array([row,col])/2)
  rot_mat = cv2.getRotationMatrix2D(center,angle,1.0)
  new_image = cv2.warpAffine(image, rot_mat, (col,row))
  return new_image




def main():
    header = st.container()
    viewer= st.container()
  
    row_number, col_number = st.columns((1,1))
    viewer_image, composite_image = st.columns((1,1))
    metric1,metric2,metric3 = st.columns((1,1,1))



    hide_streamlit_style = """
            <style>
            #MainMenu {
            visibility: visible;
            }

            footer:before{
                content: 'Copyright @2022 Minos Biosciences' ;
                color: #3EAABD;
                display: block;
                position: relative;
            }                
            </style>
            """
    modify_container_padding ="""
        <style>
            .appview-container .main .block-container{{
            padding-bottom: {padding_bottom}px;}}
        </style>
        """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    #st.markdown(modify_container_padding, unsafe_allow_html=True)

    st.sidebar.video('https://www.youtube.com/watch?v=KqDEuwkvSus')
    st.sidebar.image("images/logo-minos-pdf.001_transp.png", use_column_width=True)
    st.sidebar.markdown('<h1>Our approach</h1>', unsafe_allow_html=True)
    st.sidebar.markdown('<p>Minos Biosciences is on the path to BRIDGE MOLECULAR and CELL BIOLOGY in a manner never achieved before that will, in turn, allow scientists to uncover the full picture of cell diversity and dynamics.</p>', unsafe_allow_html=True)
    st.sidebar.markdown('<h2>Single-cell revolution</h2>', unsafe_allow_html=True)
    st.sidebar.markdown('<p>Single-cell analysis is key to tackle cell diversity, and it has become in recent years an irreplaceable tool in all fields of biological and medical research. Current single-cell technologies however, despite their remarkable progress, address only fragments of the puzzle – whereas combining multiple modes of single-cell analysis is essential to unlock the complexity of biology and reveal the complete picture.</p>', unsafe_allow_html=True)
    st.sidebar.markdown('<h2>Minos solution</h2>', unsafe_allow_html=True)
    st.sidebar.markdown('<p>The single-cell solution developed by minos offers the unique ability to directly combine sequencing-based multi-omic analysis and image-based phenotypic analysis at single-cell resolution. This is enabled using a breakthrough microfluidics concept to isolate cells combined with innovative approaches in imaging, molecular biology and also bioinformatics.It will provide highly accurate insights into complex cell populations and their dynamics, opening up unique perspectives in a vast array of fundamental and translational research areas, as well as precision medicine therapeutics and diagnostics.</p>', unsafe_allow_html=True)
    st.sidebar.markdown('<h2>Minos impact</h2>', unsafe_allow_html=True)
    st.sidebar.markdown("<p>Minos solution has the potential to tremendously<strong>&nbsp;</strong><b>impact major healthcare fields,</b>&nbsp;such as:</p><ul><li><b>Cancer disease</b><strong>:</strong> connecting genetic &amp; non-genetic factors, plasticity and cell environment will be essential to understand tumour evolution and drug resistance, to design better and more personalized therapeutic strategies.</li><li><b>Autoimmune disorders:</b> unravelling the complex role of immune cells at the multi-omic and phenotypic levels will result in the development of better treatments.</li><li><b>Infectious disease:&nbsp;</b>correlating host-pathogen interaction to genetic and epigenetic variations will allow elucidating infection and proliferation mechanisms to improve therapy and prevention.</li></ul>", unsafe_allow_html=True)
    st.sidebar.markdown("<a href=https://www.minosbiosciences.com/> <h2>Our website</h2> </a>",unsafe_allow_html=True)

    with header:
        st.title("Welcome to the Minos Biosciences cage viewer application!")
        st.markdown('This app displays cages from any chosen chip')



    with viewer:
        st.header("Cage viewer")
        angles = st.secrets.angles
        
        chip_number_choice= st.selectbox(
        'Select the chip you want to display',
        ('None','58', '66', '67', '69', '70', '71','72', '74', '75'))
        #st.write('You selected:', chip_number_choice)
        if chip_number_choice!='None':
            try:
                raw_chip_image = get_image(bucket= bucket, file_path='RAW_CHIPS/CHIP%s.ome.jpg'%chip_number_choice, div=255, ang=float(angles[chip_number_choice]))
            except:
                print("Problème de chargement de l'image \n Verifier les angles")

            try:
                df_cages_position = gcp_csv_to_df(bucket=bucket, file_path="cage_positions/df_CHIP_%s_cages_position.xlsx"%(chip_number_choice))
            except:
                print('Echec chargement cages positions')

            try:
                single_cell_indexes =  gcp_csv_to_df(bucket= bucket, file_path="single_cell/Single_cell_chip_%s.xlsx"%chip_number_choice)   
                with metric1:
                    st.metric('Single cell cages count', "%s cages "%str(single_cell_indexes.shape[0]) )
                with metric2:
                    st.metric('Mouse single cell cages count',"%s cages"%str(single_cell_indexes[single_cell_indexes['Single_cell_green']==1].shape[0] + single_cell_indexes[single_cell_indexes['Single_cell_green_only_flex']==1].shape[0]))
                with metric3:
                    st.metric('Human single cell cages count',"%s cages"%str(single_cell_indexes[single_cell_indexes['Single_cell_blue']==1].shape[0]+ single_cell_indexes[single_cell_indexes['Single_cell_blue_only_flex']==1].shape[0]))
                
            except:
                st.write(' ')
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
            
            with viewer_image:
                try:
                    im_bf = get_image(bucket=bucket,file_path=filename)
                    st.image(im_bf,caption="Chip %s row %s column %s"%(chip_number_choice,row_number_choice,col_number_choice), width=image_width)
                except:
                    st.write(' ')

            with composite_image:
                try:
                    if chip_number_choice in ['72', '74','75']:
                        im_composite = get_image(bucket=bucket, file_path="DATASET_CHIP_" + chip_number_choice + "/COMPOSITE_DATASET_CHIP" + chip_number_choice + '_' + row_number_choice + "_" + col_number_choice + ".tif", div=255 )
                    else:
                        im_composite = get_image(bucket=bucket, file_path="DATASET_CHIP_" +chip_number_choice+ "/DATASET_CHIP" + chip_number_choice + "composite_" + row_number_choice + "_" + col_number_choice + ".tif", div=255)
                    st.image(im_composite, caption="Composite row %s column %s"%(row_number_choice,col_number_choice), width=image_width)
                except:
                    st.write(' ')
            #with rr:
            #    try:
            #        im_pred = get_image(bucket=bucket, file_path="DATASET_CHIP_" + chip_number_choice + "/PRED_DATASET_CHIP" +chip_number_choice + '_' + row_number_choice + "_" + col_number_choice + ".tif", div=255 )
            #        st.image(im_pred, caption="Prediction row %s column %s"%(row_number_choice,col_number_choice), width=image_width)
            #    except:
            #        st.write(' ')
        #st.markdown('Cage displayed: Chip %s\nRow number: %s\nColumn number: %s'%(chip_number_choice, row_number_choice, col_number_choice) )
    if chip_number_choice!='None':
        options = st.multiselect(
        'Additional content',
        ['Whole chip %s'%(chip_number_choice), 'Single cell indexes', 'Locate cage %s_%s on chip %s'%(row_number_choice,col_number_choice,chip_number_choice)]#,     ['Whole chip %s'%(chip_number_choice)]
        )
        #raw_chip_image = get_image(bucket= bucket, file_path='RAW_CHIPS/CHIP%s.ome.jpg'%chip_number_choice, div=255, ang=float(angles[chip_number_choice]))
        #st.write(options)

        #see_whole_chip = st.checkbox('See Chip %s'%chip_number_choice, help='Check this box if you want to see the whole chip', value=False)
        if 'Whole chip %s'%(chip_number_choice) in options:    
            try:
                raw_chip_image = get_image(bucket= bucket, file_path='RAW_CHIPS/CHIP%s.ome.jpg'%chip_number_choice, div=255, ang=float(angles[chip_number_choice]))
                st.image(raw_chip_image, use_column_width=True)
            except:
                st.write(' ')
        if 'Single cell indexes' in options:
            try:
                st.dataframe(single_cell_indexes)
            except:
                st.write('Single cell cages indices not available')
        if 'Locate cage %s_%s on chip %s'%(row_number_choice,col_number_choice,chip_number_choice) in options:
            #try:
            #raw_chip_image = get_image(bucket= bucket, file_path='RAW_CHIPS/CHIP%s.ome.jpg'%chip_number_choice, div=255, ang=float(angles[chip_number_choice]))
            show_cage_pos_on_chip(raw_chip_image , df_cages_position, "%s_%s"%(row_number_choice,col_number_choice),int(chip_number_choice),save=True)
                #cage_localisation_image = cv2.imread(rr)
                #cage_localisation_image = cv2.cvtColor(cage_localisation_image, cv2.COLOR_BGR2RGB)
                #st.image(cage_localisation_image, use_column_width=True)
                #os.remove(rr)
            #except:
                #st.write('Cage localization not available')


        #see_whole_chip = st.checkbox('See Chip %s'%chip_number_choice, help='Check this box if you want to see the whole chip', value=False)
        
main()