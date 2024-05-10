import streamlit as st
import pandas as pd
import io
import numpy as np
import pandas_read_xml as pdx
# alos pip install openpyxl  
#pip install pandas_read_xml
#add excel sheets to workbook & then download the same
with open('style.css') as f:
       st.markdown(f'<style>{f.read()}/<style>',unsafe_allow_html=True)
op=st.radio(label="Select",options=["excle","Style DF"])
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
    st.write("Style DF")
    #delet &# inxml file
    df = pd.read_csv("my_data.csv")

    st.dataframe(df)
    

    # style
    th_props = [
    ('font-size', '16px'),
    ('text-align', 'center'),
    ('font-weight', 'bold'),
    ('color', '#6d6d6d'),
    ('background-color', '#f7ffff')
    ]
                                
    td_props = [
    ('font-size', '12px')
    ]
                                    
    styles = [
    dict(selector="th", props=th_props),
    dict(selector="td", props=td_props)
    ]

    # table
    df2=df.style.set_table_styles(styles)
    st.table(df2)
    st.dataframe(df.style.set_table_styles(styles))
    st.markdown(df.to_html(classes='table table-stripped'), unsafe_allow_html=True)
    