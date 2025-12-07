import pandas as pd
import google.generativeai as genai
import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv

# load_dotenv(r"C:\Users\mdars\OneDrive\Desktop\Fynd assesment\.env")
# google_api_key=os.getenv("GOOGLE_API_KEY")
google_api_key=st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=google_api_key)
model=genai.GenerativeModel("gemini-2.0-flash")

st.title("User feedback Dashboard")

rating=st.radio("Select Rating:", [1, 2, 3, 4, 5], horizontal=True)
review=st.text_area("Write your review")

if not os.path.exists("storage"):
    os.makedirs("storage")
DATA_FILE = "storage/data.csv"

# Create CSV if not exists
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["rating", "review", "ai_response", "summary", "actions", "date","time"])
    df.to_csv(DATA_FILE, index=False)

if st.button("Submit"):
    if review.strip()=="":
        st.error("please enter a review")
    else:
        # AI response to user
        prompt=f"""
You are a friendly assistant.
A user gave this rating and review

Rating:{rating}
Review:{review}

Give a short helpful reply to user.
return plain text only.
"""
        ai_response=model.generate_content(prompt).text.strip()

        # summary for admin
        summary_prompt=f"""
Summarize this review in one sentence:

{review}
"""
        summary=model.generate_content(summary_prompt).text.strip()

        # recommended actions
        action_prompt=f"""
Suggest one recommended business action based on this review:

{review}
"""
        action=model.generate_content(action_prompt).text.strip()

        # save to csv
        new_row={
        "rating":rating,
        "review":review,
        "ai_response":ai_response,
        "summary":summary,
        "actions":action,
        "date":datetime.now().date(),
        "time":datetime.now().strftime("%H:%M:%S")

        }
        df=pd.read_csv(DATA_FILE)
        df=pd.concat([df,pd.DataFrame([new_row])],ignore_index=True)
        df.to_csv(DATA_FILE,index=False)

        st.success("Review Submitted Successfully")
        st.write("AI response:")
        st.info(ai_response)