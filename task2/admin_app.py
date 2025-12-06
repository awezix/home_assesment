import streamlit as st
import pandas as pd

st.title("Admin dashboard")
DATA_FILE = "storage/data.csv"
df=pd.read_csv(DATA_FILE)

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


