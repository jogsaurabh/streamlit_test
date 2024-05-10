import streamlit as st

st.header("show hide container")
if 'hide' not in st.session_state:
    st.session_state.hide = True

def show_hide():
    st.session_state.hide = not st.session_state.hide

def onclickfunction(selection,otherOption):
        
    if selection != "Another option...":
        st.info(f":white_check_mark: The selected option is {selection} ")
        st.toast(f":white_check_mark: The selected option is {selection} ")
    else: 
        st.info(f":red[:white_check_mark: The written option is {otherOption} -]")
        st.toast(f":red[:white_check_mark: The written option is {otherOption} -]")
    st.session_state.hide =False
    st.button('Add New', on_click=show_hide,key="shcont")
if st.session_state.hide:
    secret = st.container(border=True)
    with secret:
        selection=None
        otherOption=None
        st.write('hi...this is conatiner')
        options = ["Another option..."]+[f"Option #{i}" for i in range(3)]
        selection = st.selectbox("Select option", options=options,index=1,key="selctiontxb")
        # Create text input for user entry
        if selection == "Another option...":
            otherOption=st.text_input("enter",key="enete")
        onclick=st.button("Submit",key="onclick",on_click=onclickfunction,args=(selection,otherOption))


st.write("---")
st.header("other way")
if 'input' not in st.session_state:
    st.session_state.input = True

def show_result():
    # Copy info from widgets into a different key in session state to avoid 
    # deletion when the widgets disappear
    st.session_state.result = (st.session_state.thing, st.session_state.count)
    st.session_state.input = False

def reset():
    st.session_state.input = True

if st.session_state.input:
    # Show input widgets if in input mode
    
    t=st.text_input('Name a thing', key='thing')
    n=st.number_input('Count them',key='count',step=1)
    st.button('Submit', on_click=show_result) # Callback changes it to result mode
else:
   # Otherwise, not in input mode, so show result
    st.write(f'There are {st.session_state.result[1]} {st.session_state.result[0]}s...')
    st.button('Add New', on_click=reset) # Callback changes it to input mode