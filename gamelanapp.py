import base64
import os
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

def parse_sequence(sequence_text):
    return sequence_text.split()

# =========================================================
# DATA
# =========================================================
PHOTO_DIR = os.path.join(os.path.dirname(__file__), "photos")

instruments = {
    "Saron": {
        "image":"saron.jpg",
        "desc":"Melodi asas",
        "function":"Memainkan melodi utama yang memandu lagu.",
        "sound":"tajam",
        "role":"Pemimpin keluarga yang menetapkan arah dan tempo.",
        "hint":"Bunyi yang tajam dan jelas"
    },
    "Bonang":{
        "image":"bonang.jpg",
        "desc":"Melodi hiasan",
        "function":"Menghias melodi dengan variasi yang berkilau.",
        "sound":"berlapis",
        "role":"Anak sulung yang menceriakan suasana keluarga.",
        "hint":"Bunyi yang berdering dan merdu"
    },
    "Gambang":{
        "image":"gambang.jpg",
        "desc":"Tekstur kayu",
        "function":"Menambah tekstur kayu yang lembut dalam lagu.",
        "sound":"lembut",
        "role":"Adik yang membawa kelembutan dan harmoni.",
        "hint":"Bunyi yang lembut dan hangat"
    },
    "Kenong":{
        "image":"kenong.jpg",
        "desc":"Struktur lagu",
        "function":"Menanda struktur dan bahagian dalam lagu.",
        "sound":"dalam",
        "role":"Nenek yang menandakan giliran dan susunan keluarga.",
        "hint":"Bunyi yang dalam dan bergema"
    },
    "Gong":{
        "image":"gong.jpg",
        "desc":"Penamat frasa",
        "function":"Menutup frasa dengan penegasan yang padu.",
        "sound":"dalam",
        "role":"Datuk yang mengakhiri cerita dengan wibawa.",
        "hint":"Bunyi yang kuat dan berkuasa"
    }
}

songs = {
    "Timang Burung": {
        "notes":["1","2","3","5","6"],
        "labels":["Do","Re","Mi","So","La"],
        "notation":"""
TIMANG BURUNG
| - 2 2 3 | 6 5 3 2 | 3 2 1 1 | 5 5 3 5 |
| - 5 5 2 | 3 2 3 5 | - 3 5 6 | 5 3 2 5 |
| - 5 5 2 | 3 2 3 5 1 | - 3 5 6 | 5 3 2 3 1 |
| - 3 2 1 | 1 2 3 1 | 3 2 1 1 | 5 6 i 2 |
| - 2 2 3 | 6 5 3 2 | 3 2 1 1 | 5 5 3 5 |
""",
        "sequence": parse_sequence("""
            - 2 2 3 6 5 3 2 3 2 1 1 5 5 3 5
            - 5 5 2 3 2 3 5 - 3 5 6 5 3 2 5
            - 5 5 2 3 2 3 5 1 - 3 5 6 5 3 2 3 1
            - 3 2 1 1 2 3 1 3 2 1 1 5 6 i 2
            - 2 2 3 6 5 3 2 3 2 1 1 5 5 3 5
        """)
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
        "sequence": parse_sequence("""
            5 3 5 5 5 5 - - 5 6 5 6 i 6 5 - -
            5 3 5 5 5 5 - - 5 6 5 6 i 6 5 - -
            3 1 1 2 3 6 5 6 5 3 2 1 2 3 2 1 - -
            i 6 1 2 1 2 3 2 1
            i 6 1 2 1 2 3 2 1
        """)
    }
}

# =========================================================
# FUNCTIONS
# =========================================================
def play_note(inst, song, note):
    st.toast(f"🔊 {inst}: {note}")

def instrument_image_path(image_name):
    local_path = os.path.join(PHOTO_DIR, image_name)
    if os.path.exists(local_path):
        return local_path
    return None

def auto_play_step(inst, song_name):
    sequence = songs[song_name]["sequence"]
    idx = st.session_state.get("autoplay_idx", 0)
    if idx >= len(sequence):
        st.session_state.autoplay_active = False
        st.session_state.autoplay_idx = 0
        st.toast("✅ Mainan selesai")
        return
    play_note(inst, song_name, sequence[idx])
    st.session_state.autoplay_idx = idx + 1
    time.sleep(0.3)

def render_audio_player(audio_path, autoplay=False, element_id="demo-audio"):
    if os.path.exists(audio_path):
        with open(audio_path, "rb") as audio_file:
            audio_base64 = base64.b64encode(audio_file.read()).decode("utf-8")
        autoplay_attr = "autoplay" if autoplay else ""
        st.markdown(
            f"""
            <audio id="{element_id}" controls {autoplay_attr} controlslist="nodownload noplaybackrate" style="width:100%;">
                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
            """,
            unsafe_allow_html=True
        )
    else:
        st.error(f"❌ Audio tak jumpa: {audio_path}")

