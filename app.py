import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
from datetime import datetime

# --- CONFIGURATION & SETUP ---
# Securely load API Key
try:
    google_api_key = st.secrets["GOOGLE_API_KEY"]

except:
    st.error("Google API Key not found. Please set it in st.secrets.")
    st.stop()


genai.configure(api_key=google_api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

# Ensure storage exists (Global for both views)
if not os.path.exists("storage"):
    os.makedirs("storage")
DATA_FILE = "storage/data.csv"

# Create CSV if it doesn't exist
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["rating", "review", "ai_response", "summary", "actions", "date", "time"])
    df.to_csv(DATA_FILE, index=False)

# --- ROUTING LOGIC ---
# Checks the URL for ?role=admin
query_params = st.query_params
role = query_params.get("role", "user")

# ==========================================
# ADMIN DASHBOARD LOGIC (role=admin)
# ==========================================
if role == "admin":
    st.set_page_config(page_title="Admin Dashboard", layout="wide")
    st.title("Admin dashboard")

    # Read data
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
    else:
        df = pd.DataFrame()

    if len(df) == 0:
        st.warning("No data found")
    else:
        st.subheader("All users submissions")
        st.dataframe(df)

        st.subheader("Analytics")
        avg_rating = df["rating"].mean()
        total_reviews = len(df)

        col1, col2 = st.columns(2)
        col1.metric("Average Rating: ", round(avg_rating, 2))
        col2.metric("Total reviews: ", total_reviews)

        # Rating Distribution
        st.subheader("Rating Distribution")
        st.bar_chart(df["rating"].value_counts().sort_index())

# ==========================================
# USER DASHBOARD LOGIC (Default view)
# ==========================================
else:
    st.set_page_config(page_title="User Feedback")
    st.title("User feedback Dashboard")

    rating = st.radio("Select Rating:", [1, 2, 3, 4, 5], horizontal=True)
    review = st.text_area("Write your review")

    if st.button("Submit"):
        if review.strip() == "":
            st.error("please enter a review")
        else:
            with st.spinner("Processing..."):
                # AI response to user
                prompt = f"""
                You are a friendly assistant.
                A user gave this rating and review

                Rating:{rating}
                Review:{review}

                Give a short helpful reply to user.
                return plain text only.
                """
                ai_response = model.generate_content(prompt).text.strip()

                # summary for admin
                summary_prompt = f"""
                Summarize this review in one sentence:

                {review}
                """
                summary = model.generate_content(summary_prompt).text.strip()

                # recommended actions
                action_prompt = f"""
                Suggest one recommended business action based on this review:

                {review}
                """
                action = model.generate_content(action_prompt).text.strip()

                # save to csv
                new_row = {
                    "rating": rating,
                    "review": review,
                    "ai_response": ai_response,
                    "summary": summary,
                    "actions": action,
                    "date": datetime.now().date(),
                    "time": datetime.now().strftime("%H:%M:%S")
                }
                
                # Load existing data, append, and save
                df = pd.read_csv(DATA_FILE)
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)

            st.success("Review Submitted Successfully")
            st.write("AI response:")
            st.info(ai_response)