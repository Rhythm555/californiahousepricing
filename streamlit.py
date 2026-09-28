import streamlit as st
import requests

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="California House Price Predictor",
    page_icon="🏡",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #eef4ff 0%, #f8fbff 100%);
    }

    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #173b65;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 17px;
        color: #60758c;
        margin-bottom: 25px;
    }

    .result-card {
        background: white;
        padding: 28px;
        border-radius: 18px;
        border: 1px solid #dce7f5;
        box-shadow: 0 5px 18px rgba(30, 70, 120, 0.08);
        text-align: center;
    }

    .result-label {
        color: #60758c;
        font-size: 16px;
        font-weight: 600;
    }

    .result-value {
        color: #176b52;
        font-size: 38px;
        font-weight: 800;
        margin-top: 8px;
    }

    div.stButton > button {
        background-color: #176b52;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 12px 25px;
        font-weight: 700;
        width: 100%;
    }

    div.stButton > button:hover {
        background-color: #10533f;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


# ---------------- HEADER ----------------
st.markdown(
    '<div class="main-title">🏡 California House Price Predictor</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Estimate a house value using machine learning. Enter the property and location details below.</div>',
    unsafe_allow_html=True
)

st.divider()

# ---------------- INPUT FORM ----------------
st.subheader("📋 Property Information")

with st.form("house_prediction_form"):

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🏠 Housing Details")

        med_inc = st.number_input(
            "Median Income",
            min_value=0.0,
            value=3.5,
            step=0.1,
            help="Median income in the district, in units of $10,000."
        )

        house_age = st.number_input(
            "House Age",
            min_value=0.0,
            value=25.0,
            step=1.0
        )

        ave_rooms = st.number_input(
            "Average Rooms",
            min_value=0.1,
            value=5.0,
            step=0.1
        )

        ave_bedrms = st.number_input(
            "Average Bedrooms",
            min_value=0.1,
            value=1.0,
            step=0.1
        )

    with col2:
        st.markdown("#### 📍 Population & Location")

        population = st.number_input(
            "Population",
            min_value=0.0,
            value=1000.0,
            step=10.0
        )

        ave_occup = st.number_input(
            "Average Occupancy",
            min_value=0.1,
            value=3.0,
            step=0.1
        )

        latitude = st.number_input(
            "Latitude",
            min_value=32.0,
            max_value=42.0,
            value=34.05,
            step=0.01,
            format="%.4f"
        )

        longitude = st.number_input(
            "Longitude",
            min_value=-125.0,
            max_value=-114.0,
            value=-118.24,
            step=0.01,
            format="%.4f"
        )

    st.markdown("---")
    predict_button = st.form_submit_button("🔍 Predict House Price")


# ---------------- PREDICTION ----------------
if predict_button:

    if ave_bedrms > ave_rooms:
        st.error("Average bedrooms cannot be greater than average rooms.")

    else:
        input_data = {
            "MedInc": med_inc,
            "HouseAge": house_age,
            "AveRooms": ave_rooms,
            "AveBedrms": ave_bedrms,
            "Population": population,
            "AveOccup": ave_occup,
            "Latitude": latitude,
            "Longitude": longitude
        }

        with st.spinner("Analyzing property details..."):

            try:
                response = requests.post(
                    "http://127.0.0.1:8000/predict",
                    json=input_data,
                    timeout=30
                )

                if response.status_code == 200:
                    result = response.json()
                    prediction = float(result["prediction"])

                    st.success("Prediction completed successfully!")

                    st.markdown(
                        f"""
                        <div class="result-card">
                            <div class="result-label">Predicted House Value</div>
                            <div class="result-value">${prediction * 100000:,.0f}</div>
                            <p style="color:#60758c;">
                                Estimated value based on your model
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.info(
                        f"Raw model prediction: {prediction:.4f} "
                        "(in units of $100,000)"
                    )

                else:
                    st.error(
                        f"API Error: {response.status_code} — {response.text}"
                    )

            except requests.exceptions.ConnectionError:
                st.error(
                    "Could not connect to FastAPI. "
                    "Make sure your backend is running."
                )

            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {e}")


# ---------------- FOOTER ----------------
st.divider()
st.caption("Built with Streamlit, FastAPI and Scikit-learn | California Housing Prediction")