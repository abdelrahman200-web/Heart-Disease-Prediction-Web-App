import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
import os
# Load model
model = pickle.load(open("heart_disease_model.pkl", "rb"))
csv_path = "user_data_log.csv"

st.set_page_config(page_title="Heart Disease Predictor", layout="centered")
st.title("💓 Heart Disease Prediction App")
st.write("Provide your medical info to assess the risk of heart disease.")

# Sidebar input
st.sidebar.header("Enter Patient Data:")

def user_input():
    age = st.sidebar.slider("Age", 29, 77, 55)
    sex = st.sidebar.selectbox("Sex (0 = female, 1 = male)", [0, 1])
    cp = st.sidebar.selectbox("Chest Pain Type", [1, 2, 3, 4])
    trestbps = st.sidebar.slider("Resting Blood Pressure", 80, 200, 120)
    chol = st.sidebar.slider("Serum Cholesterol (mg/dl)", 100, 600, 240)
    fbs = st.sidebar.selectbox("Fasting Blood Sugar > 120", [0, 1])
    restecg = st.sidebar.selectbox("Resting ECG Result", [0, 1, 2])
    thalach = st.sidebar.slider("Max Heart Rate", 70, 210, 150)
    exang = st.sidebar.selectbox("Exercise Induced Angina", [0, 1])
    oldpeak = st.sidebar.slider("ST Depression (oldpeak)", 0.0, 6.2, 1.0)
    slope = st.sidebar.selectbox("Slope of ST Segment", [1, 2, 3])
    ca = st.sidebar.selectbox("Number of Vessels Colored (ca)", [0, 1, 2, 3, 4])
    thal = st.sidebar.selectbox("Thalassemia", [3,6,7])
   
    features = {
        "thalach": thalach,        
        "oldpeak": oldpeak,
        "age": age,       
        "chol": chol,
        "trestbps": trestbps,
        "ca": ca,
        "thal": thal,
        "cp": cp
    }

    return pd.DataFrame([features])

input_df = user_input()

st.subheader("Patient Data")
st.write(input_df)

# Prediction
if st.button("Predict Heart Disease"):
    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1]

    result_df = input_df.copy()
    result_df["prediction"] = prediction
    result_df["probability"] = probability
    if not os.path.exists(csv_path):
        result_df.to_csv(csv_path, index=False)
    else:
        result_df.to_csv(csv_path, mode='a', header=False, index=False)

    if prediction == 1:
        st.error(f"⚠️ High risk of heart disease (Confidence: {probability:.2f})")
    else:
        st.success(f"✅ Low risk of heart disease (Confidence: {1 - probability:.2f})")
if os.path.exists(csv_path):
    st.subheader("📊 User Data Trends")
    log_data = pd.read_csv(csv_path)
    # Age distribution
    age_chart = px.histogram(log_data, x='age', color='prediction',
                             title="Age Distribution by Risk Level",
                             nbins=20)
    st.plotly_chart(age_chart)