import streamlit as st
from google import genai

st.title("Conversational Assistant")

# 1. Initialize the Gemini Client (Replace with your actual API key)
# It is best practice to set this as an environment variable, but you can paste it here for testing.
API_KEY = "YOUR_GEMINI_API_KEY"
client = genai.Client(api_key=API_KEY)

# 2. Set up a system instruction to tell the AI how to behave
SYSTEM_INSTRUCTION = """
You are a friendly data-gathering assistant. Your goal is to find out the user's name, age, and favorite hobby. 
Do not interview them rigidly. Have a natural, flowing conversation. 
If they go off-topic, acknowledge what they said politely, but gently guide them back to finding out the missing pieces of information.
"""

# 3. Initialize chat history in Streamlit session state so it remembers past messages
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model="gemini-2.5-flash",
        config={"system_instruction": SYSTEM_INSTRUCTION}
    )
    # Start the conversation with an opening line
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I'd love to chat and get to know you a bit. What's your name?"}]

# 4. Display past chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Handle new user input
if user_input := st.chat_input("Type your message here..."):
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Send message to Gemini chat session (which automatically tracks history)
    response = st.session_state.chat.send_message(user_input)
    
    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
