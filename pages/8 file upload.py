import streamlit as st
import datetime
import os
Annexure=st.file_uploader("Upload File",type=['pdf','xlsx','docx','png','jpg'],key='Annexure')
file_name=st.text_input("Enter File Name without extention...Name should be Unique",key='comfilname')
currenT_time = str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '_')
currenT_time=currenT_time.replace(".","_")
if Annexure is not None:
    file_name=f'{file_name}_{currenT_time}_{Annexure.name}'
    st.write(file_name)
    
    
    with open(os.path.join("obsev_docs",file_name),"wb") as f: 
        f.write(Annexure.getbuffer())