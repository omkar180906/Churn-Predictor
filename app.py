"""
Customer Churn Prediction System
================================
A Streamlit application for predicting customer churn
using a pre-trained Random Forest Classifier.

Author: ML Engineering Team
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import warnings
import logging
from typing import Optional, Dict, Any, Tuple

# Visualization imports
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns

# Suppress version mismatch warnings for model loading
warnings.filterwarnings("ignore", category=UserWarning)

# Configure logging for developer debugging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# ============================================================
# Page Configuration
# ============================================================
st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="C",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# Custom CSS — Clean, Professional Styling
# ============================================================
def inject_custom_css():
    """Inject custom CSS for the DDE3E8, 3A0F34, and EAAA00 color scheme."""
    st.markdown("""
    <style>
    /* ---- Global Font Stack (Fast & Native) ---- */
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        color: #3A0F34;
    }

    /* ---- Solid Opaque Background & Permanent Anti-Ghosting Rules ---- */
    html, body, [data-testid="stAppViewContainer"], .stApp, section.main, [data-testid="stMain"] {
        background-color: #DDE3E8 !important;
        opacity: 1 !important;
    }

    /* 1. Eliminate stale element watermarks: completely hide stale elements from prior page runs */
    [data-stale="true"],
    [data-stale="true"] *,
    div[data-stale="true"],
    [data-testid="stElementContainer"][data-stale="true"],
    .element-container[data-stale="true"],
    div.stApp[data-test-script-state="running"] [data-stale="true"] {
        opacity: 0 !important;
        display: none !important;
        visibility: hidden !important;
        transition: none !important;
        pointer-events: none !important;
    }

    /* 2. Never dim running containers */
    div.stApp[data-test-script-state="running"],
    div.stApp[data-test-script-state="running"] [data-testid="stAppViewContainer"],
    div.stApp[data-test-script-state="running"] [data-testid="stMain"],
    div.stApp[data-test-script-state="running"] [data-testid="stVerticalBlock"] {
        opacity: 1 !important;
        filter: none !important;
        transition: none !important;
    }

    /* 3. Active elements remain fully opaque with 0 transition delay */
    .element-container:not([data-stale="true"]),
    [data-testid="stElementContainer"]:not([data-stale="true"]),
    [data-testid="stVerticalBlock"] > div:not([data-stale="true"]) {
        opacity: 1 !important;
        filter: none !important;
        transition: none !important;
    }

    /* 4. Hide Streamlit rerun status spinner and toolbar completely */
    div[data-testid="stStatusWidget"],
    .stStatusWidget,
    div[data-testid="stToolbar"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* ---- Hide default Streamlit branding ---- */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ---- Stat cards ---- */
    .stat-card {
        background: #FFFFFF;
        border: 1px solid #DDE3E8;
        border-top: 4px solid #EAAA00;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(58, 15, 52, 0.05);
    }
    .stat-card .stat-label {
        font-size: 12px;
        font-weight: 600;
        color: #3A0F34;
        opacity: 0.75;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        margin: 0 0 6px 0;
    }
    .stat-card .stat-value {
        font-size: 26px;
        font-weight: 800;
        color: #3A0F34;
        margin: 0;
    }

    /* ---- Result cards ---- */
    .result-card {
        border-radius: 8px;
        padding: 24px;
        text-align: center;
        margin: 12px 0;
        border: 2px solid;
        box-shadow: 0 4px 12px rgba(58, 15, 52, 0.08);
    }
    .result-churn {
        background: #3A0F34;
        border-color: #EAAA00;
        color: #FFFFFF;
    }
    .result-churn h2 {
        color: #EAAA00 !important;
        font-weight: 800;
    }
    .result-churn p {
        color: #DDE3E8 !important;
    }
    .result-no-churn {
        background: #FFFFFF;
        border-color: #EAAA00;
        color: #3A0F34;
    }
    .result-no-churn h2 {
        color: #3A0F34 !important;
        font-weight: 800;
    }
    .result-no-churn p {
        color: #3A0F34 !important;
    }

    /* ---- Risk badges ---- */
    .risk-low {
        background: #FFFFFF;
        color: #3A0F34;
        border: 2px solid #DDE3E8;
        padding: 8px 18px;
        border-radius: 6px;
        display: inline-block;
        font-weight: 700;
        font-size: 14px;
        letter-spacing: 0.5px;
    }
    .risk-medium {
        background: #EAAA00;
        color: #3A0F34;
        border: 2px solid #EAAA00;
        padding: 8px 18px;
        border-radius: 6px;
        display: inline-block;
        font-weight: 700;
        font-size: 14px;
        letter-spacing: 0.5px;
    }
    .risk-high {
        background: #3A0F34;
        color: #EAAA00;
        border: 2px solid #EAAA00;
        padding: 8px 18px;
        border-radius: 6px;
        display: inline-block;
        font-weight: 700;
        font-size: 14px;
        letter-spacing: 0.5px;
    }

    /* ---- Section headers ---- */
    .section-header {
        font-size: 26px;
        font-weight: 800;
        color: #3A0F34;
        margin-bottom: 4px;
        letter-spacing: -0.3px;
    }
    .section-subheader {
        font-size: 15px;
        color: #3A0F34;
        opacity: 0.75;
        margin-bottom: 20px;
    }

    /* ---- Page header ---- */
    .page-header {
        padding: 30px 0 20px 0;
    }
    .page-title {
        font-size: 34px;
        font-weight: 800;
        color: #3A0F34;
        margin-bottom: 6px;
        line-height: 1.25;
    }
    .page-subtitle {
        font-size: 16px;
        color: #3A0F34;
        opacity: 0.8;
        font-weight: 400;
        margin-bottom: 20px;
    }

    /* ---- Info box ---- */
    .info-box {
        background: #FFFFFF;
        border: 1px solid #DDE3E8;
        border-left: 5px solid #EAAA00;
        border-radius: 6px;
        padding: 16px;
        margin: 14px 0;
        font-size: 14px;
        color: #3A0F34;
        box-shadow: 0 2px 4px rgba(58, 15, 52, 0.04);
    }

    /* ---- Recommendation box ---- */
    .recommendation-box {
        background: #FFFFFF;
        border-radius: 6px;
        padding: 20px;
        margin: 14px 0;
        border: 1px solid #DDE3E8;
        color: #3A0F34;
        box-shadow: 0 2px 6px rgba(58, 15, 52, 0.05);
    }
    .rec-low {
        border-left: 5px solid #DDE3E8;
    }
    .rec-medium {
        border-left: 5px solid #EAAA00;
    }
    .rec-high {
        border-left: 5px solid #3A0F34;
    }

    /* ---- Sidebar styling ---- */
    [data-testid="stSidebar"] {
        background: #3A0F34 !important;
    }
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3,
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown li,
    [data-testid="stSidebar"] .stMarkdown span,
    [data-testid="stSidebar"] label {
        color: #DDE3E8 !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: rgba(221, 227, 232, 0.2) !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label span {
        color: #DDE3E8 !important;
    }

    /* ---- Divider ---- */
    .custom-divider {
        height: 3px;
        background: linear-gradient(90deg, #3A0F34 0%, #EAAA00 50%, #DDE3E8 100%);
        margin: 24px 0;
        border-radius: 2px;
    }

    /* ---- Streamlit form submit button ---- */
    .stButton > button {
        background: #3A0F34;
        color: #EAAA00;
        border: 2px solid #EAAA00;
        border-radius: 6px;
        padding: 12px 24px;
        font-weight: 700;
        font-size: 15px;
        letter-spacing: 0.5px;
        width: 100%;
        transition: all 0.25s ease;
        box-shadow: 0 4px 10px rgba(58, 15, 52, 0.2);
    }
    .stButton > button:hover {
        background: #EAAA00;
        color: #3A0F34;
        border-color: #3A0F34;
        box-shadow: 0 6px 14px rgba(234, 170, 0, 0.35);
    }

    /* ---- Progress bar ---- */
    .stProgress > div > div > div > div {
        background-color: #EAAA00 !important;
    }

    /* ---- Tabs styling ---- */
    button[data-baseweb="tab"] {
        color: #3A0F34 !important;
        font-weight: 600;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #3A0F34 !important;
        border-bottom-color: #EAAA00 !important;
    }
    div[data-baseweb="tab-highlight"] {
        background-color: #EAAA00 !important;
    }

    /* Form wrappers and cards */
    div[data-testid="stForm"] {
        background: #FFFFFF;
        border: 1px solid #DDE3E8;
        border-radius: 8px;
        padding: 24px;
        box-shadow: 0 4px 12px rgba(58, 15, 52, 0.04);
    }
    div[data-testid="stExpander"] {
        background: #FFFFFF;
        border: 1px solid #DDE3E8 !important;
        border-radius: 6px;
    }
    </style>
    """, unsafe_allow_html=True)


# ============================================================
# Data Loading & Caching
# ============================================================

@st.cache_resource
def load_model() -> Optional[Dict[str, Any]]:
    """Load the trained model and feature names from the pickle file.
    
    The original pkl was saved as {"model": rfc, "features_names": [...]},
    but sklearn version differences may cause it to unpickle as the model
    directly. We handle both cases and always use model.feature_names_in_
    as the authoritative feature source when available.
    """
    try:
        model_data = joblib.load("Customer_churn_model.pkl")
        if isinstance(model_data, dict):
            model = model_data.get("model")
            feature_names = model_data.get("features_names", [])
        else:
            # sklearn version mismatch: pkl unpickles as the model directly
            model = model_data
            feature_names = []

        # Always prefer model.feature_names_in_ as the authoritative source
        if hasattr(model, 'feature_names_in_'):
            feature_names = list(model.feature_names_in_)

        if not feature_names:
            logger.error("Could not determine feature names from model.")
            return None

        logger.info("Model loaded successfully.")
        return {"model": model, "feature_names": feature_names}
    except FileNotFoundError:
        logger.error("Customer_churn_model.pkl not found.")
        return None
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return None


@st.cache_resource
def load_encoders() -> Optional[Dict]:
    """Load the label encoders from the pickle file."""
    try:
        encoders = joblib.load("encoders.pkl")
        logger.info("Encoders loaded successfully.")
        return encoders
    except FileNotFoundError:
        logger.error("encoders.pkl not found.")
        return None
    except Exception as e:
        logger.error(f"Error loading encoders: {e}")
        return None


@st.cache_data
def load_dataset() -> Optional[pd.DataFrame]:
    """Load the customer churn dataset for analytics."""
    try:
        df = pd.read_csv("miniprojectchurn.csv")
        # TotalCharges is stored as object in the original CSV — coerce to numeric
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
        df = df.dropna(subset=['TotalCharges'])
        logger.info(f"Dataset loaded successfully. Shape: {df.shape}")
        return df
    except FileNotFoundError:
        logger.warning("miniprojectchurn.csv not found.")
        return None
    except Exception as e:
        logger.error(f"Error loading dataset: {e}")
        return None


# ============================================================
# Helper Functions
# ============================================================

def encode_input(input_data: Dict[str, Any], encoders: Dict) -> Optional[Dict[str, Any]]:
    """
    Encode categorical inputs using the saved label encoders.
    Returns encoded dict or None if encoding fails.
    """
    encoded = input_data.copy()
    for col, encoder in encoders.items():
        if col in encoded:
            val = encoded[col]
            if val in list(encoder.classes_):
                encoded[col] = int(encoder.transform([val])[0])
            else:
                return None  # Unknown category
    return encoded


def prepare_input(encoded_data: Dict[str, Any], feature_names: list) -> Optional[pd.DataFrame]:
    """
    Create a DataFrame with the exact feature order expected by the model.
    Returns None if feature count doesn't match.
    """
    try:
        df = pd.DataFrame([encoded_data])[feature_names]
        if df.shape[1] != 19:
            return None
        return df
    except KeyError as e:
        logger.error(f"Feature ordering error: {e}")
        return None


def make_prediction(model, input_df: pd.DataFrame) -> Tuple[int, float]:
    """Run prediction and return (class, churn_probability)."""
    prediction = model.predict(input_df)[0]
    proba = model.predict_proba(input_df)[0]
    churn_probability = float(proba[1])  # Probability of class 1 (Churn)
    return int(prediction), churn_probability


def calculate_risk(churn_probability: float) -> str:
    """Classify risk level based on churn probability."""
    if churn_probability <= 0.30:
        return "LOW"
    elif churn_probability <= 0.60:
        return "MEDIUM"
    else:
        return "HIGH"


def generate_recommendation(risk_level: str) -> str:
    """Generate a business recommendation based on risk level."""
    recommendations = {
        "LOW": "Low churn risk. Continue standard engagement and monitor periodically.",
        "MEDIUM": "Moderate churn risk. Consider reaching out with a personalized offer or checking in on satisfaction.",
        "HIGH": "High churn risk. Prioritize retention: offer a discount, assign dedicated support, or propose a longer-term contract.",
    }
    return recommendations.get(risk_level, "Unable to generate recommendation.")


def render_stat_card(label: str, value: str):
    """Render a clean stat card."""
    st.markdown(f"""
    <div class="stat-card">
        <p class="stat-label">{label}</p>
        <p class="stat-value">{value}</p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# Sidebar
# ============================================================

def render_sidebar():
    """Render the navigation sidebar."""
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; padding: 20px 0;">
            <h2 style="margin: 8px 0 4px 0; font-weight: 800; color: #EAAA00; font-size: 20px; letter-spacing: 0.5px;">
                Churn Prediction
            </h2>
            <p style="font-size: 13px; color: #DDE3E8; opacity: 0.85;">Customer risk analysis tool</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        page = st.radio(
            "Navigation",
            ["Home", "Prediction", "Analytics", "Model Details"],
            label_visibility="visible",
        )

        st.markdown("---")

        st.markdown("""
        <div style="padding: 16px; background: rgba(221, 227, 232, 0.1); 
                    border: 1px solid rgba(234, 170, 0, 0.35);
                    border-radius: 6px; margin-top: 12px;">
            <p style="font-size: 12px; text-transform: uppercase; letter-spacing: 0.8px; 
                      font-weight: 700; margin-bottom: 12px; color: #EAAA00;">System</p>
            <p style="margin: 6px 0; font-size: 13px; color: #DDE3E8;"><strong style="color: #FFFFFF;">Model:</strong> Random Forest</p>
            <p style="margin: 6px 0; font-size: 13px; color: #DDE3E8;"><strong style="color: #FFFFFF;">Features:</strong> 19</p>
            <p style="margin: 6px 0; font-size: 13px; color: #DDE3E8;"><strong style="color: #FFFFFF;">Type:</strong> Binary Classification</p>
            <p style="margin: 6px 0; font-size: 13px; color: #DDE3E8;"><strong style="color: #FFFFFF;">Trees:</strong> 100</p>
        </div>
        """, unsafe_allow_html=True)

    return page


# ============================================================
# PAGE 1 — HOME
# ============================================================

def page_home():
    """Render the Home / Landing page."""
    st.markdown("""
    <div class="page-header">
        <div class="page-title">Customer Churn Prediction</div>
        <div class="page-subtitle">Predict whether a customer is likely to leave based on their profile and usage patterns.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # About section
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown("### What is customer churn?")
        st.markdown("""
        Churn is when a customer stops using your product or service. Predicting it early
        lets you intervene before the customer leaves, which is significantly cheaper than
        acquiring a replacement.
        """)
        st.markdown("### Why predict churn?")
        st.markdown("""
        - Identify at-risk customers before they leave
        - Focus retention efforts where they matter most
        - Retention costs a fraction of new customer acquisition
        - Replace guesswork with data-driven decisions
        """)

    with col2:
        st.markdown("### What this tool does")
        st.markdown("""
        This system uses a trained Random Forest model (100 trees, 19 input features) to
        analyze a customer's profile and predict churn. For each prediction you get:
        
        1. **Prediction** - Will the customer churn or stay?
        2. **Probability** - Model confidence as a percentage
        3. **Risk level** - Low, Medium, or High
        4. **Recommendation** - A suggested retention action
        """)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Feature list
    with st.expander("View all 19 input features", expanded=False):
        features = [
            ("Gender", "Customer's gender"),
            ("Senior Citizen", "Whether the customer is a senior citizen"),
            ("Partner", "Whether the customer has a partner"),
            ("Dependents", "Whether the customer has dependents"),
            ("Tenure", "Number of months the customer has stayed"),
            ("Phone Service", "Whether the customer has phone service"),
            ("Multiple Lines", "Whether the customer has multiple lines"),
            ("Internet Service", "Type of internet service"),
            ("Online Security", "Whether the customer has online security"),
            ("Online Backup", "Whether the customer has online backup"),
            ("Device Protection", "Whether the customer has device protection"),
            ("Tech Support", "Whether the customer has tech support"),
            ("Streaming TV", "Whether the customer streams TV"),
            ("Streaming Movies", "Whether the customer streams movies"),
            ("Contract", "Type of contract"),
            ("Paperless Billing", "Whether the customer uses paperless billing"),
            ("Payment Method", "Customer's payment method"),
            ("Monthly Charges", "Amount charged monthly"),
            ("Total Charges", "Total amount charged"),
        ]
        feat_df = pd.DataFrame(features, columns=["Feature", "Description"])
        feat_df.index = range(1, len(feat_df) + 1)
        st.table(feat_df)

    # How to use
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown("### How to use")
    st.markdown("""
    1. Go to **Prediction** in the sidebar.
    2. Fill in the customer's details (demographics, services, billing).
    3. Click **Predict** to see the result, probability, risk level, and a recommended action.
    """)


# ============================================================
# PAGE 2 — PREDICTION
# ============================================================

def page_prediction(model_data: Dict, encoders: Dict):
    """Render the Customer Churn Prediction page."""
    model = model_data["model"]
    feature_names = model_data["feature_names"]

    st.markdown('<div class="section-header">Churn Prediction</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">Enter customer details below, then click Predict.</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Input form
    with st.form(key="prediction_form"):
        st.markdown("#### Customer Demographics")
        d1, d2, d3, d4 = st.columns(4)
        with d1:
            gender = st.selectbox("Gender", options=["Female", "Male"], index=0,
                                  help="Customer's gender")
        with d2:
            senior_citizen = st.selectbox("Senior Citizen", options=["No", "Yes"], index=0,
                                          help="Whether the customer is 65 or older")
        with d3:
            partner = st.selectbox("Partner", options=["No", "Yes"], index=0,
                                   help="Whether the customer has a partner")
        with d4:
            dependents = st.selectbox("Dependents", options=["No", "Yes"], index=0,
                                      help="Whether the customer has dependents")

        st.markdown("---")
        st.markdown("#### Services")
        s1, s2, s3 = st.columns(3)
        with s1:
            phone_service = st.selectbox("Phone Service", options=["No", "Yes"], index=1)
            multiple_lines = st.selectbox("Multiple Lines",
                                          options=["No", "Yes", "No phone service"], index=0)
        with s2:
            internet_service = st.selectbox("Internet Service",
                                            options=["DSL", "Fiber optic", "No"], index=0)
            online_security = st.selectbox("Online Security",
                                           options=["No", "Yes", "No internet service"], index=0)
        with s3:
            online_backup = st.selectbox("Online Backup",
                                         options=["No", "Yes", "No internet service"], index=0)
            device_protection = st.selectbox("Device Protection",
                                             options=["No", "Yes", "No internet service"], index=0)

        s4, s5, s6 = st.columns(3)
        with s4:
            tech_support = st.selectbox("Tech Support",
                                        options=["No", "Yes", "No internet service"], index=0)
        with s5:
            streaming_tv = st.selectbox("Streaming TV",
                                        options=["No", "Yes", "No internet service"], index=0)
        with s6:
            streaming_movies = st.selectbox("Streaming Movies",
                                            options=["No", "Yes", "No internet service"], index=0)

        st.markdown("---")
        st.markdown("#### Billing and Contract")
        b1, b2, b3, b4 = st.columns(4)
        with b1:
            contract = st.selectbox("Contract",
                                    options=["Month-to-month", "One year", "Two year"], index=0)
        with b2:
            paperless_billing = st.selectbox("Paperless Billing", options=["No", "Yes"], index=0)
        with b3:
            payment_method = st.selectbox("Payment Method",
                                          options=["Electronic check", "Mailed check",
                                                   "Bank transfer (automatic)",
                                                   "Credit card (automatic)"],
                                          index=0)
        with b4:
            tenure = st.number_input("Tenure (months)", min_value=0, max_value=72,
                                     value=12, step=1,
                                     help="Number of months the customer has stayed with the company")

        c1, c2 = st.columns(2)
        with c1:
            monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0,
                                              max_value=500.0, value=50.0, step=0.05,
                                              format="%.2f")
        with c2:
            total_charges = st.number_input("Total Charges ($)", min_value=0.0,
                                            max_value=10000.0, value=600.0, step=0.05,
                                            format="%.2f")

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Predict")

    # ---- Process Prediction ----
    if submitted:
        # Validate inputs
        errors = []
        if monthly_charges < 0:
            errors.append("Monthly Charges must be non-negative.")
        if total_charges < 0:
            errors.append("Total Charges must be non-negative.")
        if tenure < 0 or tenure > 72:
            errors.append("Tenure should be between 0 and 72 months.")

        if errors:
            for err in errors:
                st.error(err)
            return

        # Build raw input dict
        senior_citizen_val = 1 if senior_citizen == "Yes" else 0

        raw_input = {
            "gender": gender,
            "SeniorCitizen": senior_citizen_val,
            "Partner": partner,
            "Dependents": dependents,
            "tenure": tenure,
            "PhoneService": phone_service,
            "MultipleLines": multiple_lines,
            "InternetService": internet_service,
            "OnlineSecurity": online_security,
            "OnlineBackup": online_backup,
            "DeviceProtection": device_protection,
            "TechSupport": tech_support,
            "StreamingTV": streaming_tv,
            "StreamingMovies": streaming_movies,
            "Contract": contract,
            "PaperlessBilling": paperless_billing,
            "PaymentMethod": payment_method,
            "MonthlyCharges": monthly_charges,
            "TotalCharges": total_charges,
        }

        # Encode categorical features
        encoded = encode_input(raw_input, encoders)
        if encoded is None:
            st.error("Unable to process one or more categories. Please select valid options for all fields.")
            return

        # Prepare input DataFrame
        input_df = prepare_input(encoded, feature_names)
        if input_df is None:
            st.error("Feature mismatch detected. The input does not match the model's expected 19 features.")
            return

        # Verify feature count
        if input_df.shape[1] != 19:
            st.error(f"Expected 19 features, but got {input_df.shape[1]}. Cannot proceed with prediction.")
            return

        # Make prediction
        try:
            prediction, churn_probability = make_prediction(model, input_df)
        except Exception as e:
            st.error(f"Prediction failed. Please check your inputs. Error: {e}")
            logger.error(f"Prediction error: {e}")
            return

        risk_level = calculate_risk(churn_probability)
        recommendation = generate_recommendation(risk_level)

        # ---- Display Results ----
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Results</div>', unsafe_allow_html=True)

        # Result card row
        r1, r2, r3 = st.columns(3)

        with r1:
            if prediction == 1:
                st.markdown("""
                <div class="result-card result-churn">
                    <p style="margin:0; font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:0.8px; color:#DDE3E8;">Prediction</p>
                    <h2 style="margin:8px 0 4px 0; font-size:22px; color:#EAAA00;">Customer Will Churn</h2>
                    <p style="margin:0; font-size:13px; color:#DDE3E8;">Likely to leave</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="result-card result-no-churn">
                    <p style="margin:0; font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:0.8px; color:#3A0F34; opacity:0.8;">Prediction</p>
                    <h2 style="margin:8px 0 4px 0; font-size:22px; color:#3A0F34;">Customer Will Stay</h2>
                    <p style="margin:0; font-size:13px; color:#3A0F34; opacity:0.8;">Likely to remain</p>
                </div>
                """, unsafe_allow_html=True)

        with r2:
            prob_pct = churn_probability * 100
            st.markdown(f"""
            <div class="stat-card">
                <p class="stat-label">Churn Probability</p>
                <p class="stat-value">{prob_pct:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)
            st.progress(churn_probability)

        with r3:
            risk_css = {"LOW": "risk-low", "MEDIUM": "risk-medium", "HIGH": "risk-high"}[risk_level]
            st.markdown(f"""
            <div style="text-align:center; padding: 20px;">
                <p style="margin-bottom: 12px; color: #3A0F34; font-size: 12px; font-weight:600; text-transform:uppercase; letter-spacing:0.6px;">Risk Level</p>
                <span class="{risk_css}">{risk_level} RISK</span>
            </div>
            """, unsafe_allow_html=True)

        # Recommendation box
        st.markdown("<br>", unsafe_allow_html=True)
        rec_css = {"LOW": "rec-low", "MEDIUM": "rec-medium", "HIGH": "rec-high"}[risk_level]
        st.markdown(f"""
        <div class="recommendation-box {rec_css}">
            <h4 style="margin: 0 0 8px 0; color: #3A0F34;">Suggested Action</h4>
            <p style="margin: 0; font-size: 14px; line-height: 1.6; color: #3A0F34;">{recommendation}</p>
            <p style="margin: 8px 0 0 0; font-size: 12px; color: #3A0F34; opacity: 0.7; font-style: italic;">
                This recommendation is based on model predictions and should be used as guidance,
                not as a guarantee of preventing churn.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Detailed input summary
        with st.expander("View Input Summary", expanded=False):
            summary_df = pd.DataFrame([{k: str(v) for k, v in raw_input.items()}]).T
            summary_df.columns = ["Value"]
            summary_df.index.name = "Feature"
            st.dataframe(summary_df, width='stretch')


# ============================================================
# PAGE 3 — ANALYTICS DASHBOARD
# ============================================================

def page_analytics(model_data: Dict):
    """Render the Analytics Dashboard page."""
    model = model_data["model"]
    feature_names = model_data["feature_names"]
    df = load_dataset()

    st.markdown('<div class="section-header">Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">Summary statistics and charts from the customer dataset.</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    if df is None:
        st.warning("The customer dataset (miniprojectchurn.csv) is not available. "
                    "Analytics require the dataset. The Prediction page still works.")
        # Still show feature importance if model supports it
        if hasattr(model, 'feature_importances_'):
            _render_feature_importance(model, feature_names)
        return

    # ---- Key Metrics ----
    total = len(df)
    churned = len(df[df['Churn'] == 'Yes'])
    not_churned = len(df[df['Churn'] == 'No'])
    churn_rate = (churned / total) * 100
    avg_monthly = df['MonthlyCharges'].mean()
    avg_tenure = df['tenure'].mean()

    m1, m2, m3, m4, m5, m6 = st.columns(6)
    with m1:
        render_stat_card("Total Customers", f"{total:,}")
    with m2:
        render_stat_card("Churned", f"{churned:,}")
    with m3:
        render_stat_card("Retained", f"{not_churned:,}")
    with m4:
        render_stat_card("Churn Rate", f"{churn_rate:.1f}%")
    with m5:
        render_stat_card("Avg Monthly ($)", f"{avg_monthly:.2f}")
    with m6:
        render_stat_card("Avg Tenure (mo)", f"{avg_tenure:.0f}")

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # ---- Color palette ----
    palette = {"No": "#3A0F34", "Yes": "#EAAA00"}
    sns.set_style("whitegrid", {"grid.color": "#DDE3E8", "axes.edgecolor": "#DDE3E8"})
    plt.rcParams.update({
        'font.family': 'sans-serif',
        'font.size': 11,
        'text.color': '#3A0F34',
        'axes.labelcolor': '#3A0F34',
        'xtick.color': '#3A0F34',
        'ytick.color': '#3A0F34',
        'axes.titlesize': 13,
        'axes.titleweight': 'bold',
        'axes.titlecolor': '#3A0F34',
        'figure.facecolor': '#FFFFFF',
        'axes.facecolor': '#FFFFFF',
    })

    # ---- Charts ----
    tab1, tab2, tab3 = st.tabs(["Distribution and Contracts", "Services and Tenure", "Feature Importance"])

    with tab1:
        col1, col2 = st.columns(2)

        # Chart 1: Churn Distribution
        with col1:
            st.markdown("##### Churn Distribution")
            fig1, ax1 = plt.subplots(figsize=(6, 4))
            counts = df['Churn'].value_counts()
            bars = ax1.bar(counts.index, counts.values,
                           color=[palette['No'], palette['Yes']],
                           edgecolor='white', linewidth=2, width=0.5, 
                           zorder=3)
            for bar, val in zip(bars, counts.values):
                ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 40,
                         f"{val:,}", ha='center', fontweight='bold', fontsize=12)
            ax1.set_xlabel("Churn Status")
            ax1.set_ylabel("Number of Customers")
            ax1.set_title("Customer Churn Distribution")
            ax1.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig1)
            plt.close(fig1)

        # Chart 2: Churn by Contract
        with col2:
            st.markdown("##### Churn by Contract Type")
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            contract_data = df.groupby(['Contract', 'Churn']).size().unstack(fill_value=0)
            contract_data.plot(kind='bar', ax=ax2, color=[palette['No'], palette['Yes']],
                               edgecolor='white', linewidth=1.5, width=0.6, zorder=3)
            ax2.set_xlabel("Contract Type")
            ax2.set_ylabel("Number of Customers")
            ax2.set_title("Churn by Contract Type")
            ax2.legend(title="Churn", framealpha=0.9)
            ax2.set_xticklabels(ax2.get_xticklabels(), rotation=30, ha='right')
            ax2.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig2)
            plt.close(fig2)

        col3, col4 = st.columns(2)

        # Chart 3: Churn by Payment Method
        with col3:
            st.markdown("##### Churn by Payment Method")
            fig5, ax5 = plt.subplots(figsize=(6, 4))
            pm_data = df.groupby(['PaymentMethod', 'Churn']).size().unstack(fill_value=0)
            pm_data.plot(kind='bar', ax=ax5, color=[palette['No'], palette['Yes']],
                         edgecolor='white', linewidth=1.5, width=0.6, zorder=3)
            ax5.set_xlabel("Payment Method")
            ax5.set_ylabel("Number of Customers")
            ax5.set_title("Churn by Payment Method")
            ax5.legend(title="Churn", framealpha=0.9)
            ax5.set_xticklabels(ax5.get_xticklabels(), rotation=30, ha='right')
            ax5.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig5)
            plt.close(fig5)

        # Chart 4: Monthly Charges Distribution
        with col4:
            st.markdown("##### Monthly Charges by Churn Status")
            fig6, ax6 = plt.subplots(figsize=(6, 4))
            for label, color in palette.items():
                subset = df[df['Churn'] == label]['MonthlyCharges']
                ax6.hist(subset, bins=30, alpha=0.6, label=f"Churn={label}",
                         color=color, edgecolor='white', linewidth=0.8)
            ax6.set_xlabel("Monthly Charges ($)")
            ax6.set_ylabel("Frequency")
            ax6.set_title("Monthly Charges Distribution by Churn")
            ax6.legend(framealpha=0.9)
            ax6.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig6)
            plt.close(fig6)

    with tab2:
        col5, col6 = st.columns(2)

        # Chart 5: Churn by Internet Service
        with col5:
            st.markdown("##### Churn by Internet Service")
            fig3, ax3 = plt.subplots(figsize=(6, 4))
            inet_data = df.groupby(['InternetService', 'Churn']).size().unstack(fill_value=0)
            inet_data.plot(kind='bar', ax=ax3, color=[palette['No'], palette['Yes']],
                           edgecolor='white', linewidth=1.5, width=0.6, zorder=3)
            ax3.set_xlabel("Internet Service")
            ax3.set_ylabel("Number of Customers")
            ax3.set_title("Churn by Internet Service")
            ax3.legend(title="Churn", framealpha=0.9)
            ax3.set_xticklabels(ax3.get_xticklabels(), rotation=0)
            ax3.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig3)
            plt.close(fig3)

        # Chart 6: Churn by Tenure Group
        with col6:
            st.markdown("##### Churn by Tenure Group")
            fig4, ax4 = plt.subplots(figsize=(6, 4))
            df_copy = df.copy()
            df_copy['TenureGroup'] = pd.cut(df_copy['tenure'],
                                            bins=[0, 12, 36, 72],
                                            labels=['0-12 months', '13-36 months', '37+ months'],
                                            include_lowest=True)
            tenure_data = df_copy.groupby(['TenureGroup', 'Churn']).size().unstack(fill_value=0)
            tenure_data.plot(kind='bar', ax=ax4, color=[palette['No'], palette['Yes']],
                             edgecolor='white', linewidth=1.5, width=0.6, zorder=3)
            ax4.set_xlabel("Tenure Group")
            ax4.set_ylabel("Number of Customers")
            ax4.set_title("Churn by Tenure Group")
            ax4.legend(title="Churn", framealpha=0.9)
            ax4.set_xticklabels(ax4.get_xticklabels(), rotation=0)
            ax4.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig4)
            plt.close(fig4)

    with tab3:
        _render_feature_importance(model, feature_names)


def _render_feature_importance(model, feature_names):
    """Render feature importance chart and table."""
    if not hasattr(model, 'feature_importances_'):
        st.info("Feature importance is not available for this model.")
        return

    importances = model.feature_importances_
    fi_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    }).sort_values('Importance', ascending=True)

    st.markdown("##### Feature Importance (Random Forest)")
    st.markdown("""
    <div class="info-box">
        <strong>How to read this:</strong> Feature importance shows how much each feature contributes
        to the model's predictions. Higher values mean the feature has more influence on the output.
        This does <em>not</em> imply causation.
    </div>
    """, unsafe_allow_html=True)

    col_chart, col_table = st.columns([1.5, 1])

    with col_chart:
        fig, ax = plt.subplots(figsize=(8, 7))
        custom_fi_cmap = LinearSegmentedColormap.from_list("fi_plum_gold", ["#3A0F34", "#EAAA00"])
        colors = [custom_fi_cmap(i) for i in np.linspace(0.3, 1.0, len(fi_df))]
        bars = ax.barh(fi_df['Feature'], fi_df['Importance'], color=colors,
                       edgecolor='#3A0F34', linewidth=0.8, height=0.7)
        ax.set_xlabel("Importance Score", color='#3A0F34')
        ax.set_title("Feature Importance (Random Forest)", fontweight='bold', pad=15, color='#3A0F34')
        ax.grid(axis='x', alpha=0.5, color='#DDE3E8')
        for bar, val in zip(bars, fi_df['Importance']):
            ax.text(bar.get_width() + 0.003, bar.get_y() + bar.get_height()/2,
                    f'{val:.4f}', va='center', fontsize=9, fontweight='bold', color='#3A0F34')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with col_table:
        st.markdown("##### Importance Rankings")
        fi_table = fi_df.sort_values('Importance', ascending=False).reset_index(drop=True)
        fi_table.index = range(1, len(fi_table) + 1)
        fi_table['Importance'] = fi_table['Importance'].apply(lambda x: f"{x:.4f}")
        fi_table.index.name = "Rank"
        st.dataframe(fi_table, width='stretch', height=500)


# ============================================================
# PAGE 4 — MODEL INFORMATION
# ============================================================

def page_model_info(model_data: Dict):
    """Render the Model Information page."""
    model = model_data["model"]
    feature_names = model_data["feature_names"]

    st.markdown('<div class="section-header">Model Details</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subheader">Technical specifications and evaluation metrics for the Random Forest model.</div>',
                unsafe_allow_html=True)
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Two-column layout for explanation
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### What is Random Forest?")
        st.markdown("""
        Random Forest is an ensemble method that trains multiple decision trees on random
        subsets of the data and features. The final prediction is the majority vote across
        all trees.
        
        **Key properties:**
        - Combines predictions from many decision trees (bagging)
        - Each tree sees a random subset of features at each split
        - Resistant to overfitting compared to single decision trees
        - Provides built-in feature importance rankings
        - Handles both numerical and categorical features
        """)

    with col2:
        st.markdown("### Output interpretation")
        st.markdown("""
        This is a binary classification model with two possible outputs:
        
        | Class | Label | Meaning |
        |-------|-------|---------|
        | **0** | Not Churn | Customer is likely to stay |
        | **1** | Churn | Customer is likely to leave |
        
        The model also outputs a probability score between 0 and 1 for each class.
        The probability of Class 1 is used as the churn probability.
        """)

        st.markdown("### Hyperparameters")
        params = model.get_params()
        key_params = {
            'n_estimators': 'Number of Trees',
            'criterion': 'Split Criterion',
            'max_depth': 'Max Depth',
            'max_features': 'Max Features per Split',
            'min_samples_split': 'Min Samples to Split',
            'min_samples_leaf': 'Min Samples per Leaf',
            'random_state': 'Random State',
            'bootstrap': 'Bootstrap Sampling',
        }
        params_df = pd.DataFrame([
            {"Parameter": desc, "Value": str(params.get(key, "N/A"))}
            for key, desc in key_params.items()
        ])
        params_df.index = range(1, len(params_df) + 1)
        st.table(params_df)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # ---- Model Performance Metrics ----
    st.markdown("### Performance Metrics")
    st.markdown("""
    <div class="info-box">
        <strong>Note:</strong> These metrics were computed on the held-out test set
        (20% of the data). The training set was balanced using SMOTE.
    </div>
    """, unsafe_allow_html=True)

    # Display known metrics from the notebook evaluation
    perf1, perf2, perf3, perf4 = st.columns(4)
    with perf1:
        render_stat_card("Accuracy", "77.86%")
    with perf2:
        render_stat_card("Precision (Churn)", "58%")
    with perf3:
        render_stat_card("Recall (Churn)", "59%")
    with perf4:
        render_stat_card("F1 Score (Churn)", "58%")

    st.markdown("<br>", unsafe_allow_html=True)

    # Classification Report
    col_cr, col_cm = st.columns(2)

    with col_cr:
        st.markdown("##### Classification Report")
        report_data = {
            'Class': ['Not Churn (0)', 'Churn (1)', '', 'Accuracy', 'Macro Avg', 'Weighted Avg'],
            'Precision': ['0.85', '0.58', '', '', '0.72', '0.78'],
            'Recall': ['0.85', '0.59', '', '0.78', '0.72', '0.78'],
            'F1-Score': ['0.85', '0.58', '', '', '0.72', '0.78'],
            'Support': ['1036', '373', '', '1409', '1409', '1409'],
        }
        report_df = pd.DataFrame(report_data)
        report_df.index = [''] * len(report_df)
        st.table(report_df)

    with col_cm:
        st.markdown("##### Confusion Matrix")
        cm = np.array([[878, 158], [154, 219]])
        fig_cm, ax_cm = plt.subplots(figsize=(5, 4))
        custom_cm_cmap = LinearSegmentedColormap.from_list("custom_cm", ["#DDE3E8", "#EAAA00", "#3A0F34"])
        sns.heatmap(cm, annot=True, fmt='d', cmap=custom_cm_cmap,
                    xticklabels=['Predicted: Stay', 'Predicted: Churn'],
                    yticklabels=['Actual: Stay', 'Actual: Churn'],
                    linewidths=2, linecolor='#FFFFFF',
                    annot_kws={'size': 16, 'weight': 'bold', 'color': '#3A0F34'})
        ax_cm.set_title("Confusion Matrix", fontweight='bold', pad=12, color='#3A0F34')
        plt.tight_layout()
        st.pyplot(fig_cm)
        plt.close(fig_cm)

    # Confusion matrix explanation
    with st.expander("Understanding the Confusion Matrix", expanded=False):
        st.markdown("""
        | Cell | Name | Count | Meaning |
        |------|------|-------|---------|
        | Top-Left | **True Negative (TN)** | 878 | Correctly predicted the customer would stay |
        | Top-Right | **False Positive (FP)** | 158 | Incorrectly predicted churn (they actually stayed) |
        | Bottom-Left | **False Negative (FN)** | 154 | Incorrectly predicted stay (they actually churned) |
        | Bottom-Right | **True Positive (TP)** | 219 | Correctly predicted the customer would churn |
        
        > Recall for the churn class (59%) indicates how many actual churners we correctly identify.
        > In a business context, False Negatives (missing a customer who is actually going to churn)
        > can be particularly costly, as it means missing the opportunity to intervene.
        """)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Training methodology
    with st.expander("Training Methodology", expanded=False):
        st.markdown("""
        ### Data Preprocessing
        1. **Dataset**: 7,043 customer records with 21 features (including customerID and Churn target)
        2. **Label Encoding**: 15 categorical features were encoded using LabelEncoder
        3. **Train/Test Split**: 80/20 split with random_state=42
        4. **SMOTE**: Synthetic Minority Oversampling Technique was applied to balance the training set
           - Before SMOTE: Imbalanced (5,174 No vs 1,869 Yes)
           - After SMOTE: Balanced (4,138 No vs 4,138 Yes)
        
        ### Model Selection
        Three models were compared using 5-fold cross-validation:
        
        | Model | Cross-Validation Accuracy |
        |-------|--------------------------|
        | Decision Tree | 78% |
        | **Random Forest** | **84%** |
        | XGBoost | 83% |
        
        Random Forest was selected as the best-performing model.
        
        ### Scikit-learn Version
        The model was trained using scikit-learn 1.6.1.
        """)


# ============================================================
# Main Application
# ============================================================

def main():
    """Main application entry point."""
    inject_custom_css()

    # Load resources
    model_data = load_model()
    encoders = load_encoders()

    # Sidebar navigation
    page = render_sidebar()

    # Resource availability check
    model_available = model_data is not None
    encoders_available = encoders is not None

    # Route to selected page
    if page == "Home":
        page_home()

    elif page == "Prediction":
        if not model_available:
            st.error("Model could not be loaded. Please ensure Customer_churn_model.pkl "
                     "exists in the project directory.")
        elif not encoders_available:
            st.error("Encoders could not be loaded. Please ensure encoders.pkl "
                     "exists in the project directory.")
        else:
            page_prediction(model_data, encoders)

    elif page == "Analytics":
        if not model_available:
            st.error("Model could not be loaded. Feature importance cannot be displayed.")
        else:
            page_analytics(model_data)

    elif page == "Model Details":
        if not model_available:
            st.error("Model could not be loaded. Model information cannot be displayed.")
        else:
            page_model_info(model_data)


if __name__ == "__main__":
    main()
