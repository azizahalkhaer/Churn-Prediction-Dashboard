import pandas as pd
import joblib
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

# 1. Load Data
df = pd.read_csv('data/Customer-Churn-Records.csv')
features = ['CreditScore', 'Geography', 'Gender', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'Card Type']
df_model = df[features + ['Exited']].copy()

# 2. Encoding & Simpan Encodernya!
encoders = {} # Buat dictionary untuk menyimpan encoder tiap kolom
for col in ['Geography', 'Gender', 'Card Type']:
    le = LabelEncoder()
    df_model[col] = le.fit_transform(df_model[col])
    encoders[col] = le # Simpan encoder ke dalam dictionary

X = df_model[features]
y = df_model['Exited']

# 3. Split & SMOTE
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
smote = SMOTE(random_state=42)
X_train_sm, y_train_sm = smote.fit_resample(X_train, y_train)

# 4. Train XGBoost
print("--- Training XGBoost ---")
xgb_model = XGBClassifier(n_estimators=200, max_depth=5, learning_rate=0.05, random_state=42, eval_metric='logloss')
xgb_model.fit(X_train_sm, y_train_sm)

# 5. Simpan Model dan Encoder
joblib.dump(xgb_model, 'models/xgb_model.pkl')
joblib.dump(encoders, 'models/encoders.pkl') # Simpan encodernya!

print("XGBoost dan Encoder Berhasil Disimpan!")