import streamlit as st
import utils

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Enlightening English",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Session state ─────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state["page"] = "home"
if "lesson_id" not in st.session_state:
    st.session_state["lesson_id"] = None
if "theme" not in st.session_state:
    st.session_state["theme"] = "light"


# ── Theme-aware CSS ───────────────────────────────────────────────────────────
def _build_css(theme: str) -> str:
    if theme == "dark":
        css_vars = """
            --bg-base:    #0B1826;
            --bg-surface: #0F2035;
            --bg-raised:  #152844;
            --bg-hover:   #1C3258;
            --primary:    #15AEEA;
            --primary-lt: #73CEF2;
            --primary-glow: rgba(21,174,234,0.12);
            --primary-dim:  rgba(21,174,234,0.28);
            --film:  #F07090;
            --tv:    #A78BFA;
            --song:  #34D399;
            --text-1: #E8F4FD;
            --text-2: #7BAECB;
            --text-3: #3F6C88;
            --rule:   #1A3048;
            --task-bg:   #152844;
            --task-text: #E8F4FD;
            --shadow:    0 4px 24px rgba(0,0,0,0.45);
            --shadow-lg: 0 16px 48px rgba(0,0,0,0.65);
        """
    else:
        css_vars = """
            --bg-base:    #FFFFFF;
            --bg-surface: #F4F8FD;
            --bg-raised:  #EBF3FB;
            --bg-hover:   #DCECF8;
            --primary:    #15AEEA;
            --primary-lt: #73CEF2;
            --primary-glow: rgba(21,174,234,0.10);
            --primary-dim:  rgba(21,174,234,0.22);
            --film:  #E8567A;
            --tv:    #8B5CF6;
            --song:  #10B981;
            --text-1: #0D1B2A;
            --text-2: #4A6E8A;
            --text-3: #90AEC0;
            --rule:   #E0EBF5;
            --task-bg:   #EBF3FB;
            --task-text: #0D1B2A;
            --shadow:    0 4px 20px rgba(15,70,120,0.07);
            --shadow-lg: 0 16px 40px rgba(15,70,120,0.14);
        """

    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=Lora:ital,wght@0,400;0,600;1,400;1,600&display=swap');

    :root {{ {css_vars} }}

    #MainMenu, footer, header {{ visibility: hidden; }}
    .stDeployButton {{ display: none; }}
    [data-testid="collapsedControl"] {{ display: none; }}

    html, body,
    [data-testid="stAppViewContainer"],
    [data-testid="stApp"],
    [data-testid="stMain"],
    section[data-testid="stMain"] > div {{
        background-color: var(--bg-base) !important;
        color: var(--text-1);
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}

    .block-container {{
        padding-top: 1.5rem !important;
        padding-bottom: 5rem !important;
        max-width: 1220px;
    }}

    h1, h2, h3 {{
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        color: var(--text-1) !important;
    }}
    p, li, span, div, label {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: var(--text-1);
    }}

    /* ── Buttons ── */
    .stButton > button {{
        background: var(--primary);
        border: none;
        color: #fff !important;
        border-radius: 10px;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 0.88rem;
        font-weight: 600;
        padding: 0.55rem 1.4rem;
        width: 100%;
        transition: all 0.2s ease;
        box-shadow: 0 2px 10px var(--primary-glow);
    }}
    .stButton > button:hover {{
        background: #0D9ACC;
        transform: translateY(-1px);
        box-shadow: 0 6px 20px var(--primary-dim);
    }}

    /* ── Toggle ── */
    [data-testid="stToggleLabel"] {{
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.82rem !important;
        color: var(--text-2) !important;
    }}

    /* ── Lesson card ── */
    .lesson-card {{
        background: var(--bg-surface);
        border-radius: 16px;
        overflow: hidden;
        box-shadow: var(--shadow);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        margin-bottom: 0.5rem;
    }}
    .card-img-wrap {{
        position: relative;
        overflow: hidden;
    }}
    .card-img-wrap img {{
        width: 100%;
        height: 280px;
        object-fit: cover;
        display: block;
        transition: transform 0.4s ease;
    }}
    .card-placeholder {{
        width: 100%;
        height: 280px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--bg-raised);
        color: var(--text-3);
        font-size: 3rem;
        transition: transform 0.4s ease;
    }}
    .card-img-wrap:hover img,
    .card-img-wrap:hover .card-placeholder {{
        transform: scale(1.04);
    }}
    .card-overlay {{
        position: absolute;
        inset: 0;
        background: rgba(10,22,40,0.52);
        display: flex;
        align-items: center;
        justify-content: center;
        opacity: 0;
        transition: opacity 0.3s ease;
        backdrop-filter: blur(2px);
    }}
    .card-img-wrap:hover .card-overlay {{ opacity: 1; }}
    .card-overlay-pill {{
        background: var(--primary);
        color: #fff;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        padding: 0.45rem 1.25rem;
        border-radius: 100px;
    }}

    /* ── Section headers ── */
    .section-hdr {{
        display: flex;
        align-items: center;
        gap: 0.85rem;
        margin: 3rem 0 0.5rem;
    }}
    .section-badge {{
        background: var(--primary-glow);
        color: var(--primary);
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 0.62rem;
        font-weight: 700;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        padding: 3px 10px;
        border-radius: 100px;
        border: 1px solid var(--primary-dim);
        white-space: nowrap;
        flex-shrink: 0;
    }}
    .section-title {{
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        color: var(--text-1) !important;
        margin: 0 !important;
    }}
    .section-rule {{
        flex: 1;
        height: 1px;
        background: var(--rule);
    }}

    /* ── Prose body ── */
    .prose-body p {{
        font-family: 'Lora', serif !important;
        font-size: 1rem !important;
        line-height: 1.85 !important;
        color: var(--text-2) !important;
    }}
    .prose-body h2 {{
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        margin-top: 1.75rem !important;
        color: var(--text-1) !important;
    }}
    .prose-body strong {{
        color: var(--text-1) !important;
        font-weight: 600 !important;
    }}

    /* ── Scrollbar ── */
    ::-webkit-scrollbar {{ width: 5px; }}
    ::-webkit-scrollbar-track {{ background: var(--bg-base); }}
    ::-webkit-scrollbar-thumb {{ background: var(--primary-dim); border-radius: 3px; }}
    </style>
    """


st.markdown(_build_css(st.session_state["theme"]), unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═════════════════════════════════════════════════════════════════════════════

def _section_header(number: str, label: str):
    st.markdown(
        f"""
        <div class="section-hdr">
            <span class="section-badge">{number}</span>
            <h2 class="section-title">{label}</h2>
            <div class="section-rule"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_nav(show_back: bool = False):
    col_action, _, col_toggle = st.columns([2, 7, 1])
    with col_action:
        if show_back:
            if st.button("← Library", key="nav_back"):
                st.session_state["page"] = "home"
                st.rerun()
        else:
            st.markdown(
                "<div style='padding:0.5rem 0;'>"
                "<span style='font-family:\"Plus Jakarta Sans\",sans-serif;"
                "font-size:0.95rem;font-weight:800;color:var(--primary);'>"
                "Enlightening English</span></div>",
                unsafe_allow_html=True,
            )
    with col_toggle:
        is_dark = st.toggle("🌙", value=(st.session_state["theme"] == "dark"), key="dark_toggle")
        if is_dark != (st.session_state["theme"] == "dark"):
            st.session_state["theme"] = "dark" if is_dark else "light"
            st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
