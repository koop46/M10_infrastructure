import streamlit as st
import ui 
from services.services import authenticate
from glenda import glenda_talk

st.set_page_config(layout="wide")


if 'credentials' not in st.session_state:
    st.session_state.credentials = False
if "token" not in st.session_state:
    st.session_state.token = ""

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


with st.expander("Log in"):

    usr = st.text_input("Username")
    pswd = st.text_input("Password", type="password")

    login_button = st.button("Log in")
    if login_button:
        auth_response = authenticate(usr, pswd)

        if auth_response[1] == 200:
            
            st.session_state.token = auth_response[0]["access_token"]
            st.session_state.credentials = True



app_ui = ui.layout(st.session_state.token)

if st.session_state.credentials == True:  #If true open up rest of UI

    left, right = st.columns([0.5, 0.5])

    with left:
        
        st.title("M10 AI DB")
        st.title("")


        create_tab, read_tab, update_tab, delete_tab, download_tab = st.tabs(["Create data", "Get data", "Update", "Delete", "DB Backup"])


        with create_tab:
            app_ui.create_data()


        with read_tab:
            app_ui.read_tab()


        with update_tab:
            app_ui.update_tab()    


        with delete_tab:
            app_ui.delete_tab()


        with download_tab:
            app_ui.download_tab()


    with right:

        st.title("Glenda")

        with st.container(height=500, border=False):
            glenda_talk(local=True)


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


