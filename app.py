import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
from backend import predict_churn
import base64

# --- 1. KONFIGURASI HALAMAN ---
try:
    img_icon = Image.open("icon.png")
    st.set_page_config(page_title="Churn Prediction Dashboard", page_icon=img_icon, layout="wide", initial_sidebar_state="expanded")
except:
    st.set_page_config(page_title="Churn Prediction Dashboard", page_icon="🏦", layout="wide", initial_sidebar_state="expanded")

# Inisialisasi Halaman via URL Query Parameter
query_params = st.query_params
if "nav" in query_params:
    st.session_state.page = query_params["nav"]
elif 'page' not in st.session_state:
    st.session_state.page = "Overview"

# --- LOAD DATASET ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data/Customer-Churn-Records.csv')
        df['Status'] = df['Exited'].map({0: 'Retained', 1: 'Churned'})
        return df
    except:
        return pd.DataFrame()

df = load_data()

# --- FUNGSI TEMA GRAFIK ---
def apply_dark_theme(fig, title_text=""):
    fig.update_layout(
        title=dict(text=title_text, font=dict(family="Inter", size=16, color="#F8FAFC")),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", 
        margin=dict(l=10, r=10, t=40, b=10),
        font=dict(family="Inter, sans-serif", color="#94A3B8"),
        xaxis=dict(showgrid=False, zeroline=False, showline=False, showticklabels=True),
        yaxis=dict(showgrid=False, zeroline=False, showline=False, showticklabels=False),
        showlegend=False, hovermode="x unified"
    )
    for trace in fig.data:
        if type(trace).__name__ in ['Bar', 'Pie', 'Histogram', 'Scatterpolar']:
            trace.marker.line.width = 0
    return fig

def apply_card_theme(fig):
    fig.update_layout(
        paper_bgcolor="#161E2E", 
        plot_bgcolor="rgba(0,0,0,0)", 
        margin=dict(l=15, r=15, t=40, b=15),
        font=dict(family="Inter, sans-serif", color="#94A3B8", size=11),
        xaxis=dict(showgrid=False, zeroline=False, showline=False),
        yaxis=dict(showgrid=False, zeroline=False, showline=False, showticklabels=False),
        showlegend=False, hovermode="x unified",
        title_font=dict(size=14, color="#F8FAFC") 
    )
    for trace in fig.data:
        if type(trace).__name__ in ['Bar', 'Pie', 'Histogram', 'Scatterpolar']:
            trace.marker.line.width = 0
    return fig

