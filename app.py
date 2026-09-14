
import streamlit as st
from datetime import date
from pathlib import Path
import random
import json
import os
import hmac
import urllib.request
import urllib.error

# ============================================================
# RODNEY + MARIAH — OUR LITTLE WORLD
# Simplified version: Home · Ask Mariah · Memories · Mariah
# ============================================================

st.set_page_config(
    page_title="Rodney + Mariah",
    page_icon="🪴",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CORE DETAILS
# ============================================================

YOUR_NAME = "Rodney"
HER_NAME = "Mariah"
HER_FULL_NAME = "Mariah Lizette Duenez"

ANNIVERSARY = (10, 1)
HER_BIRTHDAY = (11, 5)

MILESTONES = [
    {
        "date": "May 17, 2026 — 2:51 AM",
        "title": 'The first “I luv you”',
        "detail": "Sunday, 2:51 AM",
    },
    {
        "date": "May 26, 2026 — 12:34 AM",
        "title": '“I love you”',
        "detail": "Tuesday, 12:34 AM",
    },
    {
        "date": "May 29, 2026 — 7:35 AM",
        "title": 'First call “I love you”',
        "detail": "Friday, 7:35 AM",
    },
]

REASONS = [
    "I love how seriously you take your future.",
    "I love that you have strong standards and actually live by them.",
    "I love how much you know about the things you care about.",
    "I love that you can talk about art, books, politics, and ideas with real opinions.",
    "I love your confidence.",
    "I love the way you naturally take charge.",
    "I love how disciplined you are when you decide you want something.",
    "I love that your taste is so specifically you.",
    "I love that you can be logical without being boring.",
    "I love hearing you talk about the things you genuinely care about.",
    "I love that you make me want to remember tiny details.",
    "I love that I know which coffee matches which kind of work you're doing.",
    "I love how ambitious you are.",
    "I love how career-driven you are.",
    "I love how much thought you put into the future.",
    "I love how independent your mind is.",
    "I love that you know what you like and what you don't.",
    "I love how intentional you are.",
    "I love that you have your own taste instead of following everyone else's.",
    "I love how much personality you put into the things you choose.",
    "I love how passionate you are about literature.",
    "I love how seriously you take art and design.",
    "I love that you can appreciate tiny details other people overlook.",
    "I love that you make museums sound like an actually good date.",
    "I love how much there still is for me to learn about you.",
    "I love learning your little routines.",
    "I love remembering your oddly specific preferences.",
    "I love that your coffee order changes depending on what you're working on.",
    "I love that sage green feels like such a you color.",
    "I love that you somehow have opinions about everything in the best way.",
    "I love your sarcastic 'mkay.'",
    "I love how structured you are.",
    "I love that spontaneity isn't required for something to feel special to you.",
    "I love how thoughtful your aesthetic is.",
    "I love your girl-boss energy.",
    "I love how capable you are.",
    "I love that you challenge me to pay attention.",
    "I love that I want to know every random little fact about you.",
    "I love how much you care about doing things well.",
    "I love that you're not easy to summarize.",
    "I love that you have strong opinions and aren't afraid to have them.",
    "I love that there is always another detail about you worth remembering.",
    "I love that even your comfort things are very specifically Mariah.",
    "I love the way your brain works.",
    "I love that you're both creative and logical.",
    "I love how driven you are without losing your interests outside of work.",
    "I love that you make me want to plan things properly instead of winging it.",
    "I love that you know exactly what kind of flowers you like.",
    "I love that you can make a simple coffee run feel like part of your routine.",
    "I love getting to know you more than I did yesterday.",
]

# ============================================================
# MARIAH KNOWLEDGE
# ============================================================

PROFILE = {
    "Personality": [
        "Ambitious and career-driven",
        "Disciplined with long-term goals",
        "Strong personal standards",
        "Logical decision-maker",
        "Naturally takes charge",
        "Confident and assertive",
        "ENTJ",
        "Prefers structure and routine over spontaneity",
        "Knowledgeable and interested in politics, art, literature, illustration, and architecture",
    ],
    "Favorites": [
        "Favorite color: sage green",
        "Favorite numbers: 9 and 81",
        "Favorite Russian author: Fyodor Dostoevsky",
        "Comfort anime: Hunter x Hunter",
        "Also likes Psycho-Pass",
        "Likes literary nonfiction",
        "Likes dystopian books and movies",
        "Likes drawing and reading",
        "Likes museums, exhibitions, and aquariums",
        "Likes Ikebana and Dutch Master flower arrangements",
        "Favorite ice cream: rocky road or mango",
        "Favorite cake: chocolate fudge",
        "Favorite gummy: berry Trolli worms",
    ],
    "Coffee": [
        "Literature / essay work: hot pistachio latte",
        "Illustration / architecture work: hot caramel macchiato",
        "Coffee is always hot",
    ],
    "Food": [
        "Favorite dish: tacos tapatios from Del Rio",
        "Second favorite: enchiladas verdes with cheese inside",
        "Little Panda comfort order: rice, vegetables, and tofu",
        "Likes strawberries",
        "Prefers wheat bread",
        "Does not like onions",
        "Hates pozole",
        "No oranges",
        "No watermelon",
        "No peanut butter",
        "No cotton candy",
        "No vanilla cake",
        "Does not drink milk alone or in cereal",
        "Was vegetarian for 6 years",
    ],
    "Style": [
        "Aesthetic: black, olive green, navy blue, dark brown, grey, barely white",
        "Graphic tees: M / loose fit",
        "Pants: usually 25–26 depending on brand",
        "Sweats: M, no cuffed ankles",
        "Shoes: women’s 7.5 / 8",
        "Ring size: 9",
        "Likes matching silver accessories for phone, bag, or wrist",
        "Gold earrings only",
        "Necklaces and rings are silver right now",
    ],
    "Remember": [
        "Hates moths",
        "Cannot swim",
        "Dislikes water, boats, and the ocean",
        "Gets carsick and chewing gum helps",
        "Likes blue 5 Gum",
        "Prefers planned / structured dates",
        "Uses “mkay” sarcastically",
        "“Sweetcheeks” is off the table",
        "“Babe” sounds dismissive",
        "“I miss your face” sounds superficial",
    ],
}

DATE_IDEAS = [
    (
        "The Mariah Day",
        "Brunch + hot coffee → thrifting → skincare / little shopping → exhibition or museum → pick up something from the exhibit → home for a spa night."
    ),
    (
        "Ikebana Date",
        "Pick out flowers together, learn some basic Ikebana principles, then each make an arrangement and explain your choices."
    ),
    (
        "Dutch Master Flowers",
        "Go to an art museum, find Dutch floral still lifes, then recreate the mood with a dramatic flower arrangement at home."
    ),
    (
        "Museum + Coffee",
        "Get hot coffee first, then visit a museum or exhibition. Each of you picks one piece to talk about afterward over food."
    ),
    (
        "Dystopian Night",
        "Pick a dystopian movie or book, order comfort food, then debate whether the society could actually happen."
    ),
    (
        "Bookstore Challenge",
        "Go to a bookstore and each choose one book for the other based on the cover, title, and first page."
    ),
    (
        "Architecture Walk",
        "Pick an area with interesting buildings, grab a caramel macchiato, photograph favorite details, then sketch one afterward."
    ),
    (
        "Aquarium Day",
        "Aquarium date, then dinner somewhere with a vegetarian-friendly menu. No boats involved."
    ),
    (
        "Tacos + Thrifting",
        "Tacos first, then TJ Maxx / Marshalls / thrifting, and finish with Starbucks."
    ),
]

GIFT_IDEAS = [
    "Mid-century modern black lamp with stainless-steel details",
    "Silver matching phone / bag / wrist accessory",
    "Structured Ikebana-style arrangement",
    "Dutch Master-inspired flower arrangement",
    "A beautiful Dostoevsky edition",
    "A dystopian or literary nonfiction book",
    "Museum or exhibition tickets",
    "Art or architecture book",
    "A sage-green item that fits her aesthetic",
    "Chocolate fudge cake + hot coffee study care package",
]

# ============================================================
# STORAGE — SUPABASE IN CLOUD, LOCAL JSON AS FALLBACK
# ============================================================

ROOT = Path(__file__).parent
MEMORY_DIR = ROOT / "assets" / "memories"
DATA_FILE = ROOT / "our_little_world_data.json"

MEMORY_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_DATA = {
    "memory_notes": {},
    "next_see_date": "2026-09-30",
    "custom_timestamps": [],
}

def _secret(name, default=""):
    try:
        return str(st.secrets.get(name, default))
    except Exception:
        return str(os.getenv(name, default))

SUPABASE_URL = _secret("SUPABASE_URL", "").rstrip("/")
SUPABASE_KEY = _secret("SUPABASE_KEY", "")
APP_PIN = _secret("APP_PIN", "1001")

def supabase_enabled():
    return bool(SUPABASE_URL and SUPABASE_KEY)

def _supabase_request(method, endpoint, payload=None, extra_headers=None):
    url = f"{SUPABASE_URL}{endpoint}"
    body = None

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
    }

    if extra_headers:
        headers.update(extra_headers)

    if payload is not None:
        body = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        url=url,
        data=body,
        headers=headers,
        method=method,
    )

    with urllib.request.urlopen(req, timeout=8) as response:
        raw = response.read().decode("utf-8")
        return json.loads(raw) if raw else None

