import streamlit as st
import random
import json
from openai import OpenAI

# with st.sidebar:
#     openai_api_key = st.secrets["openai"]["api_key"]
#     # openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
#     # "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
#     # "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
#     # "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

# st.title("💬 Guess a historical figure")

# if "messages" not in st.session_state:
#     st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# for msg in st.session_state.messages:
#     st.chat_message(msg["role"]).write(msg["content"])

# if prompt := st.chat_input():
#     if not openai_api_key:
#         st.info("Please add your OpenAI API key to continue.")
#         st.stop()

#     client = OpenAI(api_key=openai_api_key)
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     st.chat_message("user").write(prompt)
#     response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
#     msg = response.choices[0].message.content
#     st.session_state.messages.append({"role": "assistant", "content": msg})
#     st.chat_message("assistant").write(msg)







# Define the app pages
PAGES = {
    "Welcome": "welcome",
    "Play": "play",
    "Statistics": "stats"
}

# Create the page navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choose a page", list(PAGES.keys()))

# Welcome page
if page == "Welcome":
    st.title("Welcome to the Chat Application")
    st.write("Select a page from the sidebar to start!")

# Chat page
elif page == "Play":
    # st.title("Chat with OpenAI")

    # # User input for the chat
    # user_input = st.text_input("Ask me anything:")

    # # Generate response when user clicks "Send"
    # if st.button("Send") and user_input:
    #     try:
    #         # Use the correct API for chat-based completions (v1/chat/completions endpoint)
    #         response = openai.ChatCompletion.create(
    #             model="gpt-3.5-turbo",  # Use the chat model like "gpt-3.5-turbo" or "gpt-4"
    #             messages=[{"role": "user", "content": user_input}],  # Correct format for chat model
    #             max_tokens=150
    #         )
    #         # Extract and display the chat response
    #         st.write(response['choices'][0]['message']['content'].strip())  # Display the response
    #     except Exception as e:
    #         st.error(f"Error: {e}")

            
    # openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    # "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    # "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    # "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"
    # openai_api_key = st.secrets["openai"]["api_key"]
    # st.title("💬 Guess a historical figure")
    # if "messages" not in st.session_state:
    #     st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    # for msg in st.session_state.messages:
    #     st.chat_message(msg["role"]).write(msg["content"])

    # if prompt := st.chat_input():
    #     if not openai_api_key:
    #         st.info("Please add your OpenAI API key to continue.")
    #         st.stop()

    #     client = OpenAI(api_key=openai_api_key)
    #     st.session_state.messages.append({"role": "user", "content": prompt})
    #     st.chat_message("user").write(prompt)
    #     response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    #     msg = response.choices[0].message.content
    #     st.session_state.messages.append({"role": "assistant", "content": msg})
    #     st.chat_message("assistant").write(msg)



# Load the foods data from the JSON file
    def load_foods():
        with open("foods.json", "r") as file:
            return json.load(file)["foods"]

    # Pick a random food from the list
    foods = load_foods()
    random_food = random.choice(foods)

    # Set the food's name to be guessed (for OpenAI to help with)
    food_name = random_food["name"]

    # Set up OpenAI API key
    openai_api_key = st.secrets["openai"]["api_key"]
    st.title("💬 Guess the Food")

    # Check if the session state for messages exists, if not, create one
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "Let's play! I'm thinking of a food. You can ask yes or no questions to guess it."},
            {"role": "system", "content": "Remember, the user can only ask yes or no questions. Respond accordingly!"}
        ]

    # Display the conversation so far
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # Process the user input
    if prompt := st.chat_input():
        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()

        # Add the user's input to the session's messages
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Send the conversation and random food data to OpenAI to continue the guessing game
        client = OpenAI(api_key=openai_api_key)
        
        # If it's the first question, introduce the food to be guessed
        if "food" not in st.session_state:
            st.session_state["food"] = food_name
            st.session_state["messages"].append({
                "role": "assistant", 
                "content": f"Okay, I am thinking of a food. Let's start with this: It's called {food_name}. Try asking yes/no questions to guess it!"
            })

        # Get OpenAI's response
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        msg = response.choices[0].message.content

        # Add the response to the session's messages
        st.session_state.messages.append({"role": "assistant", "content": msg})

        # Display the assistant's response
        st.chat_message("assistant").write(msg)



# Statistics page
elif page == "Statistics":
    st.title("Statistics Page")

    # Example of showing some basic statistics
    st.write("Here are some statistics about your application:")

    # Dummy data for the statistics
    st.write("Total API Calls: 10")
    st.write("Average Response Time: 250ms")
    st.write("Total Characters Used: 5000")