def origin_map():
    st.subheader("🗺️ Asal-usul Gamelan")
    df = pd.DataFrame({"lat":[-7.25,4.21,6.86], "lon":[112.76,101.97,101.25]})
    st.map(df)

def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()

# =========================================================
# SIDEBAR NAVIGATION
# =========================================================
menu = st.sidebar.selectbox(
    "Pilih Menu",
    ["Kenali Bunyi Instrumen","Studio Interaktif", "Demo Lagu Penuh", "Kuiz Bunyi"]
)

# KENALI BUNYI INSTRUMEN

if menu == "Kenali Bunyi Instrumen":
    st.header("Kenal Instrumen")
    st.caption("Info ringkas tentang instrumen utama gamelan.")

    st.markdown("""
    <style>
    .inst-card {
        background:#3E2723;
        padding:16px;
        border-radius:14px;
        border:1px solid #5D4037;
        margin-bottom:16px;
    }
    .inst-title {font-size:20px; font-weight:800; color:#FFD700; margin-bottom:6px;}
    .inst-meta {color:#FFF8E1; margin-bottom:6px;}
    </style>
    """, unsafe_allow_html=True)

    inst_items = list(instruments.items())
    for row_start in range(0, len(inst_items), 2):
        cols = st.columns(2)
        for col, (name, info) in zip(cols, inst_items[row_start:row_start + 2]):
            with col:
                image_path = instrument_image_path(info["image"])
                if image_path:
                    st.image(image_path, use_container_width=True)
                else:
                    st.warning(f"Gambar tidak dijumpai: photos/{info['image']}")
                st.markdown(
                    f"""
                    <div class="inst-card">
                        <div class="inst-title">{name}</div>
                        <div class="inst-meta"><strong>Fungsi:</strong> {info["function"]}</div>
                        <div class="inst-meta"><strong>Bunyi macam apa?</strong> {info["sound"]}</div>
                        <div class="inst-meta"><strong>Peranan dalam simfoni kekeluargaan:</strong> {info["role"]}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# =========================================================
# STUDIO INTERAKTIF
# =========================================================
elif menu == "Studio Interaktif":
    st.header("🎶 Studio Interaktif")
    inst = st.selectbox("Pilih Instrumen", list(instruments.keys()), key="studio_inst")
    song = st.selectbox("Pilih Lagu", list(songs.keys()), key="studio_song")
    studio_image_path = instrument_image_path(instruments[inst]["image"])
    if studio_image_path:
        st.image(studio_image_path)
    else:
        st.warning(f"Gambar tidak dijumpai: photos/{instruments[inst]['image']}")
    st.write(instruments[inst]["desc"])
    st.markdown(f'<div class="notation-box">{songs[song]["notation"]}</div>', unsafe_allow_html=True)

    cols = st.columns(5)
    for i, (note, label) in enumerate(zip(songs[song]["notes"], songs[song]["labels"])):
        with cols[i]:
            if st.button(f"{label}\n{note}", key=f"studio_note_{song}_{i}"):
                play_note(inst, song, note)

    if "autoplay_active" not in st.session_state:
        st.session_state.autoplay_active = False
    if "autoplay_idx" not in st.session_state:
        st.session_state.autoplay_idx = 0

    if st.button(f"▶️ Main Skala {song} (Auto)", use_container_width=True, key="studio_auto"):
        st.session_state.autoplay_active = True
        st.session_state.autoplay_idx = 0

    if st.button("⏹️ Henti Main", use_container_width=True, key="studio_stop"):
        st.session_state.autoplay_active = False
        st.session_state.autoplay_idx = 0
        st.toast("⏹️ Audio dihentikan")
        
    if st.session_state.autoplay_active:
        st.info(f"▶️ Memainkan {song} secara automatik...")
        auto_play_step(inst, song)
        if st.session_state.autoplay_active:
            safe_rerun()

# =========================================================
# DEMO LAGU
# =========================================================
elif menu == "Demo Lagu Penuh":␊
    st.header("🎧 Demo Lagu Penuh")␊
    demo_songs = {␊
        "Timang Burung": "demo/timang_burung.mp3",␊
        "Lenggang Kangkung": "demo/lenggang_kangkung.mp3",␊
    }

    song = st.selectbox("Pilih Lagu Demo", list(demo_songs.keys()), key="demo_song")

    if "music_playing" not in st.session_state:
        st.session_state.music_playing = False
    if "demo_play_id" not in st.session_state:
        st.session_state.demo_play_id = 0

    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ Main Lagu", use_container_width=True, key="demo_play"):
            st.session_state.music_playing = True
            st.session_state.demo_play_id += 1

    with col2:
        if st.button("⏹️ Hentikan", use_container_width=True, key="demo_stop"):
            st.session_state.music_playing = False
            st.toast("⏹️ Muzik dihentikan")
            safe_rerun()

    if st.session_state.music_playing:
        render_audio_player(
            demo_songs[song],
            autoplay=True,
            element_id=f"demo-audio-{st.session_state.demo_play_id}"
        )
            
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




















