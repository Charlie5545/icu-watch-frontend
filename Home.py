import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go

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
        st.dataframe(df)

        if st.button("🔮 Get Prediction"):
            with st.spinner('Processing your data...'):
                uploaded_file.seek(0)
                files = {'file': uploaded_file}
                try:
                    response = requests.post(predict_url, files=files)
                    response.raise_for_status()

                    prediction = response.json().get('predictions')

                    if prediction is None:
                        st.error("No prediction found in the API response.")
                    else:
                        st.success("🎉 Prediction successful!")

                        st.subheader("Prediction:")
                        # Assuming prediction is a list with one float value
                        prediction_value = prediction[0] if isinstance(prediction, list) else prediction
                        st.write(f"The prediction for this patient is: {prediction_value:.4f}")

                        # Create a new column with the prediction value
                        df['Prediction'] = prediction_value

                        st.subheader("Data with Prediction")
                        st.dataframe(df)

                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="Download Data with Prediction as CSV",
                            data=csv,
                            file_name="patient_data_with_prediction.csv",
                            mime="text/csv",
                        )
                except requests.RequestException as e:
                    st.error(f"Error communicating with the server: {str(e)}")
                    st.write("Response content:", response.text)
    except Exception as e:
        st.error(f"Error processing the file: {str(e)}")
else:
    st.info("👆 Please upload a CSV file to get a prediction.")

st.markdown("---")
st.markdown("© 2024 ICU Watch. All rights reserved.")