# HOME PAGE
# ═════════════════════════════════════════════════════════════════════════════

def render_home():
    _render_nav(show_back=False)

    st.markdown(
        """
        <div style="text-align:center;padding:2.5rem 1rem 0.5rem;">
            <div style="
                display:inline-block;
                background:var(--primary-glow);
                border:1px solid var(--primary-dim);
                color:var(--primary);
                font-family:'Plus Jakarta Sans',sans-serif;
                font-size:0.68rem;font-weight:700;
                letter-spacing:0.18em;text-transform:uppercase;
                padding:4px 16px;border-radius:100px;
                margin-bottom:1.25rem;
            ">English Literature · Language · Life</div>
            <h1 style="
                font-family:'Plus Jakarta Sans',sans-serif !important;
                font-size:3.25rem;font-weight:800 !important;
                line-height:1.15;margin:0 0 1rem;
                color:var(--text-1) !important;
                letter-spacing:-0.025em;
            ">Stories that<br>
            <span style="
                background:linear-gradient(135deg,#15AEEA 0%,#73CEF2 100%);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                background-clip:text;
            ">open the world</span></h1>
            <p style="
                font-family:'Plus Jakarta Sans',sans-serif;
                font-size:1rem;color:var(--text-2);
                max-width:520px;margin:0 auto 1.5rem;
                line-height:1.65;
            ">Deep dives into great works of English literature — exploring craft, context, and why these stories still matter today.</p>
            <div style="
                display:flex;justify-content:center;gap:2.5rem;
                padding:1.25rem 0 2rem;
                border-top:1px solid var(--rule);
                margin-top:1.25rem;
            ">
                <span style="font-size:0.78rem;color:var(--text-3);font-weight:600;">📚 Deep Analysis</span>
                <span style="font-size:0.78rem;color:var(--text-3);font-weight:600;">🌍 World Context</span>
                <span style="font-size:0.78rem;color:var(--text-3);font-weight:600;">🎬 Modern Links</span>
                <span style="font-size:0.78rem;color:var(--text-3);font-weight:600;">✍️ Reflection Tasks</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    lessons = utils.load_all_lessons("data/lessons")

    if not lessons:
        st.markdown(
            "<p style='color:var(--text-2);text-align:center;margin-top:3rem;'>"
            "No lessons found in data/lessons/ — add a .json file to begin.</p>",
            unsafe_allow_html=True,
        )
        return

    st.markdown(
        f"<div style='display:flex;align-items:center;gap:0.75rem;margin:0 0 1.25rem;'>"
        "<span style='font-family:\"Plus Jakarta Sans\",sans-serif;font-size:0.72rem;"
        "font-weight:700;color:var(--text-3);text-transform:uppercase;letter-spacing:0.14em;'>"
        "All Lessons</span>"
        "<div style='flex:1;height:1px;background:var(--rule);'></div>"
        f"<span style='font-size:0.72rem;color:var(--text-3);font-weight:500;'>{len(lessons)} available</span>"
        "</div>",
        unsafe_allow_html=True,
    )

    cols = st.columns(3, gap="large")
    for i, lesson in enumerate(lessons):
        with cols[i % 3]:
            _render_book_card(lesson)


def _render_book_card(lesson: dict):
    cover   = lesson.get("cover_image_url", "")
    title   = lesson.get("title", "Untitled")
    author  = lesson.get("author", "")
    era     = lesson.get("era", "")
    tagline = lesson.get("tagline", "")
    themes  = lesson.get("themes", [])

    theme_chips = "".join(
        f'<span style="display:inline-block;background:var(--primary-glow);'
        f'border:1px solid var(--primary-dim);color:var(--primary);'
        f'font-family:\"Plus Jakarta Sans\",sans-serif;font-size:0.62rem;font-weight:600;'
        f'letter-spacing:0.08em;text-transform:uppercase;border-radius:100px;'
        f'padding:2px 9px;margin:2px 3px 0 0;">{t}</span>'
        for t in themes[:4]
    )

    img_block = (
        f'<div class="card-img-wrap">'
        f'<img src="{cover}" alt="{title}"/>'
        f'<div class="card-overlay"><span class="card-overlay-pill">Open Lesson →</span></div>'
        f'</div>'
        if cover else
        '<div class="card-img-wrap">'
        '<div class="card-placeholder">📖</div>'
        '<div class="card-overlay"><span class="card-overlay-pill">Open Lesson →</span></div>'
        '</div>'
    )

    st.markdown(
        f"""
        <div class="lesson-card">
            {img_block}
            <div style="padding:1.25rem 1.3rem 1.4rem;">
                <p style="
                    font-family:'Plus Jakarta Sans',sans-serif;
                    font-size:0.68rem;font-weight:700;letter-spacing:0.14em;
                    text-transform:uppercase;color:var(--primary);margin:0 0 0.25rem;
                ">{era}</p>
                <h3 style="
                    font-family:'Plus Jakarta Sans',sans-serif !important;
                    font-size:1.15rem;font-weight:700 !important;
                    margin:0 0 0.22rem;line-height:1.3;
                    color:var(--text-1) !important;
                ">{title}</h3>
                <p style="
                    font-family:'Plus Jakarta Sans',sans-serif;
                    margin:0 0 0.65rem;color:var(--text-2);font-size:0.82rem;
                ">{author}</p>
                <p style="
                    font-family:'Lora',serif;
                    margin:0 0 0.9rem;color:var(--text-2);
                    font-size:0.87rem;line-height:1.55;font-style:italic;
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
# LESSON PAGE
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

    _render_nav(show_back=True)
    _render_hero(lesson)
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
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
    theme    = st.session_state.get("theme", "light")

    bg_fade = "#0B1826" if theme == "dark" else "#FFFFFF"

    theme_chips = "".join(
        f'<span style="display:inline-block;background:rgba(21,174,234,0.18);'
        f'border:1px solid rgba(21,174,234,0.35);color:#73CEF2;'
        f'font-family:\"Plus Jakarta Sans\",sans-serif;font-size:0.65rem;font-weight:600;'
        f'letter-spacing:0.1em;text-transform:uppercase;border-radius:100px;'
        f'padding:3px 11px;margin:3px 4px 0 0;">{t}</span>'
        for t in themes
    )

    if hero_url:
        bg = (
            f'background-image: linear-gradient(to bottom, rgba(10,22,40,0.05) 0%, '
            f'rgba(10,22,40,0.72) 55%, {bg_fade} 100%), url("{hero_url}"); '
            f'background-size: cover; background-position: center 30%;'
        )
    else:
        bg = 'background: linear-gradient(160deg, #0F2035 0%, #0B1826 100%);'

    st.markdown(
        f"""
        <div style="
            {bg}
            border-radius: 20px;
            min-height: 480px;
            display: flex;
            flex-direction: column;
            justify-content: flex-end;
            padding: 4rem 2.5rem 2.5rem;
        ">
            <p style="
                font-family:'Plus Jakarta Sans',sans-serif;
                font-size:0.65rem;font-weight:700;
                letter-spacing:0.22em;text-transform:uppercase;
                color:#73CEF2;margin:0 0 0.65rem;
            ">{era}</p>
            <h1 style="
                font-family:'Plus Jakarta Sans',sans-serif !important;
                font-size:3.5rem;font-weight:800 !important;
                margin:0 0 0.4rem;line-height:1.1;
                letter-spacing:-0.025em;
                text-shadow:0 2px 24px rgba(0,0,0,0.7);
                color:#E8F4FD !important;
            ">{title}</h1>
            <p style="
                font-family:'Plus Jakarta Sans',sans-serif;
                font-size:1rem;font-weight:400;
                color:rgba(232,244,253,0.72);margin:0 0 0.75rem;
            ">{author}</p>
            <div style="width:48px;height:2px;background:#15AEEA;margin:0 0 0.85rem;border-radius:2px;"></div>
            <p style="
                font-family:'Lora',serif;font-style:italic;
                font-size:0.97rem;color:rgba(232,244,253,0.58);
                margin:0 0 1.1rem;max-width:580px;line-height:1.65;
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
        "<p style='color:var(--text-3);font-size:0.88rem;margin:-0.25rem 0 1.25rem;'>"
        "The things they never told you in the classroom.</p>",
        unsafe_allow_html=True,
    )

    for detail in details:
        st.markdown(
            f"""
            <div style="
                display:flex;gap:1rem;align-items:flex-start;
                background:var(--bg-surface);
                border-radius:12px;padding:1.1rem 1.3rem;
                margin-bottom:0.6rem;
                border-left:3px solid var(--primary);
            ">
                <span style="color:var(--primary);font-size:1rem;margin-top:2px;flex-shrink:0;">→</span>
                <p style="margin:0;line-height:1.75;color:var(--text-2);font-size:0.95rem;">{detail}</p>
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
            background:var(--bg-surface);
            border-radius:14px;padding:1.6rem 1.8rem;
            margin-bottom:1.5rem;
        ">
            <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.3rem;">
                <span style="font-size:0.9rem;">📍</span>
                <span style="
                    font-family:'Plus Jakarta Sans',sans-serif;
                    color:var(--primary);font-size:0.68rem;font-weight:700;
                    letter-spacing:0.16em;text-transform:uppercase;
                ">Location</span>
            </div>
            <h3 style="
                font-family:'Plus Jakarta Sans',sans-serif !important;
                font-size:1.3rem;font-weight:700 !important;
                margin:0 0 0.75rem;color:var(--text-1) !important;
            ">{location}</h3>
            <p style="
                font-family:'Lora',serif;font-size:0.95rem;
                line-height:1.75;color:var(--text-2);margin:0;
            ">{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if places:
        st.markdown(
            "<p style='color:var(--text-3);font-size:0.68rem;font-weight:700;"
            "letter-spacing:0.16em;text-transform:uppercase;margin:0 0 0.75rem;'>"
            "Places to Visit</p>",
            unsafe_allow_html=True,
        )
        place_cols = st.columns(min(len(places), 3))
        for i, place in enumerate(places):
            with place_cols[i % 3]:
                st.markdown(
                    f"""
                    <div style="
                        background:var(--bg-raised);
                        border-radius:12px;padding:1.15rem;
                        border-bottom:2px solid var(--primary);
                        height:100%;
                    ">
                        <p style="color:var(--primary);font-size:0.82rem;font-weight:700;margin:0 0 0.35rem;">{place.get('name','')}</p>
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
        "<p style='color:var(--text-3);font-size:0.88rem;margin:-0.25rem 0 1.25rem;'>"
        "What the author is doing — and why it opens windows onto the world.</p>",
        unsafe_allow_html=True,
    )

    for tech in techniques:
        name    = tech.get("technique", "")
        example = tech.get("example", "")
        world   = tech.get("world_connection", "")

        st.markdown(
            f"""
            <div style="
                background:var(--bg-surface);
                border-radius:14px;padding:1.5rem 1.7rem;
                margin-bottom:1rem;
            ">
                <p style="
                    font-family:'Plus Jakarta Sans',sans-serif;
                    color:var(--primary);font-weight:700;
                    font-size:0.95rem;letter-spacing:0.02em;
                    margin:0 0 0.75rem;
                ">{name}</p>
                <p style="
                    font-family:'Lora',serif;font-style:italic;
                    font-size:0.93rem;line-height:1.7;
                    color:var(--text-2);
                    margin:0 0 1rem;
                    border-left:2px solid var(--primary-dim);
                    padding-left:1rem;
                ">{example}</p>
                <div style="
                    background:var(--bg-raised);
                    border-left:3px solid var(--primary);
                    border-radius:0 10px 10px 0;
                    padding:0.85rem 1rem;
                ">
                    <p style="
                        font-family:'Plus Jakarta Sans',sans-serif;
                        color:var(--text-3);font-size:0.65rem;
                        text-transform:uppercase;letter-spacing:0.13em;
                        margin:0 0 0.3rem;font-weight:700;
                    ">In the world today</p>
                    <p style="
                        color:var(--text-2);font-size:0.9rem;
                        line-height:1.65;margin:0;
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
                border-left:4px solid var(--primary);
                padding:0.75rem 1.5rem;
                margin:0 0 2rem;
                max-width:780px;
                background:var(--primary-glow);
                border-radius:0 12px 12px 0;
            ">
                <p style="
                    font-family:'Lora',serif;font-size:1.25rem;
                    font-style:italic;line-height:1.65;
                    color:var(--text-1);margin:0;
                ">{first_sentence}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="prose-body" style="max-width:780px;">', unsafe_allow_html=True)
    st.markdown(analysis)
    st.markdown("</div>", unsafe_allow_html=True)


def _render_modern_connections(lesson: dict):
    connections = lesson.get("modern_connections", [])
    if not connections:
        return

    _section_header("05", "Modern Connections")
    st.markdown(
        "<p style='color:var(--text-3);font-size:0.88rem;margin:-0.25rem 0 1.25rem;'>"
        "Where these themes live today — in film, TV, and music.</p>",
        unsafe_allow_html=True,
    )

    for conn in connections:
        ctype      = conn.get("type", "film").lower()
        title      = conn.get("title", "")
        connection = conn.get("connection", "")
        colour     = f"var(--{ctype})" if ctype in ("film", "tv", "song") else "var(--primary)"

        st.markdown(
            f"""
            <div style="
                background:var(--bg-surface);
                border-radius:12px;padding:1.2rem 1.4rem;
                margin-bottom:0.75rem;
                display:flex;gap:1rem;align-items:flex-start;
            ">
                <span style="
                    color:{colour};
                    font-family:'Plus Jakarta Sans',sans-serif;
                    font-size:0.62rem;font-weight:700;
                    letter-spacing:0.12em;text-transform:uppercase;
                    border:1.5px solid {colour};border-radius:100px;
                    padding:3px 10px;margin-top:2px;flex-shrink:0;white-space:nowrap;
                ">{ctype}</span>
                <div>
                    <p style="
                        font-family:'Plus Jakarta Sans',sans-serif;
                        font-weight:700;font-size:1rem;
                        color:var(--text-1);margin:0 0 0.35rem;line-height:1.3;
                    ">{title}</p>
                    <p style="
                        font-family:'Plus Jakarta Sans',sans-serif;
                        color:var(--text-2);font-size:0.9rem;
                        line-height:1.65;margin:0;
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
        "<p style='color:var(--text-3);font-size:0.88rem;font-style:italic;"
        "font-family:Lora,serif;margin:-0.25rem 0 1.25rem;'>"
        "No grades. No right answers. Just you and the page.</p>",
        unsafe_allow_html=True,
    )

    for i, task in enumerate(tasks, 1):
        st.markdown(
            f"""
            <div style="
                background:var(--task-bg);
                border-radius:12px;padding:1.25rem 1.4rem;
                margin-bottom:0.65rem;
                display:flex;gap:1.1rem;align-items:flex-start;
            ">
                <span style="
                    font-family:'Plus Jakarta Sans',sans-serif;
                    font-size:1.1rem;font-weight:800;
                    color:var(--primary);line-height:1.2;flex-shrink:0;
                ">{i}</span>
                <p style="
                    font-family:'Lora',serif;font-size:0.95rem;
                    line-height:1.7;color:var(--task-text);
                    margin:0;padding-top:0.05rem;
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
        "<p style='color:var(--text-3);font-size:0.88rem;margin:-0.25rem 0 1.25rem;'>"
        "Open questions. There are no right answers — only honest ones.</p>",
        unsafe_allow_html=True,
    )

    for question in questions:
        st.markdown(
            f"""
            <div style="
                background:var(--bg-surface);
                border-radius:12px;padding:1.25rem 1.5rem;
                margin-bottom:0.65rem;
                border-left:3px solid var(--primary);
            ">
                <p style="
                    font-family:'Plus Jakarta Sans',sans-serif;
                    font-size:0.95rem;line-height:1.7;
                    color:var(--text-2);margin:0;
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
