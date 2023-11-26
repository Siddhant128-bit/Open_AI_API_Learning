import streamlit as st
import PyPDF2
from utils import get_initial_message, get_chatgpt_response, update_chat,get_api_key
from streamlit_chat import message
from dotenv import load_dotenv
load_dotenv()

st.title("DocXtract Pro")
api_key= get_api_key()

# Upload PDF file through Streamlit
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

# Check if a file has been uploaded
if uploaded_file is not None:
    st.success("File successfully uploaded!")

    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    num_pages = len(pdf_reader.pages)

    page_content=''    
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        page_content+=page.extract_text()
    
    st.session_state['messages'] = get_initial_message(page_content)

    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
    if 'past' not in st.session_state:
        st.session_state['past'] = []

    if "my_text" not in st.session_state:
        st.session_state.my_text = ""
        
    def submit():
        st.session_state.my_text = st.session_state.widget
        st.session_state.widget = ""

    st.text_input("Ask me about the doc: ", key="widget", on_change=submit)

    query = st.session_state.my_text
    if 'messages' not in st.session_state:
        st.session_state['messages'] = get_initial_message(page_content)


    if query:
        with st.spinner("generating..."):
            messages = st.session_state['messages']
            messages = update_chat(messages, "user", query)
            response = get_chatgpt_response(messages,api_key)
            messages = update_chat(messages, "assistant", response)
            st.session_state.past.append(query)
            st.session_state.generated.append(response)
            


    if st.session_state['generated']:
        
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
        try:
            with st.expander("Show Messages"):
                st.write(messages)
        except:
            st.write('Retry Query Please')
