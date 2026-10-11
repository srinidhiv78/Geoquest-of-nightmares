
import re
import requests
import streamlit as st

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Geoquest-Of-Nightmares",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --------------------------------------------------
# THEME AND ANIMATIONS
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Poppins:wght@300;400;500;600;700&display=swap');

.stApp {
    background: radial-gradient(
        ellipse at top,
        #124b55 0%,
        #092e3a 40%,
        #061923 100%
    );
    color: #f3f5ed;
    font-family: 'Poppins', sans-serif;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    font-family: 'Orbitron', sans-serif !important;
    text-align: center;
}

h1 { color: #ffd777 !important; letter-spacing: 2px; }
h2 { color: #55e6d1 !important; }
h3 { color: #ffe5a1 !important; }

p, label, li { color: #edf5f1; }

div[data-testid="stMetric"] {
    background: rgba(16, 83, 91, 0.65);
    border: 1px solid rgba(85, 230, 209, 0.35);
    padding: 15px;
    border-radius: 15px;
}

div[data-testid="stMetricLabel"] { color: #b7e8df; }
div[data-testid="stMetricValue"] { color: #ffd777; }

.stButton > button,
.stFormSubmitButton > button {
    background: linear-gradient(135deg, #20bba9, #087f83);
    color: white;
    border: 1px solid #6ef5dd;
    border-radius: 12px;
    font-weight: 700;
    min-height: 45px;
    transition: 0.2s ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: linear-gradient(135deg, #ffd777, #f2a93b);
    color: #092b35;
    border-color: #ffe8a6;
}

.stTextInput input {
    background: #102f3a;
    color: white;
    border: 1px solid #55e6d1;
    border-radius: 10px;
}

.adventure-card {
    background: rgba(10, 52, 63, 0.82);
    border: 1px solid rgba(85, 230, 209, 0.4);
    border-radius: 20px;
    padding: 24px;
    margin: 14px 0;
    box-shadow: 0 8px 28px rgba(0, 0, 0, 0.18);
}

.welcome-banner {
    background: linear-gradient(
        135deg,
        rgba(14, 94, 102, 0.95),
        rgba(9, 39, 54, 0.96)
    );
    border: 2px solid #d9b65c;
    border-radius: 25px;
    padding: 32px 24px;
    text-align: center;
    margin-bottom: 25px;
}

.pikachu-stage {
    text-align: center;
    overflow: hidden;
    padding: 15px 0;
}

@keyframes pikachu-jump {
    0%, 100% { transform: translate(0, 0) rotate(0deg); }
    15% { transform: translate(-55px, -30px) rotate(-12deg); }
    30% { transform: translate(45px, -65px) rotate(12deg); }
    45% { transform: translate(-35px, -15px) rotate(-9deg); }
    60% { transform: translate(55px, -45px) rotate(10deg); }
    75% { transform: translate(-25px, -35px) rotate(-8deg); }
    90% { transform: translate(20px, -10px) rotate(5deg); }
}

.pikachu-happy {
    animation: pikachu-jump 1.4s ease-in-out infinite;
    width: 230px;
    max-width: 80%;
    display: block;
    margin: 25px auto;
}

.pikachu-crying {
    width: 300px;
    max-width: 90%;
    display: block;
    margin: 25px auto;
    border-radius: 18px;
}

.footer-text {
    text-align: center;
    color: #8fcac5;
    font-size: 0.85rem;
    margin-top: 35px;
}

hr { border-color: rgba(85, 230, 209, 0.3); }

@media (prefers-reduced-motion: reduce) {
    .pikachu-happy { animation: none; }
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# LOCATION DATA
# --------------------------------------------------
ROUNDS = [
    {
        "name": "Gudaibiya",
        "country": "Bahrain",
        "flag": "🇧🇭",
        "emoji": "🕌",
        "location_answers": ["gudaibiya", "gudabiya"],
        "country_answers": ["bahrain"],
        "photo_search": "Gudaibiya Bahrain mosque buildings",
        "clue": (
            "This destination is in a small island country in the "
            "Persian Gulf. Its capital city is Manama."
        ),
        "description": (
            "Your first mystery destination is somewhere in the Middle "
            "East. Look carefully at the architecture and surroundings!"
        ),
        "gift": "🎁 Gift 1",
        "street_view": None,
    },
    {
        "name": "Zagreb",
        "country": "Croatia",
        "flag": "🇭🇷",
        "emoji": "🏰",
        "location_answers": ["zagreb"],
        "country_answers": ["croatia"],
        "photo_search": "Zagreb Croatia city landmarks",
        "clue": (
            "This European capital is known for its historic Upper Town, "
            "colourful rooftops and St. Mark's Church."
        ),
        "description": (
            "Head to Europe! Search the architecture, rooftops and "
            "cityscape for clues to this destination."
        ),
        "gift": "🎁 Gift 2",
        "street_view": (
            "https://www.google.com/maps/@?api=1&map_action=pano"
            "&viewpoint=45.8150,15.9819"
        ),
    },
    {
        "name": "Uttarakhand",
        "country": "India",
        "flag": "🇮🇳",
        "emoji": "🏔️",
        "location_answers": ["uttarakhand"],
        "country_answers": ["india"],
        "photo_search": "Uttarakhand India Himalayas mountains temples",
        "clue": (
            "This Indian state lies in the Himalayas and is famous for "
            "mountains, pilgrimage sites and beautiful valleys."
        ),
        "description": (
            "Your next destination is in northern India. Look for "
            "mountain landscapes, temples and Himalayan scenery."
        ),
        "gift": "🎁 Gift 3",
        "street_view": None,
    },
    {
        "name": "Khabarovsk",
        "country": "Russia",
        "flag": "🇷🇺",
        "emoji": "❄️",
        "location_answers": ["khabarovsk"],
        "country_answers": ["russia"],
        "photo_search": "Khabarovsk Russia city Amur river landmarks",
        "clue": (
            "This Russian city lies near the Amur River in the country's "
            "Far East, close to the Chinese border."
        ),
        "description": (
            "The final destination is in the Russian Far East. Look for "
            "riverfront views, grand buildings and a colder climate."
        ),
        "gift": "🎁 Gift 4",
        "street_view": (
            "https://www.google.com/maps/@?api=1&map_action=pano"
            "&viewpoint=48.4802,135.0719"
        ),
    },
]


# --------------------------------------------------
# PHOTO SEARCH
# Photos display without captions or source links.
# --------------------------------------------------
@st.cache_data(ttl=3600, show_spinner=False)
def get_location_photos(search_term, limit=4):
    api_url = "https://commons.wikimedia.org/w/api.php"

    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": f"filetype:bitmap {search_term}",
        "gsrnamespace": 6,
        "gsrlimit": limit,
        "prop": "imageinfo",
        "iiprop": "url",
        "iiurlwidth": 850,
    }

    headers = {
        "User-Agent": "GeoquestOfNightmares/1.0 (location guessing game)"
    }

    try:
        response = requests.get(
            api_url,
            params=params,
            headers=headers,
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()

        pages = data.get("query", {}).get("pages", {})
        photos = []

        for page in pages.values():
            image_info = page.get("imageinfo", [])
            if not image_info:
                continue

            image_data = image_info[0]
            image_url = (
                image_data.get("thumburl")
                or image_data.get("url")
            )

            if image_url:
                photos.append({
                    "url": image_url,
                    "caption": page.get("title", ""),
                    "source": image_data.get("descriptionurl", ""),
                })

        return photos[:limit]

    except (requests.RequestException, ValueError, KeyError):
        return []


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
defaults = {
    "screen": "welcome",
    "level": 0,
    "lives": 4,
    "clue_used": False,
    "clue_visible": False,
    "completed": [],
    "lost": [],
    "last_message": "",
    "location_correct": False,
    "country_correct": False,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def reset_round():
    st.session_state.lives = 4
    st.session_state.clue_used = False
    st.session_state.clue_visible = False
    st.session_state.last_message = ""
    st.session_state.location_correct = False
    st.session_state.country_correct = False


def start_game():
    st.session_state.screen = "playing"
    st.session_state.level = 0
    st.session_state.completed = []
    st.session_state.lost = []
    reset_round()


def normalize_answer(answer):
    return re.sub(r"[^a-z0-9\s]", "", answer.lower()).strip()


def use_clue():
    if (
        not st.session_state.clue_used
        and st.session_state.lives > 0
    ):
        st.session_state.lives -= 1
        st.session_state.clue_used = True
        st.session_state.clue_visible = True

        if st.session_state.lives <= 0:
            st.session_state.screen = "lost"

            level = st.session_state.level
            if level not in st.session_state.lost:
                st.session_state.lost.append(level)


def check_answer(location_guess, country_guess):
    place = ROUNDS[st.session_state.level]

    location_guess = normalize_answer(location_guess)
    country_guess = normalize_answer(country_guess)

    location_correct = (
        location_guess in place["location_answers"]
    )
    country_correct = (
        country_guess in place["country_answers"]
    )

    st.session_state.location_correct = location_correct
    st.session_state.country_correct = country_correct

    # Either correct answer clears the round.
    if location_correct or country_correct:
        st.session_state.screen = "won"

        if st.session_state.level not in st.session_state.completed:
            st.session_state.completed.append(
                st.session_state.level
            )

        # Cheeky message if exactly one answer is correct.
        if location_correct != country_correct:
            st.session_state.last_message = (
                "😏 Well, at least you got 1 thing right!"
            )
        else:
            st.session_state.last_message = (
                "🔥 BOTH answers correct! Look at you, genius!"
            )

    else:
        st.session_state.lives -= 1
        st.session_state.last_message = (
            "❌ Both answers are wrong! You lost one life. "
            "Better luck on your next attempt!"
        )

        if st.session_state.lives <= 0:
            st.session_state.screen = "lost"

            if st.session_state.level not in st.session_state.lost:
                st.session_state.lost.append(
                    st.session_state.level
                )


def advance_level():
    if st.session_state.level >= len(ROUNDS) - 1:
        st.session_state.screen = "finished"
    else:
        st.session_state.level += 1
        reset_round()
        st.session_state.screen = "playing"


# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown(
    "<h1>⚡ GEOQUEST-OF-NIGHTMARES ⚡</h1>",
    unsafe_allow_html=True,
)

st.markdown(
    "<p style='text-align:center;color:#55e6d1;'>"
    "🌍 🧭 🔍 🎁 ✨ YOUR ADVENTURE AWAITS ✨ 🎁 🔍 🧭 🌍"
    "</p>",
    unsafe_allow_html=True,
)

st.divider()


# --------------------------------------------------
# WELCOME SCREEN
# --------------------------------------------------
if st.session_state.screen == "welcome":

    st.markdown("""
    <div class="welcome-banner">
        <h1>🌌 YOUR NEXT ADVENTURE STARTS HERE 🌌</h1>
        <h3>🗺️ Four mystery locations. Four lives per round. Four gifts to unlock.</h3>
        <p style="font-size:1.1rem;">
            Think you can find them all? 🔍⚡🎁
        </p>
        <p>
            Travel around the world through pictures, clues and guesses.
            Every location hides a surprise!
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 🎮 HOW TO PLAY 🎮")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="adventure-card">
            <h3>❤️ Your Lives</h3>
            <p>❤️ ❤️ ❤️ ❤️</p>
            <p>You begin every round with four lives.</p>
            <p>❌ Both answers wrong? Lose one life.</p>
            <p>💡 Asking for a clue costs one life.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="adventure-card">
            <h3>🎁 Your Gifts</h3>
            <p>🗺️ Enter the location and country separately.</p>
            <p>🎯 Either answer correct means you clear the round.</p>
            <p>🎁 Clear the round to unlock its gift.</p>
            <p>💔 Lose all four lives and that round's gift is lost.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="adventure-card" style="text-align:center;">
        <h2>🌍 FOUR STOPS, FOUR GIFTS, ONE BIG ADVENTURE 🌍</h2>
        <p>🇧🇭 Bahrain &nbsp; ➜ &nbsp; 🇭🇷 Croatia</p>
        <p>🇮🇳 India &nbsp; ➜ &nbsp; 🇷🇺 Russia</p>
        <p>🔍 Study the photographs. Use your clues wisely. Trust your instincts!</p>
        <p>⚡ Are you ready, explorer? ⚡</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    _, center, _ = st.columns([1, 2, 1])

    with center:
        if st.button(
            "🚀 START LEVEL 1 🚀",
            use_container_width=True,
        ):
            start_game()
            st.rerun()


# --------------------------------------------------
# PLAYING SCREEN
# --------------------------------------------------
elif st.session_state.screen == "playing":

    level = st.session_state.level
    place = ROUNDS[level]

    st.markdown(
        f"<h2>{place['flag']} LEVEL {level + 1}: MYSTERY DESTINATION {place['emoji']}</h2>",
        unsafe_allow_html=True,
    )

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric("🧭 LEVEL", f"{level + 1} / 4")

    with metric2:
        st.metric("❤️ LIVES LEFT", st.session_state.lives)

    with metric3:
        st.metric(
            "🎁 GIFTS UNLOCKED",
            len(st.session_state.completed),
        )

    st.progress((level + 1) / len(ROUNDS))

    st.markdown(
        f"""
        <div class="adventure-card">
            <h3>🔎 INVESTIGATE THE LOCATION 🔎</h3>
            <p style="text-align:center;">{place['description']}</p>
            <p style="text-align:center;">
                📸 Examine the photographs and work out where you are!
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.spinner("📸 Loading mystery location photographs..."):
        photos = get_location_photos(
            place["photo_search"],
            limit=4,
        )

    if photos:
        for start in range(0, len(photos), 2):
            photo_cols = st.columns(2)

            for col, photo in zip(
                photo_cols,
                photos[start:start + 2],
            ):
                with col:
                    # No caption or source link below the photo.
                    st.image(
                        photo["url"],
                        use_container_width=True,
                    )
    else:
        st.warning(
            "📷 The photos could not be loaded right now. "
            "Please refresh the app and try again."
        )

    if place["street_view"]:
        st.markdown(
            f"""
            <div style="text-align:center;padding:12px;">
                <a href="{place['street_view']}" target="_blank"
                   style="color:#55e6d1;font-weight:700;font-size:1.05rem;">
                   🌐 Open Street View for a closer look
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    st.markdown("### 💡 Need a clue?")

    clue_col, clue_text_col = st.columns([1, 2])

    with clue_col:
        st.button(
            "💡 USE A CLUE (-1 LIFE)",
            on_click=use_clue,
            disabled=(
                st.session_state.clue_used
                or st.session_state.lives <= 0
            ),
            use_container_width=True,
        )

    with clue_text_col:
        if st.session_state.clue_visible:
            st.info(f"🧩 CLUE: {place['clue']}")

    # Two separate answer boxes.
    st.markdown("### 🎯 Enter your two answers")

    st.caption(
        "You only need ONE correct answer to clear the round. "
        "But let's see if you can get both! 😏"
    )

    with st.form(f"answer_form_{level}"):

        location_guess = st.text_input(
            "📍 Box 1: City / Location",
            placeholder="Enter the city or location...",
            key=f"location_guess_{level}",
        )

        country_guess = st.text_input(
            "🌍 Box 2: Country",
            placeholder="Enter the country...",
            key=f"country_guess_{level}",
        )

        submitted = st.form_submit_button(
            "🔓 SUBMIT MY ANSWERS",
            use_container_width=True,
        )

    if submitted:
        if not location_guess.strip() and not country_guess.strip():
            st.warning("😏 At least TRY one of the boxes!")
        else:
            check_answer(location_guess, country_guess)
            st.rerun()

    st.markdown(
        "<div class='footer-text'>"
        "🧭 Think carefully, explorer. Every life counts! ❤️"
        "</div>",
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# WIN SCREEN
# --------------------------------------------------
elif st.session_state.screen == "won":

    place = ROUNDS[st.session_state.level]

    st.markdown(
        f"<h2>🎉 CORRECT! YOU CLEARED {place['name'].upper()}! 🎉</h2>",
        unsafe_allow_html=True,
    )

    st.markdown("""
    <div class="pikachu-stage">
        <img
            class="pikachu-happy"
            src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png"
            alt="Happy Pikachu jumping"
        />
        <h3 style="text-align:center;color:#FFD777;">
            ⚡ PIKACHUUU, WOAHH! ⚡
        </h3>
        <p style="text-align:center;font-size:1.1rem;">
            You advanced to the next level! 🎉
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Show the cheeky message when only one answer was correct.
    if (
        st.session_state.location_correct
        != st.session_state.country_correct
    ):
        st.markdown("""
        <div class="adventure-card"
             style="text-align:center;border-color:#FFD777;">
            <h2>😏 WELL, AT LEAST YOU GOT 1 THING RIGHT!</h2>
            <p>One answer carried the whole team. We'll take it! 😂</p>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="adventure-card" style="text-align:center;">
            <h2>🧠 BOTH ANSWERS RIGHT!</h2>
            <p>Okay, show-off. We see you! 🔥😎</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="adventure-card" style="text-align:center;">
            <h2>🎁 YOU UNLOCKED {place['gift'].upper()} 🎁</h2>
            <p>{place['flag']} {place['name']}, {place['country']}</p>
            <p>🏆 One more mystery solved! Keep that adventure spirit alive!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.level < len(ROUNDS) - 1:
        button_text = "⚡ ADVANCE TO THE NEXT LEVEL ⚡"
    else:
        button_text = "🏆 CLAIM YOUR FINAL VICTORY 🏆"

    _, center, _ = st.columns([1, 2, 1])

    with center:
        if st.button(button_text, use_container_width=True):
            advance_level()
            st.rerun()


# --------------------------------------------------
# LOSS SCREEN
# --------------------------------------------------
elif st.session_state.screen == "lost":

    place = ROUNDS[st.session_state.level]

    st.markdown(
        "<h2>💔 OH NO! YOU RAN OUT OF LIVES! 💔</h2>",
        unsafe_allow_html=True,
    )

    st.markdown("""
    <div class="pikachu-stage">
        <img
            class="pikachu-crying"
            src="https://i.kym-cdn.com/photos/images/newsfeed/000/511/073/083.gif"
            alt="Crying Pikachu"
        />
        <h3 style="text-align:center;color:#FF9AA8;">
            😭 YOU'RE A LOSER, PIKA! 💔
        </h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="adventure-card" style="text-align:center;">
            <h3>🎁 {place['gift']} REMAINS LOCKED</h3>
            <p>You couldn't solve the mystery of {place['name']}, {place['country']}.</p>
            <p>Don't give up! There's another destination waiting for you.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.level < len(ROUNDS) - 1:
        button_text = "🧭 CONTINUE TO THE NEXT LOCATION"
    else:
        button_text = "🏁 SEE MY FINAL RESULTS"

    _, center, _ = st.columns([1, 2, 1])

    with center:
        if st.button(button_text, use_container_width=True):
            advance_level()
            st.rerun()


# --------------------------------------------------
# FINAL RESULTS
# --------------------------------------------------
elif st.session_state.screen == "finished":

    st.markdown("""
    <div class="welcome-banner">
        <h1>🏆 ADVENTURE COMPLETE! 🏆</h1>
        <h2>🌍 YOU MADE IT THROUGH ALL FOUR LOCATIONS! 🌍</h2>
        <p style="font-size:1.2rem;">
            Every destination had a mystery. Every round had a challenge.
            Now it's time to reveal your results!
        </p>
    </div>
    """, unsafe_allow_html=True)

    won_count = len(st.session_state.completed)
    lost_count = len(st.session_state.lost)

    result1, result2, result3 = st.columns(3)

    with result1:
        st.metric("🎁 GIFTS UNLOCKED", f"{won_count} / 4")

    with result2:
        st.metric("💔 GIFTS MISSED", f"{lost_count} / 4")

    with result3:
        st.metric("🗺️ LOCATIONS VISITED", "4 / 4")

    st.markdown("## 🎁 YOUR ADVENTURE RESULTS 🎁")

    for i, place in enumerate(ROUNDS):
        if i in st.session_state.completed:
            status = "🎉 GIFT UNLOCKED!"
        else:
            status = "🔒 GIFT NOT UNLOCKED"

        st.markdown(
            f"""
            <div class="adventure-card">
                <h3>{place['flag']} {place['name']}, {place['country']}</h3>
                <p style="text-align:center;">{status}</p>
                <p style="text-align:center;">{place['gift']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if won_count == 4:
        st.balloons()
        st.markdown(
            "<h2>👑 PERFECT SCORE! YOU ARE THE ULTIMATE GEOQUEST CHAMPION! 👑</h2>",
            unsafe_allow_html=True,
        )
    elif won_count >= 2:
        st.markdown(
            "<h2>⚡ AMAZING WORK, EXPLORER! ⚡</h2>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<h2>💚 EVERY ADVENTURE IS A NEW MEMORY! 💚</h2>",
            unsafe_allow_html=True,
        )

    _, center, _ = st.columns([1, 2, 1])

    with center:
        if st.button("🔄 PLAY AGAIN", use_container_width=True):
            start_game()
            st.rerun()


# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown(
    "<div class='footer-text'>"
    "✨ MADE WITH ❤️, MYSTERY & A LITTLE BIT OF PIKACHU MAGIC ⚡"
    "</div>",
    unsafe_allow_html=True,
)

