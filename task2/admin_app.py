import streamlit as st
import pandas as pd
import os

# creating storage folder if does not exist
if not os.path.exists("storage"):
    os.makedirs("storage")

DATA_FILE = "storage/data.csv"
# create csv if does not exist
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["rating", "review", "ai_response", "summary", "actions", "date","time"])
    df.to_csv(DATA_FILE, index=False)

df=pd.read_csv(DATA_FILE)

st.title("Admin dashboard")
if len(df)==0:
    st.warning("No data found")
else:
    st.subheader("All users submissions")
    st.dataframe(df)

    st.subheader("Analytics")
    avg_rating=df["rating"].mean()
    total_reviews=len(df)

    st.metric("Average Rating: ",round(avg_rating,2))
    st.metric("Total reviews: ",total_reviews)

    # rating
    st.subheader("Rating Distribution")
    st.bar_chart(df["rating"].value_counts().sort_index())


