import streamlit as st
import random
import json
from openai import OpenAI


# Define the app pages
PAGES = {
    "Welcome": "welcome",
    "Play": "play",
    "Stats": "stats"
}

# Create the page navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Choose a page", list(PAGES.keys()))

# Welcome page
if page == "Welcome":
    st.title("Welcome to the Food Guessing Game")
    st.write("Select Play in the sidebar to start guessing and check your game stats on the Stats page")

# Chat page
elif page == "Play":

# Load the foods data from the JSON file
    def load_foods():
        with open("data/foods.json", "r") as file:
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
            {"role": "system", "content": "Remember, the user can only ask yes or no questions. Respond accordingly."}
        ]

    # Display the conversation so far
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # Process the user input
    if prompt := st.chat_input():
        # if not openai_api_key:
        #     st.info("Please add your OpenAI API key to continue.")
        #     st.stop()

        # Add the user's input to the session's messages
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Send the conversation and random food data to OpenAI to continue the guessing game
        client = OpenAI(api_key=openai_api_key)
        
        # If it's the first question, introduce the food to be guessed
        if "food" not in st.session_state:
            st.session_state["food"] = food_name
            # st.session_state["messages"].append({
            #     "role": "assistant", 
            #     "content": f"Okay, I am thinking of a food. Let's start with this: It's called {food_name}. Try asking yes/no questions to guess it!"
            # })

        # Get OpenAI's response
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        msg = response.choices[0].message.content

        # Add the response to the session's messages
        st.session_state.messages.append({"role": "assistant", "content": msg})

        # Display the assistant's response
        st.chat_message("assistant").write(msg)



# Statistics page
elif page == "Stats":
    st.title("Statistics")

    # Example of showing some basic statistics
    st.write("Here are some statistics about your games:")

    # Dummy data for the statistics
    st.write("Total Games: 10")
    st.write("Average nunmber of guesses per game: 5")
    st.write("Least number of guesses per game: 5")
    st.write("Highest number of guesses per game: 15")
