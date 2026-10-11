
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Birthday GeoQuest", page_icon="🌍", layout="wide")

# Four secret locations
ROUNDS = [
    {
        "name": "Gudaibiya, Bahrain",
        "answer": ["gudaibiya", "bahrain"],
        "lat": 26.2185, "lon": 50.5830,
        "clues": [
            "This place is in the Middle East.",
            "It is in an island country in the Persian Gulf.",
            "The country hosts a Formula One Grand Prix.",
            "Its capital is Manama."
        ]
    },
    {
        "name": "Zagreb, Croatia",
        "answer": ["zagreb", "croatia"],
        "lat": 45.8150, "lon": 15.9819,
        "clues": [
            "This place is in Europe.",
            "The country borders the Adriatic Sea.",
            "Its flag has red, white and blue.",
            "You are looking for the country's capital."
        ]
    },
    {
        "name": "Uttarakhand, India",
        "answer": ["uttarakhand", "india"],
        "lat": 30.0869, "lon": 79.0193,
        "clues": [
            "This place is in South Asia.",
            "The Himalayas are a major geographical feature.",
            "It is famous for pilgrimage sites and hill stations.",
            "It is a state in India."
        ]
    },
    {
        "name": "Khabarovsk, Russia",
        "answer": ["khabarovsk", "russia"],
        "lat": 48.4802, "lon": 135.0719,
        "clues": [
            "This place is in Asia.",
            "It is in the Russian Far East.",
            "The Amur River runs alongside the city.",
            "The city's name starts with K."
        ]
    }
]

# Optional: add a Google Maps Embed API key in Streamlit Secrets.
API_KEY = st.secrets.get("GOOGLE_MAPS_API_KEY", "")

if "round" not in st.session_state:
    st.session_state.round = 0
    st.session_state.lives = 4
    st.session_state.clue_index = 0
    st.session_state.status = "playing"
    st.session_state.clue_message = ""

def next_round():
    st.session_state.round += 1
    st.session_state.lives = 4
    st.session_state.clue_index = 0
    st.session_state.status = "playing"
    st.session_state.clue_message = ""

st.title("🌍 THE BIRTHDAY GEOQUEST")
st.caption("Four locations. Four gifts. Can you find them all?")

i = st.session_state.round

if i >= len(ROUNDS):
    st.balloons()
    st.title("🏆 YOU DID IT!")
    st.subheader("All four levels completed! Happy Birthday! 🎂")
    st.success("Go and collect your four physical gifts!")
    if st.button("Play again"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    st.stop()

place = ROUNDS[i]

st.progress((i + 1) / 4)
left, right = st.columns(2)
left.subheader(f"LEVEL {i + 1} / 4")
right.subheader("Lives: " + "❤️" * st.session_state.lives
                 + "🤍" * (4 - st.session_state.lives))

st.info("Explore the location and guess where you are. Each clue or wrong guess costs one life.")

# Street View, with photo/video fallback
if API_KEY:
    url = (
        "https://www.google.com/maps/embed/v1/streetview"
        f"?key={API_KEY}&location={place['lat']},{place['lon']}"
        "&heading=0&pitch=0&fov=90"
    )
    components.iframe(url, height=450, scrolling=False)
else:
    st.warning("Street View needs a Google Maps API key. Until it is configured, use the backup media below.")
    st.markdown("### Explore the location")
    st.write("You can add your own photos or short video clips for each level.")
    st.link_button(
        "Open street-level map",
        f"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={place['lat']},{place['lon']}"
    )

with st.expander("🧩 Request a clue — costs one life"):
    if st.session_state.clue_index < len(place["clues"]):
        if st.button("Reveal next clue", key=f"clue_{i}"):
            st.session_state.lives -= 1
            clue = place["clues"][st.session_state.clue_index]
            st.session_state.clue_index += 1
            st.session_state.clue_message = clue
            if st.session_state.lives <= 0:
                st.session_state.status = "lost"
            st.rerun()
    else:
        st.write("You've used all available clues.")
    if st.session_state.clue_message:
        st.info(st.session_state.clue_message)

with st.form(f"guess_{i}"):
    guess = st.text_input("Your guess", placeholder="Enter a city, region or country")
    submitted = st.form_submit_button("Lock in guess 🔒", use_container_width=True)

if submitted and st.session_state.status == "playing":
    guess_clean = guess.lower().strip()
    if any(a in guess_clean for a in place["answer"]):
        st.session_state.status = "won"
        st.rerun()
    else:
        st.session_state.lives -= 1
        if st.session_state.lives <= 0:
            st.session_state.status = "lost"
        else:
            st.error("Wrong guess! You lost one life.")
        st.rerun()

if st.session_state.status == "won":
    st.balloons()
    st.markdown("## 😲 Pikachuuu, woahh!")
    st.success("You advanced to the next level!")
    st.markdown("### 🎁 Gift unlocked! Go collect your present!")
    st.image(
        "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png",
        width=220
    )
    if st.button("Continue to next level ➜", use_container_width=True):
        next_round()
        st.rerun()

elif st.session_state.status == "lost":
    st.markdown("## 😈 YOU'RE A LOSER, PIKA!")
    st.error("You ran out of lives. This round's gift is locked!")
    st.image(
        "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png",
        width=180
    )
    if st.button("Try the next level ➜", use_container_width=True):
        next_round()
        st.rerun()

st.divider()
st.caption("Rules: 4 lives per level • Clue = −1 life • Wrong guess = −1 life • Correct answer = gift unlocked 🎁")
