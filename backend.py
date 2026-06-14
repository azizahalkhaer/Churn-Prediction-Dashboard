import streamlit as st
import joblib
import pandas as pd
import xgboost as xgb # Wajib diimport

# 1. Gunakan cache_resource agar model cuma di-load SATU KALI saat aplikasi nyala
@st.cache_resource
def load_model():
    try:
        # Pastikan nama file ini SAMA PERSIS dengan yang di GitHub
        return joblib.load('xgb_model.pkl')
    except Exception as e:
        st.error(f"Gagal memuat model: {e}")
        return None

# Muat model sekali saja di awal
model_xgb = load_model()

def predict_churn(data_input):
    if model_xgb is None:
        return None, 0.0

    # Buat DataFrame
    df_input = pd.DataFrame([data_input])
    
    # Mapping (Hardcode agar tidak tergantung LabelEncoder eksternal)
    geo_map = {"France": 0, "Germany": 1, "Spain": 2}
    gen_map = {"Female": 0, "Male": 1}
    card_map = {"DIAMOND": 0, "GOLD": 1, "PLATINUM": 2, "SILVER": 3}
    
    # Terapkan mapping
    df_input['Geography'] = df_input['Geography'].map(geo_map)
    df_input['Gender'] = df_input['Gender'].map(gen_map)
    df_input['Card Type'] = df_input['Card Type'].map(card_map)
    
    # 2. Penting: Pastikan urutan fitur SAMA PERSIS dengan saat training model!
    features = ['CreditScore', 'Geography', 'Gender', 'Age', 'Tenure', 
                'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'Card Type']
    
    # Cek apakah kolom sudah benar
    df_input = df_input[features]
    
    # 3. Prediksi
    # Gunakan .predict dan .predict_proba
    prediction = model_xgb.predict(df_input)
    probability = model_xgb.predict_proba(df_input)[0][1] 
    
    return prediction[0], probability
