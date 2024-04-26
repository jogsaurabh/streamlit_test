import streamlit as st
import re
import pandas as pd
import datetime

from datetime import date,timedelta
from streamlit_option_menu import option_menu
# Make a regular expression
# for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
from functions import del_lic,get_user_rights,check_login,add_new_license,get_licen,update_license
st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout='wide'
)
with open('style.css') as f:
       st.markdown(f'<style>{f.read()}/<style>',unsafe_allow_html=True)
#st.markdown("""---""")
headerSection = st.container()
mainSection = st.container()
loginSection = st.container()
logOutSection = st.container()
superadmin_con = st.container()
today=datetime.datetime.now()

def show_login_page():
    with loginSection:
        tab1,tab2 =st.tabs(["Existing Users","Reset Password"])
        with tab1:
            # if 'loginerror' not in st.session_state:
            #     st.session_state['loginerror'] = ""
            if st.session_state['loggedIn'] == False:
                #it means no login then only go ahead
                st.title("Login") 
                userName = st.text_input (label="User ID", value="", placeholder="Enter your email",key="k1")
                     #get Companies for user
                password = st.text_input (label="Password", value="",placeholder="Enter password", type="password",key="k2")
                if userName=="superadmin":
                    if len(password)>0 and len(userName)>1:
                        st.button ("Login", key="supadminbutton",on_click=check_login, args= (userName, password,"AceProcure","superadmin"))
                else:

                    if(re.fullmatch(regex, userName)):
                        rights=get_user_rights()
                        #st.session_state['loginerror'] = ""
                        mask = rights['username'] == userName
                        #st.write(mask)
                        comp_name= rights[mask]
                        #comp_name=comp_name['company_name']
                        compname=st.selectbox("Select Company",comp_name['company_name'])
                        mask1=comp_name['company_name']==compname
                        #st.write(mask1)
                        roleds=comp_name[mask1]
                        #st.write(roleds)
                        if roleds.size !=0:
                            role=roleds['Role'].values[0]
                        else:
                            role=""
                        
                        if len(password)>0 and len(userName)>1 and compname:
                            st.button ("Login", on_click=check_login, args= (userName, password,compname,role))
                    else:
                        if len(userName)>1:
                            #st.session_state['loginerror'] = "Login Id must be an email"
                            st.toast("Invalid User Id... User Id must be in Email format.")
            #st.toast(f'Error:- {st.session_state['loginerror']}')
                #if userName=="admin" and password=="AcePro":
                #     st.button ("Login", on_click=check_login, args= (userName, password,compname,role))
                # else:
                #     st.button ("Login", on_click=check_login, args= (userName, password,compname,role))
        with tab2:
            with st.form("New User",clear_on_submit=True):
                
                st.title("Change Password")
                userid = st.text_input (label="User Id", value="", placeholder="Enter your user ID",key="k5")
                password = st.text_input (label="Password", value="",placeholder="Enter Current Password", type="password",key="k6")
                new_pass = st.text_input (label="New Password", value="", placeholder="Enter New Password", type="password",key="k3")
                renew_pass = st.text_input (label="New Password", value="", placeholder="ReEnter New Password", type="password",key="k4")
                submit_user =st.form_submit_button("Submit")
                if submit_user:
                    if new_pass == renew_pass:
                        #createuser=create_user(displayname,userid,password,designation)
                        newpass=update_password(userid,password,new_pass)
                        st.success(newpass)
                    else:
                        st.success('New Password and ReEntered Password not matching...')
                #st.form_submit_button("Submit",on_click=Register_Clicked, args= (userid, password,designation,displayname))
                #st.button ("Register", on_click=Register_Clicked, args= (userid, password,designation,displayname))

def show_view():
    st.success("show_view")

def LoggedOut_Clicked():
    st.session_state['loggedIn'] = False
    #loginuser=""

def show_logout_page():
    loginSection.empty()
    with logOutSection:
        st.sidebar.button ("Log Out", key="logout", on_click=LoggedOut_Clicked)

def show_admin():
    st.success("Admin")

def add_new_lic():
    placeholder = st.empty()
    def newlice(name,Expiry_Date,time_zone,email):
        #1st check email
        if(re.fullmatch(regex, email)):
             clearfields=["tnamelic","licemail"]
             allfields= False
             for i in clearfields:
                  if len(st.session_state[f'{i}'])<1:
                       allfields=True
             #if (len(names)<1 or len(names1)<1 or len(names2)<1):
             if allfields:
                st.toast("Enter All Manadtory Fields *")
             else:
                #now add record
                addrecord= add_new_license(name,Expiry_Date,time_zone,email)
                #placeholder.empty()
                
                if addrecord==True:
                    st.toast("Record Added Successfully...Continue to Add more", icon="👍")
                                
                else:
                    st.toast(f"Error:-{addrecord}", icon="👎")
                    st.toast("Try Again")
                #clear text fields on form
                for i in clearfields:
                        #st.write(st.session_state[f'{i}'])
                        st.session_state[f'{i}']=""
        else:
            #st.toast(email)
            st.toast("email not in Proper format...")


    with placeholder.container(border=True):
        
        st.subheader("Add New License")
        
        name=st.text_input(f"Enter Name :red[*]",key="tnamelic")
        Expiry_Date=st.date_input("Set Expiry Date",value=today,min_value=today,key="dexpdate")
        time_zone=st.number_input("Enter Time Difference",min_value=-720,max_value=840,value=0,key="ntime")
        email=st.text_input(f"email :red[*]",key="licemail")
        
        st.button("Submit",on_click=newlice,
                                args=[st.session_state.tnamelic,st.session_state.dexpdate,st.session_state.ntime,st.session_state.licemail])
        
