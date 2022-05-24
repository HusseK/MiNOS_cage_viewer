import streamlit as st
import cv2
from google.oauth2 import service_account
from google.cloud import storage

#credentials = service_account.Credentials.from_service_account_info(
#    st.secrets["gcp_service_account"]
#)
credentials = service_account.Credentials.from_service_account_file(
    'minos-350712-2dc2472d64bd.json')

client = storage.Client(credentials=credentials)
bucket_name = 'cells_and_cages'
print('#############################')
print('#############################')
print('#############################')
print('#############################')
print('#############################')
print('#############################')

def read_file(bucket_name, file_path):
    bucket = client.bucket(bucket_name)
    content = bucket.blob(file_path).download_as_string().decode("utf-8")
    return content


header = st.container()
dataset_explanation = st.container()
viewer= st.container()

image, image_rgb = st.columns((2,2))
row_number, col_number = st.columns((1,1))

example_image = cv2.imread('DATASET_CHIP71_1_7.tif')
example_image_rgb = cv2.imread('DATASET_CHIP71composite_1_7.tif')
example_image_rgb = cv2.cvtColor(example_image_rgb, cv2.COLOR_BGR2RGB)


with header:
    st.title("Welcome to the Minos Biosciences cage viewer application!")
    st.text('This app displays cages from any chosen chip')
    st.text('\n \n \n \n \n \n')

with dataset_explanation:
    st.title("Chips")
    st.text('These images...')

with viewer:
    st.title("Cage viewer")
    st.text("Here you can choose a chip then a cage to see what it looks like.")
    with image:
        st.image(example_image)

    with image_rgb:
        st.image(example_image_rgb)
    
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

filename = 'DATASET_CHIP_' + chip_number_choice + '_' + row_number_choice + '_' + col_number_choice + '.tif'
st.text('Cage displayed: Chip %s \t Row number: %s \t Column number: %s'%(chip_number_choice, row_number_choice, col_number_choice) )
    
content = read_file(bucket_name=bucket_name, file_path="DATASET_CHIP_71/DATASET_CHIP71_1_7.tif")
img_content = cv2.imread(content)
st.image(img_content)