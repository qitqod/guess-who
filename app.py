import streamlit as st
import openai
import pandas as pd
import random

# Set OpenAI API key (replace "your-api-key" with your actual API key)
openai.api_key = "your-api-key"

# Sidebar for navigation
page = st.sidebar.selectbox("Navigation", ["Welcome", "Chat Interface", "Statistics Page"])

# Page 1: Welcome Page
if page == "Welcome":
    st.title("Welcome to the App")
    st.write("This is a multi-page Streamlit app.")
    st.write("""
    - Navigate through the pages using the sidebar.
    - Try out the chat interface connected to OpenAI.
    - View some random statistics on the Statistics Page.
    """)

# Page 2: Chat Interface
elif page == "Chat Interface":
    st.title("Chat with OpenAI")
    
    # Input box for user query
    user_input = st.text_input("Enter your question:", "")
    
    if st.button("Send"):
        if user_input.strip():
            # Send user input to OpenAI's GPT model
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": user_input}],
                )
                # Display response
                st.write("**OpenAI Response:**")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a valid question.")

# Page 3: Statistics Page
elif page == "Statistics Page":
    st.title("Statistics Page")
    st.write("Here are some random statistics generated for you.")
    
    # Create random data
    data = {
        "Category": ["A", "B", "C", "D"],
        "Values": [random.randint(10, 100) for _ in range(4)],
    }
    df = pd.DataFrame(data)
    
    # Display table
    st.write("### Data Table:")
    st.dataframe(df)
    
    # Display bar chart
    st.write("### Bar Chart:")
    st.bar_chart(df.set_index("Category"))

