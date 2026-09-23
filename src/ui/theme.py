"""Theme configuration, design tokens and custom CSS injection for Streamlit."""

import streamlit as st

# Color Palette Constants
COLOR_PETROLEUM_PRIMARY = "#1A3644"
COLOR_PETROLEUM_DARK = "#0F2537"
COLOR_PETROLEUM_LIGHT = "#2C4C5E"

COLOR_PROGRESS_PURPLE = "#7C3AED"
COLOR_COMPLETED_GREEN = "#10B981"
COLOR_ATTENTION_ORANGE = "#F59E0B"
COLOR_OVERDUE_RED = "#EF4444"


def _initialize_theme_state() -> None:
    """Keep the public theme value and its widget synchronized."""
    st.session_state.setdefault("edutrack_dark_mode", False)
    st.session_state.setdefault(
        "_edutrack_dark_mode_widget", st.session_state["edutrack_dark_mode"]
    )


def render_theme_toggle() -> None:
    """Render the shared theme control at the sidebar position chosen by the shell."""
    _initialize_theme_state()

    def persist_theme() -> None:
        st.session_state["edutrack_dark_mode"] = bool(
            st.session_state["_edutrack_dark_mode_widget"]
        )

    st.toggle(
        "Modo escuro",
        key="_edutrack_dark_mode_widget",
        on_change=persist_theme,
    )


