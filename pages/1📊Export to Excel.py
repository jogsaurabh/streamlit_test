import streamlit as st
import pandas as pd
import io
import pandas_read_xml as pdx
# alos pip install openpyxl  
#pip install pandas_read_xml
#add excel sheets to workbook & then download the same
with open('style.css') as f:
       st.markdown(f'<style>{f.read()}/<style>',unsafe_allow_html=True)
op=st.radio(label="Select",options=["excle","xml"])
if op=="excle":

    buffer = io.BytesIO()
    files=["my_data.csv","my_data1.csv","my_data2.csv"]
    with pd.ExcelWriter(buffer) as writer:
        
        for f in files:
            df = pd.read_csv(f)
            df.to_excel(writer,sheet_name=f)
            st.dataframe(df)
    st.download_button(label="Download File",data=buffer,file_name="queries.xlsx")
    buffer.flush()
else:
    st.write("xml")
    #delet &# inxml file
    st.button("show xml",key="showxml")