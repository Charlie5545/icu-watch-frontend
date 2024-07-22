import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="ICU Watch - Sepsis Prediction", layout="wide")

st.markdown("""
<style>
    .reportview-container .main .block-container {
        max-width: 1000px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stButton>button {
        color: #ffffff;
        background-color: #4CAF50;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
</style>
""", unsafe_allow_html=True)

API_URL = "https://api-fcf7rbbebq-ew.a.run.app/"
predict_url = f"{API_URL}/predict"

st.title("🏥 ICU Watch - Sepsis Prediction")
st.header("Welcome to our prediction service")
st.markdown("""
Our platform leverages advanced data science to provide predictions and insights,
enhancing patient care and operational efficiency. Our goal is to predict Sepsis 6
hours prior to appearance.""")

uploaded_file = st.file_uploader("📤 Upload your CSV file", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("File successfully uploaded!")

        st.subheader("Preview of uploaded data:")
        st.dataframe(df.head(6))

        if st.button("🔮 Get Prediction"):
            with st.spinner('Processing your data...'):
                uploaded_file.seek(0)
                files = {'file': uploaded_file}
                try:
                    response = requests.post(predict_url, files=files)
                    response.raise_for_status()

                    predictions = response.json().get('predictions')
                    st.success("🎉 Prediction successful!")

                    st.subheader("Predictions:")
                    st.write(predictions)

                    df['Prediction'] = predictions
                    st.subheader("Visualization of Predictions")
                    st.line_chart(df['Prediction'])

                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download Predictions as CSV",
                        data=csv,
                        file_name="sepsis_predictions.csv",
                        mime="text/csv",
                    )
                except requests.RequestException as e:
                    st.error(f"Error communicating with the server: {str(e)}")
    except Exception as e:
        st.error(f"Error processing the file: {str(e)}")
else:
    st.info("👆 Please upload a CSV file to get predictions.")

st.markdown("---")
st.markdown("© 2024 ICU Watch. All rights reserved.")