def inject_custom_css() -> None:
    """Inject custom CSS for EduTrack visual identity into Streamlit."""
    _initialize_theme_state()
    dark_mode = bool(st.session_state["edutrack_dark_mode"])

    custom_css = """
    <style>
    /* Design Tokens */
    :root {
        --color-primary: #1A3644;
        --color-primary-dark: #0F2537;
        --color-primary-light: #2C4C5E;
        --color-purple: #7C3AED;
        --color-green: #10B981;
        --color-orange: #F59E0B;
        --color-red: #EF4444;
        --radius-card: 14px;
        --radius-pill: 9999px;
    }

    /* Global Typography & Background Adjustments */
    .stApp {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* Hide only the public repository link and preserve sidebar controls */
    [data-testid="stToolbar"] a[href*="github.com"] {
        display: none !important;
    }

    /* Custom Metric Cards */
    .edutrack-card {
        background-color: var(--background-secondary, #FFFFFF);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: var(--radius-card);
        padding: 1.25rem 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        margin-bottom: 1rem;
    }

    .edutrack-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
    }

    .edutrack-card-title {
        font-size: 0.875rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748B;
        margin-bottom: 0.5rem;
    }

    .edutrack-card-value {
        font-size: 2.25rem;
        font-weight: 700;
        line-height: 1.1;
        color: var(--color-primary);
    }

    .edutrack-card-subtitle {
        font-size: 0.8125rem;
        color: #94A3B8;
        margin-top: 0.35rem;
    }

    /* Status Chip Badges */
    .edutrack-chip {
        display: inline-flex;
        align-items: center;
        padding: 0.25rem 0.75rem;
        border-radius: var(--radius-pill);
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.025em;
        text-transform: uppercase;
    }

    .chip-concluid {
        background-color: rgba(16, 185, 129, 0.15);
        color: #047857;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }

    .chip-pendente {
        background-color: rgba(245, 158, 11, 0.15);
        color: #B45309;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }

    .chip-andamento {
        background-color: rgba(124, 58, 237, 0.15);
        color: #6D28D9;
        border: 1px solid rgba(124, 58, 237, 0.3);
    }

    .chip-atrasada {
        background-color: rgba(239, 68, 68, 0.15);
        color: #B91C1C;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }

    /* Header Banner Styling */
    .edutrack-header-banner {
        background: linear-gradient(135deg, #1A3644 0%, #2C4C5E 60%, #7C3AED 100%);
        color: #FFFFFF;
        padding: 1.75rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 20px -5px rgba(26, 54, 68, 0.3);
    }

    .edutrack-header-title {
        font-size: 1.875rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.025em;
    }

    .edutrack-header-desc {
        font-size: 1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }

    /* Progress bar override */
    .stProgress > div > div > div > div {
        background-color: var(--color-purple) !important;
        border-radius: 9999px;
    }

    /* Sidebar mobile opener: always visible */
    [data-testid="stExpandSidebarButton"] {
        background: #7C3AED !important;
        border: 2px solid #FFFFFF !important;
        border-radius: 0 12px 12px 0 !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.28) !important;
        z-index: 999999 !important;
    }

    [data-testid="stExpandSidebarButton"] button {
        color: #FFFFFF !important;
    }

    [data-testid="stExpandSidebarButton"] svg {
        fill: #FFFFFF !important;
        stroke: #FFFFFF !important;
    }

    [data-testid="stExpandSidebarButton"],
    [data-testid="stExpandSidebarButton"] button,
    [data-testid="stExpandSidebarButton"] span,
    [data-testid="stExpandSidebarButton"] i,
    [data-testid="stExpandSidebarButton"] svg,
    [data-testid="stExpandSidebarButton"] svg path {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
        stroke: #FFFFFF !important;
        opacity: 1 !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    [data-testid="stExpandSidebarButton"]:hover,
    [data-testid="stExpandSidebarButton"]:focus,
    [data-testid="stExpandSidebarButton"]:active {
        background-color: #7C3AED !important;
        color: #FFFFFF !important;
    }

    [data-testid="stExpandSidebarButton"] button {
        min-width: 2.75rem !important;
        min-height: 2.75rem !important;
    }

    /* Responsive Mobile Adjustments (<= 768px / 390px) */
    @media (max-width: 768px) {
        /* Allow columns to stack vertically on small screens */
        [data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
            gap: 0.75rem !important;
            width: 100% !important;
            max-width: 100% !important;
            min-width: 0 !important;
            box-sizing: border-box !important;
        }

        [data-testid="column"] {
            width: 100% !important;
            max-width: 100% !important;
            flex: 1 1 100% !important;
            flex-basis: 100% !important;
            min-width: 0 !important;
            box-sizing: border-box !important;
        }

        /* Adjust mobile container width without hiding content */
        .main .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            width: 100% !important;
            max-width: 100% !important;
            min-width: 0 !important;
            box-sizing: border-box !important;
        }

        .edutrack-header-banner {
            padding: 1.25rem 1rem;
            margin-bottom: 1.25rem;
            width: 100%;
            max-width: 100%;
            min-width: 0;
            box-sizing: border-box;
        }

        .edutrack-header-title {
            font-size: 1.4rem;
        }

        .edutrack-header-desc {
            font-size: 0.875rem;
        }

        .edutrack-card {
            padding: 1rem;
            margin-bottom: 0.5rem;
            width: 100%;
            max-width: 100%;
            min-width: 0;
            box-sizing: border-box;
        }

        .edutrack-card-value {
            font-size: 1.75rem;
        }

        /* Responsive Plotly containers */
        .stPlotlyChart,
        .stPlotlyChart > div,
        .js-plotly-plot,
        .plot-container {
            width: 100% !important;
            max-width: 100% !important;
            min-width: 0 !important;
            box-sizing: border-box !important;
        }
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    if dark_mode:
        st.markdown(
            """
            <style>
            .stApp,
            [data-testid="stAppViewContainer"] {
                background-color: #0B1720;
                color: #E5EDF3;
            }

            [data-testid="stHeader"] {
                background-color: rgba(11, 23, 32, 0.95);
            }

            [data-testid="stHeader"] button,
            [data-testid="stHeader"] svg,
            [data-testid="stHeaderActionElements"] button,
            [data-testid="stHeaderActionElements"] svg {
                color: #F8FAFC !important;
                fill: #F8FAFC !important;
                stroke: #F8FAFC !important;
                opacity: 1 !important;
            }

            [data-testid="stSidebar"] {
                background-color: #102532;
            }

            [data-testid="stSidebar"] p,
            [data-testid="stSidebar"] span,
            [data-testid="stSidebar"] label,
            [data-testid="stSidebar"] h1,
            [data-testid="stSidebar"] h2,
            [data-testid="stSidebar"] h3 {
                color: #E5EDF3;
            }

            [data-testid="stSidebar"] a,
            [data-testid="stSidebar"] a:visited,
            .stApp a[href^="mailto:"],
            .stApp a[href^="mailto:"]:visited {
                color: #F8FAFC !important;
                -webkit-text-fill-color: #F8FAFC !important;
                opacity: 1 !important;
            }

            .stApp p,
            .stApp label,
            .stApp h1,
            .stApp h2,
            .stApp h3 {
                color: #E5EDF3;
            }

            .edutrack-card,
            [data-testid="stMetric"] {
                background-color: #142B39;
                border-color: #2C4C5E;
            }

            .edutrack-card-title,
            .edutrack-card-subtitle {
                color: #B8C7D1;
            }

            .edutrack-card-value {
                color: #F3F7FA;
            }

            [data-testid="stTextInput"] input,
            [data-testid="stTextArea"] textarea,
            [data-testid="stNumberInput"] input,
            [data-baseweb="select"] > div {
                background-color: #142B39 !important;
                color: #F3F7FA !important;
                border-color: #456274 !important;
            }

            .stButton > button,
            .stDownloadButton > button,
            [data-testid="stFormSubmitButton"] > button,
            [data-testid="stSidebar"] .stButton > button {
                background-color: #7C3AED !important;
                color: #F8FAFC !important;
                border: 1px solid #A78BFA !important;
                opacity: 1 !important;
            }

            .stButton > button p,
            .stDownloadButton > button p,
            [data-testid="stFormSubmitButton"] > button p,
            [data-testid="stSidebar"] .stButton > button p {
                color: #F8FAFC !important;
                opacity: 1 !important;
            }

            .stButton > button:hover,
            .stDownloadButton > button:hover,
            [data-testid="stFormSubmitButton"] > button:hover,
            [data-testid="stSidebar"] .stButton > button:hover {
                background-color: #8B5CF6 !important;
                color: #FFFFFF !important;
                border-color: #C4B5FD !important;
            }

            .stButton > button:focus-visible,
            .stDownloadButton > button:focus-visible,
            [data-testid="stFormSubmitButton"] > button:focus-visible {
                outline: 3px solid #A78BFA !important;
                outline-offset: 2px !important;
            }

            .stButton > button:disabled,
            .stDownloadButton > button:disabled,
            [data-testid="stFormSubmitButton"] > button:disabled {
                background-color: #4C3A70 !important;
                color: #DDD6FE !important;
                border-color: #6D5A91 !important;
                opacity: 1 !important;
                cursor: not-allowed !important;
            }

            .stButton > button:disabled p,
            .stDownloadButton > button:disabled p,
            [data-testid="stFormSubmitButton"] > button:disabled p {
                color: #DDD6FE !important;
                opacity: 1 !important;
            }
            [data-testid="stExpandSidebarButton"] {
                background-color: #7C3AED !important;
                border: 2px solid #FFFFFF !important;
                border-radius: 10px !important;
                box-shadow: 0 4px 14px rgba(0, 0, 0, 0.35) !important;
            }

            [data-testid="stExpandSidebarButton"] button,
            [data-testid="stExpandSidebarButton"] svg,
            [data-testid="stExpandSidebarButton"] span {
                color: #FFFFFF !important;
                fill: #FFFFFF !important;
                stroke: #FFFFFF !important;
            }

            </style>
            """,
            unsafe_allow_html=True,
        )
