import streamlit as st
import time
import random
import pandas as pd

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Gamelan Melayu Interaktif",
    page_icon="🎶",
    layout="wide"
)

# ===============================
# SIDEBAR CSS  ← LETAK SINI
# ===============================
st.markdown("""
<style>
/* Sidebar background */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2E1A12, #4E342E, #5D4037);
    border-right: 2px solid #8D6E63;
}

/* Sidebar label (contoh: Pilih Menu) */
[data-testid="stSidebar"] label {
    color: #FFF8E1 !important;
    font-weight: 700;
}

/* Sidebar selectbox */
[data-testid="stSidebar"] select {
    background-color: #3E2723 !important;
    color: #FFF8E1 !important;
    border-radius: 8px;
    border: 1px solid #8D6E63;
}

/* Dropdown options */
[data-testid="stSidebar"] option {
    background-color: #3E2723;
    color: #FFF8E1;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# THEME CSS (GLOBAL)
# =========================================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#2E1A12,#4E342E,#8D6E63);
    color:#FFF8E1;
    font-family: Georgia, serif;
}
h1,h2,h3 {color:#FFD700; text-align:center;}
div.stButton > button {
    background: linear-gradient(#D4AF37,#AA8C2C);
    color:black;
    font-weight:bold;
    border-radius:10px;
    height:70px;
}
.notation-box {
    font-family: monospace;
    background:#111;
    color:#00FF88;
    padding:15px;
    border-left:5px solid gold;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# DATA
# =========================================================
instruments = {
    "Saron": {
        "image":"https://upload.wikimedia.org/wikipedia/commons/6/69/Saron_demung_STSI.jpg",
        "desc":"Melodi asas",
        "hint":"Bunyi yang tajam dan jelas"
    },
    "Bonang":{
        "image":"https://upload.wikimedia.org/wikipedia/commons/a/a2/Bonang_barung_STSI.jpg",
        "desc":"Melodi hiasan",
        "hint":"Bunyi yang berdering dan merdu"
    },
    "Gambang":{
        "image":"https://upload.wikimedia.org/wikipedia/commons/a/a0/Gambang_STSI.jpg",
        "desc":"Tekstur kayu",
        "hint":"Bunyi yang lembut dan hangat"
    },
    "Kenong":{
        "image":"https://upload.wikimedia.org/wikipedia/commons/6/63/Kenong_Japan.jpg",
        "desc":"Struktur lagu",
        "hint":"Bunyi yang dalam dan bergema"
    },
    "Gong":{
        "image":"https://upload.wikimedia.org/wikipedia/commons/0/03/Gong_ageng_kempul_suwukan_STSI.jpg",
        "desc":"Penamat frasa",
        "hint":"Bunyi yang kuat dan berkuasa"
    }
}

songs = {
    "Timang Burung": {
        "notes":["1","2","3","5","6"],
        "labels":["Do","Re","Mi","So","La"],
        "notation":"""
TIMANG BURUNG
| -2 2 3 | 6 5 3 2 | 3 2 1 1 | 5 5 3 5 |
| -5 5 2 | 3 2 3 5 | -3 5 6 | 5 3 2 5 |
| -5 5 2 | 3 2 3 5 1 | -3 5 6 | 5 3 2 3 1 |
| -3 2 1 | 1 2 3 1 | 3 2 1 1 | 5 6 i 2 |
| -2 2 3 | 6 5 3 2 | 3 2 1 1 | 5 5 3 5 |
""",
        "sequence":[
            "-2","2","3","6","5","3","2","3","2","1","1","5","5","3","5",
            "-5","5","2","3","2","3","5","-3","5","6","5","3","2","5",
            "-5","5","2","3","2","3","5","1","-3","5","6","5","3","2","3","1",
            "-3","2","1","1","2","3","1","3","2","1","1","5","6","i","2",
            "-2","2","3","6","5","3","2","3","2","1","1","5","5","3","5"
        ]
    },
    "Lenggang Kangkung": {
        "notes":["1","2","3","5","6"],
        "labels":["Do","Re","Mi","So","La"],
        "notation":"""
LENGGANG KANGKUNG
| 5 3 5 5 | 5 5 - - | 5 6 5 6 i | 6 5 - - |
| 5 3 5 5 | 5 5 - - | 5 6 5 6 i | 6 5 - - |
| 3 1 1 2 3 | 6 5 6 5 | 3 2 1 2 3 | 2 1 - - |
| .i 6 1 2 | 1 2 3 2 1 | .i 6 1 2 | 1 2 3 2 1 |
""",
        "sequence":[
            "5","3","5","5","5","5","-","-","5","6","5","6","i","6","5","-","-",
            "5","3","5","5","5","5","-","-","5","6","5","6","i","6","5","-","-",
            "3","1","1","2","3","6","5","6","5","3","2","1","2","3","2","1","-","-",
            "i","6","1","2","1","2","3","2","1",
            "i","6","1","2","1","2","3","2","1"
        ]
    }
}

# =========================================================
# FUNCTIONS
# =========================================================
def play_note(inst, song, note):
    st.toast(f"🔊 {inst}: {note}")

def auto_play(inst, song_name):
    st.info(f"▶️ Memainkan {song_name} secara automatik...")
    for note in songs[song_name]["sequence"]:
        play_note(inst, song_name, note)
        time.sleep(0.3)

def auto_play_silent(song):
    audio_path = songs[song]

    if os.path.exists(audio_path):
        st.audio(audio_path, format="audio/mp3")
    else:
        st.error(f"❌ Audio tak jumpa: {audio_path}")

def origin_map():
    st.subheader("🗺️ Asal-usul Gamelan")
    df = pd.DataFrame({"lat":[-7.25,4.21,6.86], "lon":[112.76,101.97,101.25]})
    st.map(df)

def safe_rerun():
    # Streamlit baru ada st.rerun(); kita guard supaya tak crash kalau version lain.
    if hasattr(st, "rerun"):
        st.rerun()

# =========================================================
# SIDEBAR NAVIGATION
# =========================================================
menu = st.sidebar.selectbox(
    "Pilih Menu",
    ["Studio Interaktif", "Demo Lagu Penuh", "Kuiz Bunyi", "Peta Asal-usul"]
)

# =========================================================
# STUDIO INTERAKTIF
# =========================================================
if menu == "Studio Interaktif":
    st.header("🎹 Studio Interaktif")
    inst = st.selectbox("Pilih Instrumen", list(instruments.keys()), key="studio_inst")
    song = st.selectbox("Pilih Lagu", list(songs.keys()), key="studio_song")

    st.image(instruments[inst]["image"])
    st.write(instruments[inst]["desc"])
    st.markdown(f'<div class="notation-box">{songs[song]["notation"]}</div>', unsafe_allow_html=True)

    cols = st.columns(5)
    for i, (note, label) in enumerate(zip(songs[song]["notes"], songs[song]["labels"])):
        with cols[i]:
            if st.button(f"{label}\n{note}", key=f"studio_note_{song}_{i}"):
                play_note(inst, song, note)

    if st.button(f"▶️ Main Skala {song} (Auto)", use_container_width=True, key="studio_auto"):
        auto_play(inst, song)

# =========================================================
# DEMO LAGU
# =========================================================
elif menu == "Demo Lagu Penuh":
    st.header("🎧 Demo Lagu Penuh")
    song = {
    "Timang Burung": "demo/timang_burung.mp3",
    "Lenggang Kangkung": "demo/lenggang_kangkung.mp3",
}


    if "music_playing" not in st.session_state:
        st.session_state.music_playing = False

    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ Main Lagu", use_container_width=True, key="demo_play"):
            st.session_state.music_playing = True
            auto_play_silent(song)
            st.session_state.music_playing = False

    with col2:
        if st.button("⏹️ Hentikan", use_container_width=True, key="demo_stop"):
            st.session_state.music_playing = False
            st.audio(b"")
            st.toast("⏹️ Muzik dihentikan")
            safe_rerun()
    st.caption("Kredit : YouTube : WarisanNusantara - Warisan Gamelan Melayu - Timang Burung, Youtube : cataloQue - Lenggang Kangkung")

# =========================================================
# QUIZ BUNYI (STRUCTURED GAME)
# =========================================================

elif menu == "Kuiz Bunyi":

    # Quiz-only CSS
    st.markdown("""
    <style>
    .quiz-wrap {max-width: 980px; margin: 0 auto;}
    .quiz-top {display:flex; gap:14px; align-items:flex-start; justify-content:space-between; margin: 8px 0 14px 0;}
    .scorebox {
        background:#FFF8E1;
        padding:6px 10px;
        border-radius:8px;
        border:1px solid #DDD;
        width:120px;
        text-align:center;
        font-weight:700;
        font-size:13px;
        color:black;
    }
    .quiz-card {
        background:#3E2723;
        padding:18px 18px;
        border-radius:14px;
        border:1px solid #5D4037;
        margin-bottom:12px;
    }
    .quiz-title {font-size:20px; font-weight:800; color:white; margin-bottom:6px;}
    .quiz-hint {color:white; opacity:0.9; font-style:italic; margin-bottom:10px;}

    /* RADIO - WHITE TEXT, CLEAN */
    div[role="radiogroup"] input[type="radio"] {display:none;}
    div[role="radiogroup"] label{
        background:#5D4037;
        padding:8px 14px;
        border-radius:10px;
        border:1px solid #7B5E57;
        cursor:pointer;
        margin-right:8px;
        margin-bottom:6px;
        display:inline-block;
    }
    div[role="radiogroup"] label > div {color:white !important; font-weight:700;}
    div[role="radiogroup"] label:hover {background:#6D4C41;}
    div[role="radiogroup"] input[type="radio"]:checked + div {
        background:#8D6E63;
        color:white !important;
    }

    /* make quiz buttons smaller than global */
    div.stButton > button {height:52px !important; border-radius:12px !important;}
    </style>
    """, unsafe_allow_html=True)

    st.header("🎯 Kuiz Bunyi Gamelan")

    TOTAL_QUESTIONS = min(5, len(instruments))

    # init game state (prefix quiz_)
    if "quiz_order" not in st.session_state:
        st.session_state.quiz_order = random.sample(list(instruments.keys()), k=len(instruments))
    if "quiz_idx" not in st.session_state:
        st.session_state.quiz_idx = 0
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0

    def quiz_reset():
        st.session_state.quiz_order = random.sample(list(instruments.keys()), k=len(instruments))
        st.session_state.quiz_idx = 0
        st.session_state.quiz_score = 0

    # end game
    if st.session_state.quiz_idx >= TOTAL_QUESTIONS:
        st.success(f"🎉 Tamat! Skor akhir: {st.session_state.quiz_score}/{TOTAL_QUESTIONS}")
        if st.button("🔄 Main Semula", use_container_width=True, key="quiz_retry_end"):
            quiz_reset()
            safe_rerun()
        st.stop()

    secret = st.session_state.quiz_order[st.session_state.quiz_idx]
    q_no = st.session_state.quiz_idx + 1

    st.markdown('<div class="quiz-wrap">', unsafe_allow_html=True)

    # top bar (progress + small score)
    st.markdown('<div class="quiz-top">', unsafe_allow_html=True)
    st.progress(min((q_no - 1) / TOTAL_QUESTIONS, 1.0))
    st.markdown(f'<div class="scorebox">Skor: {st.session_state.quiz_score}/{TOTAL_QUESTIONS}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # question card
    st.markdown(f"""
    <div class="quiz-card">
        <div class="quiz-title">Soalan {q_no}</div>
        <div class="quiz-hint">💡 Hint: {instruments[secret]["hint"]}</div>
    </div>
    """, unsafe_allow_html=True)

    # sound button (optional)
    if st.button("🔊 Main Bunyi Misteri", use_container_width=True, key=f"quiz_play_{st.session_state.quiz_idx}"):
        st.toast("🎵 Bunyi misteri dimainkan")

    # answers (unique key per question so it doesn’t “stick”)
    guess = st.radio(
        "",
        list(instruments.keys()),
        horizontal=True,
        label_visibility="collapsed",
        key=f"quiz_guess_{st.session_state.quiz_idx}"
    )

    # check answer: update score immediately, show feedback briefly, then next question
    if st.button("✓ Semak Jawapan", use_container_width=True, key=f"quiz_check_{st.session_state.quiz_idx}"):
        if guess == secret:
            st.session_state.quiz_score += 1
            st.info("✅ Betul!")
        else:
            st.info(f"❌ Salah! Jawapan betul: {secret}")

        time.sleep(0.9)  # bagi user nampak feedback sekejap
        st.session_state.quiz_idx += 1
        safe_rerun()

    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# ORIGIN MAP
# =========================================================
elif menu == "Peta Asal-usul":
    origin_map()

# =========================================================
# FOOTER
# =========================================================
st.markdown("<center style='color:gold'>Warisan Budaya Kita 🇲🇾</center>", unsafe_allow_html=True)




