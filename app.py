import streamlit as st
import sqlite3
import google.generativeai as genai

# Replace 'your_actual_google_api_key' with your actual Google API key
API_KEY = "AIzaSyAxLrjHSBLlRzs-j1yNKZvT6NrSXS9uuEE"

# Configure GenAI API key
genai.configure(api_key=API_KEY)

# Function to get a response from the Gemini model
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content([prompt[0], question])
    return response.text

# Function to retrieve query results from the database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

# Prompt for converting natural language questions to SQL
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
    SECTION \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
    \nExample 2 - Tell me all the students studying in Data Science class?, 
    the SQL command will be something like this SELECT * FROM STUDENT 
    where CLASS="Data Science"; 
    also the sql code should not have ``` in beginning or end and sql word in output
    """
]

# Enhanced Streamlit Interface
st.set_page_config(
    page_title="AI SQL Genie",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Applying black background and styling elements
st.markdown(
    """
    <style>
    body {
        background-color: #000000;
        color: white;
        font-family: Arial, sans-serif;
    }
    .main {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.4);
    }
    .stButton button {
        background-color: #FF6F61;
        color: white;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 10px;
        border: none;
        cursor: pointer;
        transition: transform 0.2s, background-color 0.3s;
    }
    .stButton button:hover {
        background-color: #FF8A65;
        transform: scale(1.1);
    }
    .sql-box {
        font-family: monospace;
        background-color: rgba(0, 0, 0, 0.7);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        color: #00E676;
    }
    .result-box {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 15px;
        margin: 10px 0;
        border-radius: 10px;
        color: #4CAF50;
    }
    .sidebar-content {
        background: linear-gradient(to bottom, #2c5364, #203a43, #0f2027);
        color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.5);
        animation: fadeIn 2s ease-in-out;
    }
    @keyframes fadeIn {
        from {opacity: 0;}
        to {opacity: 1;}
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Main Title
st.title("✨ Text to SQL Query Generator 🧞")
st.subheader("Effortlessly generate SQL queries from natural language.")

# Input and Submission Button
question = st.text_input("🧐 What's your question?", key="input")
submit = st.button("🔍 Generate SQL Query & Fetch Data")

# Handle Submission
if submit:
    with st.spinner("🧞 Generating your query..."):
        # Generate SQL query
        response = get_gemini_response(question, prompt)
        st.markdown(
            f"""
            <div style="text-align: center; font-size: 20px; color: #00E676;">
                🎉 Generated SQL Query:
            </div>
            <div class="sql-box">
                {response}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Execute the SQL query
        rows = read_sql_query(response, "student.db")
        st.markdown(
            """
            <div style="text-align: center; font-size: 20px; color: black;">
                📊 Database Results:
            </div>
            """,
            unsafe_allow_html=True,
        )

        if rows:
            for idx, row in enumerate(rows, start=1):
                st.markdown(
                    f"""
                    <div class="result-box">
                        <b>Row {idx}:</b> {row}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.error("No data found for the given query!")

# Sidebar Content
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-content">
            <h2>About the App</h2>
            <p>
                🚀 Assistant for converting natural 
                language questions into SQL queries and retrieving data from your database.
            </p>
            <p style="text-align:center;">👨‍💻 Created by <b>Siddharth Bhimpure</b></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Footer
st.markdown(
    """
    <hr>
    <div style="text-align: center; font-size: 16px; color: black;">
        🌌 Developed by Siddharth Bhimpure
    </div>
    """,
    unsafe_allow_html=True,
)
