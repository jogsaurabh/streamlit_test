import streamlit as st
from sqlalchemy.sql import text
import pandas as pd
from functions import get_licen
conn = st.connection('pets_db', type='sql')

cont1 =st.container(border=True)

df1=conn.query("select * from pet_owners")
def dataframe_with_selections(df):
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)

    # Get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        column_config={"Select": st.column_config.CheckboxColumn(required=True)},
        disabled=df.columns,
        height=300
    )
    
    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df.Select]
    return selected_rows.drop('Select', axis=1)

def openpopup(df):
    #with popc:
        #cont1.empty()
        #with st.popover(" Rows to delete",use_container_width=True):
            popc =st.empty()
            with popc.container():
                selection = dataframe_with_selections(df)
                mylist=selection["id"].tolist()
                tnewlist=tuple(mylist)
                if len(selection)>0:
                    yesbutton=st.button("Delet Selected",key="yesa")
                    if yesbutton:
                        with conn.session as s:
                            if len(mylist)>1:
                                s.execute(text(f'DELETE from pet_owners WHERE id In {tnewlist}')) 
                            else:
                                s.execute(text(f'DELETE from pet_owners WHERE id = {tnewlist[0]}'))        
                                s.commit()
                                s.close()

                

with cont1:
     
    st.dataframe(df1)    
    st.button("Submit",key='buttonsubmit',on_click=openpopup,args=[df1])
        