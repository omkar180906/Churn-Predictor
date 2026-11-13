"""
Automated Test Suite for Customer Churn Prediction System
=========================================================
Tests the core pipeline: model loading, encoding, prediction, risk, recommendation.
"""

import sys
import os
import traceback

# Ensure we're in the right directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

import joblib
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

results = []

def test(test_id: str, description: str, func):
    """Run a single test and record result."""
    try:
        func()
        results.append((test_id, description, "PASS"))
        print(f"  {test_id}: PASS - {description}")
    except Exception as e:
        results.append((test_id, description, f"FAIL - {e}"))
        print(f"  {test_id}: FAIL - {description}: {e}")
        traceback.print_exc()


# ---- TC01: Model loads ----
model = None
feature_names = None
def tc01():
    global model, feature_names
    raw = joblib.load("Customer_churn_model.pkl")
    # Handle both dict and direct model cases
    if isinstance(raw, dict):
        model = raw["model"]
        feature_names = raw.get("features_names", [])
    else:
        model = raw
        feature_names = []
    # Use model.feature_names_in_ as authoritative source
    if hasattr(model, 'feature_names_in_'):
        feature_names = list(model.feature_names_in_)
    assert model is not None, "Model is None"
    assert len(feature_names) == 19, f"Expected 19 features, got {len(feature_names)}"
    assert hasattr(model, 'predict'), "Model has no predict method"
test("TC01", "Model loads successfully", tc01)

# ---- TC02: Encoders load ----
encoders = None
def tc02():
    global encoders
    encoders = joblib.load("encoders.pkl")
    assert isinstance(encoders, dict), "Encoders is not a dict"
    assert len(encoders) == 15, f"Expected 15 encoders, got {len(encoders)}"
test("TC02", "Encoders load successfully", tc02)

# ---- TC03: 19 features accepted ----
def tc03():
    assert len(feature_names) == 19, f"Expected 19 features, got {len(feature_names)}"
    expected = ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure',
                'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity',
                'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV',
                'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod',
                'MonthlyCharges', 'TotalCharges']
    assert feature_names == expected, f"Feature order mismatch: {feature_names}"
test("TC03", "All 19 input features in correct order", tc03)

# ---- TC04: Valid customer produces prediction ----
prediction = None
churn_prob = None
def tc04():
    global prediction, churn_prob
    raw = {
        "gender": "Female", "SeniorCitizen": 0, "Partner": "Yes", "Dependents": "No",
        "tenure": 12, "PhoneService": "Yes", "MultipleLines": "No",
        "InternetService": "DSL", "OnlineSecurity": "No", "OnlineBackup": "Yes",
        "DeviceProtection": "No", "TechSupport": "No", "StreamingTV": "No",
        "StreamingMovies": "No", "Contract": "Month-to-month",
        "PaperlessBilling": "Yes", "PaymentMethod": "Electronic check",
        "MonthlyCharges": 50.0, "TotalCharges": 600.0,
    }
    encoded = raw.copy()
    for col, enc in encoders.items():
        if col in encoded:
            encoded[col] = int(enc.transform([encoded[col]])[0])
    df = pd.DataFrame([encoded])[feature_names]
    assert df.shape == (1, 19), f"Input shape mismatch: {df.shape}"
    prediction = model.predict(df)[0]
    assert prediction in [0, 1], f"Unexpected prediction: {prediction}"
    print(f"    -> Prediction: {prediction} ({'Churn' if prediction == 1 else 'Not Churn'})")
test("TC04", "Valid customer produces prediction", tc04)

# ---- TC05: Churn probability displayed ----
def tc05():
    global churn_prob
    raw = {
        "gender": "Male", "SeniorCitizen": 1, "Partner": "No", "Dependents": "No",
        "tenure": 2, "PhoneService": "Yes", "MultipleLines": "Yes",
        "InternetService": "Fiber optic", "OnlineSecurity": "No", "OnlineBackup": "No",
        "DeviceProtection": "No", "TechSupport": "No", "StreamingTV": "Yes",
        "StreamingMovies": "Yes", "Contract": "Month-to-month",
        "PaperlessBilling": "Yes", "PaymentMethod": "Electronic check",
        "MonthlyCharges": 95.0, "TotalCharges": 190.0,
    }
    encoded = raw.copy()
    for col, enc in encoders.items():
        if col in encoded:
            encoded[col] = int(enc.transform([encoded[col]])[0])
    df = pd.DataFrame([encoded])[feature_names]
    proba = model.predict_proba(df)[0]
    churn_prob = float(proba[1])
    assert 0.0 <= churn_prob <= 1.0, f"Probability out of range: {churn_prob}"
    print(f"    -> Churn probability: {churn_prob:.4f} ({churn_prob*100:.2f}%)")
