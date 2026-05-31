import streamlit as st
import numpy as np
from PIL import Image
import io
import base64
import time
import os

# ── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VietCash · Nhận Diện Tiền VN",
    page_icon="💴",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700;900&family=Space+Mono:wght@400;700&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; }

html, body, .stApp {
    background: #0A0A0F !important;
    font-family: 'Be Vietnam Pro', sans-serif !important;
    color: #F0F0F0 !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none; }

/* ── Noise texture overlay ── */
.stApp::before {
    content: '';
    position: fixed; inset: 0; z-index: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.035'/%3E%3C/svg%3E");
    pointer-events: none;
}

/* ── Main wrapper ── */
.main-wrapper {
    position: relative; z-index: 1;
    min-height: 100vh;
    padding: 0 0 60px 0;
}

/* ── Header ── */
.site-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 20px 48px;
    border-bottom: 1px solid rgba(245,197,24,0.15);
    background: rgba(10,10,15,0.85);
    backdrop-filter: blur(20px);
    position: sticky; top: 0; z-index: 100;
}
.logo {
    display: flex; align-items: center; gap: 12px;
}
.logo-mark {
    width: 38px; height: 38px; border-radius: 10px;
    background: linear-gradient(135deg, #F5C518 0%, #E8A000 100%);
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; box-shadow: 0 0 20px rgba(245,197,24,0.4);
}
.logo-text {
    font-size: 22px; font-weight: 900; letter-spacing: -0.5px;
    background: linear-gradient(90deg, #F5C518, #FFF4B3);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.logo-sub {
    font-size: 11px; color: rgba(240,240,240,0.4); font-family: 'Space Mono', monospace;
    letter-spacing: 2px; text-transform: uppercase;
}
.header-badge {
    font-family: 'Space Mono', monospace; font-size: 10px;
    color: rgba(245,197,24,0.7); border: 1px solid rgba(245,197,24,0.25);
    padding: 4px 12px; border-radius: 20px; letter-spacing: 2px;
    text-transform: uppercase;
}

/* ── Hero ── */
.hero {
    padding: 56px 48px 40px;
    display: grid; grid-template-columns: 1fr 1fr; gap: 64px; align-items: center;
}
.hero-left h1 {
    font-size: clamp(32px, 4vw, 54px); font-weight: 900; line-height: 1.1;
    letter-spacing: -1.5px; margin-bottom: 16px;
}
.hero-left h1 span {
    background: linear-gradient(90deg, #F5C518 30%, #FFF176);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-left p {
    font-size: 16px; color: rgba(240,240,240,0.55); line-height: 1.7;
    max-width: 420px;
}
.stat-row {
    display: flex; gap: 32px; margin-top: 32px;
}
.stat-item { text-align: left; }
.stat-num {
    font-size: 28px; font-weight: 900; font-family: 'Space Mono', monospace;
    background: linear-gradient(90deg, #F5C518, #FFF4B3);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.stat-label { font-size: 11px; color: rgba(240,240,240,0.4); text-transform: uppercase; letter-spacing: 1.5px; margin-top: 2px; }

/* ── Denomination grid ── */
.denom-grid {
    display: grid; grid-template-columns: repeat(4,1fr); gap: 8px;
}
.denom-chip {
    background: rgba(245,197,24,0.07); border: 1px solid rgba(245,197,24,0.15);
    border-radius: 10px; padding: 10px 8px; text-align: center;
    transition: all 0.2s;
}
.denom-chip:hover { background: rgba(245,197,24,0.14); border-color: rgba(245,197,24,0.4); transform: translateY(-2px); }
.denom-chip .amount { font-family: 'Space Mono', monospace; font-size: 12px; font-weight: 700; color: #F5C518; }
.denom-chip .unit { font-size: 9px; color: rgba(240,240,240,0.4); margin-top: 2px; text-transform: uppercase; letter-spacing: 1px; }

/* ── Main content ── */
.content-area {
    padding: 0 48px;
    display: grid; grid-template-columns: 1fr 1fr; gap: 32px;
}

/* ── Cards ── */
.card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px; padding: 28px;
    position: relative; overflow: hidden;
}
.card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(245,197,24,0.4), transparent);
}
.card-title {
    font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 2.5px;
    color: rgba(245,197,24,0.8); margin-bottom: 20px;
    display: flex; align-items: center; gap: 8px;
}
.card-title::before {
    content: ''; display: block; width: 3px; height: 14px;
    background: #F5C518; border-radius: 2px;
}

/* ── Tabs ── */
.tab-bar {
    display: flex; gap: 4px; margin-bottom: 20px;
    background: rgba(0,0,0,0.3); border-radius: 12px; padding: 4px;
}
.tab-btn {
    flex: 1; padding: 9px; border-radius: 9px; border: none;
    font-family: 'Be Vietnam Pro', sans-serif; font-size: 13px; font-weight: 600;
    cursor: pointer; transition: all 0.2s; color: rgba(240,240,240,0.5);
    background: transparent;
}
.tab-btn.active {
    background: rgba(245,197,24,0.15); color: #F5C518;
    border: 1px solid rgba(245,197,24,0.25);
}

/* ── Result card ── */
.result-main {
    text-align: center; padding: 32px 20px;
}
.result-amount {
    font-family: 'Space Mono', monospace; font-size: 52px; font-weight: 700;
    background: linear-gradient(135deg, #F5C518, #FFF176);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    line-height: 1; margin-bottom: 4px;
}
.result-label {
    font-size: 13px; color: rgba(240,240,240,0.45); letter-spacing: 3px; text-transform: uppercase;
}
.confidence-ring {
    width: 120px; height: 120px; margin: 24px auto;
    position: relative;
}
.conf-text {
    font-family: 'Space Mono', monospace; font-size: 22px; font-weight: 700; color: #F5C518;
    text-align: center;
}
.conf-sublabel { font-size: 10px; color: rgba(240,240,240,0.4); text-align: center; text-transform: uppercase; letter-spacing: 2px; }

/* ── Top-3 bars ── */
.pred-bar-row {
    display: flex; align-items: center; gap: 10px; margin-bottom: 10px;
}
.pred-bar-label { font-family: 'Space Mono', monospace; font-size: 11px; color: #F5C518; width: 80px; text-align: right; flex-shrink: 0; }
.pred-bar-track { flex: 1; height: 6px; background: rgba(255,255,255,0.06); border-radius: 3px; overflow: hidden; }
.pred-bar-fill { height: 100%; border-radius: 3px; transition: width 0.6s ease; }
.pred-bar-pct { font-family: 'Space Mono', monospace; font-size: 10px; color: rgba(240,240,240,0.5); width: 42px; text-align: right; flex-shrink: 0; }

/* ── Upload zone ── */
.upload-hint {
    text-align: center; padding: 40px 20px;
    border: 2px dashed rgba(245,197,24,0.2); border-radius: 16px;
    color: rgba(240,240,240,0.3); font-size: 14px; line-height: 1.8;
}
.upload-icon { font-size: 40px; margin-bottom: 12px; display: block; }

/* ── Camera notice ── */
.cam-notice {
    background: rgba(245,197,24,0.06); border: 1px solid rgba(245,197,24,0.2);
    border-radius: 12px; padding: 14px 18px; font-size: 13px;
    color: rgba(245,197,24,0.8); margin-bottom: 16px;
    display: flex; align-items: flex-start; gap: 10px;
}

/* ── History ── */
.hist-item {
    display: flex; align-items: center; gap: 14px;
    padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.05);
}
.hist-thumb {
    width: 44px; height: 44px; border-radius: 8px; object-fit: cover;
    border: 1px solid rgba(245,197,24,0.2);
}
.hist-thumb-placeholder {
    width: 44px; height: 44px; border-radius: 8px;
    background: rgba(245,197,24,0.1); display: flex; align-items: center; justify-content: center; font-size: 18px;
}
.hist-amount { font-family: 'Space Mono', monospace; font-size: 15px; font-weight: 700; color: #F5C518; }
.hist-conf { font-size: 11px; color: rgba(240,240,240,0.4); }
.hist-time { font-size: 10px; color: rgba(240,240,240,0.25); margin-left: auto; font-family: 'Space Mono', monospace; }

/* ── Empty state ── */
.empty-state {
    text-align: center; padding: 48px 20px;
    color: rgba(240,240,240,0.25); font-size: 13px; line-height: 2;
}
.empty-icon { font-size: 36px; display: block; margin-bottom: 12px; opacity: 0.4; }

/* ── Streamlit widget overrides ── */
.stFileUploader > div { background: transparent !important; border: none !important; }
.stFileUploader label { display: none !important; }
[data-testid="stFileUploadDropzone"] {
    background: rgba(245,197,24,0.04) !important;
    border: 2px dashed rgba(245,197,24,0.25) !important;
    border-radius: 14px !important; min-height: 140px !important;
}
[data-testid="stFileUploadDropzone"]:hover {
    background: rgba(245,197,24,0.08) !important;
    border-color: rgba(245,197,24,0.5) !important;
}
.stButton > button {
    width: 100% !important; background: linear-gradient(135deg, #F5C518, #E8A000) !important;
    color: #0A0A0F !important; font-family: 'Be Vietnam Pro', sans-serif !important;
    font-weight: 700 !important; font-size: 14px !important;
    border: none !important; border-radius: 12px !important; padding: 12px !important;
    letter-spacing: 0.5px !important; transition: all 0.2s !important;
    box-shadow: 0 4px 20px rgba(245,197,24,0.3) !important;
}
.stButton > button:hover { transform: translateY(-1px) !important; box-shadow: 0 8px 28px rgba(245,197,24,0.45) !important; }
.stCamera > div { border-radius: 14px !important; overflow: hidden !important; }
[data-testid="stCameraInput"] video { border-radius: 14px !important; }
[data-testid="stCameraInput"] { border: 1px solid rgba(245,197,24,0.2) !important; border-radius: 16px !important; overflow: hidden !important; }
div[data-testid="stImage"] img { border-radius: 12px; }

/* ── Footer ── */
.footer {
    text-align: center; padding: 40px;
    color: rgba(240,240,240,0.2); font-size: 11px; font-family: 'Space Mono', monospace;
    letter-spacing: 1.5px; border-top: 1px solid rgba(255,255,255,0.04); margin-top: 40px;
}

/* ── Spinner ── */
.scan-anim {
    text-align: center; padding: 20px;
    font-family: 'Space Mono', monospace; font-size: 12px;
    color: rgba(245,197,24,0.7); letter-spacing: 3px; text-transform: uppercase;
}

/* ── Responsive ── */
@media (max-width: 900px) {
    .hero { grid-template-columns: 1fr; padding: 32px 20px 24px; gap: 32px; }
    .content-area { grid-template-columns: 1fr; padding: 0 20px; }
    .site-header { padding: 16px 20px; }
    .stat-row { gap: 20px; }
}
</style>
""", unsafe_allow_html=True)

# ── Model loading ───────────────────────────────────────────────────────────
CLASS_NAMES = ['1000', '10000', '100000', '2000', '20000', '200',
               '200000', '5000', '50000', '500', '500000']

DENOM_DISPLAY = {
    '200': '200đ', '500': '500đ', '1000': '1.000đ', '2000': '2.000đ',
    '5000': '5.000đ', '10000': '10.000đ', '20000': '20.000đ',
    '50000': '50.000đ', '100000': '100.000đ', '200000': '200.000đ', '500000': '500.000đ'
}

DENOM_COLOR = {
    '200': '#7EC8E3', '500': '#A8D8A8', '1000': '#FFD700', '2000': '#FF8C94',
    '5000': '#B388FF', '10000': '#FF6E40', '20000': '#4FC3F7',
    '50000': '#81C784', '100000': '#F48FB1', '200000': '#FFB74D', '500000': '#CE93D8'
}

IMG_SIZE = (128, 128)

@st.cache_resource(show_spinner=False)
def load_model():
    """Load model – tìm file .keras hoặc .h5 trong thư mục model/"""
    try:
        import tensorflow as tf
        model_dir = os.path.join(os.path.dirname(__file__), 'model')
        for ext in ['*.keras', '*.h5']:
            import glob as _glob
            files = _glob.glob(os.path.join(model_dir, ext))
            if files:
                m = tf.keras.models.load_model(files[0])
                return m, None
        return None, "Chưa tìm thấy file model trong thư mục `model/`"
    except Exception as e:
        return None, str(e)

def preprocess(pil_img: Image.Image) -> np.ndarray:
    img = pil_img.convert('RGB').resize(IMG_SIZE)
    arr = np.array(img, dtype=np.float32) / 255.0
    return np.expand_dims(arr, 0)

def predict(model, pil_img: Image.Image):
    arr   = preprocess(pil_img)
    proba = model.predict(arr, verbose=0)[0]
    top3  = np.argsort(proba)[::-1][:3]
    return [(CLASS_NAMES[i], float(proba[i])) for i in top3]

def img_to_b64(pil_img: Image.Image, size=(44, 44)) -> str:
    thumb = pil_img.convert('RGB').resize(size)
    buf = io.BytesIO()
    thumb.save(buf, format='JPEG', quality=70)
    return base64.b64encode(buf.getvalue()).decode()

# ── Session state ───────────────────────────────────────────────────────────
if 'history' not in st.session_state:
    st.session_state.history = []
if 'tab' not in st.session_state:
    st.session_state.tab = 'upload'
if 'result' not in st.session_state:
    st.session_state.result = None
if 'preview_img' not in st.session_state:
    st.session_state.preview_img = None

model, model_err = load_model()

# ── HEADER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-wrapper">
<div class="site-header">
  <div class="logo">
    <div class="logo-mark">💴</div>
    <div>
      <div class="logo-text">VietCash</div>
      <div class="logo-sub">AI Currency · VN</div>
    </div>
  </div>
  <div class="header-badge">CNN · MobileNetV2</div>
</div>
""", unsafe_allow_html=True)

# ── HERO ────────────────────────────────────────────────────────────────────
denom_chips = ''.join([
    f'<div class="denom-chip"><div class="amount">{DENOM_DISPLAY[k]}</div><div class="unit">VNĐ</div></div>'
    for k in ['200','500','1000','2000','5000','10000','20000','50000','100000','200000','500000']
])

st.markdown(f"""
<div class="hero">
  <div class="hero-left">
    <h1>Nhận diện<br><span>tiền Việt Nam</span><br>tức thì</h1>
    <p>Chụp ảnh hoặc upload ảnh tờ tiền — AI phân tích và trả kết quả trong vài giây. Hỗ trợ đầy đủ 11 mệnh giá từ 200đ đến 500.000đ.</p>
    <div class="stat-row">
      <div class="stat-item"><div class="stat-num">11</div><div class="stat-label">Mệnh giá</div></div>
      <div class="stat-item"><div class="stat-num">~95%</div><div class="stat-label">Accuracy</div></div>
      <div class="stat-item"><div class="stat-num">&lt;1s</div><div class="stat-label">Phân tích</div></div>
    </div>
  </div>
  <div>
    <div class="denom-grid">{denom_chips}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── CONTENT AREA ────────────────────────────────────────────────────────────
st.markdown('<div class="content-area">', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

# ──────────────────────────────
# LEFT: Input
# ──────────────────────────────
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Nhập ảnh</div>', unsafe_allow_html=True)

    # Tab switcher
    t1, t2 = st.columns(2)
    with t1:
        if st.button("📁  Upload ảnh",
                     type="primary" if st.session_state.tab == 'upload' else "secondary",
                     use_container_width=True):
            st.session_state.tab = 'upload'
            st.rerun()
    with t2:
        if st.button("📷  Chụp Camera",
                     type="primary" if st.session_state.tab == 'camera' else "secondary",
                     use_container_width=True):
            st.session_state.tab = 'camera'
            st.rerun()

    st.markdown("---")

    input_img = None

    if st.session_state.tab == 'upload':
        uploaded = st.file_uploader(
            "Chọn ảnh",
            type=['jpg', 'jpeg', 'png', 'webp'],
            label_visibility="collapsed"
        )
        if uploaded:
            input_img = Image.open(uploaded)
            st.image(input_img, use_container_width=True, caption="Ảnh đã chọn")

    else:  # camera
        st.markdown("""
        <div class="cam-notice">
          <span>📡</span>
          <div><b>Camera Mode</b> — Chụp ảnh tờ tiền trong khung hình, sau đó nhấn <b>Nhận diện</b>.</div>
        </div>
        """, unsafe_allow_html=True)
        cam_img = st.camera_input("Chụp ảnh tiền", label_visibility="collapsed")
        if cam_img:
            input_img = Image.open(cam_img)

    # Analyze button
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_btn = st.button("🔍  Nhận diện ngay", use_container_width=True, type="primary")

    if analyze_btn:
        if input_img is None:
            st.warning("⚠️ Vui lòng chọn ảnh hoặc chụp camera trước!")
        elif model is None:
            st.error(f"❌ Model chưa được tải: {model_err}")
        else:
            with st.spinner("Đang phân tích..."):
                time.sleep(0.3)
                preds = predict(model, input_img)
                st.session_state.result = preds
                st.session_state.preview_img = input_img.copy()
                # Add to history
                st.session_state.history.insert(0, {
                    'preds': preds,
                    'thumb': img_to_b64(input_img),
                    'time': time.strftime('%H:%M:%S')
                })
                if len(st.session_state.history) > 8:
                    st.session_state.history = st.session_state.history[:8]
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ──────────────────────────────
# RIGHT: Result
# ──────────────────────────────
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Kết quả phân tích</div>', unsafe_allow_html=True)

    if st.session_state.result is None:
        st.markdown("""
        <div class="empty-state">
          <span class="empty-icon">🔎</span>
          Chưa có kết quả<br>
          Chọn ảnh và nhấn <b>Nhận diện ngay</b>
        </div>
        """, unsafe_allow_html=True)
    else:
        preds = st.session_state.result
        top_class, top_conf = preds[0]
        disp = DENOM_DISPLAY.get(top_class, top_class + 'đ')
        color = DENOM_COLOR.get(top_class, '#F5C518')

        # Main result
        st.markdown(f"""
        <div class="result-main">
          <div class="result-amount" style="background: linear-gradient(135deg, {color}, #FFFFFF88);
               -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{disp}</div>
          <div class="result-label">Mệnh giá nhận diện</div>
        </div>
        """, unsafe_allow_html=True)

        # Confidence
        conf_pct = int(top_conf * 100)
        status = "✅ Rất chắc chắn" if conf_pct >= 90 else "⚠️ Khá chắc chắn" if conf_pct >= 70 else "❓ Không chắc"
        st.metric(label=status, value=f"{conf_pct}%", delta="Confidence")

        # Top-3 bars
        st.markdown("**Top 3 dự đoán:**")
        for i, (cls, prob) in enumerate(preds):
            pct = prob * 100
            bar_color = '#F5C518' if i == 0 else '#888' if i == 1 else '#555'
            width = int(pct)
            label = DENOM_DISPLAY.get(cls, cls + 'đ')
            st.markdown(f"""
            <div class="pred-bar-row">
              <div class="pred-bar-label">{label}</div>
              <div class="pred-bar-track">
                <div class="pred-bar-fill" style="width:{width}%;background:{bar_color};"></div>
              </div>
              <div class="pred-bar-pct">{pct:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)

        # Preview thumb
        if st.session_state.preview_img:
            st.markdown("<br>", unsafe_allow_html=True)
            st.image(st.session_state.preview_img, use_container_width=True,
                     caption=f"Ảnh đã phân tích · {disp}")

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # content-area

# ── HISTORY ─────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
hist_col, _ = st.columns([2, 1])
with hist_col:
    st.markdown('<div style="padding: 0 48px;">', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:11px;font-weight:600;text-transform:uppercase;
         letter-spacing:2.5px;color:rgba(245,197,24,0.8);margin-bottom:16px;
         display:flex;align-items:center;gap:8px;">
      <span style="display:block;width:3px;height:14px;background:#F5C518;border-radius:2px;"></span>
      Lịch sử nhận diện
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.history:
        st.markdown("""
        <div style="color:rgba(240,240,240,0.2);font-size:13px;padding:16px 0;">
          Chưa có lịch sử — kết quả sẽ hiện ở đây sau khi bạn nhận diện.
        </div>
        """, unsafe_allow_html=True)
    else:
        for item in st.session_state.history:
            top_cls, top_conf = item['preds'][0]
            disp = DENOM_DISPLAY.get(top_cls, top_cls + 'đ')
            color = DENOM_COLOR.get(top_cls, '#F5C518')
            conf_pct = int(top_conf * 100)
            st.markdown(f"""
            <div class="hist-item">
              <img src="data:image/jpeg;base64,{item['thumb']}" class="hist-thumb">
              <div>
                <div class="hist-amount" style="color:{color};">{disp}</div>
                <div class="hist-conf">{conf_pct}% confidence</div>
              </div>
              <div class="hist-time">{item['time']}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑 Xóa lịch sử", use_container_width=False):
            st.session_state.history = []
            st.session_state.result = None
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ── MODEL STATUS ─────────────────────────────────────────────────────────────
if model is None:
    st.markdown("""
    <div style="margin: 0 48px 20px; padding: 20px 24px;
         background: rgba(255,80,80,0.07); border: 1px solid rgba(255,80,80,0.25);
         border-radius: 14px; font-size: 13px;">
      <b style="color:#FF6B6B;">⚠️ Model chưa được tải</b><br><br>
      Để app hoạt động, cần đặt file model (<code>.keras</code> hoặc <code>.h5</code>)
      vào thư mục <code>model/</code> trong project.<br><br>
      <b>Cách train model:</b> Chạy notebook <code>CNN_TienVietNam_Drive.ipynb</code>,
      sau đó download file <code>.keras</code> và đặt vào <code>model/</code>.
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="margin: 0 48px 20px; padding: 12px 20px;
         background: rgba(46,204,113,0.07); border: 1px solid rgba(46,204,113,0.2);
         border-radius: 12px; font-size: 12px; color: rgba(46,204,113,0.8);">
      ✅ Model đã sẵn sàng · MobileNetV2 Transfer Learning · 11 mệnh giá
    </div>
    """, unsafe_allow_html=True)

# ── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  VIETCASH · CNN IMAGE CLASSIFICATION · DATASET BY NGUYỄN TRỌNG ĐẠI · UEH LOGISTICS
</div>
</div>
""", unsafe_allow_html=True)
