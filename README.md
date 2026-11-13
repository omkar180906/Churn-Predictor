# Customer Churn Prediction System

A predictive analytics application that estimates customer attrition probability using an ensemble classification model. Built with Python, Streamlit, and Scikit-learn.

---

## Abstract

Customer churn, the rate at which existing customers discontinue their relationship with a business, is one of the most consequential metrics in subscription-based and service-oriented industries. The cost of acquiring a new customer is estimated at 5 to 25 times the cost of retaining an existing one, making churn prediction a high-priority application of supervised machine learning.

This project implements a complete churn prediction pipeline: data preprocessing with class-imbalance correction (SMOTE), model training and evaluation via stratified cross-validation, and deployment as an interactive web application. The system ingests 19 demographic, service, and billing features from a customer profile, passes them through a serialised Random Forest Classifier (100 estimators), and returns a churn prediction, a calibrated probability score, a risk classification, and a context-aware retention recommendation.

---

## Capabilities

| Capability | Description |
|---|---|
| **Binary Classification** | Predicts whether a given customer will churn or remain, based on 19 engineered features |
| **Probability Estimation** | Outputs the model's posterior probability of churn as a percentage with an associated progress indicator |
| **Risk Stratification** | Classifies each prediction into Low (0-30%), Medium (31-60%), or High (61-100%) risk tiers |
| **Retention Recommendations** | Generates tier-specific retention strategies informed by the predicted risk level |
| **Exploratory Analytics** | Presents distribution, segmentation, and correlation charts across 7,000+ historical customer records |
| **Feature Importance Analysis** | Ranks the relative contribution of each input feature to the model's decision boundary using Gini importance |
| **Model Transparency** | Displays hyperparameters, evaluation metrics, the confusion matrix, and the full classification report |
| **Input Validation** | Enforces domain constraints on all 19 input features with descriptive error messages |

---

## Technology Stack

| Component | Technology | Role |
|---|---|---|
| Language | Python 3.x | Core runtime |
| Web Framework | Streamlit | Application interface and server |
| Data Processing | Pandas, NumPy | Tabular data manipulation and numerical computation |
| Machine Learning | Scikit-learn 1.6.1 | Model training, evaluation, and inference |
| Visualisation | Matplotlib, Seaborn | Statistical charting and figure rendering |
| Serialisation | Joblib | Model and encoder persistence (pickle protocol) |

---

## Installation

### 1. Clone or download the repository

```bash
cd Customer-Churn-Prediction
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> **Compatibility note:** The serialised model artifact was produced with `scikit-learn==1.6.1`. Using a different version may result in unpickling warnings or attribute mismatches. Pin to this version for guaranteed compatibility.

---

## Running the Application

```bash
streamlit run app.py
```

The application will launch a local development server and be accessible at `http://localhost:8501`.

---

## Project Structure

```
Customer-Churn-Prediction/
├── app.py                        Main Streamlit application (UI, routing, prediction logic)
├── Customer_churn_model.pkl      Serialised Random Forest model (100 estimators, 19 features)
├── encoders.pkl                  Serialised LabelEncoders for 15 categorical features
├── miniprojectchurn.csv          Source dataset (7,043 customer records, 21 columns)
├── MINIPROJECT.ipynb             Model training and evaluation notebook
├── test_app.py                   Automated test suite (12 test cases)
├── requirements.txt              Python dependency manifest
└── README.md                     Project documentation
```

---

## Model Architecture

### Algorithm: Random Forest Classifier

Random Forest is an ensemble learning method that constructs a multitude of decision trees during training and aggregates their individual predictions through majority voting. This bagging approach reduces variance and mitigates overfitting relative to a single decision tree, while retaining interpretability through feature importance scores derived from mean decrease in Gini impurity.

### Specifications

| Parameter | Value |
|---|---|
| Algorithm | Random Forest Classifier (sklearn.ensemble.RandomForestClassifier) |
| Number of Estimators | 100 |
| Split Criterion | Gini Impurity |
| Random State | 42 |
| Number of Input Features | 19 |
| Classification Type | Binary (Churn / Not Churn) |
| Class Balancing | SMOTE (Synthetic Minority Oversampling Technique) |
| Train/Test Partition | 80/20 stratified split |

### Model Selection

