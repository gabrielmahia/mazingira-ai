import streamlit as st
import urllib.request, json

st.set_page_config(page_title="Mazingira AI — Mazingira na NEMA", page_icon="🌿", layout="centered")
st.markdown("""<style>
.stApp{background:#050e07;color:#e8f5e9}
.env-card{background:#0a1f0d;border:1px solid #1b5e20;border-radius:10px;padding:14px 18px;margin:8px 0}
.alert{background:#1a0a00;border:1px solid #e65100;border-radius:8px;padding:10px 14px;margin:8px 0}
.stButton>button{background:#1b5e20;color:#fff;border:none;border-radius:8px;padding:10px 24px;font-weight:700;width:100%}
</style>""", unsafe_allow_html=True)

API_KEY = st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY","")
SYSTEM = """Wewe ni mshauri wa mazingira Kenya. Eleza sheria za NEMA na haki za mazingira kwa Kiswahili.
Toa ushauri wa vitendo na hatua sahihi za kisheria. Kama kuna tatizo la haraka la kimazingira, onyesha namna ya kuripoti."""

def ask(q):
    if not API_KEY: return "❌ API key not configured."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    body = {"contents":[{"role":"user","parts":[{"text":q}]}],
            "systemInstruction":{"parts":[{"text":SYSTEM}]},
            "generationConfig":{"temperature":0.25,"maxOutputTokens":700}}
    try:
        req = urllib.request.Request(url,data=json.dumps(body).encode(),headers={"Content-Type":"application/json"},method="POST")
        with urllib.request.urlopen(req,timeout=30) as r:
            return json.loads(r.read())["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e: return f"❌ {e}"

st.markdown("# 🌿 Mazingira AI")
st.markdown("**Mazingira na NEMA Kenya — Haki na Uzingatifu**")
tab1,tab2,tab3,tab4 = st.tabs(["📋 Mwongozo wa NEMA","🚨 Ripoti Uchafuzi","🌡️ Hali ya Hewa","🌳 Uzingatifu wa Biashara"])

with tab1:
    project = st.selectbox("Aina ya mradi:", ["Ujenzi wa jengo","Kiwanda","Migodi","Kilimo cha biashara","Hotel/resort","Mradi wa maji","Barabara","Mradi wa nishati"])
    if st.button("📋 Mwongozo wa EIA", key="eia_btn"):
        with st.spinner("..."): result = ask(f"Mwongozo wa NEMA EIA kwa {project} Kenya. Toa: Haja ya EIA (ndiyo/hapana), Hatua za kupata kibali, Muda, Gharama za makadirio, Hati zinazohitajika.")
        st.markdown(f'<div class="env-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="alert"><b>Kutaka kuripoti uchafuzi wa mazingira?</b><br>NEMA Hotline: 0800 724 800 (bure) | Email: info@nema.go.ke</div>', unsafe_allow_html=True)
    pollution_type = st.selectbox("Aina ya uchafuzi:", ["Mto/ziwa kumwagwa taka","Hewa chafu ya kiwanda","Taka za kemikali","Kelele kupita kiasi","Ukataji miti haramu","Taka za plastiki","Mafuriko ya maji machafu"])
    county_env = st.selectbox("Kaunti:", ["Nairobi","Mombasa","Kisumu","Nakuru","Thika/Kiambu"])
    if st.button("🚨 Jinsi ya Kuripoti", key="rep_btn"):
        with st.spinner("..."): result = ask(f"Jinsi ya kuripoti {pollution_type} katika {county_env} Kenya. Toa: Hatua za kuripoti, Mamlaka inayohusika, Haki zangu, Nini kinachoweza kutokea baada ya ripoti.")
        st.markdown(f'<div class="env-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

with tab3:
    region = st.selectbox("Mkoa:", ["Pwani (Coast)","Bonde la Ufa (Rift Valley)","Nyanza","Mashariki (Eastern)","Kaskazini Mashariki","Kati (Central)","Nairobi"])
    climate_q = st.selectbox("Habari:", ["Mwaka huu mvua zitakuwa vipi?","Hatari za ukame eneo langu","Hatari za mafuriko","Mabadiliko ya hali ya hewa — athari kwa wakulima"])
    if st.button("🌡️ Habari za Hali ya Hewa", key="cl_btn"):
        with st.spinner("..."): result = ask(f"{climate_q} — {region} Kenya 2024-2025. Toa: Utabiri wa jumla, Hatua za kujikinga, Vyanzo vya data (KMD/ICPAC).")
        st.markdown(f'<div class="env-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

with tab4:
    biz_type = st.selectbox("Biashara yako:", ["Kiwanda cha chakula","Garage ya magari","Saluni/spa","Mkahawa/hotel","Uchakataji wa taka","Uchimbaji madini"])
    if st.button("✅ Mahitaji ya Mazingira", key="comp_btn"):
        with st.spinner("..."): result = ask(f"Mahitaji ya mazingira ya NEMA kwa {biz_type} Kenya. Toa: Vibali vinavyohitajika, Gharama, Jinsi ya kutumia tena maji/nishati, Adhabu za kukiuka.")
        st.markdown(f'<div class="env-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("🌿 Mazingira AI v1.0 | NEMA: nema.go.ke | Hotline: 0800 724 800 | CC BY-NC-ND 4.0")