def _merge_defaults(existing):
    if not isinstance(existing, dict):
        existing = {}

    merged = json.loads(json.dumps(DEFAULT_DATA))
    merged.update(existing)
    merged.setdefault("memory_notes", {})
    merged.setdefault("next_see_date", "2026-09-30")
    merged.setdefault("custom_timestamps", [])
    return merged

def load_data():
    if supabase_enabled():
        try:
            rows = _supabase_request(
                "GET",
                "/rest/v1/app_state?key=eq.main&select=value"
            )

            if rows and isinstance(rows, list) and rows[0].get("value") is not None:
                return _merge_defaults(rows[0]["value"])

            fresh = _merge_defaults({})
            save_data(fresh)
            return fresh
        except Exception:
            pass

    if not DATA_FILE.exists():
        DATA_FILE.write_text(
            json.dumps(DEFAULT_DATA, indent=2),
            encoding="utf-8",
        )
        return json.loads(json.dumps(DEFAULT_DATA))

    try:
        existing = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        return _merge_defaults(existing)
    except Exception:
        return json.loads(json.dumps(DEFAULT_DATA))

def save_data(data):
    if supabase_enabled():
        try:
            _supabase_request(
                "POST",
                "/rest/v1/app_state?on_conflict=key",
                payload={
                    "key": "main",
                    "value": data,
                },
                extra_headers={
                    "Prefer": "resolution=merge-duplicates,return=minimal"
                },
            )
            return
        except Exception:
            pass

    DATA_FILE.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8",
    )

