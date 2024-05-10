import streamlit as st

placeholder_for_selectbox = st.empty()
with placeholder_for_selectbox.container(border=True):
        selection=None
        otherOption=None
        # Create selectbox
        options = ["Another option..."]+[f"Option #{i}" for i in range(3)]
        selection = st.selectbox("Select option", options=options,index=1,key="selctiontxb")

        # Create text input for user entry
        if selection == "Another option...": 
            otherOption = st.text_input("Add New...",key="2")

        # Just to show the selected option
        onclick=st.button("Submit",key="onclick")
        if onclick:
            if selection != "Another option...":
                st.info(f":white_check_mark: The selected option is {selection} ")
                st.toast(f":white_check_mark: The selected option is {selection} ")
            else: 
                st.info(f":red[:white_check_mark: The written option is {otherOption} -]")
                st.toast(f":red[:white_check_mark: The written option is {otherOption} -]")


# Layout for the form OTHER OPTION
if "listoptios" not in st.session_state:
    st.session_state.listoptios=["Another option..."]+[f"Option #{i}" for i in range(3)]

def addlist():
    st.write(st.session_state.st3)
    st.session_state.listoptios.append(st.session_state.st3)
    st.write(st.session_state.listoptios)
st.write("----")
st.header("Other option session sate to add in list")
selection1 = st.selectbox("Select option", options=st.session_state.listoptios,index=1,key="3")
# Create text input for user entry
if selection1 == "Another option...": 

    otherOption1 = st.text_input("Add New...",key="st3",on_change=addlist)