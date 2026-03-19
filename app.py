import streamlit as st
import utils

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Enlightening English",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ── Google Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Lora:ital,wght@0,400;0,600;1,400;1,600&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

    /* ── Design tokens ── */
    :root {
        --bg-base:    #0f0f0f;
        --bg-surface: #161616;
        --bg-raised:  #1d1d1d;
        --bg-hover:   #232323;
        --gold:       #D4A853;
        --gold-dim:   #7A5E28;
        --gold-faint: #7A5E2820;
        --terracotta: #B8572A;
        --sage:       #5F7E64;
        --blue:       #6B9FD4;
        --text-1:     #F2EDE4;
        --text-2:     #9C9080;
        --text-3:     #5A524A;
        --rule:       #1F1F1F;
    }

    /* ── Chrome removal ── */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }
    [data-testid="collapsedControl"] { display: none; }

    /* ── Base ── */
    html, body,
    [data-testid="stAppViewContainer"],
    [data-testid="stApp"],
    [data-testid="stMain"],
    section[data-testid="stMain"] > div {
        background-color: var(--bg-base) !important;
        color: var(--text-1);
        font-family: 'Space Grotesk', sans-serif;
    }

    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 5rem !important;
        max-width: 1220px;
    }

    /* ── Global typography ── */
    h1, h2, h3 {
        font-family: 'DM Serif Display', serif !important;
        color: var(--text-1) !important;
        font-weight: 400 !important;
    }
    p, li, span, div, label {
        font-family: 'Space Grotesk', sans-serif;
        color: var(--text-1);
    }

    /* ── Streamlit button ── */
    .stButton > button {
        background: transparent;
        border: 1px solid var(--gold-dim);
        color: var(--gold);
        border-radius: 4px;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.8rem;
        font-weight: 500;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        padding: 0.45rem 1.2rem;
        width: 100%;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background: var(--gold);
        color: var(--bg-base);
        border-color: var(--gold);
    }

    /* ── Card hover effect ── */
    .book-card-wrap {
        position: relative;
        border-radius: 10px 10px 0 0;
        overflow: hidden;
        cursor: pointer;
    }
    .book-card-wrap .card-overlay {
        position: absolute;
        inset: 0;
        background: rgba(15,15,15,0.75);
        display: flex;
        align-items: center;
        justify-content: center;
        opacity: 0;
        transition: opacity 0.3s ease;
        border-radius: 10px 10px 0 0;
    }
    .book-card-wrap:hover .card-overlay {
        opacity: 1;
    }
    .card-overlay-text {
        color: var(--gold);
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.82rem;
        font-weight: 600;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        border: 1px solid var(--gold-dim);
        padding: 0.5rem 1.4rem;
        border-radius: 4px;
    }

    /* ── Analysis prose override ── */
    .prose-body p {
        font-family: 'Lora', serif !important;
        font-size: 1rem !important;
        line-height: 1.85 !important;
        color: #D4CEC6 !important;
    }
    .prose-body h2 {
        font-family: 'DM Serif Display', serif !important;
        font-size: 1.35rem !important;
        margin-top: 1.75rem !important;
    }
    .prose-body strong {
        color: var(--text-1) !important;
        font-weight: 600 !important;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: var(--bg-base); }
    ::-webkit-scrollbar-thumb { background: #2a2a2a; border-radius: 3px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Session state ─────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state["page"] = "home"
if "lesson_id" not in st.session_state:
    st.session_state["lesson_id"] = None


# ═════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═════════════════════════════════════════════════════════════════════════════

def _section_header(number: str, label: str):
    st.markdown(
        f"""
        <div style="
            display: flex;
            align-items: center;
            gap: 1rem;
            margin: 3rem 0 1.5rem 0;
            position: relative;
        ">
            <span style="
                font-family: 'DM Serif Display', serif;
                font-size: 5rem;
                color: var(--text-1);
                opacity: 0.05;
                line-height: 1;
                position: absolute;
                left: -0.5rem;
                top: -0.75rem;
                pointer-events: none;
                user-select: none;
            ">{number}</span>
            <h2 style="
                font-family: 'DM Serif Display', serif !important;
                font-size: 1.65rem;
                margin: 0;
                padding-left: 0.25rem;
                letter-spacing: 0.01em;
                position: relative;
                z-index: 1;
            ">{label}</h2>
            <div style="
                flex: 1;
                height: 1px;
                background: var(--rule);
            "></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ═════════════════════════════════════════════════════════════════════════════
# HOME PAGE — Gallery
# ═════════════════════════════════════════════════════════════════════════════

def render_home():
    # ── Logotype header ──
    st.markdown(
        """
        <div style="text-align: center; padding: 2.5rem 0 0.5rem;">
            <h1 style="
                font-family: 'DM Serif Display', serif !important;
                font-size: 3.5rem;
                font-weight: 400 !important;
                margin: 0 0 0.5rem 0;
                background: linear-gradient(135deg, #D4A853 0%, #F2EDE4 55%, #D4A853 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                letter-spacing: 0.01em;
            ">Enlightening English</h1>
            <p style="
                font-family: 'Space Grotesk', sans-serif;
                font-size: 0.72rem;
                letter-spacing: 0.28em;
                text-transform: uppercase;
                color: var(--gold);
                margin: 0 0 1.5rem 0;
                font-weight: 500;
            ">Literature for the curious &nbsp;·&nbsp; Stories for the world</p>
            <div style="
                width: 48px;
                height: 1px;
                background: var(--gold-dim);
                margin: 0 auto 2.5rem;
            "></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    lessons = utils.load_all_lessons("data/lessons")

    if not lessons:
        st.markdown(
            "<p style='color:var(--text-2); text-align:center; margin-top:3rem; "
            "font-family:Space Grotesk,sans-serif;'>No lessons found in data/lessons/ — drop a .json file in to begin.</p>",
            unsafe_allow_html=True,
        )
        return

    cols = st.columns(3, gap="large")
    for i, lesson in enumerate(lessons):
        with cols[i % 3]:
            _render_book_card(lesson)


def _render_book_card(lesson: dict):
    cover      = lesson.get("cover_image_url", "")
    title      = lesson.get("title", "Untitled")
    author     = lesson.get("author", "")
    era        = lesson.get("era", "")
    tagline    = lesson.get("tagline", "")
    themes     = lesson.get("themes", [])

    theme_chips = "".join(
        f'<span style="'
        f'display:inline-block;border:1px solid var(--gold-dim);color:var(--gold);'
        f'font-family:Space Grotesk,sans-serif;font-size:0.65rem;letter-spacing:0.1em;'
        f'text-transform:uppercase;border-radius:2px;padding:2px 9px;margin:2px 3px 0 0;'
        f'">{t}</span>'
        for t in themes[:4]
    )

    if cover:
        img_block = (
            f'<div class="book-card-wrap">'
            f'<img src="{cover}" style="width:100%;height:320px;object-fit:cover;display:block;"/>'
            f'<div class="card-overlay"><span class="card-overlay-text">Open Reading Room →</span></div>'
            f'</div>'
        )
    else:
        img_block = (
            '<div class="book-card-wrap">'
            '<div style="width:100%;height:320px;background:var(--bg-raised);display:flex;'
            'align-items:center;justify-content:center;color:var(--text-3);font-size:3rem;">📖</div>'
            '<div class="card-overlay"><span class="card-overlay-text">Open Reading Room →</span></div>'
            '</div>'
        )

    st.markdown(
        f"""
        <div style="
            background: var(--bg-surface);
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 8px 32px rgba(0,0,0,0.7);
            margin-bottom: 0.4rem;
            transition: transform 0.25s ease, box-shadow 0.25s ease;
        ">
            {img_block}
            <div style="padding: 1.1rem 1.2rem 1.3rem;">
                <h3 style="
                    font-family: 'DM Serif Display', serif !important;
                    font-size: 1.2rem;
                    font-weight: 400 !important;
                    margin: 0 0 0.2rem 0;
                    line-height: 1.3;
                    color: var(--text-1) !important;
                ">{title}</h3>
                <p style="
                    font-family: 'Space Grotesk', sans-serif;
                    margin: 0 0 0.65rem 0;
                    color: var(--text-2);
                    font-size: 0.8rem;
                    letter-spacing: 0.04em;
                ">{author} &nbsp;·&nbsp; <em style='font-style:italic;'>{era}</em></p>
                <p style="
                    font-family: 'Lora', serif;
                    margin: 0 0 0.9rem 0;
                    color: #C0B8AC;
                    font-size: 0.88rem;
                    line-height: 1.55;
                    font-style: italic;
                ">"{tagline}"</p>
                <div>{theme_chips}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Explore →", key=f"btn_{lesson.get('id', title)}"):
        st.session_state["page"] = "lesson"
        st.session_state["lesson_id"] = lesson.get("id")
        st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
# LESSON PAGE — Reading Room
# ═════════════════════════════════════════════════════════════════════════════

def render_lesson():
    lesson_id = st.session_state.get("lesson_id")
    lesson = utils.load_lesson(f"data/lessons/{lesson_id}.json")

    if lesson is None:
        st.error("Could not load this lesson.")
        if st.button("← Back to Library"):
            st.session_state["page"] = "home"
            st.rerun()
        return

    if st.button("← Back to Library"):
        st.session_state["page"] = "home"
        st.rerun()

    _render_hero(lesson)
    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    _render_juicy_details(lesson)
    _render_authors_world(lesson)
    _render_literary_techniques(lesson)
    _render_analysis(lesson)
    _render_modern_connections(lesson)
    _render_reflective_tasks(lesson)
    _render_discussion_questions(lesson)
    st.markdown("<div style='height:4rem'></div>", unsafe_allow_html=True)


def _render_hero(lesson: dict):
    hero_url = lesson.get("hero_image_url", lesson.get("cover_image_url", ""))
    title    = lesson.get("title", "")
    author   = lesson.get("author", "")
    era      = lesson.get("era", "")
    tagline  = lesson.get("tagline", "")
    themes   = lesson.get("themes", [])

    theme_chips = "".join(
        f'<span style="'
        f'display:inline-block;border:1px solid var(--gold-dim);color:var(--gold);'
        f'font-family:Space Grotesk,sans-serif;font-size:0.68rem;letter-spacing:0.12em;'
        f'text-transform:uppercase;border-radius:2px;padding:3px 12px;margin:3px 4px 0 0;'
        f'">{t}</span>'
        for t in themes
    )

    bg = (
        f'background-image: linear-gradient(to bottom, rgba(15,15,15,0) 0%, rgba(15,15,15,0.7) 50%, #0f0f0f 100%), url("{hero_url}"); '
        f'background-size: cover; background-position: center 30%;'
        if hero_url
        else 'background: linear-gradient(160deg, #1a1a1a 0%, #0f0f0f 100%);'
    )

    st.markdown(
        f"""
        <div style="
            {bg}
            border-radius: 14px;
            min-height: 520px;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            padding: 5rem 3rem 3rem;
        ">
            <p style="
                font-family: 'Space Grotesk', sans-serif;
                font-size: 0.68rem;
                letter-spacing: 0.28em;
                text-transform: uppercase;
                color: var(--gold);
                margin: 0 0 0.75rem 0;
            ">{era}</p>
            <h1 style="
                font-family: 'DM Serif Display', serif !important;
                font-size: 4rem;
                font-weight: 400 !important;
                margin: 0 0 0.4rem 0;
                line-height: 1.1;
                letter-spacing: -0.02em;
                text-shadow: 0 2px 20px rgba(0,0,0,0.9);
                color: var(--text-1) !important;
            ">{title}</h1>
            <p style="
                font-family: 'Space Grotesk', sans-serif;
                font-size: 1.05rem;
                font-weight: 300;
                color: var(--text-2);
                margin: 0 0 0.75rem 0;
            ">{author}</p>
            <div style="width:60px;height:1px;background:var(--gold-dim);margin:0 0 0.9rem 0;"></div>
            <p style="
                font-family: 'Lora', serif;
                font-style: italic;
                font-size: 1rem;
                color: #A09585;
                margin: 0 0 1.25rem 0;
                max-width: 600px;
                line-height: 1.6;
            ">"{tagline}"</p>
            <div>{theme_chips}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_juicy_details(lesson: dict):
    details = lesson.get("juicy_details", [])
    if not details:
        return

    _section_header("01", "The Juicy Details")
    st.markdown(
        "<p style='color:var(--text-2);font-size:0.88rem;margin:-0.75rem 0 1.5rem;'>"
        "The things they never told you in the classroom."
        "</p>",
        unsafe_allow_html=True,
    )

    for detail in details:
        st.markdown(
            f"""
            <div style="
                display: flex;
                gap: 1.25rem;
                align-items: flex-start;
                background: var(--bg-surface);
                border-radius: 8px;
                padding: 1.1rem 1.4rem;
                margin-bottom: 0.65rem;
                border-left: 4px solid var(--gold);
            ">
                <span style="color:var(--gold);font-size:1rem;margin-top:1px;flex-shrink:0;line-height:1.6;">—</span>
                <p style="margin:0;line-height:1.75;color:#DDD6CD;font-size:0.95rem;">{detail}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_authors_world(lesson: dict):
    world = lesson.get("authors_world")
    if not world:
        return

    _section_header("02", "The Author's World")

    location    = world.get("location", "")
    description = world.get("description", "")
    places      = world.get("places_to_visit", [])

    st.markdown(
        f"""
        <div style="
            background: var(--bg-surface);
            border-radius: 10px;
            padding: 1.6rem 1.8rem;
            margin-bottom: 1.5rem;
        ">
            <p style="
                font-family: 'Space Grotesk', sans-serif;
                color: var(--gold);
                font-size: 0.7rem;
                letter-spacing: 0.18em;
                text-transform: uppercase;
                margin: 0 0 0.4rem;
            ">📍 Location</p>
            <h3 style="
                font-family: 'DM Serif Display', serif !important;
                font-size: 1.3rem;
                font-weight: 400 !important;
                margin: 0 0 0.8rem;
                color: var(--text-1) !important;
            ">{location}</h3>
            <p style="
                font-family: 'Lora', serif;
                font-size: 0.95rem;
                line-height: 1.75;
                color: #C0B8AC;
                margin: 0;
            ">{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if places:
        st.markdown(
            "<p style='color:var(--text-2);font-size:0.7rem;letter-spacing:0.18em;"
            "text-transform:uppercase;margin:0 0 0.85rem;'>Places to Visit</p>",
            unsafe_allow_html=True,
        )
        place_cols = st.columns(min(len(places), 3))
        for i, place in enumerate(places):
            with place_cols[i % 3]:
                st.markdown(
                    f"""
                    <div style="
                        background: var(--bg-raised);
                        border-radius: 8px;
                        padding: 1.15rem;
                        border-bottom: 2px solid var(--gold-dim);
                        height: 100%;
                    ">
                        <p style="color:var(--gold);font-size:0.8rem;font-weight:600;margin:0 0 0.4rem;">{place.get('name','')}</p>
                        <p style="color:var(--text-2);font-size:0.87rem;line-height:1.6;margin:0;">{place.get('why','')}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def _render_literary_techniques(lesson: dict):
    techniques = lesson.get("literary_techniques", [])
    if not techniques:
        return

    _section_header("03", "Literary Craft")
    st.markdown(
        "<p style='color:var(--text-2);font-size:0.88rem;margin:-0.75rem 0 1.5rem;'>"
        "What the author is doing — and why it opens windows onto the world."
        "</p>",
        unsafe_allow_html=True,
    )

    for tech in techniques:
        name    = tech.get("technique", "")
        example = tech.get("example", "")
        world   = tech.get("world_connection", "")
        initial = name[0].upper() if name else "?"

        st.markdown(
            f"""
            <div style="
                background: var(--bg-surface);
                border-radius: 10px;
                padding: 1.5rem 1.7rem;
                margin-bottom: 1rem;
                position: relative;
                overflow: hidden;
            ">
                <span style="
                    font-family: 'DM Serif Display', serif;
                    font-size: 9rem;
                    color: var(--text-1);
                    opacity: 0.04;
                    position: absolute;
                    right: 0.75rem;
                    top: -1.5rem;
                    line-height: 1;
                    pointer-events: none;
                    user-select: none;
                ">{initial}</span>
                <p style="
                    font-family: 'Space Grotesk', sans-serif;
                    color: var(--gold);
                    font-weight: 600;
                    font-size: 0.95rem;
                    letter-spacing: 0.04em;
                    margin: 0 0 0.7rem;
                    position: relative;
                ">{name}</p>
                <p style="
                    font-family: 'Lora', serif;
                    font-style: italic;
                    font-size: 0.93rem;
                    line-height: 1.7;
                    color: #C8C0B4;
                    margin: 0 0 1rem;
                    border-left: 2px solid var(--rule);
                    padding-left: 1rem;
                    position: relative;
                ">{example}</p>
                <div style="
                    background: var(--bg-raised);
                    border-left: 3px solid var(--gold-dim);
                    border-radius: 0 6px 6px 0;
                    padding: 0.9rem 1rem;
                ">
                    <p style="
                        font-family: 'Space Grotesk', sans-serif;
                        color: var(--text-2);
                        font-size: 0.68rem;
                        text-transform: uppercase;
                        letter-spacing: 0.13em;
                        margin: 0 0 0.35rem;
                    ">In the world today</p>
                    <p style="
                        color: var(--gold);
                        font-size: 0.9rem;
                        line-height: 1.65;
                        margin: 0;
                    ">{world}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_analysis(lesson: dict):
    analysis = lesson.get("analysis", "")
    if not analysis:
        return

    _section_header("04", "Deep Analysis")

    # Pull the first sentence as a pull quote
    first_sentence = ""
    for line in analysis.split("\n"):
        stripped = line.strip().lstrip("#").strip()
        if stripped and not stripped.startswith("*") and len(stripped) > 40:
            first_sentence = stripped
            break

    if first_sentence:
        st.markdown(
            f"""
            <div style="
                border-left: 4px solid var(--gold);
                padding: 0.75rem 1.5rem;
                margin: 0 0 2rem 0;
                max-width: 780px;
            ">
                <p style="
                    font-family: 'Lora', serif;
                    font-size: 1.35rem;
                    font-style: italic;
                    line-height: 1.65;
                    color: #D4CEC6;
                    margin: 0;
                ">{first_sentence}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="prose-body" style="max-width:780px;">',
        unsafe_allow_html=True,
    )
    st.markdown(analysis)
    st.markdown("</div>", unsafe_allow_html=True)


def _render_modern_connections(lesson: dict):
    connections = lesson.get("modern_connections", [])
    if not connections:
        return

    _section_header("05", "Modern Connections")
    st.markdown(
        "<p style='color:var(--text-2);font-size:0.88rem;margin:-0.75rem 0 1.5rem;'>"
        "Where these themes live today — in film, TV, and music."
        "</p>",
        unsafe_allow_html=True,
    )

    type_colours = {
        "film": "var(--terracotta)",
        "tv":   "var(--blue)",
        "song": "var(--sage)",
    }

    for conn in connections:
        ctype      = conn.get("type", "film").lower()
        title      = conn.get("title", "")
        connection = conn.get("connection", "")
        colour     = type_colours.get(ctype, "var(--gold)")

        st.markdown(
            f"""
            <div style="
                background: var(--bg-surface);
                border-radius: 8px;
                padding: 1.2rem 1.4rem;
                margin-bottom: 0.75rem;
                display: flex;
                gap: 1rem;
                align-items: flex-start;
            ">
                <span style="
                    color: {colour};
                    font-family: 'Space Grotesk', sans-serif;
                    font-size: 0.65rem;
                    font-weight: 700;
                    letter-spacing: 0.12em;
                    text-transform: uppercase;
                    border: 1px solid {colour};
                    border-radius: 3px;
                    padding: 3px 8px;
                    margin-top: 3px;
                    flex-shrink: 0;
                    white-space: nowrap;
                ">{ctype}</span>
                <div>
                    <p style="
                        font-family: 'DM Serif Display', serif;
                        font-weight: 400;
                        font-size: 1rem;
                        color: var(--text-1);
                        margin: 0 0 0.4rem;
                        line-height: 1.3;
                    ">{title}</p>
                    <p style="
                        font-family: 'Space Grotesk', sans-serif;
                        color: var(--text-2);
                        font-size: 0.9rem;
                        line-height: 1.65;
                        margin: 0;
                    ">{connection}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_reflective_tasks(lesson: dict):
    tasks = lesson.get("reflective_tasks", [])
    if not tasks:
        return

    _section_header("06", "Reflective Tasks")
    st.markdown(
        "<p style='color:var(--text-2);font-size:0.88rem;font-style:italic;"
        "font-family:Lora,serif;margin:-0.75rem 0 1.5rem;'>"
        "No grades. No right answers. Just you and the page."
        "</p>",
        unsafe_allow_html=True,
    )

    for i, task in enumerate(tasks, 1):
        st.markdown(
            f"""
            <div style="
                background: #F2EDE4;
                border-radius: 8px;
                padding: 1.25rem 1.4rem;
                margin-bottom: 0.75rem;
                display: flex;
                gap: 1.1rem;
                align-items: flex-start;
            ">
                <span style="
                    font-family: 'DM Serif Display', serif;
                    font-size: 1.5rem;
                    color: var(--gold);
                    line-height: 1.1;
                    flex-shrink: 0;
                ">{i}.</span>
                <p style="
                    font-family: 'Lora', serif;
                    font-size: 0.95rem;
                    line-height: 1.7;
                    color: #2a2218;
                    margin: 0;
                    padding-top: 0.15rem;
                ">{task}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _render_discussion_questions(lesson: dict):
    questions = lesson.get("discussion_questions", [])
    if not questions:
        return

    _section_header("07", "Discussion Questions")
    st.markdown(
        "<p style='color:var(--text-2);font-size:0.88rem;margin:-0.75rem 0 1.5rem;'>"
        "Open questions. There are no right answers — only honest ones."
        "</p>",
        unsafe_allow_html=True,
    )

    for question in questions:
        st.markdown(
            f"""
            <div style="
                background: var(--bg-surface);
                border-radius: 8px;
                padding: 1.25rem 1.5rem;
                margin-bottom: 0.65rem;
                border-left: 3px solid var(--gold-dim);
                position: relative;
                overflow: hidden;
            ">
                <span style="
                    font-family: 'DM Serif Display', serif;
                    font-size: 6rem;
                    color: var(--text-1);
                    opacity: 0.05;
                    position: absolute;
                    right: 0.75rem;
                    top: -1rem;
                    line-height: 1;
                    pointer-events: none;
                    user-select: none;
                ">?</span>
                <p style="
                    font-family: 'Space Grotesk', sans-serif;
                    font-size: 0.95rem;
                    line-height: 1.7;
                    color: #DDD6CD;
                    margin: 0;
                    position: relative;
                ">{question}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ═════════════════════════════════════════════════════════════════════════════
# Router
# ═════════════════════════════════════════════════════════════════════════════

if st.session_state["page"] == "home":
    render_home()
else:
    render_lesson()