data = load_data()

# ============================================================
# HELPERS
# ============================================================

def next_occurrence(month, day):
    today = date.today()
    target = date(today.year, month, day)
    if target < today:
        target = date(today.year + 1, month, day)
    return target, (target - today).days

def memory_images():
    valid = {".png", ".jpg", ".jpeg", ".webp"}
    return sorted([p for p in MEMORY_DIR.iterdir() if p.suffix.lower() in valid])

def bullets(items):
    return "\n".join(f"• {x}" for x in items)

# ============================================================
# LOCAL MARIAH CHATBOT
# ============================================================

def mariah_reply(question):
    q = question.lower().strip()

    if any(x in q for x in ["boat", "ocean", "swim", "water date", "beach"]):
        return (
            "Rodney, definitely not 😭 Mariah can’t swim and she already dislikes water, boats, and the ocean, "
            "so that kind of date is basically the opposite of her vibe. A museum, exhibition, bookstore, flower-arranging date, "
            "or even an aquarium would fit her way better."
        )

    if "coffee" in q or "latte" in q or "macchiato" in q:
        if any(x in q for x in ["literature", "essay", "reading", "writing"]):
            return (
                "If she’s working on literature or an essay, get her a hot pistachio latte. "
                "That’s her lock-in coffee for that kind of work, and the important part is that she prefers her coffee hot."
            )
        if any(x in q for x in ["architecture", "illustration", "drawing", "design"]):
            return (
                "If she’s doing illustration or architecture-related work, go with a hot caramel macchiato. "
                "That’s the coffee she associates with that kind of creative work."
            )
        return (
            "Her coffee order depends on what she’s doing. For literature or essay work, she goes for a hot pistachio latte. "
            "For illustration or architecture work, she prefers a hot caramel macchiato. Either way, make it hot."
        )

    if any(x in q for x in ["food", "eat", "dinner", "lunch", "restaurant", "meal", "snack"]):
        return (
            "For food, the safest move is something close to what she already loves. Her favorite is tacos tapatios from Del Rio, "
            "and enchiladas verdes with cheese inside are another strong choice. Her Little Panda comfort order is rice, vegetables, and tofu. "
            "If you want dessert, chocolate fudge cake is very safe, and rocky road or mango are her preferred ice cream flavors. "
            "I’d avoid onions, pozole, oranges, watermelon, peanut butter, cotton candy, vanilla cake, white bread, and random gummies."
        )

    if any(x in q for x in ["cake", "dessert", "sweet", "candy", "gummy"]):
        return (
            "Chocolate fudge cake is the safest answer. She specifically does not want vanilla cake. "
            "For candy, berry Trolli worms are the one gummy she actually likes, and for ice cream she goes for rocky road or mango."
        )

    if any(x in q for x in ["gift", "birthday", "buy her", "present", "surprise"]):
        gifts = random.sample(GIFT_IDEAS, min(4, len(GIFT_IDEAS)))
        return (
            "I’d keep the gift structured and very aligned with her taste instead of choosing something random. "
            f"A few good directions would be {gifts[0].lower()}, {gifts[1].lower()}, {gifts[2].lower()}, or {gifts[3].lower()}. "
            "Her current known birthday target is a mid-century modern black lamp with stainless-steel details, so that is still the strongest clue."
        )

    if any(x in q for x in ["necklace", "earring", "ring", "jewelry", "bracelet", "silver", "gold"]):
        return (
            "Her jewelry setup is pretty specific. Her earrings are gold, while her necklaces and rings are silver right now. "
            "She also likes matching silver accessories for things like her phone, bag, or wrist. Her ring size is 9."
        )

    if any(x in q for x in ["size", "shirt", "pants", "sweats", "shoes", "clothes", "graphic tee"]):
        return (
            "For clothes, she usually wears a medium in shirts and likes graphic tees loose. Her pants are generally around 25 to 26, "
            "although she’s picky and it depends on the brand. Sweats are a medium and she does not like cuffed ankles. "
            "Her shoe size is around women’s 7.5 to 8, and her ring size is 9."
        )

    if any(x in q for x in ["date", "plan", "saturday", "weekend", "day together"]):
        title, plan = random.choice(DATE_IDEAS)
        return (
            f"I’d do the {title}. {plan} "
            "That kind of plan fits her because she likes structure and routine more than something completely spontaneous."
        )

    if any(x in q for x in ["flower", "bouquet", "arrangement", "ikebana"]):
        return (
            "She seems to care more about intentional flower arrangements than a random bouquet. "
            "Ikebana and Dutch Master-style arrangements are especially her thing, so something composed and visually deliberate would feel much more personal."
        )

    if any(x in q for x in ["book", "read", "author", "dostoevsky", "literature"]):
        return (
            "She likes literary nonfiction and dystopian books, and Dostoevsky is her favorite Russian author. "
            "A beautiful edition of Dostoevsky or a well-chosen dystopian or literary nonfiction book would make sense for her."
        )

    if any(x in q for x in ["anime", "hxh", "hunter", "psycho-pass", "psycho pass"]):
        return (
            "Hunter x Hunter is her comfort anime, and she also likes Psycho-Pass. "
            "If you’re choosing something familiar for a cozy night, Hunter x Hunter is probably the safer comfort pick."
        )

    if any(x in q for x in ["car", "carsick", "road trip", "gum"]):
        return (
            "She gets carsick, so bring gum if you’re going on a longer drive. "
            "Blue 5 Gum is the one she likes, which is exactly the kind of tiny detail worth remembering."
        )

    if any(x in q for x in ["color", "aesthetic", "palette", "style"]):
        return (
            "Her aesthetic is muted and structured: sage green, black, olive green, navy blue, dark brown, grey, and barely white. "
            "I’d think clean, mature, understated, and intentional rather than bright or overly cute."
        )

    if any(x in q for x in ["personality", "what is she like", "describe mariah", "entj"]):
        return (
            "Mariah comes across as ambitious, disciplined, logical, confident, assertive, and very long-term focused. "
            "She has strong standards, naturally takes charge, and seems much more comfortable with structure and routine than spontaneity. "
            "That ENTJ, girl-boss description actually fits her pretty well."
        )

    if any(x in q for x in ["call her", "nickname", "sweetcheeks", "babe", "miss your face"]):
        return (
            "There are a few wording landmines. Sweetcheeks is completely off the table, babe can sound dismissive to her, "
            "and “I miss your face” comes across as superficial. Also, when she says “mkay,” she’s usually being sarcastic."
        )

    if any(x in q for x in ["what does she like", "what does mariah like", "favorites", "favorite"]):
        return (
            "She likes art, literature, politics, drawing, architecture, museums, exhibitions, aquariums, Dostoevsky, dystopian books and movies, "
            "Hunter x Hunter, Psycho-Pass, Ikebana, Dutch Master flower arrangements, hot coffee, sage green, chocolate fudge cake, "
            "rocky road or mango ice cream, and berry Trolli worms. The overall pattern is that she likes things that feel thoughtful, structured, and aesthetically intentional."
        )

    return (
        "I know a lot of Mariah lore, but ask me something a little more specific. "
        "You could ask what coffee to get her, what kind of date would fit her, what food to avoid, what jewelry she likes, "
        "what size she wears, or whether a specific gift idea sounds like her."
    )

