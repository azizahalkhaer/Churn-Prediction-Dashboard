import joblib
import pandas as pd

# 1. Hanya load XGBoost (Tidak perlu scaler!)
try:
    model_xgb = joblib.load('models/xgb_model.pkl')
except Exception as e:
    print(f"Error loading model: {e}")

def predict_churn(data_input):
    df_input = pd.DataFrame([data_input])
    
    # 2. Hardcode mapping sesuai logika LabelEncoder temanmu
    geo_map = {"France": 0, "Germany": 1, "Spain": 2}
    gen_map = {"Female": 0, "Male": 1}
    card_map = {"DIAMOND": 0, "GOLD": 1, "PLATINUM": 2, "SILVER": 3}
    
    df_input['Geography'] = df_input['Geography'].map(geo_map)
    df_input['Gender'] = df_input['Gender'].map(gen_map)
    df_input['Card Type'] = df_input['Card Type'].map(card_map)
    
    # 3. Urutan 10 Fitur HARUS SAMA PERSIS dengan Colab temanmu
    features = ['CreditScore', 'Geography', 'Gender', 'Age', 'Tenure', 
                'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'Card Type']
    df_input = df_input[features]
    
    # 4. Prediksi LANGSUNG tanpa di-scale
    prediction = model_xgb.predict(df_input)
    probability = model_xgb.predict_proba(df_input)[0][1] 
    
    return prediction[0], probability