import pandas as pd
import pygwalker as pyg
import streamlit as st
from pygwalker.api.streamlit import StreamlitRenderer
import streamlit.components.v1 as stc
st.set_page_config(layout="wide")


st.title("Data Analysis with PyGWalker.")
# Import your data
df1 = pd.read_csv("https://kanaries-app.s3.ap-northeast-1.amazonaws.com/public-datasets/bike_sharing_dc.csv")

#second way
@st.cache_resource
def get_pyg_renderer() -> "StreamlitRenderer":
    df = pd.read_csv("rgp.csv",encoding = "ISO 8859-1")
    # If you want to use feature of saving chart config, set `spec_io_mode="rw"`
    return StreamlitRenderer(df1, spec="./gw_config.json", spec_io_mode="rw")


renderer = get_pyg_renderer()

renderer.explorer()