# --- 2. ADVANCED CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
    
    .stApp { background-color: #0B0F19; background-image: radial-gradient(at 0% 0%, rgba(49, 46, 129, 0.3) 0px, transparent 50%), radial-gradient(at 100% 100%, rgba(124, 58, 237, 0.1) 0px, transparent 50%); color: #F8FAFC; }
    [data-testid="stSidebar"] { background-color: #111827 !important; border-right: 1px solid rgba(255,255,255,0.05); }
    
    header, footer, .stDeployButton {display: none !important; visibility: hidden !important;}
    .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    @keyframes slideUpFade { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
    
    .custom-header { display: flex; justify-content: space-between; align-items: center; padding-bottom: 20px; margin-bottom: 10px; margin-top: 5px; }
    .header-title { font-size: 1.5rem; font-weight: 800; color: #FFFFFF; margin: 0; letter-spacing: 0.5px; }
    .icon-box { border: 1px solid rgba(255,255,255,0.1); border-radius: 50%; width: 35px; height: 35px; display: flex; align-items: center; justify-content: center; position: relative; color: white;}
    .badge { position: absolute; top: -2px; right: -2px; background: #8B5CF6; color: white; font-size: 0.55rem; font-weight: bold; width: 14px; height: 14px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
    
    .dribbble-card { background: #161E2E; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 20px; height: 100%; margin-bottom: 20px; transition: all 0.3s ease; }
    .metric-card { background: #161E2E; border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 12px; padding: 15px; margin-bottom: 15px; transition: transform 0.2s;}
    .metric-card:hover { transform: translateY(-3px); border-color: rgba(139, 92, 246, 0.4);}
    .metric-title { font-size: 0.75rem; color: #94A3B8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;}
    .metric-value { font-size: 1.4rem; font-weight: 800; color: #F8FAFC; margin-top: 5px;} 
    
    .premium-card { background: linear-gradient(135deg, #4338CA 0%, #7C3AED 100%); border-radius: 16px; padding: 24px; height: 100%; margin-bottom: 20px; border: none; box-shadow: 0 10px 25px rgba(124, 58, 237, 0.3); }
    
    [data-testid="stForm"] { border: none !important; background: transparent !important; padding: 0 !important; }
    .stPlotlyChart { background: #161E2E; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.2); }
    
    .prog-container { width: 100%; background-color: rgba(255,255,255,0.05); border-radius: 10px; height: 6px; margin-top: 5px; margin-bottom: 15px;}
    .prog-purple { background: #8B5CF6; height: 100%; border-radius: 10px; }
    .prog-blue { background: #3B82F6; height: 100%; border-radius: 10px; }
    .prog-orange { background: #F97316; height: 100%; border-radius: 10px; }
    .prog-text { display: flex; justify-content: space-between; font-size: 0.8rem; font-weight: 500; color: #CBD5E1; }
    
    div[data-baseweb="select"] > div, div[data-baseweb="base-input"], div[data-baseweb="input"] { background-color: #0B0F19 !important; border-radius: 8px !important; }
    div[data-baseweb="input"], div[data-baseweb="select"] > div { border: 1px solid rgba(255,255,255,0.2) !important; }
    input[type="number"], div[data-baseweb="select"] { color: #F8FAFC !important; background-color: #0B0F19 !important; -webkit-text-fill-color: #F8FAFC !important; font-weight: 600 !important; font-size: 1rem !important; }
    .stNumberInput button { display: none !important; } 
    
    .stButton>button { width: 100%; border-radius: 8px; background: #3B82F6; color: white !important; font-weight: 600; padding: 10px; border: none; transition: all 0.2s;}
    .stButton>button:hover { background: #2563EB; }
    
    /* FIX: SIDEBAR ICON HOVER EFFECT */
    .icon-link { transition: 0.2s; opacity: 0.5; display: block; text-align: center; margin-bottom: 30px;}
    .icon-link:hover { opacity: 1; transform: scale(1.1); }
    .icon-link.active { opacity: 1; }
    
    p, label, .st-cx { color: #94A3B8 !important; font-size: 0.85rem !important;}
</style>
""", unsafe_allow_html=True)

# --- FUNGSI UNTUK MERUBAH SVG MENJADI BASE64 AGAR BISA DIKLIK SEBAGAI LINK HTML ---
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except:
        return ""

# --- 3. SIDEBAR (PURE SVG ICONS, MURNI GAMBAR) ---
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    try: 
        st.image("logo.svg", use_container_width=True)
    except: 
        st.markdown("<h3 style='text-align: center; color:#FFFFFF; font-weight:800;'>OneBank AI</h3>", unsafe_allow_html=True)
    
    st.markdown("<div style='text-align: center; color: #64748B; font-size: 1.5rem; margin-top: 20px; margin-bottom: 40px; font-weight: 800;'>☰</div>", unsafe_allow_html=True)
    
    # Ambil Base64 dari SVG kamu
    icon1_b64 = get_base64_image("icon1.svg")
    icon2_b64 = get_base64_image("icon2.svg")
    
    active_ov = "active" if st.session_state.page == "Overview" else ""
    active_an = "active" if st.session_state.page == "Analytic Dashboard" else ""

    # KITA INJEKSIKAN HTML LINK `<a>` DENGAN GAMBAR SVG DI DALAMNYA
    # URL di-set untuk memuat ulang halaman dengan parameter `nav=nama_halaman`
    if icon1_b64 and icon2_b64:
        html_code = f"""
        <a href="?nav=Overview" target="_self" class="icon-link {active_ov}">
            <img src="data:image/svg+xml;base64,{icon1_b64}" width="28">
        </a>
        <a href="?nav=Analytic+Dashboard" target="_self" class="icon-link {active_an}">
            <img src="data:image/svg+xml;base64,{icon2_b64}" width="28">
        </a>
        """
        st.markdown(html_code, unsafe_allow_html=True)
    else:
        st.warning("File icon1.svg atau icon2.svg tidak ditemukan di folder!")


# --- 4. HEADER ---
st.markdown("""
<div class="custom-header">
    <h1 class="header-title">CHURN PREDICTION DASHBOARD</h1>
    <div style="display: flex; gap: 15px;">
        <div class="icon-box"><svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg></div>
        <div class="icon-box"><svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path></svg><div class="badge">2</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

color_map = {'Retained': '#38BDF8', 'Churned': '#A78BFA'}

# ==========================================
# 5. HALAMAN OVERVIEW
# ==========================================
if st.session_state.page == "Overview":
    if df.empty: st.warning("Dataset not found.")
    else:
        total_cust = len(df)
        retained = len(df[df['Exited'] == 0])
        churned = len(df[df['Exited'] == 1])
        avg_bal = df["Balance"].sum()/1000000
        
        k1, k2, k3, k4 = st.columns(4)
        k1.markdown(f'<div class="metric-card" style="border-top: 3px solid #38BDF8;"><div class="metric-title">Total Population</div><div class="metric-value">{total_cust:,}</div></div>', unsafe_allow_html=True)
        k2.markdown(f'<div class="metric-card"><div class="metric-title">Retained Rate</div><div class="metric-value" style="color:#38BDF8;">{(retained/total_cust)*100:.1f}%</div></div>', unsafe_allow_html=True)
        k3.markdown(f'<div class="metric-card"><div class="metric-title">Churned Rate</div><div class="metric-value" style="color:#A78BFA;">{(churned/total_cust)*100:.1f}%</div></div>', unsafe_allow_html=True)
        k4.markdown(f'<div class="metric-card"><div class="metric-title">Total Balance</div><div class="metric-value">${avg_bal:.1f}M</div></div>', unsafe_allow_html=True)
        
        c_left, c_right = st.columns([1.5, 1])
        with c_left:
            df_age_group = df.groupby(['Age', 'Status']).size().reset_index(name='Count')
            fig_bar = px.bar(df_age_group, x="Age", y="Count", color="Status", color_discrete_map=color_map)
            fig_bar.update_traces(opacity=0.85)
            fig_bar.update_layout(height=260) 
            st.plotly_chart(apply_dark_theme(fig_bar, "Age Distribution Analysis"), use_container_width=True, config={'displayModeBar': False})

        with c_right:
            geo_df = df['Geography'].value_counts().reset_index()
            geo_df.columns = ['Geography', 'Count']
            fig_pie = px.pie(geo_df, values='Count', names='Geography', hole=0.7, color_discrete_sequence=['#8B5CF6', '#3B82F6', '#64748B'])
            fig_pie.update_layout(height=260, showlegend=True, legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.1))
            st.plotly_chart(apply_dark_theme(fig_pie, "Geography Origin"), use_container_width=True, config={'displayModeBar': False})

        st.markdown('<div class="dribbble-card" style="height: auto; padding: 25px; margin-top:10px;">', unsafe_allow_html=True)
        st.markdown("<div style='font-weight:600; color:#F8FAFC; margin-bottom: 20px; font-size:1.1rem;'>Customer Engagement Statistics</div>", unsafe_allow_html=True)
        
        pct_active = int((df['IsActiveMember'].sum() / total_cust) * 100)
        pct_card = int((df['HasCrCard'].sum() / total_cust) * 100)
        
        col_prog1, col_prog2 = st.columns(2)
        with col_prog1:
            st.markdown(f"""
                <div class="prog-text"><span>Active Members</span><span style="color:#A78BFA">{pct_active}%</span></div>
                <div class="prog-container"><div class="prog-purple" style="width: {pct_active}%;"></div></div>
            """, unsafe_allow_html=True)
        with col_prog2:
            st.markdown(f"""
                <div class="prog-text"><span>Credit Card Owners</span><span style="color:#38BDF8">{pct_card}%</span></div>
                <div class="prog-container"><div class="prog-blue" style="width: {pct_card}%;"></div></div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ==========================================
# 6. HALAMAN ANALYTIC DASHBOARD
# ==========================================
elif st.session_state.page == "Analytic Dashboard":
    st.markdown("<h4 style='color:#F8FAFC; margin-bottom:15px; font-weight:600; font-size:1.1rem;'>Prediction Model Configuration</h4>", unsafe_allow_html=True)
    
    with st.form("analytic_form"):
        col1, col2, col3 = st.columns(3)
        with col1: age = st.slider("Age (Years)", 18, 100, 30)
        with col2: credit_score = st.slider("Credit Score", 300, 900, 650)
        with col3: balance = st.number_input("Account Balance ($)", 0.0, value=45000.0, format="%.2f")
            
        st.markdown("<br>", unsafe_allow_html=True)
        col4, col5, col6 = st.columns(3)
        with col4: tenure = st.select_slider("Tenure (Years with Bank)", options=list(range(0, 11)), value=4)
        with col5: num_products = st.radio("Number Of Products", options=[1, 2, 3, 4], horizontal=True)
        with col6: gender = st.radio("Gender", options=["Female", "Male"], horizontal=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col7, col8, col9, col10 = st.columns([1.2, 1.2, 1, 1])
        with col7: geography = st.selectbox("Geography Origin", ["France", "Spain", "Germany"])
        with col8: card_type = st.selectbox("Card Type", ["DIAMOND", "GOLD", "SILVER", "PLATINUM"])
        with col9: has_cr_card_toggle = st.toggle("Owns Credit Card", value=True)
        with col10: is_active_toggle = st.toggle("Active Member", value=True)
        
        st.markdown("<div style='margin-bottom:10px;'></div>", unsafe_allow_html=True)
        submit = st.form_submit_button("Run Prediction Analysis")

    if submit:
        data_input = {
            'CreditScore': credit_score, 'Geography': geography, 'Gender': gender,
            'Age': age, 'Tenure': tenure, 'Balance': balance, 'NumOfProducts': num_products,
            'HasCrCard': 1 if has_cr_card_toggle else 0, 'IsActiveMember': 1 if is_active_toggle else 0,
            'Card Type': card_type
        }
        
        with st.spinner("Processing Neural Network Pipeline..."):
            hasil, probabilitas = predict_churn(data_input)
            st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 20px 0;'>", unsafe_allow_html=True)
            
            r1, r2 = st.columns([1, 1.5])
            with r1: 
                gauge_color = "#F97316" if hasil == 1 else "#38BDF8"
                fig_g = go.Figure(go.Indicator(
                    mode = "gauge+number", value = probabilitas * 100, title = {'text': "Risk Probability", 'font': {'size': 13, 'color': '#94A3B8'}},
                    number = {'suffix': "%", 'font': {'color': gauge_color, 'size': 35}},
                    gauge = {'axis': {'range': [0, 100], 'visible': False}, 'bar': {'color': gauge_color, 'thickness': 0.7}, 'bgcolor': "rgba(255,255,255,0.05)"}
                ))
                fig_g.update_layout(height=230)
                st.plotly_chart(apply_card_theme(fig_g), use_container_width=True, config={'displayModeBar': False})
                if hasil == 1: st.error("HIGH RISK: Model predicts potential Churn.")
                else: st.success("SAFE: Model predicts customer Retention.")
                
            with r2: 
                categories = ['Age', 'Credit Score', 'Balance', 'Tenure', 'Products']
                user_rad = [(age/100)*100, (credit_score/900)*100, (balance/250000)*100, (tenure/10)*100, (num_products/4)*100]
                avg_rad = [(df['Age'].mean()/100)*100, (df['CreditScore'].mean()/900)*100, (df['Balance'].mean()/250000)*100, (df['Tenure'].mean()/10)*100, (df['NumOfProducts'].mean()/4)*100] if not df.empty else [40, 70, 30, 50, 40]
                
                fig_radar = go.Figure()
                fig_radar.add_trace(go.Scatterpolar(r=avg_rad, theta=categories, fill='toself', name='Avg Pop.', marker_color='#475569'))
                fig_radar.add_trace(go.Scatterpolar(r=user_rad, theta=categories, fill='toself', name='This User', marker_color='#8B5CF6'))
                fig_radar.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 100])), height=230, title="Numerical Persona Mapping", showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5))
                st.plotly_chart(apply_card_theme(fig_radar), use_container_width=True, config={'displayModeBar': False})

            st.markdown("<h5 style='color:#94A3B8; font-size:0.9rem; margin-bottom:10px;'>Categorical Comparison vs Population</h5>", unsafe_allow_html=True)
            c1, c2, c3, c4, c5 = st.columns(5)
            
            def make_mini_bar(df_col, user_val, title):
                counts = df[df_col].value_counts().reset_index()
                counts.columns = ['Category', 'Count']
                counts['Category'] = counts['Category'].astype(str)
                counts['Color'] = counts['Category'].apply(lambda x: '#38BDF8' if x == str(user_val) else '#334155')
                fig = go.Figure(go.Bar(x=counts['Category'], y=counts['Count'], marker_color=counts['Color']))
                fig.update_layout(height=160, title=title, margin=dict(l=5,r=5,t=30,b=5))
                return apply_card_theme(fig)

            if not df.empty:
                cr_val = 1 if has_cr_card_toggle else 0
                act_val = 1 if is_active_toggle else 0
                with c1: st.plotly_chart(make_mini_bar('Geography', geography, "Geography"), use_container_width=True, config={'displayModeBar': False})
                with c2: st.plotly_chart(make_mini_bar('Gender', gender, "Gender"), use_container_width=True, config={'displayModeBar': False})
                with c3: st.plotly_chart(make_mini_bar('Card Type', card_type, "Card Type"), use_container_width=True, config={'displayModeBar': False})
                with c4: st.plotly_chart(make_mini_bar('HasCrCard', cr_val, "Credit Card (1=Yes)"), use_container_width=True, config={'displayModeBar': False})
                with c5: st.plotly_chart(make_mini_bar('IsActiveMember', act_val, "Active (1=Yes)"), use_container_width=True, config={'displayModeBar': False})