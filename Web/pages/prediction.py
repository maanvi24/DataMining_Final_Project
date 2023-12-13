import streamlit as st
import joblib
import os

# Load Models
current_directory = os.path.dirname(os.path.abspath(__file__))

# Load Model for Movement
model_path_movement = os.path.join(current_directory, 'Logistic Regression_accuracy_0.61.joblib')
try:
    loaded_model_movement = joblib.load(model_path_movement)
except Exception as e:
    st.error(f"Error loading movement model: {e}")
    st.stop()

# Load Model for Sentiment
model_path_sentiment = os.path.join(current_directory, 'Random Forest Regression_mse_0.02_r2_0.22.joblib')
try:
    loaded_model_sentiment = joblib.load(model_path_sentiment)
except Exception as e:
    st.error(f"Error loading sentiment model: {e}")
    st.stop()

# Load Models for Relevance
model_path_relevance = os.path.join(current_directory, 'best_models_dictionary.joblib')
try:
    models_path_relevance = joblib.load(model_path_relevance)
except Exception as e:
    st.error(f"Error loading relevance models: {e}")
    st.stop()

# Define the predefined relevance topics
predefined_relevance_topics = [
    'Blockchain',
    'Earnings',
    'IPO',
    'Mergers & Acquisitions',
    'Financial Markets',
    'Energy & Transportation',
    'Finance',
    'Life Sciences',
    'Manufacturing',
    'Real Estate & Construction',
    'Retail & Wholesale',
    'Technology'
]

# Streamlit App
st.title("Predictions Generator")

# Input for article text
article_text = st.text_area("Enter article text...")

# Predict button
if st.button("Predict"):
    st.write("Predicting...")

    # Send request to Flask server for prediction
    prediction_response = loaded_model_movement.predict([article_text])
    likelihood = loaded_model_movement.predict_proba([article_text])[0][1] * 100

    # Display prediction and other results
    st.write("Prediction Result:", 'up' if prediction_response[0] == 1 else 'down')

    if prediction_response[0] == 1 and likelihood is not None:
        st.write(f"There is a {likelihood:.2f}% likelihood of the stock going up.")
    elif prediction_response[0] == 0 and likelihood is not None:
        st.write(f"There is a {100 - likelihood:.2f}% likelihood of the stock going down.")
    else:
        st.warning("Unable to determine prediction result or likelihood.")

    sentiment_prediction = loaded_model_sentiment.predict([article_text])[0]
    st.write(f"Sentiment Score: {round(sentiment_prediction, 2)}")

    for topic in predefined_relevance_topics:
        relevance_prediction = models_path_relevance[topic].predict([article_text])[0]
        st.write(f"Relevance Score for {topic}: {round(float(relevance_prediction), 2)}")

    st.success("Prediction completed!")
