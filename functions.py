import sqlite3
import pandas as pd
import streamlit as st
import os.path
import pickle
from datetime import date,timedelta
from datetime import datetime
import numpy as np
from os.path import join, dirname, abspath
#db_path = join(dirname(dirname(abspath(__file__))), 'autoaudit.db')
db_path='acepro.db'

def get_user_rights():
    try:
        sqliteConnection = sqlite3.connect(db_path)
        cursor = sqliteConnection.cursor()
        query="SELECT * from Users_Rights"
        sql_query=pd.read_sql_query(query,sqliteConnection)
        userrights = pd.DataFrame(sql_query)
        cursor.close()
    except sqlite3.Error as error:
        userrights=error
        st.write(userrights)
    except :
        userrights="Run time Error...Invalid Input or Data type Mismatch" 
        st.error(userrights)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            #message=("The SQLite connection is closed")
    return userrights

def check_login(username,password,comp_name,role) :
    try:
        sqliteConnection = sqlite3.connect(db_path)
        if username!="superadmin":
            #check if licence is not expired for thar user
            cursor = sqliteConnection.cursor()
            cursor.execute(f"select Expiry_Date from License WHERE id = (SELECT licese_id from Users_Rights WHERE username='{username}' AND company_name='{comp_name}')")
            exp_date=cursor.fetchone()
            #st.success(exp_date[0])
            date_object = datetime.strptime(exp_date[0], '%Y-%m-%d').date()
            #st.success(date_object)
            if date_object < date.today():  
                    
                    st.toast("Licenec has Expired...Please Contact to Renew the Licence...")     
                    return False
                    #gdruve="https://drive.google.com/file/d/18c0EASbKEC3vDXzVLJqzkeJj9mz0uPoe/view?usp=sharing"
            else:  
                    #sqliteConnection = sqlite3.connect(gdruve)
                    #st.success(exp_date)
                    cursor = sqliteConnection.cursor()
                    cursor.execute(f"SELECT password from Users where username='{username}'")
                    passworddb=cursor.fetchone()
                    #st.success(passworddb)
                    cursor.close()
                    sqliteConnection.close()
                    #st.write(passworddb[0])
                    if passworddb:
                        if passworddb[0]==password:
                            #st.success(passworddb)
                            st.session_state['loggedIn'] = True
                            st.session_state['User']=username
                            st.session_state['Company']=comp_name
                            st.session_state['Role']=role
                            
                            #auditid=get_audit_by_com(comp_name,audit)
                            #audit_id=auditid['id'].values[0]
                            #st.session_state['AuditID']=audit_id
                            #st.session_state['url']='https://google.com'
                            return True
                        else:
                            st.session_state['loggedIn'] = False
                            st.toast("Invalid password")
                            
                            return False
                    else:
                        st.session_state['loggedIn'] = False
                        st.toast("Invalid user name ")
                        #st.session_state["loginerror"]="Invalid User Id "
                        return False
            
        else:   
            if password==st.secrets["adminpass"]:
                #st.success("Admin")
                st.session_state['loggedIn'] = True
                st.session_state['Company']="superadmin"
                st.session_state['Role']="superadmin"
                st.session_state['superadmin']='superadmin'
                return True
            else:
                st.toast("Invalid password")
                #st.session_state["loginerror"]="Invalid password"
                return False

               
    except sqlite3.Error as error:
        if sqliteConnection:
            sqliteConnection.close()
        st.toast(f"Error:{error}")
        return False
    except :
        st.toast("License Invalid")
        return False

    finally:
        if sqliteConnection:
            sqliteConnection.close()
            #message=("The SQLite connection is closed")

def add_new_license(name,Expiry_Date,time_zone,email):
    try:
        sqliteConnection = sqlite3.connect(db_path)
        cursor = sqliteConnection.cursor()
        #st.success("Done1")
        #add DS name in table
        sqlite_insert_with_param = """INSERT INTO License
                          (name,Expiry_Date,time_zone,email) 
                          VALUES (?,?,?,?);"""
        data_tuple = (name,Expiry_Date,time_zone,email)
        #st.success("Done2")
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        cursor.close()
        return True
    except sqlite3.Error as error:
        message_verify=error
        return message_verify
    except Exception as e:
        message_verify=e
        return e
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def get_licen():

    try:
        sqliteConnection = sqlite3.connect(db_path)
        cursor = sqliteConnection.cursor()
        query="SELECT * from License"
        sql_query=pd.read_sql_query(query,sqliteConnection)
        cursor.close()
        return sql_query
    
    except Exception as e:
        return e
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            #message=("The SQLite connection is closed")

def update_license(name,Expiry_Date,time_zone,email):

    try:
        sqliteConnection = sqlite3.connect(db_path)
        cursor = sqliteConnection.cursor()
        #update audit status
        query=f"UPDATE License SET name ='{name}', Expiry_Date='{Expiry_Date}',time_zone={time_zone} WHERE `email` = '{email}'"
        #query=f"SELECT Review from Audit_AR where DataSetName='{DsName}' AND CompanyName='{comp_name}'"
        #st.write(query)
        cursor.execute(query)
        sqliteConnection.commit()
        cursor.close()
        return True
    except sqlite3.Error as error:
        return error
    except Exception as e:
        return e 
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            #message=("The SQLite connection is closed")

def del_lic(mylist,tnewlist):
    try:
        sqliteConnection = sqlite3.connect(db_path)
        cursor = sqliteConnection.cursor()
        #update audit status
        if len(mylist)>1:
            query=f"UPDATE License SET Is_Active = 'False' WHERE id In {tnewlist}"
        else:
            query=f"UPDATE License SET Is_Active = 'False' WHERE id = {tnewlist[0]}"
        #query=f"SELECT Review from Audit_AR where DataSetName='{DsName}' AND CompanyName='{comp_name}'"
        #st.write(query)
        cursor.execute(query)
        sqliteConnection.commit()
        cursor.close()
        st.toast(f'Records Deleted...')
        return True
    except sqlite3.Error as error:
        st.toast(f'{error}')
        return error
    except Exception as e:
        st.toast(f'{e}')
        return e 
    finally:
        if sqliteConnection:
            sqliteConnection.close()
    
            