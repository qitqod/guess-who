import streamlit as st
import openai

# Set up your OpenAI API key (Ensure you've set this using secrets as shown earlier)
openai.api_key = st.secrets["openai"]["api_key"]

# Define the app pages
PAGES = {
    "Welcome": "welcome",
    "Chat": "chat",
    "Statistics": "statistics"
}

# Create the page navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choose a page", list(PAGES.keys()))

# Welcome page
if page == "Welcome":
    st.title("Welcome to the Chat Application")
    st.write("This is a simple web app using Streamlit and OpenAI's API.")
    st.write("Select a page from the sidebar to start!")

# Chat page
elif page == "Chat":
    st.title("Chat with OpenAI")

    # User input for the chat
    user_input = st.text_input("Ask me anything:")

    # Generate response when user clicks "Send"
    if st.button("Send") and user_input:
        try:
            # Use the new API for chat-based completions (v1/chat/completions endpoint)
            response = openai.chat_completions.create(
                model="gpt-3.5-turbo",  # Use the chat model like "gpt-3.5-turbo" or "gpt-4"
                messages=[{"role": "user", "content": user_input}],  # Correct format for chat model
                max_tokens=150
            )
            # Extract and display the chat response
            st.write(response['choices'][0]['message']['content'].strip())  # Display the response
        except Exception as e:
            st.error(f"Error: {e}")

# Statistics page
elif page == "Statistics":
    st.title("Statistics Page")

    # Example of showing some basic statistics
    st.write("Here are some statistics about your application:")

    # Dummy data for the statistics
    st.write("Total API Calls: 10")
    st.write("Average Response Time: 250ms")
    st.write("Total Characters Used: 5000")