Three candidate algorithms were evaluated using 5-fold stratified cross-validation on the SMOTE-balanced training set:

| Model | Mean CV Accuracy |   
|---|---|
| Decision Tree Classifier | 78% |
| **Random Forest Classifier** | **84%** |
| XGBoost Classifier | 83% |

Random Forest was selected as the final model based on its superior cross-validation performance and resistance to overfitting.

### Evaluation Metrics (Held-Out Test Set)

| Metric | Not Churn (0) | Churn (1) | Macro Average | Weighted Average |
|---|---|---|---|---|
| Precision | 0.85 | 0.58 | 0.72 | 0.78 |
| Recall | 0.85 | 0.59 | 0.72 | 0.78 |
| F1-Score | 0.85 | 0.58 | 0.72 | 0.78 |
| Support | 1,036 | 373 | 1,409 | 1,409 |

**Overall Accuracy:** 77.86%

### Confusion Matrix

|  | Predicted: Stay | Predicted: Churn |
|---|---|---|
| **Actual: Stay** | 878 (TN) | 158 (FP) |
| **Actual: Churn** | 154 (FN) | 219 (TP) |

---

## Data Preprocessing Pipeline

1. **Source Data**: 7,043 customer records with 21 attributes (including `customerID` and target variable `Churn`)
2. **Type Coercion**: `TotalCharges` column cast from object to float64; rows with non-numeric values dropped
3. **Label Encoding**: 15 categorical features transformed via `sklearn.preprocessing.LabelEncoder`, with fitted encoders serialised to `encoders.pkl`
4. **Train/Test Split**: 80/20 partition using `train_test_split(random_state=42)`
5. **Class Imbalance Correction**: SMOTE applied to the training partition only
   - Pre-SMOTE distribution: 5,174 Not Churn / 1,869 Churn (73.5% / 26.5%)
   - Post-SMOTE distribution: 4,138 Not Churn / 4,138 Churn (50% / 50%)

---

## Input Feature Specification

The model expects exactly 19 features in the following order:

| # | Feature | Data Type | Accepted Values |
|---|---|---|---|
| 1 | Gender | Categorical | Female, Male |
| 2 | SeniorCitizen | Binary | 0 (No), 1 (Yes) |
| 3 | Partner | Categorical | No, Yes |
| 4 | Dependents | Categorical | No, Yes |
| 5 | Tenure | Numerical | 0 to 72 (months) |
| 6 | PhoneService | Categorical | No, Yes |
| 7 | MultipleLines | Categorical | No, Yes, No phone service |
| 8 | InternetService | Categorical | DSL, Fiber optic, No |
| 9 | OnlineSecurity | Categorical | No, Yes, No internet service |
| 10 | OnlineBackup | Categorical | No, Yes, No internet service |
| 11 | DeviceProtection | Categorical | No, Yes, No internet service |
| 12 | TechSupport | Categorical | No, Yes, No internet service |
| 13 | StreamingTV | Categorical | No, Yes, No internet service |
| 14 | StreamingMovies | Categorical | No, Yes, No internet service |
| 15 | Contract | Categorical | Month-to-month, One year, Two year |
| 16 | PaperlessBilling | Categorical | No, Yes |
| 17 | PaymentMethod | Categorical | Electronic check, Mailed check, Bank transfer (automatic), Credit card (automatic) |
| 18 | MonthlyCharges | Numerical | 0 to 500 (USD) |
| 19 | TotalCharges | Numerical | 0 to 10,000 (USD) |

---

## Output Specification

| Output | Description |
|---|---|
| **Prediction** | Binary label: Churn or Not Churn |
| **Probability** | Posterior probability of the Churn class (0-100%) |
| **Risk Level** | Low (0-30%), Medium (31-60%), or High (61-100%) |
| **Recommendation** | Retention strategy calibrated to the predicted risk tier |

---

## Testing

The project includes an automated test suite (`test_app.py`) covering 12 test cases:

```bash
py test_app.py
```

Test coverage includes model loading, encoder validation, feature ordering, prediction output, probability bounds, risk classification logic, recommendation generation, input validation, dataset integrity, feature importance availability, and source compilation.

---

## Authors

Machine Learning Engineering Team

---

## License

This project was developed for educational purposes as part of an academic mini project.
