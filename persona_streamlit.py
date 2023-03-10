import pandas as pd
import streamlit as st
from PIL import Image

def customer_level_based():
    df = pd.read_csv("persona.csv")
    df.columns = [col.lower() for col in df.columns]
    agg_df = df.groupby(["country", "source", "sex", "age"]).agg({"price": "mean"}).sort_values("price",
                                                                                                ascending=False).reset_index()
    agg_df["new_age_cat"] = pd.cut(agg_df["age"], bins=[0, 18, 23, 30, 40, 70],
                                   labels=["0_18", "19_23", "24_30", "31_40", "41_70"])
    agg_df["customer_level_based"] = [
        row[0].upper() + "_" + row[1].upper() + "_" + row[2].upper() + "_" + row[5].upper()
        for row in agg_df.values]
    agg_df_segment = agg_df.groupby("customer_level_based").agg({"price": "mean"}).reset_index()
    agg_df_segment["segment"] = pd.qcut(agg_df_segment["price"], 4, labels=["D", "C", "B", "A"])
    return agg_df_segment

def generate_new_user(gen, source, country, age):
    if (age <= 70) and (age >= 0):
        age_range = ""
        if 0 <= age <= 18:
            age_range += "0_18"
        elif 19 <= age <= 23:
            age_range += "19_23"
        elif 24 <= age <= 30:
            age_range += "24_30"
        elif 31 <= age <= 40:
            age_range += "31_40"
        elif 41 <= age <= 70:
            age_range += "41_70"
    country = country[0:3]
    new_user = "{0}_{1}_{2}_{3}".format(country.upper(), source.upper(), gen.upper(), str(age_range))
    show_result(new_user)


def show_result(new_user):
    df = customer_level_based()
    print(new_user)
    price = df.loc[df["customer_level_based"] == new_user, "price"].values[0]
    segment = df.loc[df["customer_level_based"] == new_user, "segment"].values
    st.success(f"Average revenue generated by the new customer = {price:.2f}$")
    st.success(f"New customer segment = {segment}")

st.title("Rule Based Customer Segmentation")
img = "https://raw.githubusercontent.com/suleymansennn/DS-Bootcamp/main/week3/customer.jpeg"
st.image(img)


age = st.number_input("Enter your age", step=1)
gender = st.radio(label="Select your gender", options=("Male", "Female"))
source = st.radio(label="Select your source", options=("IOS", "Android"))
country = st.radio(label="Select your country", options=("Brazil", "Turkey" ,"Usa", "Canada", "Deutschland", "France"))
calculate = st.button(label="Calculate")

if calculate:
    generate_new_user(gender, source, country, age)




