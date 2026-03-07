import streamlit as st
import joblib
import os

# App Title
st.set_page_config(page_title="Agri-Intel Predictor", layout="centered")
st.title("🌾 Agri-Intel Predictor")

# පයිල් එක තියෙන තැන ස්වයංක්‍රීයව හොයාගන්න ක්‍රමය
base_path = os.path.dirname(__file__)
model_path = os.path.join(base_path, 'agri_intel_model.pkl')

# Model එක Load කිරීම
if os.path.exists(model_path):
    model = joblib.load(model_path)
    st.success("✅ Model Loaded Successfully!")
    
    # User Input
    rain = st.number_input("Rainfall value test", value=1000)
    
    if st.button("Predict"):
        # මෙහි 10, 10 කියන්නේ උඹේ මොඩලයට අවශ්‍ය අනිත් features (උදාහරණ ලෙස)
        prediction = model.predict([[rain, 10, 10]])
        st.balloons()
        st.header(f"Predicted Yield: {prediction[0][0]:.2f}")
else:
    st.error("❌ Model file not found. Make sure 'agri_intel_model.pkl' is in the same folder.")