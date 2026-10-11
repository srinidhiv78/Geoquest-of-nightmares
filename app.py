
import re
import requests
import streamlit as st

# ==================================================
# PAGE CONFIGURATION
# ==================================================
st.set_page_config(
    page_title="Geoquest-Of-Nightmares",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==================================================
# THEME
# ==================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Poppins:wght@300;400;500;600;700&display=swap');

.stApp {
    background: radial-gradient(ellipse at top, #124b55 0%, #092e3a 40%, #061923 100%);
    color: #f3f5ed;
    font-family: 'Poppins', sans-serif;
}

.block-container {
    max-width: 1150px;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
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
    padding: 12px;
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
    min-height: 43px;
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
    padding: 20px;
    margin: 12px 0;
    box-shadow: 0 8px 28px rgba(0, 0, 0, 0.18);
}

.welcome-banner {
    background: linear-gradient(135deg, rgba(14, 94, 102, 0.95), rgba(9, 39, 54, 0.96));
    border: 2px solid #d9b65c;
    border-radius: 25px;
    padding: 28px 22px;
    text-align: center;
    margin-bottom: 22px;
}

.pikachu-stage {
    text-align: center;
    overflow: hidden;
    padding: 15px 0;
}

@keyframes pikachu-jump {
    0%, 100% { transform: translate(0, 0) rotate(0deg); }
    15% { transform: translate(-45px, -30px) rotate(-12deg); }
    30% { transform: translate(35px, -60px) rotate(12deg); }
    45% { transform: translate(-30px, -15px) rotate(-9deg); }
    60% { transform: translate(45px, -40px) rotate(10deg); }
    75% { transform: translate(-20px, -25px) rotate(-8deg); }
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

div[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0c3945, #071f2b);
    border-right: 1px solid rgba(85, 230, 209, 0.4);
}

div[data-testid="stSidebar"] h2,
div[data-testid="stSidebar"] h3 {
    color: #ffd777 !important;
}

.lives-title {
    text-align: center;
    color: #55e6d1;
    font-family: 'Orbitron', sans-serif;
    font-size: 1rem;
    font-weight: bold;
}

.lives-hearts {
    text-align: center;
    font-size: 1.65rem;
    line-height: 1.8;
    letter-spacing: 2px;
    overflow-wrap: anywhere;
}

.footer-text {
    text-align: center;
    color: #8fcac5;
    font-size: 0.85rem;
}

hr { border-color: rgba(85, 230, 209, 0.3); }

@media (prefers-reduced-motion: reduce) {
    .pikachu-happy { animation: none; }
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# LOCATION DATA AND MULTIPLE CLUES
# ==================================================
ROUNDS = [
    {
        "name": "Gudaibiya",
        "country": "Bahrain",
        "flag": "🇧🇭",
        "emoji": "🕌",
        "location_answers": ["gudaibiya", "gudabiya"],
        "country_answers": ["bahrain"],
        "photo_searches": [
            "Gudaibiya Bahrain mosque",
            "Gudaibiya Manama Bahrain",
            "Adliya Bahrain architecture",
        ],
        "clues": [
            "This destination is in the Middle East.",
            "It is in an island country in the Persian Gulf.",
            "The country's capital is Manama.",
            "The location's name begins with the letter G.",
        ],
        "description": (
            "Your first mystery destination is somewhere in the Middle East. "
            "Study the architecture and surroundings carefully!"
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
        "photo_searches": [
            "Zagreb Croatia city",
            "St Mark Church Zagreb Croatia",
            "Zagreb Upper Town rooftops",
        ],
        "clues": [
            "Your destination is in Europe.",
            "It is the capital of its country.",
            "The city is famous for its historic Upper Town and colourful rooftops.",
            "The country's name begins with C, and the city begins with Z.",
        ],
        "description": (
            "Head to Europe! Look at the architecture, rooftops and "
            "cityscape for clues."
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
        "photo_searches": [
            "Uttarakhand India Himalayas",
            "Uttarakhand mountain valley",
            "Uttarakhand temples mountains",
        ],
        "clues": [
            "Your destination is in Asia.",
            "It is a state in northern India.",
            "The Himalayas are a major feature of this region.",
            "Its name begins with U and ends with 'hand'.",
        ],
        "description": (
            "Your next destination is in northern India. Look for mountain "
            "landscapes, temples and Himalayan scenery."
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
        "photo_searches": [
            "Khabarovsk Russia city",
            "Khabarovsk Amur River",
            "Khabarovsk Russia architecture",
        ],
        "clues": [
            "Your final destination is in Asia.",
            "It is in the Far East of a very large country.",
            "The Amur River flows near this city.",
            "The city and country are both in Russia's eastern region.",
        ],
        "description": (
            "Your final destination is in the Russian Far East. Look for "
            "riverfront views, grand buildings and a colder climate."
        ),
        "gift": "🎁 Gift 4",
        "street_view": (
            "https://www.google.com/maps/@?api=1&map_action=pano"
            "&viewpoint=48.4802,135.0719"
        ),
    },
]


# ==================================================
# PHOTO SEARCH
# Uses Wikimedia Commons API with several search terms.
# Results are displayed without captions or source links.
# ==================================================
@st.cache_data(ttl=900, show_spinner=False)
def get_location_photos(search_terms, limit=4):
    api_url = "https://commons.wikimedia.org/w/api.php"
    headers = {
        "User-Agent": (
            "GeoquestOfNightmares/1.0 "
            "(educational location guessing game)"
        )
    }

    photos = []
    seen_urls = set()

    for term in search_terms:
        if len(photos) >= limit:
            break

        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": term,
            "srnamespace": 6,
            "srlimit": 10,
        }

        try:
            response = requests.get(
                api_url,
                params=params,
                headers=headers,
                timeout=20,
            )
            response.raise_for_status()
            results = response.json().get("query", {}).get("search", [])

            file_titles = [
                item["title"]
                for item in results
                if item.get("title", "").lower().endswith(
                    (".jpg", ".jpeg", ".png", ".webp")
                )
            ]

            if not file_titles:
                continue

            image_params = {
                "action": "query",
                "format": "json",
                "titles": "|".join(file_titles),
                "prop": "imageinfo",
                "iiprop": "url",
                "iiurlwidth": 850,
            }

            image_response = requests.get(
                api_url,
                params=image_params,
                headers=headers,
                timeout=20,
            )
            image_response.raise_for_status()

            pages = (
                image_response.json()
                .get("query", {})
                .get("pages", {})
            )

            for page in pages.values():
                image_info = page.get("imageinfo", [])
                if not image_info:
                    continue

                image_data = image_info[0]
                image_url = (
                    image_data.get("thumburl")
                    or image_data.get("url")
                )

                if (
                    image_url
                    and image_url not in seen_urls
                    and image_url.startswith("https://")
                ):
                    seen_urls.add(image_url)
                    photos.append({
                        "url": image_url,
                    })

                    if len(photos) >= limit:
                        break

        except (
            requests.RequestException,
            ValueError,
            KeyError,
        ):
            continue

    return photos[:limit]


# ==================================================
# SESSION STATE
# ==================================================
defaults = {
    "screen": "welcome",
    "level": 0,
    "lives": 4,
    "clues_revealed": [],
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
    st.session_state.clues_revealed = []
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
    return re.sub(
        r"[^a-z0-9\s]",
        "",
        answer.lower(),
    ).strip()


def lose_round_if_needed():
    if st.session_state.lives <= 0:
        st.session_state.lives = 0
        st.session_state.screen = "lost"

        level = st.session_state.level
        if (
            level not in st.session_state.completed
            and level not in st.session_state.lost
        ):
            st.session_state.lost.append(level)


def use_clue():
    place = ROUNDS[st.session_state.level]
    clue_index = len(st.session_state.clues_revealed)

    if st.session_state.lives <= 0:
        return

    if clue_index >= len(place["clues"]):
        return

    # Each newly revealed clue costs one life.
    st.session_state.lives -= 1
    st.session_state.clues_revealed.append(clue_index)

    lose_round_if_needed()


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

    # Either answer being correct clears the round.
    if location_correct or country_correct:
        st.session_state.screen = "won"

        if st.session_state.level not in st.session_state.completed:
            st.session_state.completed.append(
                st.session_state.level
            )

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
            "❌ Both answers are wrong! You lost one life."
        )
        lose_round_if_needed()


def advance_level():
    if st.session_state.level >= len(ROUNDS) - 1:
        st.session_state.screen = "finished"
    else:
        st.session_state.level += 1
        reset_round()
        st.session_state.screen = "playing"


# ==================================================
# SIDEBAR: LIVE HEART DISPLAY
# ==================================================
if st.session_state.screen == "playing":
    with st.sidebar:
        st.markdown(
            "<h2>❤️ YOUR LIVES</h2>",
            unsafe_allow_html=True,
        )

        lives = st.session_state.lives
        full_hearts = "❤️ " * lives
        empty_hearts = "🖤 " * (4 - lives)

        st.markdown(
            f"""
            <div class="lives-hearts">
                {full_hearts}{empty_hearts}
            </div>
            <p style="text-align:center;color:#55e6d1;">
                {lives} of 4 lives remaining
            </p>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        st.markdown(
            f"<h3>🧭 LEVEL {st.session_state.level + 1} / 4</h3>",
            unsafe_allow_html=True,
        )

        st.markdown(
            f"<p style='text-align:center;'>🎁 Gifts unlocked: "
            f"{len(st.session_state.completed)} / 4</p>",
            unsafe_allow_html=True,
        )

        st.progress(st.session_state.lives / 4)

        st.caption(
            "💡 Every clue costs one heart. "
            "Every incorrect attempt costs one heart too!"
        )


# ==================================================
# HEADER
# ==================================================
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


# ==================================================
# WELCOME SCREEN
# ==================================================
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
            <p>💡 Every clue costs one life.</p>
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
        <p>🔍 Study the photographs. Use your clues wisely.</p>
        <p>⚡ Are you ready, explorer? ⚡</p>
    </div>
    """, unsafe_allow_html=True)

    _, center, _ = st.columns([1, 2, 1])

    with center:
        if st.button(
            "🚀 START LEVEL 1 🚀",
            use_container_width=True,
        ):
            start_game()
            st.rerun()


# ==================================================
# PLAYING SCREEN
# ==================================================
elif st.session_state.screen == "playing":

    level = st.session_state.level
    place = ROUNDS[level]

    st.markdown(
        f"<h2>{place['flag']} LEVEL {level + 1}: "
        f"MYSTERY DESTINATION {place['emoji']}</h2>",
        unsafe_allow_html=True,
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

    # Load several photos using multiple search terms.
    with st.spinner("📸 Searching for location photographs..."):
        photos = get_location_photos(
            tuple(place["photo_searches"]),
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
                    st.image(
                        photo["url"],
                        use_container_width=True,
                    )
    else:
        st.warning(
            "📷 Photos could not be retrieved from Wikimedia Commons. "
            "Please check your internet connection or try refreshing."
        )

    if place["street_view"]:
        st.markdown(
            f"""
            <div style="text-align:center;padding:12px;">
                <a href="{place['street_view']}" target="_blank"
                   style="color:#55e6d1;font-weight:700;font-size:1.05rem;">
                   🌐 OPEN STREET VIEW FOR A CLOSER LOOK
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    # Multiple clues can be requested, one at a time.
    st.markdown("### 💡 NEED A CLUE?")

    clues = place["clues"]
    clues_used = len(st.session_state.clues_revealed)

    st.caption(
        f"Clues revealed: {clues_used}/{len(clues)}. "
        "Each new clue costs one heart."
    )

    if clues_used > 0:
        for clue_number in st.session_state.clues_revealed:
            st.info(
                f"🧩 CLUE {clue_number + 1}: "
                f"{clues[clue_number]}"
            )

    if clues_used < len(clues) and st.session_state.lives > 0:
        st.button(
            f"💡 REVEAL CLUE {clues_used + 1} (-1 ❤️)",
            on_click=use_clue,
            use_container_width=True,
        )
    elif clues_used >= len(clues):
        st.success("🔍 You've used all the available clues!")

    st.divider()

    st.markdown("### 🎯 ENTER YOUR TWO ANSWERS")

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
        if (
            not location_guess.strip()
            and not country_guess.strip()
        ):
            st.warning("😏 At least TRY one of the boxes!")
        else:
            check_answer(location_guess, country_guess)
            st.rerun()


# ==================================================
# WIN SCREEN
# ==================================================
elif st.session_state.screen == "won":

    place = ROUNDS[st.session_state.level]

    st.markdown(
        f"<h2>🎉 CORRECT! YOU CLEARED "
        f"{place['name'].upper()}! 🎉</h2>",
        unsafe_allow_html=True,
    )

    st.markdown("""
    <div class="pikachu-stage">
        <img
            class="pikachu-happy"
            src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png"
            alt="Happy Pikachu jumping"
        />
        <h3 style="color:#FFD777;">
            ⚡ PIKACHUUU, WOAHH! ⚡
        </h3>
        <p style="font-size:1.1rem;">
            You advanced to the next level! 🎉
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="adventure-card" style="text-align:center;">
            <h2>{st.session_state.last_message}</h2>
            <p>{place['flag']} {place['name']}, {place['country']}</p>
            <h3>🎁 YOU UNLOCKED {place['gift'].upper()} 🎁</h3>
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


# ==================================================
# LOSS SCREEN
# ==================================================
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
        <h3 style="color:#FF9AA8;">
            😭 YOU'RE A LOSER, PIKA! 💔
        </h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="adventure-card" style="text-align:center;">
            <h3>🎁 {place['gift']} REMAINS LOCKED</h3>
            <p>You couldn't solve {place['name']}, {place['country']}.</p>
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


# ==================================================
# FINAL RESULTS
# ==================================================
elif st.session_state.screen == "finished":

    st.markdown("""
    <div class="welcome-banner">
        <h1>🏆 ADVENTURE COMPLETE! 🏆</h1>
        <h2>🌍 YOU MADE IT THROUGH ALL FOUR LOCATIONS! 🌍</h2>
        <p>
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



