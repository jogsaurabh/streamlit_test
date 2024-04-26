def delete_data():
    delplace= st.empty()
    with delplace.container():
        
        df=conn.query("select * from pet_owners")
        st.session_state.df=df
        delplceholds= st.empty()
        st.cache_data.clear()
        st.cache_resource.clear()
        #num_rows="dynamic" to add / delete
        st.data_editor(st.session_state.df,hide_index=True,use_container_width=True,num_rows="dynamic",key="delet_df")
        # st.write("Here's the value in Session State:")
        # st.write(st.session_state["delet_df"])
        #get list of deleted items
        my_list=st.session_state["delet_df"].get("deleted_rows")
        # get PF of index id of Dataframe
        new_list = df.iloc[my_list]['id']
        
        tnewlist=tuple(new_list)
        #st.write(new_list)
        #st.write(tnewlist[0])
        message=""
        #st.write(owner,pet)
        
        if len(new_list)>0:
            
            with delplceholds.container(border=True):
                #with st.popover("Are you sure you want to Delete Selected records?"):
                    st.write("Are you Sure, You want to Delete?")
                    col1, col2,col3= st.columns(3)
                    with col1: 
                        yesbutton=st.button("Yes",key="yes")
                    with col2:
                        nobutton=st.button("No",key="No")
                    if yesbutton:
                            try:
                                with conn.session as s:
                                    #tuple with 1 vlue gives error eg(8,)
                                    if len(new_list)>1:
                                        s.execute(text(f'DELETE from pet_owners WHERE id In {tnewlist}')) 
                                    else:
                                        s.execute(text(f'DELETE from pet_owners WHERE id = {tnewlist[0]}'))        
                                    s.commit()
                                message=True
                            except Exception as e:
                                #st.error(e)
                                message= e
                            finally:
                                s.close()
                            if message==True:
                                st.success("Records Deleted Successfully...")                  
                            elif message=="" :
                                st.write("")
                            else:
                                    st.error(message) 
                                    st.error("Try Again") 
                    if nobutton:
                        delplceholds.empty()
                        
                        #delplace.empty()
                
        