import os
import streamlit as st
import pandas as pd


# Define the base URI of the API
#   - Potential sources are in `.streamlit/secrets.toml` or in the Secrets section
#     on Streamlit Cloud
#   - The source selected is based on the shell variable passend when launching streamlit
#     (shortcuts are included in Makefile). By default it takes the cloud API url
if 'API_URI' in os.environ:
    BASE_URI = st.secrets[os.environ.get('API_URI')]
else:
    BASE_URI = st.secrets['cloud_api_uri']
# Add a '/' at the end if it's not there
BASE_URI = BASE_URI if BASE_URI.endswith('/') else BASE_URI + '/'
# Define the url to be used by requests.get to get a prediction (adapt if needed)
url = BASE_URI + 'predict'

# Just displaying the source for the API. Remove this in your final version.
#st.markdown(f"Working with {url}")

#st.markdown("Now, the rest is up to you. Start creating your page.")


# TODO: Add some titles, introduction, ...
st.title("ICU Watch - Sepsis Prediction")
st.header("Welcome to our prediction service")
st.markdown("""
Our platform leverages advanced data science to provide predictions and insights,
enhancing patient care and operational efficiency. Our goal is to predict Sepsis 6
hours prior appearance.""")


# TODO: Request user input
#user_input = st.text_input("Enter your data for prediction:")
user_input = st.file_uploader("Upload your csv here.")
if user_input:
    df = pd.DataFrame(user_input)
    st.write(df)

    files = {'file': user_input}
    response = requests.post(url, files = files)


# TODO: Call the API using the user's input
#   - url is already defined above
#   - create a params dict based on the user's input
#   - finally call your API using the requests package
import requests


# TODO: retrieve the results
#   - add a little check if you got an ok response (status code 200) or something else
#   - retrieve the prediction from the JSON
if user_input:
    if response.status_code == 200:
        prediction = response.json().get('prediction')
        st.success(f"The prediction is: {prediction}") # display the prediction in some fancy way to the user
    else:
        st.error("There was an error with the API request.")





# TODO: [OPTIONAL] maybe you can add some other pages?
#   - some statistical data you collected in graphs
#   - description of your product
#   - a 'Who are we?'-page