# ============================================================
# STYLING
# ============================================================

st.markdown(
    """
<style>
:root {
    --sage: #A7B39A;
    --sage-dark: #626E58;
    --ink: #171817;
    --cream: #F4F2EC;
    --paper: #FAF9F5;
    --stone: #D8D3CA;
}

.stApp {
    background:
        radial-gradient(circle at 12% 4%, rgba(167,179,154,.16), transparent 26%),
        linear-gradient(180deg, #f8f7f2 0%, #efeee8 100%);
    color: #171817;
}

.block-container {
    max-width: 1500px;
    padding-top: 2.2rem;
    padding-left: 3.5rem;
    padding-right: 3.5rem;
    padding-bottom: 4rem;
}

[data-testid="stSidebar"] {
    background: #171817;
    border-right: 1px solid rgba(255,255,255,.06);
}

[data-testid="stSidebar"] * {
    color: #F4F2EC !important;
}

[data-testid="stSidebar"] [role="radiogroup"] label {
    padding-top: .25rem;
    padding-bottom: .25rem;
}

h1, h2, h3 {
    letter-spacing: -0.035em;
}

.hero {
    border: 1px solid rgba(30,30,30,.10);
    padding: 54px 48px;
    border-radius: 10px;
    background: rgba(250,249,245,.84);
    box-shadow: 0 18px 45px rgba(20,20,20,.07);
    margin-bottom: 24px;
}

.hero-kicker {
    text-transform: uppercase;
    letter-spacing: .28em;
    font-size: .70rem;
    opacity: .52;
}

.hero-title {
    font-family: Georgia, serif;
    font-size: clamp(3.6rem, 8vw, 6.5rem);
    line-height: .90;
    margin: 15px 0 20px 0;
}

.hero-sub {
    max-width: 820px;
    font-size: 1.08rem;
    opacity: .65;
    line-height: 1.65;
}

.card {
    border: 1px solid rgba(25,25,25,.11);
    border-radius: 8px;
    padding: 22px;
    background: rgba(255,255,255,.56);
    margin-bottom: 14px;
}

.sage-card {
    border-radius: 8px;
    padding: 24px;
    background: #DDE4D7;
    border: 1px solid rgba(60,70,55,.10);
    margin-bottom: 15px;
}

.dark-card {
    border-radius: 8px;
    padding: 24px;
    background: #1B1C1A;
    color: #F3F0E8;
    margin-bottom: 15px;
}

.metric-big {
    font-family: Georgia, serif;
    font-size: 2.7rem;
    font-weight: 700;
    line-height: 1;
}

.metric-small {
    opacity: .55;
    font-size: .78rem;
    text-transform: uppercase;
    letter-spacing: .13em;
    margin-top: 8px;
}

.section-kicker {
    text-transform: uppercase;
    letter-spacing: .18em;
    font-size: .72rem;
    opacity: .50;
    margin-bottom: 6px;
}

.chat-intro {
    border-radius: 10px;
    padding: 28px;
    background: #1B1C1A;
    color: #F3F0E8;
    margin-bottom: 20px;
}

.timeline {
    border-left: 2px solid #A7B39A;
    padding-left: 22px;
    margin-top: 14px;
}

.timeline-item {
    padding-bottom: 28px;
}

.timeline-date {
    text-transform: uppercase;
    letter-spacing: .11em;
    font-size: .74rem;
    opacity: .48;
}

.timeline-title {
    font-family: Georgia, serif;
    font-size: 1.35rem;
    margin-top: 5px;
}

.profile-label {
    text-transform: uppercase;
    letter-spacing: .12em;
    font-size: .72rem;
    opacity: .5;
    margin-bottom: 10px;
}

div.stButton > button {
    border-radius: 5px;
    font-weight: 650;
    border: 1px solid rgba(30,30,30,.16);
}

[data-testid="stChatMessage"] {
    background: rgba(255,255,255,.52);
    border: 1px solid rgba(30,30,30,.08);
    border-radius: 10px;
    padding: .45rem .75rem;
    margin-bottom: .75rem;
}

[data-testid="stFileUploader"] {
    border-radius: 8px;
}

.hero-wrap {
    position: relative;
}


.pin-shell {
    max-width: 580px;
    margin: 8vh auto 0 auto;
    padding: 0 1rem;
}

.pin-card {
    position: relative;
    background:
        radial-gradient(circle at 85% 10%, rgba(167,179,154,.22), transparent 28%),
        #F8F7F2;
    border: 1px solid rgba(23,24,23,.12);
    border-radius: 18px;
    padding: 54px 48px 44px 48px;
    box-shadow: 0 25px 70px rgba(20,20,20,.12);
    text-align: center;
}

.pin-couple {
    font-size: 2.5rem;
    margin-bottom: 18px;
}

.pin-kicker {
    text-transform: uppercase;
    letter-spacing: .28em;
    font-size: .68rem;
    opacity: .48;
    margin-bottom: 10px;
}

.pin-title {
    font-family: Georgia, serif;
    font-size: 3.35rem;
    line-height: .98;
    margin-bottom: 14px;
}

.pin-copy {
    max-width: 390px;
    margin: 0 auto;
    opacity: .62;
    line-height: 1.6;
}

.pin-heartline {
    margin-top: 26px;
    letter-spacing: .45em;
    opacity: .36;
    font-size: .8rem;
}

.pin-hint {
    text-align: center;
    opacity: .45;
    font-size: .78rem;
    margin-top: 16px;
}

div[data-testid="stTextInput"] input[type="password"] {
    text-align: center;
    letter-spacing: .45em;
    font-size: 1.35rem;
    height: 3.3rem;
    border-radius: 9px;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# PIN GATE
# ============================================================

def pin_gate():
    if st.session_state.get("authenticated", False):
        return

    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] { display: none; }
            [data-testid="collapsedControl"] { display: none; }
            .block-container {
                max-width: 760px !important;
                padding-top: 1rem !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="pin-shell">
            <div class="pin-card">
                <div class="pin-couple">👫</div>
                <div class="pin-kicker">Rodney × Mariah</div>
                <div class="pin-title">Our Little World.</div>
                <div class="pin-copy">
                    A tiny private corner made for two people.
                    Enter the code to come inside.
                </div>
                <div class="pin-heartline">♥ · ♥ · ♥</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    entered_pin = st.text_input(
        "PIN",
        type="password",
        max_chars=12,
        placeholder="••••",
        label_visibility="collapsed",
        key="pin_input",
    )

    left, center, right = st.columns([1, 1.25, 1])

    with center:
        unlock = st.button(
            "Enter our world",
            use_container_width=True,
            key="unlock_button",
        )

    if unlock:
        if hmac.compare_digest(str(entered_pin), str(APP_PIN)):
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("That isn't our code 🤍")

    st.markdown(
        '<div class="pin-hint">private by design · made with love</div>',
        unsafe_allow_html=True,
    )

    st.stop()

pin_gate()

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("## R + M 👫")
    st.caption("Our Little World")
    st.markdown("---")

    page = st.radio(
        "Navigation",
        ["Home", "Ask Mariah", "Memories", "Mariah"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.caption("Rodney × Mariah")

    if st.button("Lock", use_container_width=True, key="lock_app"):
        st.session_state.authenticated = False
        st.rerun()

# ============================================================
# HOME
# ============================================================

if page == "Home":
    anniversary_date, anniversary_days = next_occurrence(*ANNIVERSARY)
    birthday_date, birthday_days = next_occurrence(*HER_BIRTHDAY)

    # Editable next-seeing date, persisted locally.
    try:
        saved_see_date = date.fromisoformat(data.get("next_see_date", "2026-09-30"))
    except Exception:
        saved_see_date = date(2026, 9, 30)

    see_days = max((saved_see_date - date.today()).days, 0)

    st.markdown(
        """
        <div class="hero-wrap">
            <div class="hero">
                <div class="hero-kicker">Rodney × Mariah</div>
                <div class="hero-title">Our Little<br>World.</div>
                <div class="hero-sub">
                    A small place for the details that matter:
                    memories, dates, tiny preferences, and all the things
                    Rodney refuses to forget.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f"""
            <div class="sage-card">
                <div class="metric-big">{anniversary_days}</div>
                <div class="metric-small">days until anniversary</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="card">
                <div class="metric-big">{birthday_days}</div>
                <div class="metric-small">days until her birthday</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
            <div class="dark-card">
                <div class="metric-big">{see_days}</div>
                <div class="metric-small">days until I see her</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        new_see_date = st.date_input(
            "When am I seeing her?",
            value=saved_see_date,
            min_value=date.today(),
            format="MM/DD/YYYY",
            key="next_see_date_picker",
        )

        if new_see_date.isoformat() != data.get("next_see_date"):
            data["next_see_date"] = new_see_date.isoformat()
            save_data(data)
            st.rerun()

    st.write("")
    left, right = st.columns([1.25, 1])

    with left:
        st.markdown("### One thing I love about you")

        if "reason" not in st.session_state:
            st.session_state.reason = random.choice(REASONS)

        st.markdown(
            f"""
            <div class="sage-card" style="font-family:Georgia,serif;font-size:1.35rem;line-height:1.55;">
                “{st.session_state.reason}”
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Another one"):
            st.session_state.reason = random.choice(REASONS)
            st.rerun()

    with right:
        st.markdown("### Dates")
        st.markdown(
            """
            <div class="card">
                <div class="profile-label">Anniversary</div>
                <b>October 1, 2026</b>
                <br><br>
                <div class="profile-label">Her birthday</div>
                <b>November 05, 2005</b>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ============================================================
# ASK MARIAH
# ============================================================

elif page == "Ask Mariah":
    st.markdown("# Ask Mariah")
    st.markdown(
        """
        <div class="chat-intro">
            <div class="section-kicker" style="color:#c9d1c2;opacity:.72;">Rodney's Mariah assistant</div>
            Ask anything based on what you already know about her:
            food, coffee, gifts, dates, sizes, books, colors, jewelry, or tiny details.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Suggested prompts
    p1, p2, p3 = st.columns(3)

    suggested = None

    with p1:
        if st.button("☕ What coffee should I get her?", use_container_width=True):
            suggested = "What coffee should I get her?"

    with p2:
        if st.button("🗓️ Plan us a date", use_container_width=True):
            suggested = "Plan us a date"

    with p3:
        if st.button("🎁 Give me a gift idea", use_container_width=True):
            suggested = "Give me a gift idea"

    p4, p5, p6 = st.columns(3)

    with p4:
        if st.button("🍴 What food should I avoid?", use_container_width=True):
            suggested = "What food should I avoid?"

    with p5:
        if st.button("💍 Jewelry rules", use_container_width=True):
            suggested = "What jewelry does she like?"

    with p6:
        if st.button("👕 What size does she wear?", use_container_width=True):
            suggested = "What size clothes does she wear?"

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    typed = st.chat_input("Ask something about Mariah...")

    prompt = suggested or typed

    if prompt:
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        reply = mariah_reply(prompt)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

    if st.session_state.chat_history:
        if st.button("Clear chat"):
            st.session_state.chat_history = []
            st.rerun()

# ============================================================
# MEMORIES
# ============================================================

elif page == "Memories":
    st.markdown("# Memories")
    st.caption("Photos and the little timestamps worth keeping.")

    tab1, tab2 = st.tabs(["Photos", "Timestamps"])

    with tab1:
        uploaded = st.file_uploader(
            "Add photos",
            type=["png", "jpg", "jpeg", "webp"],
            accept_multiple_files=True,
        )

        if uploaded:
            for f in uploaded:
                safe_name = f.name.replace("/", "_").replace("\\", "_")
                (MEMORY_DIR / safe_name).write_bytes(f.getbuffer())

            st.success("Saved.")
            st.rerun()

        pics = memory_images()

        if not pics:
            st.info("No photos yet. Add a few here and this becomes your little archive.")
        else:
            cols = st.columns(3)

            for i, p in enumerate(pics):
                with cols[i % 3]:
                    st.image(str(p), use_container_width=True)

                    current = data["memory_notes"].get(p.name, "")
                    caption = st.text_input(
                        "Caption",
                        value=current,
                        key=f"caption_{p.name}",
                        placeholder="Add a little note...",
                    )

                    if caption != current:
                        data["memory_notes"][p.name] = caption
                        save_data(data)

    with tab2:
        # Built-in timestamps
        all_timestamps = []

        for item in MILESTONES:
            all_timestamps.append({
                "date": item["date"],
                "title": item["title"],
                "detail": item["detail"],
                "custom": False,
            })

        # User-added timestamps
        for item in data.get("custom_timestamps", []):
            all_timestamps.append({
                "date": item["date"],
                "title": item["title"],
                "detail": item.get("detail", ""),
                "custom": True,
            })

        st.markdown('<div class="timeline">', unsafe_allow_html=True)

        for idx, item in enumerate(all_timestamps):
            st.markdown(
                f"""
                <div class="timeline-item">
                    <div class="timeline-date">{item["date"]}</div>
                    <div class="timeline-title">{item["title"]}</div>
                    <div>{item["detail"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("### Add timestamp")

        c1, c2 = st.columns([1, 1])

        with c1:
            new_ts_date = st.date_input(
                "Date",
                value=date.today(),
                format="MM/DD/YYYY",
                key="new_timestamp_date",
            )

        with c2:
            st.markdown("**Time**")
            t1, t2, t3 = st.columns([1, 1, 1.15])

            with t1:
                new_ts_hour = st.selectbox(
                    "Hour",
                    list(range(1, 13)),
                    index=1,
                    key="new_timestamp_hour",
                    label_visibility="collapsed",
                )

            with t2:
                new_ts_minute = st.selectbox(
                    "Minute",
                    [f"{m:02d}" for m in range(60)],
                    index=36,
                    key="new_timestamp_minute",
                    label_visibility="collapsed",
                )

            with t3:
                new_ts_ampm = st.selectbox(
                    "AM/PM",
                    ["AM", "PM"],
                    index=1,
                    key="new_timestamp_ampm",
                    label_visibility="collapsed",
                )

        new_ts_title = st.text_input(
            "What happened?",
            placeholder='e.g. "First museum date"',
            key="new_timestamp_title",
        )

        new_ts_detail = st.text_input(
            "Small note (optional)",
            placeholder="Anything else you want to remember...",
            key="new_timestamp_detail",
        )

        if st.button("Add timestamp"):
            if new_ts_title.strip():
                formatted_date = new_ts_date.strftime("%B %d, %Y")
                formatted_time = f"{new_ts_hour}:{new_ts_minute} {new_ts_ampm}"
                data.setdefault("custom_timestamps", []).append(
                    {
                        "date": f"{formatted_date} — {formatted_time}",
                        "title": new_ts_title.strip(),
                        "detail": new_ts_detail.strip(),
                    }
                )
                save_data(data)
                st.success("Timestamp added.")
                st.rerun()
            else:
                st.warning("Add a title for the timestamp first.")

        if data.get("custom_timestamps"):
            st.markdown("### Your added timestamps")

            # Show simple delete controls for custom timestamps only.
            for i, item in enumerate(data["custom_timestamps"]):
                a, b = st.columns([8, 1])
                with a:
                    st.caption(f'{item["date"]} — {item["title"]}')
                with b:
                    if st.button("Delete", key=f"delete_ts_{i}"):
                        data["custom_timestamps"].pop(i)
                        save_data(data)
                        st.rerun()

# ============================================================
# MARIAH PROFILE
# ============================================================

elif page == "Mariah":
    st.markdown("# Mariah")
    st.caption("The reference page. Organized, because she would probably prefer it that way.")

    st.markdown(
        """
        <div class="hero" style="padding:36px 38px;">
            <div class="hero-kicker">Mariah Lizette Duenez</div>
            <div style="font-family:Georgia,serif;font-size:2.8rem;line-height:1.05;margin:12px 0;">
                Structured. Ambitious. Opinionated.<br>
                Very specifically Mariah.
            </div>
            <div class="hero-sub">
                Art, literature, coffee, routines, good taste, strong standards,
                and approximately zero interest in boats.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tabs = st.tabs(["Personality", "Favorites", "Food", "Style", "Remember"])

    with tabs[0]:
        for item in PROFILE["Personality"]:
            st.markdown(f"- {item}")

    with tabs[1]:
        for item in PROFILE["Favorites"]:
            st.markdown(f"- {item}")

        st.markdown("### Coffee")
        for item in PROFILE["Coffee"]:
            st.markdown(f"- {item}")

    with tabs[2]:
        for item in PROFILE["Food"]:
            st.markdown(f"- {item}")

    with tabs[3]:
        for item in PROFILE["Style"]:
            st.markdown(f"- {item}")

    with tabs[4]:
        for item in PROFILE["Remember"]:
            st.markdown(f"- {item}")
st.markdown("---")
st.caption("Rodney × Mariah")