def view_data_lic():
    vew_lic_con  = st.empty()
    with vew_lic_con.container(border=True):
        st.subheader("List of License")
        df=get_licen()
        if isinstance(df, pd.DataFrame):
            st.dataframe(df,hide_index=True)
        else:
            st.toast(df)
            st.toast("error")
        
def update_data_lic():
    update_lic_con  = st.empty()
    
    def updatelic(name,Expiry_Date,time_zone,email):
        uplic= update_license(name,Expiry_Date,time_zone,email)
                #placeholder.empty()
                
        if uplic==True:
            st.toast("Record Updated Successfully...", icon="👍")
            st.session_state.selemail="------"
                        
        else:
            st.toast(f"Error:-{uplic}", icon="👎")
            st.toast("Try Again")
        
    with update_lic_con.container(border=True):
        st.subheader("Update License")
        df=get_licen()
        email_list = df["email"].tolist()
        #add item at beginning of list 
        email_list.insert(0,"------")
        email_sel=st.selectbox("Select email to Update Record",options=email_list,key="selemail",placeholder="Choose as Option")
        if email_sel !="------":
            #get data for selected email& show as default value of widgets
            name=df.query(f"email=='{email_sel}'")["name"].item()
            Expiry_Date=df.query(f"email=='{email_sel}'")["Expiry_Date"].item()
            time_zone=df.query(f"email=='{email_sel}'")["time_zone"].item()
            #st.write(name,Expiry_Date,time_zone)
            mname=st.text_input(f"Update Name :red[*]",value=name,key="upname")
            mExpiry_Date=st.date_input("Update Date",value=datetime.datetime.strptime(Expiry_Date, '%Y-%m-%d').date(),key="update")
            mtime=st.number_input("Update Time Zoe",value=time_zone,min_value=-720,max_value=840,key="upntime")
            if len(mname)>1:
                st.button("Update",key="upadtelic",on_click=updatelic,args=[mname,mExpiry_Date,mtime,email_sel])

def get_df():
    df=get_licen()
    if isinstance(df, pd.DataFrame):
        
        return df
    else:
        
        st.toast("error")
        return False
if "df" not in st.session_state:
     st.session_state.df = pd.DataFrame()

def delete_data_lic():
    del_lic_con  = st.empty()

    
    #def updatelic(name,Expiry_Date,time_zone,email):
    
    with del_lic_con.container(border=True):
        st.subheader("Delete License")
        st.info("Select Rows to Delete...")
        df=get_df()
        if df is False:
            st.toast(df)
        else:
            # Get dataframe row-selections from user with st.data_editor
            df.insert(0, "Select", False)
            edited_df = st.data_editor(
                df,
                hide_index=True,
                column_config={"Select": st.column_config.CheckboxColumn(required=True)},
                disabled=st.session_state.df.columns,key="seldfdel"
            )
            # Filter the dataframe using the temporary column, then drop the column
            selected_rows = edited_df[edited_df.Select]
            selected_rows= selected_rows.drop('Select', axis=1)
            if len(selected_rows)>0:
                col1, col2= st.columns([3,1])
                with col1: 
                    st.error("Are you Sure you want to Delete following rows:")
                    st.dataframe(selected_rows,hide_index=True)
                with col2:
                    
                    mylist=selected_rows["id"].tolist()
                    tnewlist=tuple(mylist)
                    #st.write(mylist)
                    #st.write(tnewlist)
                    yesbutton=st.button("Yes",key="yes",on_click=del_lic,args=(mylist,tnewlist))
            
            

def show_superadmin():
    with superadmin_con:
        #st.success("Super Admin")
        with st.sidebar:
            sel=option_menu(menu_title="",options=["Manage License","With Tabs"],
                            )
        if sel=="Manage License":
           
            selected = option_menu(None, ["Add New", "View", "Update", 'Delete'],
                        icons=['cloud-plus', 'list-task', "pencil-square", 'x-circle'],
                        key='menu_1', orientation="horizontal")
            
            if selected=="Add New":
                add_new_lic()
            elif selected=="View":
                #st.cache_resource.clear()
                view_data_lic()
            elif selected=="Update":
                
                update_data_lic()
            else:
                
                delete_data_lic()
        else:
            add_t,view_t, modify_t,del_t= st.tabs(["✔️**Add New**","📋**View**","✏️**Update**","❌Delete"])
            with add_t:
                add_new_lic()
            with view_t:
                view_data_lic()
            with modify_t:
                update_data_lic()
            with del_t:
                delete_data_lic()
def show_main_page():
    st.success("show_main_page")

def show_manager():
    st.success("show_manager")

with headerSection:
    # for login checking
    if 'User' not in st.session_state:
        st.session_state['User'] = ""
    
    if 'Company' not in st.session_state:
        st.session_state['Company'] = ""
    
    if 'Role' not in st.session_state:
        st.session_state['Role'] = ""
    
    if 'loggedIn' not in st.session_state:
        st.session_state['loggedIn'] = False
        show_login_page()
                
    else:
        if st.session_state['loggedIn']:
            show_logout_page()   
            if st.session_state['Role'] == "View":
                show_view()
            elif st.session_state['Role'] == "Manager":
                show_manager()
            elif st.session_state['Role'] =="admin":
                show_admin()
            elif st.session_state['Role'] =="superadmin":
                show_superadmin()
            else:
                show_main_page()   
        else:
            show_login_page()
