
import re
import requests
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Geoquest-Of-Nightmares",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -------------------- THEME --------------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(155deg, #061F2B 0%, #0B3945 52%, #10545A 100%);
    color: #F0FFFC;
}
header[data-testid="stHeader"] {
    background: transparent;
}
footer {visibility: hidden;}
#MainMenu {visibility: hidden;}

.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3, p, label, .stMarkdown {
    color: #F0FFFC;
}
h1, h2 { letter-spacing: 0.3px; }

div.stButton > button,
div.stFormSubmitButton > button,
div.stLinkButton > a {
    background: linear-gradient(90deg, #19A99B, #46D6BE);
    color: #062D36 !important;
    border: 1px solid #68F0D9;
    border-radius: 14px;
    font-weight: 800;
    min-height: 3rem;
    transition: 0.2s ease;
}
div.stButton > button:hover,
div.stFormSubmitButton > button:hover {
    background: #7BF5DC;
    border-color: #FFFFFF;
    transform: translateY(-2px);
}
div[data-testid="stForm"],
div[data-testid="stExpander"] {
    background: rgba(9, 58, 69, 0.82);
    border: 1px solid #287A7C;
    border-radius: 18px;
    padding: 12px;
}
div[data-testid="stTextInput"] input {
    background: #F0FFFC;
    color: #092F3A;
    border-radius: 10px;
}
div[data-testid="stProgressBar"] > div > div {
    background: #55E3C5;
}
div[data-testid="stAlert"] {
    border-radius: 14px;
}
.quest-card {
    background: linear-gradient(135deg, #104653, #0C3946);
    border: 1px solid #267A7C;
    border-radius: 20px;
    padding: 23px;
    margin: 10px 0;
    min-height: 155px;
}
.hero {
    text-align: center;
    padding: 30px 12px 20px 12px;
}
.hero-title {
    color: #75F0D5;
    font-size: clamp(32px, 5vw, 55px);
    line-height: 1.15;
    font-weight: 900;
    letter-spacing: 1px;
}
.hero-subtitle {
    color: #E7FFFA;
    font-size: clamp(19px, 3vw, 28px);
    font-weight: 800;
    margin-top: 24px;
}
.hero-description {
    color: #C9F6ED;
    font-size: 18px;
    line-height: 1.8;
    margin: 18px auto;
}
.section-heading {
    text-align: center;
    color: #75F0D5;
    font-size: 27px;
    font-weight: 900;
    padding: 12px 0;
}
.centered { text-align: center; }
.gold { color: #FFD777; }
.small-note { color: #BFEAE2; font-size: 14px; }
</style>
""", unsafe_allow_html=True)


# -------------------- SECRET LOCATIONS --------------------

ROUNDS = [
    {
        "name": "Gudaibiya, Bahrain",
        "answer": ["gudaibiya", "bahrain"],
        "photo_search": "Gudaibiya Bahrain",
        "lat": 26.2185,
        "lon": 50.5830,
        "clues": [
            "🌍 This place is in the Middle East.",
            "🏝️ It is in an island country in the Persian Gulf.",
            "🏎️ The country hosts a Formula One Grand Prix.",
            "🏙️ Its capital is Manama.",
        ],
    },
    {
        "name": "Zagreb, Croatia",
        "answer": ["zagreb", "croatia"],
        "photo_search": "Zagreb Croatia",
        "lat": 45.8150,
        "lon": 15.9819,
        "clues": [
            "🌍 This place is in Europe.",
            "🌊 The country borders the Adriatic Sea.",
            "🇭🇷 Its flag has red, white and blue.",
            "🏙️ You are looking for the country's capital.",
        ],
    },
    {
        "name": "Uttarakhand, India",
        "answer": ["uttarakhand", "india"],
        "photo_search": "Uttarakhand Himalayas India",
        "lat": 30.0869,
        "lon": 79.0193,
        "clues": [
            "🌏 This place is in South Asia.",
            "🏔️ The Himalayas are a major geographical feature.",
            "🛕 It is famous for pilgrimage sites and hill stations.",
            "🇮🇳 It is a state in India.",
        ],
    },
    {
        "name": "Khabarovsk, Russia",
        "answer": ["khabarovsk", "russia"],
        "photo_search": "Khabarovsk Russia",
        "lat": 48.4802,
        "lon": 135.0719,
        "clues": [
            "🌏 This place is in Asia.",
            "❄️ It is in the Russian Far East.",
            "🌊 The Amur River runs alongside the city.",
            "🔤 The city's name starts with K.",
        ],
    },
]


# -------------------- LOCATION PHOTOS --------------------

@st.cache_data(ttl=3600, show_spinner=False)
def get_location_photos(search_term):
    """Find location-related photographs on Wikimedia Commons."""
    try:
        response = requests.get(
            "https://commons.wikimedia.org/w/api.php",
            params={
                "action": "query",
                "generator": "search",
                "gsrsearch": search_term + " photograph",
                "gsrnamespace": 6,
                "gsrlimit": 6,
                "prop": "imageinfo",
                "iiprop": "url",
                "iiurlwidth": 1100,
                "format": "json",
            },
            headers={
                "User-Agent": "GeoquestOfNightmares/1.0 (birthday game)"
            },
            timeout=12,
        )
        response.raise_for_status()
        pages = response.json().get("query", {}).get("pages", {})

        photos = []
        for page in sorted(
            pages.values(), key=lambda item: item.get("index", 999)
        ):
            info = page.get("imageinfo", [{}])[0]
            image_url = info.get("thumburl") or info.get("url")
            if image_url and image_url.lower().endswith(
                (".jpg", ".jpeg", ".png", ".webp")
            ):
                photos.append({
                    "url": image_url,
                    "title": page.get("title", "").replace("File:", ""),
                })

        return photos[:4]
    except Exception:
        return []


# -------------------- GAME STATE --------------------

defaults = {
    "screen": "welcome",
    "round": 0,
    "lives": 4,
    "clue_index": 0,
    "status": "playing",
    "clue_message": "",
    "last_guess_message": "",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def next_round():
    st.session_state.round += 1
    st.session_state.lives = 4
    st.session_state.clue_index = 0
    st.session_state.status = "playing"
    st.session_state.clue_message = ""
    st.session_state.last_guess_message = ""


def reset_game():
    for key in defaults:
        if key in st.session_state:
            del st.session_state[key]


# -------------------- WELCOME SCREEN --------------------

if st.session_state.screen == "welcome":
    st.markdown("""
    <div class="hero">
        <div style="font-size:45px;">🧭 🌊 🗺️ 🎮</div>
        <div style="color:#FFD777;font-weight:800;letter-spacing:3px;">
            🎂 THE ULTIMATE BIRTHDAY QUEST 🎂
        </div>
        <div class="hero-title">GEOQUEST-OF-NIGHTMARES</div>
        <div class="hero-subtitle">
            🌍 YOUR NEXT ADVENTURE STARTS HERE 🌍
        </div>
        <div class="hero-description">
            Four mystery locations. ❤️ Four lives per round.<br>
            🎁 Four gifts to unlock.<br><br>
            <b style="color:#FFD777;font-size:22px;">
                Think you can find them all? 🔎
            </b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-heading">📜 HOW TO PLAY 🎯</div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="quest-card">
            <div style="font-size:32px;">🗺️ 🔍 🌍</div>
            <h3>01 · Explore the mystery</h3>
            Look at the location photographs, examine your surroundings
            and figure out where you are!
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="quest-card">
            <div style="font-size:32px;">❤️ ❤️ ❤️ ❤️</div>
            <h3>02 · Protect your lives</h3>
            You start with four lives. Every clue costs one life.
            Every wrong guess costs one life. Choose wisely! ⚠️
        </div>
        """, unsafe_allow_html=True)

    c3, c4 = st.columns(2)

    with c3:
        st.markdown("""
        <div class="quest-card">
            <div style="font-size:32px;">🧩 💡 🕵️</div>
            <h3>03 · Think before you guess</h3>
            Use your clues strategically. Run out of lives before
            solving the location and you lose that round's gift! 😈
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="quest-card">
            <div style="font-size:32px;">🎁 ⚡ 🎉</div>
            <h3>04 · Unlock the rewards</h3>
            Guess correctly to unlock your physical birthday gift
            and advance to the next level! 🏆
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero" style="padding-top:10px;">
        <div class="hero-subtitle">
            ✨ Four stops, four gifts, one big adventure ✨
        </div>
        <div style="font-size:29px;margin:16px;">
            🧭 🌎 🔎 ❤️ 🎁 ⚡ 🎉
        </div>
        <div style="color:#FFD777;font-weight:800;font-size:18px;">
            Ready to begin your quest? 🚀
        </div>
    </div>
    """, unsafe_allow_html=True)

    _, start_col, _ = st.columns([1, 2, 1])
    with start_col:
        if st.button(
            "🚀 START YOUR ADVENTURE 🚀",
            use_container_width=True,
        ):
            st.session_state.screen = "game"
            st.rerun()

    st.stop()


# -------------------- FINAL SCREEN --------------------

i = st.session_state.round

if i >= len(ROUNDS):
    st.balloons()
    st.markdown("""
    <div class="hero">
        <div style="font-size:65px;">🏆 🎉 🎂 🎁</div>
        <div class="hero-title">QUEST COMPLETED!</div>
        <div class="hero-subtitle">🌍 YOU CONQUERED THE WORLD! 🌍</div>
        <div class="hero-description">
            Four locations explored. Four challenges faced.<br>
            And a birthday adventure to remember! 💙
        </div>
        <div style="font-size:35px;">⚡ 🧭 🌎 🎁 🎊</div>
    </div>
    """, unsafe_allow_html=True)

    st.success("🎁 Time to collect your birthday gifts!")

    if st.button("🔄 PLAY AGAIN", use_container_width=True):
        reset_game()
        st.rerun()

    st.stop()


# -------------------- LEVEL SCREEN --------------------

place = ROUNDS[i]

st.markdown(f"""
<div class="hero" style="padding:5px 0 12px 0;">
    <div style="font-size:28px;">🧭 🌍 🔍</div>
    <div class="hero-title" style="font-size:36px;">
        LEVEL {i + 1} / 4
    </div>
    <div class="hero-subtitle" style="margin-top:8px;">
        🗺️ THE MYSTERY CONTINUES...
    </div>
    <div class="hero-description">
        Explore carefully, think strategically and uncover your next gift! 🎁
    </div>
</div>
""", unsafe_allow_html=True)

st.progress((i + 1) / 4)

left, right = st.columns(2)
with left:
    st.markdown(
        f'<div class="quest-card" style="min-height:90px;text-align:center;">'
        f'<h3>📍 MISSION {i + 1}</h3>'
        f'<p>One mystery location awaits...</p></div>',
        unsafe_allow_html=True,
    )

with right:
    hearts = "❤️" * st.session_state.lives
    empty_hearts = "🤍" * (4 - st.session_state.lives)
    st.markdown(
        f'<div class="quest-card" style="min-height:90px;text-align:center;">'
        f'<h3>💖 YOUR LIVES</h3>'
        f'<div style="font-size:25px;">{hearts}{empty_hearts}</div>'
        f'<p>{st.session_state.lives} of 4 remaining</p></div>',
        unsafe_allow_html=True,
    )


# -------------------- GAME OUTCOME --------------------

if st.session_state.status == "playing":

    st.markdown(
        '<div class="section-heading">📸 EXPLORE THE MYSTERY LOCATION 📸</div>',
        unsafe_allow_html=True,
    )

    with st.spinner("🔎 Searching for location photographs..."):
        photos = get_location_photos(place["photo_search"])

    if photos:
        photo_cols = st.columns(min(2, len(photos)))
        for idx, photo in enumerate(photos):
            with photo_cols[idx % len(photo_cols)]:
                st.image(photo["url"], use_container_width=True)
                st.caption("📷 " + photo["title"])
    else:
        st.warning(
            "📸 We couldn't load location photos right now. "
            "Use the exploration link below instead."
        )

    maps_url = (
        "https://www.google.com/maps/search/?api=1&query="
        f"{place['lat']},{place['lon']}"
    )
    street_url = (
        "https://www.google.com/maps/@?api=1&map_action=pano&viewpoint="
        f"{place['lat']},{place['lon']}"
    )

    map_col, street_col = st.columns(2)
    with map_col:
        st.link_button("🗺️ Explore on Google Maps", maps_url,
                       use_container_width=True)
    with street_col:
        st.link_button("🚶 Try Street View", street_url,
                       use_container_width=True)

    st.markdown(
        '<div class="section-heading">🧩 NEED A HINT? 💡</div>',
        unsafe_allow_html=True,
    )

    with st.expander("🔓 Request a clue — costs one life ❤️"):
        st.write(
            f"Clues revealed: {st.session_state.clue_index} / 4"
        )

        if st.session_state.clue_index < len(place["clues"]):
            if st.button("💡 Reveal my next clue", key=f"clue_{i}"):
                st.session_state.lives -= 1
                clue = place["clues"][st.session_state.clue_index]
                st.session_state.clue_index += 1
                st.session_state.clue_message = clue

                if st.session_state.lives <= 0:
                    st.session_state.status = "lost"

                st.rerun()
        else:
            st.info("🔎 You've used all the available clues!")

        if st.session_state.clue_message:
            st.info("🧩 " + st.session_state.clue_message)

    st.markdown(
        '<div class="section-heading">🎯 LOCK IN YOUR GUESS 🎯</div>',
        unsafe_allow_html=True,
    )

    with st.form(f"guess_{i}"):
        guess = st.text_input(
            "Where in the world are you? 🌎",
            placeholder="Enter your guess...",
        )
        submitted = st.form_submit_button(
            "🔐 LOCK IN GUESS",
            use_container_width=True,
        )

    if submitted:
        guess_clean = re.sub(r"[^a-z0-9 ]", " ", guess.lower())
        guess_clean = " ".join(guess_clean.split())

        # Only accept the intended answers/aliases as whole words.
        correct = any(
            re.search(r"\b" + re.escape(answer) + r"\b", guess_clean)
            for answer in place["answer"]
        )

        if correct:
            st.session_state.status = "won"
            st.rerun()
        else:
            st.session_state.lives -= 1

            if st.session_state.lives <= 0:
                st.session_state.status = "lost"
            else:
                st.session_state.last_guess_message = (
                    "❌ Not quite! You've lost one life. Think carefully! 🧠"
                )

            st.rerun()

    if st.session_state.last_guess_message:
        st.warning(st.session_state.last_guess_message)

elif st.session_state.status == "won":
    st.balloons()
    st.markdown("""
    <div class="hero">
        <div style="font-size:50px;">⚡ 🎉 🎁 ⚡</div>
        <div class="hero-title">LOCATION UNLOCKED!</div>
        <div class="hero-subtitle">😲 Pikachuuu, woahh!</div>
        <div class="hero-description">
            You cracked the mystery! 🧠<br>
            <b style="color:#FFD777;">You advanced to the next level!</b>
        </div>
        <div style="font-size:34px;">🏆 💛 🎊 🎂</div>
    </div>
    """, unsafe_allow_html=True)

    st.success("🎁 GIFT UNLOCKED! Go collect your present!")

    st.image(
        "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png",
        width=220,
    )

    if st.button("➡️ CONTINUE TO NEXT LEVEL", use_container_width=True):
        next_round()
        st.rerun()

elif st.session_state.status == "lost":
    st.markdown("""
    <div class="hero">
        <div style="font-size:50px;">💔 😈 ⚡ 💔</div>
        <div class="hero-title">MISSION FAILED!</div>
        <div class="hero-subtitle">You're a loser, pika!</div>
        <div class="hero-description">
            All four lives are gone! ❤️‍🩹<br>
            This round's gift is locked. Time to face the next challenge! 🔥
        </div>
        <div style="font-size:32px;">🙈 🫣 🎮</div>
    </div>
    """, unsafe_allow_html=True)

    st.image(
        "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png",
        width=180,
    )

    if st.button("➡️ TRY THE NEXT LEVEL", use_container_width=True):
        next_round()
        st.rerun()

st.markdown("---")
st.markdown(
    '<div class="centered small-note">'
    '❤️ 4 lives per level &nbsp; • &nbsp; 🧩 Clue = −1 life '
    '&nbsp; • &nbsp; ❌ Wrong guess = −1 life '
    '&nbsp; • &nbsp; 🎁 Correct answer = gift unlocked'
    '</div>',
    unsafe_allow_html=True,
)