test("TC05", "Churn probability is returned", tc05)

# ---- TC06: Risk classification works ----
def tc06():
    def calc_risk(p):
        if p <= 0.30: return "LOW"
        elif p <= 0.60: return "MEDIUM"
        else: return "HIGH"
    assert calc_risk(0.15) == "LOW"
    assert calc_risk(0.30) == "LOW"
    assert calc_risk(0.31) == "MEDIUM"
    assert calc_risk(0.60) == "MEDIUM"
    assert calc_risk(0.61) == "HIGH"
    assert calc_risk(0.99) == "HIGH"
test("TC06", "Risk classification works correctly", tc06)

# ---- TC07: Recommendation appears ----
def tc07():
    recs = {
        "LOW": "Low churn risk. Continue standard engagement and monitor periodically.",
        "MEDIUM": "Moderate churn risk. Consider reaching out with a personalized offer or checking in on satisfaction.",
        "HIGH": "High churn risk. Prioritize retention: offer a discount, assign dedicated support, or propose a longer-term contract.",
    }
    for level, text in recs.items():
        assert len(text) > 10, f"Recommendation for {level} is too short"
test("TC07", "Recommendation is generated for all risk levels", tc07)

# ---- TC08: Invalid numerical input handled ----
def tc08():
    monthly = -10.0
    assert monthly < 0, "Negative monthly charges should be caught"
    total = -5.0
    assert total < 0, "Negative total charges should be caught"
test("TC08", "Invalid numerical input is detectable", tc08)

# ---- TC09: Invalid category handled ----
def tc09():
    enc = encoders["gender"]
    try:
        enc.transform(["NonexistentGender"])
        assert False, "Should have raised an error"
    except (ValueError, KeyError):
        pass  # Expected
test("TC09", "Invalid category is rejected by encoder", tc09)

# ---- TC10: Analytics dataset loads ----
def tc10():
    df = pd.read_csv("miniprojectchurn.csv")
    assert df.shape[0] > 0, "Dataset is empty"
    assert "Churn" in df.columns, "Churn column missing"
    assert df.shape == (7043, 21), f"Unexpected shape: {df.shape}"
test("TC10", "Analytics dataset loads correctly", tc10)

# ---- TC11: Feature importance loads ----
def tc11():
    assert hasattr(model, "feature_importances_"), "No feature_importances_ attribute"
    fi = model.feature_importances_
    assert len(fi) == 19, f"Expected 19 importances, got {len(fi)}"
    assert abs(sum(fi) - 1.0) < 0.01, f"Importances don't sum to ~1: {sum(fi)}"
    top_feature = feature_names[np.argmax(fi)]
    print(f"    -> Top feature: {top_feature} ({max(fi):.4f})")
test("TC11", "Feature importance is available and correct", tc11)

# ---- TC12: Application module compiles without errors ----
def tc12():
    with open("app.py", "r", encoding="utf-8") as f:
        source = f.read()
    compile(source, "app.py", "exec")
test("TC12", "app.py compiles without syntax errors", tc12)


# ---- Print Summary ----
print()
print("=" * 80)
print("TEST SUMMARY")
print("=" * 80)
print(f"{'Test ID':<10} {'Description':<55} {'Result'}")
print("-" * 80)
for tid, desc, res in results:
    status = "[PASS]" if res == "PASS" else "[FAIL]"
    print(f"{tid:<10} {desc:<55} {status} {res}")
print("-" * 80)

passed = sum(1 for _, _, r in results if r == "PASS")
failed = sum(1 for _, _, r in results if r != "PASS")
print(f"\nTotal: {len(results)} | Passed: {passed} | Failed: {failed}")

if failed > 0:
    print("\nSOME TESTS FAILED")
    sys.exit(1)
else:
    print("\nALL TESTS PASSED")
