import streamlit as st
import utilities

# -------------------------------
# Helper Functions
# -------------------------------
resp_generator = utilities.LoremIpsumGenerator()

long_response = "Just a lot of random words"


# reset message/response list
def restart():
    st.session_state.messages = []


def get_response(input_prompt):
    return resp_generator.generate(100, 150)  # Generate up to 150 characters of Lorem Ipsum


image_base = "/workspaces/vs-docker-github/images/"
# UI - Loads app images
# responder_icon = "/Users/charlesrussell/Library/Mobile Documents/com~apple~CloudDocs/Media/Projects/si-chat/av1.jpg"
responder_icon = "/workspaces/vscode-python-medium/tests/av1.jpg"

# prompter_icon = "/Users/charlesrussell/Library/Mobile Documents/com~apple~CloudDocs/Media/Projects/si-chat/ci.jpg"
prompter_icon = "/workspaces/vscode-python-medium/tests/ci.jpg"

# hdr_image = "/Users/charlesrussell/Library/Mobile Documents/com~apple~CloudDocs/Media/Projects/si-chat/sandbox.jpg"
hdr_image = "/workspaces/vscode-python-medium/tests/sandbox.jpg" 
st.image(hdr_image, output_format="auto")

# UI Reset and restart the  conversation
convo_exp = st.expander("Conversation Control")
if convo_exp.button(key='reset', label="Reset conversation"):
    restart()

# UI sidebar App configuration and options
sb = st.sidebar
exp = sb.expander("Advanced")
exp2 = sb.expander("Settings")

sel = exp.selectbox("Contact2", ("Email", "Home phone", "Mobile phone"))
rad = exp.radio(
                "Choose a shipping method",
                ("Standard (5-15 days)", "Express (2-5 days)")
            )
fu = exp.file_uploader("Choose a file")
fu2 = exp2.file_uploader("Choose a file to Upload")


# UI functional tabs separating conversations from data output
tab1, tab2 = st.tabs(["Query", "Data"])

# UI Conversations
with tab1:
    # Initialize chat history list
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({"role": "assistant", "content": "Talk LLM to Me!"})


        for message in st.session_state.messages:
            cm = tab1.chat_message(message["role"],
                                   avatar=responder_icon)
            cm.markdown(message["content"])

    # Display user prompt in chat message container
    if prompt := st.chat_input("Talk LLM to Me"):

        # Add user prompt as Dict to chat messages history List
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = get_response(prompt)

        # Add responders response to to chat messages history List
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Reversing the input list tp print last prompt/response first
        reversed_list = st.session_state.messages[::-1]

        for message in reversed_list:
            if message["role"] == 'assistant':
                cm = tab1.chat_message(message["role"], avatar=responder_icon)
                cm.markdown(message["content"])
            else:
                cm = tab1.chat_message(message["role"], avatar=prompter_icon)
                cm.markdown(message["content"])

# UI - Data Management Tab
with tab2:
    # data_hdr_image = "/Users/charlesrussell/Library/Mobile Documents/com~apple~CloudDocs/Media/Projects/si-chat/DataHeader.jpg"
    data_hdr_image = "/workspaces/vscode-python-medium/tests/DataHeader.jpg"
    st.image(data_hdr_image, output_format="auto")




