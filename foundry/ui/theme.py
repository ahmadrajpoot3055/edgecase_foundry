"""Visual system: Minimalist, clean, and modern with Poppins font only."""
from __future__ import annotations

import streamlit as st

POPPINS = "Poppins"
PRIMARY = "#4F46E5"
PRIMARY_HOVER = "#4338CA"
PRIMARY_LIGHT = "#EEF2FF"
TEXT_DARK = "#0F172A"
TEXT_MUTED = "#64748B"
BORDER = "#E2E8F0"
BG_CARD = "#FFFFFF"
BG_APP = "#F8FAFC"

CRITICAL = "#EF4444"
HIGH = "#F97316"
MEDIUM = "#F59E0B"
LOW = "#10B981"

CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&display=swap');

:root {{
  --font-family: '{POPPINS}', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --primary: {PRIMARY};
  --primary-hover: {PRIMARY_HOVER};
  --primary-light: {PRIMARY_LIGHT};
  --text-dark: {TEXT_DARK};
  --text-muted: {TEXT_MUTED};
  --border: {BORDER};
  --bg-card: {BG_CARD};
  --bg-app: {BG_APP};
  --critical: {CRITICAL};
  --high: {HIGH};
  --medium: {MEDIUM};
  --low: {LOW};
}}

/* Poppins for all text. Streamlit's Material icon spans are excluded, otherwise icon
   ligatures render as raw words like "keyboard_double_arrow_left" or "error". */
html, body, .stApp, p, div, input, textarea, button, select, label, h1, h2, h3, h4, h5, h6, summary, table, th, td,
.stApp span:not([data-testid="stIconMaterial"]):not(.material-symbols-rounded):not([class*="material"]) {{
  font-family: var(--font-family) !important;
}}
[data-testid="stIconMaterial"], .material-symbols-rounded {{
  font-family: 'Material Symbols Rounded' !important;
}}

.stApp {{
  background-color: var(--bg-app);
  color: var(--text-dark);
}}

.block-container {{
  padding-top: 1.8rem;
  padding-bottom: 3.5rem;
  max-width: 1400px;
}}

header[data-testid="stHeader"] {{
  background: transparent;
}}

#MainMenu, footer {{
  visibility: hidden;
}}

a {{
  color: var(--primary);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.15s ease;
}}
a:hover {{
  color: var(--primary-hover);
  text-decoration: underline;
}}

/* Masthead: Clean, Minimalist, Modern */
.mast {{
  position: relative;
  padding: 0.5rem 0 2rem;
}}
.mast .tape {{
  display: none;
}}
.mast .badge {{
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.35rem 0.85rem;
  border-radius: 9999px;
  background: var(--primary-light);
  color: var(--primary);
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  margin-bottom: 0.8rem;
  border: 1px solid #C7D2FE;
}}
.mast h1.title {{
  font-family: var(--font-family) !important;
  font-weight: 700;
  font-size: clamp(2.4rem, 5vw, 3.8rem);
  line-height: 1.15;
  margin: 0 0 0.5rem;
  color: var(--text-dark);
  letter-spacing: -0.03em;
}}
.mast h1.title span {{
  display: inline;
}}
.mast h1.title span + span {{
  color: var(--primary);
  margin-left: 0.4rem;
}}
.mast .lede {{
  max-width: 68ch;
  font-size: 1.02rem;
  line-height: 1.6;
  font-weight: 400;
  color: var(--text-muted);
  margin: 0.5rem 0 1rem;
}}
.mast .stamp {{
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: #F1F5F9;
  color: #475569;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 0.5rem 0.9rem;
  font-weight: 500;
  font-size: 0.82rem;
  line-height: 1.4;
  margin-top: 0.2rem;
}}

/* Section Headers */
.sec {{
  display: flex;
  align-items: center;
  gap: 0.85rem;
  margin: 2.2rem 0 1.1rem;
  padding-bottom: 0.6rem;
  border-bottom: 1px solid var(--border);
  background: transparent;
}}
.sec .n {{
  background: var(--primary-light);
  color: var(--primary);
  font-weight: 700;
  font-size: 0.85rem;
  padding: 0.35rem 0.75rem;
  border-radius: 8px;
  border: 1px solid #C7D2FE;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}}
.sec .t {{
  font-weight: 600;
  font-size: 1.3rem;
  color: var(--text-dark);
  letter-spacing: -0.015em;
}}
.sec .h {{
  margin-left: auto;
  font-size: 0.84rem;
  font-weight: 400;
  color: var(--text-muted);
  text-align: right;
}}

/* Form inputs & widgets */
[data-testid="stWidgetLabel"] p {{
  font-weight: 600 !important;
  font-size: 0.88rem !important;
  color: var(--text-dark) !important;
  margin-bottom: 0.35rem !important;
}}
.stTextArea [data-baseweb="textarea"], 
.stTextArea [data-baseweb="base-input"], 
.stTextInput [data-baseweb="input"], 
.stTextInput [data-baseweb="base-input"] {{
  border-radius: 10px !important;
  background: var(--bg-card) !important;
  transition: all 0.15s ease !important;
}}
.stTextArea [data-baseweb="textarea"], 
.stTextInput [data-baseweb="input"] {{
  border: 1px solid var(--border) !important;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.04) !important;
}}
.stTextArea [data-baseweb="textarea"]:focus-within, 
.stTextInput [data-baseweb="input"]:focus-within {{
  box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15) !important;
  border-color: var(--primary) !important;
}}
.stTextArea textarea {{
  font-size: 0.92rem !important;
  line-height: 1.6 !important;
  color: var(--text-dark) !important;
}}
[data-baseweb="select"] > div {{
  border-radius: 10px !important;
  border: 1px solid var(--border) !important;
  background: var(--bg-card) !important;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.04) !important;
}}
[data-baseweb="tag"] {{
  background: var(--primary-light) !important;
  border-radius: 6px !important;
  border: 1px solid #C7D2FE !important;
}}
[data-baseweb="tag"] span {{
  color: var(--primary) !important;
  font-weight: 500 !important;
}}
[data-baseweb="tag"] svg {{
  fill: var(--primary) !important;
}}

/* Buttons */
.stButton > button, .stDownloadButton > button {{
  border-radius: 9px !important;
  border: 1px solid var(--border) !important;
  background: var(--bg-card) !important;
  color: var(--text-dark) !important;
  font-weight: 500 !important;
  font-size: 0.85rem !important;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
  transition: all 0.15s ease !important;
  padding: 0.5rem 0.75rem !important;
  min-height: 2.75rem !important;
  height: auto !important;
  max-width: 100% !important;
  overflow: hidden !important;
}}
.stButton > button p, .stDownloadButton > button p {{
  white-space: normal !important;
  overflow-wrap: break-word !important;
  word-break: normal !important;
  line-height: 1.3 !important;
  text-align: center !important;
  margin: 0 !important;
}}
.hist-meta {{
  color: var(--text-muted) !important;
  font-size: 0.76rem;
}}
.stButton > button:hover:not(:disabled), .stDownloadButton > button:hover:not(:disabled) {{
  background: #F8FAFC !important;
  border-color: #CBD5E1 !important;
  color: var(--primary) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 3px 6px -1px rgba(0, 0, 0, 0.08) !important;
}}
.stButton > button:active:not(:disabled), .stDownloadButton > button:active:not(:disabled) {{
  transform: translateY(0) !important;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
}}
.stButton > button[kind="primary"], .stButton > button[data-testid="stBaseButton-primary"] {{
  background: var(--primary) !important;
  border-color: var(--primary-hover) !important;
  color: #FFFFFF !important;
  font-weight: 600 !important;
  font-size: 0.98rem !important;
  padding: 0.75rem 1.4rem !important;
  box-shadow: 0 4px 10px -1px rgba(79, 70, 229, 0.3) !important;
}}
.stButton > button[kind="primary"]:hover:not(:disabled), .stButton > button[data-testid="stBaseButton-primary"]:hover:not(:disabled) {{
  background: var(--primary-hover) !important;
  color: #FFFFFF !important;
  box-shadow: 0 6px 14px -1px rgba(79, 70, 229, 0.4) !important;
}}
.stButton > button:disabled, .stDownloadButton > button:disabled {{
  background: #F1F5F9 !important;
  border: 1px solid var(--border) !important;
  color: #94A3B8 !important;
  box-shadow: none !important;
  opacity: 0.7 !important;
  cursor: not-allowed !important;
}}
.sample-note {{
  font-size: 0.82rem;
  font-weight: 500;
  color: var(--text-muted);
  margin: 0.6rem 0 0.35rem;
}}
.counter {{
  font-size: 0.78rem;
  font-weight: 500;
  color: var(--text-muted);
  text-align: right;
  margin-top: 0.25rem;
}}
.counter.bad {{
  color: var(--critical);
  font-weight: 600;
}}

/* Rubric card */
.rubric {{
  border: 1px solid var(--border);
  background: var(--bg-card);
  border-radius: 12px;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04);
  overflow: hidden;
}}
.rubric h3 {{
  font-family: var(--font-family) !important;
  font-weight: 600;
  font-size: 1.05rem;
  margin: 0;
  padding: 0.75rem 1rem;
  background: #F8FAFC;
  border-bottom: 1px solid var(--border);
  color: var(--text-dark);
}}
.rubric .formula {{
  padding: 0.55rem 1rem;
  font-weight: 600;
  font-size: 0.82rem;
  color: var(--primary);
  background: #F8FAFC;
  border-bottom: 1px solid var(--border);
}}
.rubric table {{
  border-collapse: collapse;
  width: 100%;
  font-size: 0.78rem;
  line-height: 1.45;
}}
.rubric th, .rubric td {{
  text-align: left;
  vertical-align: top;
  padding: 0.55rem 0.8rem;
  border-bottom: 1px solid #F1F5F9;
}}
.rubric th {{
  background: #F8FAFC;
  color: var(--text-muted);
  font-weight: 600;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}}
.rubric td.lv {{
  font-weight: 700;
  font-size: 0.95rem;
  width: 2.2rem;
  color: var(--text-dark);
  border-right: 1px solid #F1F5F9;
}}
.bands {{
  display: flex;
  border-top: 1px solid var(--border);
}}
.bands span {{
  flex: 1;
  padding: 0.55rem 0.6rem;
  font-size: 0.74rem;
  font-weight: 600;
  text-align: center;
  border-right: 1px solid #F1F5F9;
}}
.bands span:last-child {{
  border-right: 0;
}}

/* Minimalist Risk Bands */
.b-critical {{
  background: #FEF2F2 !important;
  color: #DC2626 !important;
  border: 1px solid #FECACA;
}}
.b-high {{
  background: #FFF7ED !important;
  color: #EA580C !important;
  border: 1px solid #FFEDD5;
}}
.b-medium {{
  background: #FEFCE8 !important;
  color: #CA8A04 !important;
  border: 1px solid #FEF08A;
}}
.b-low {{
  background: #F0FDF4 !important;
  color: #16A34A !important;
  border: 1px solid #DCFCE7;
}}

/* Stats Strip: Clean Metrics KPI Cards */
.strip {{
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin: 1.25rem 0 1.75rem;
  background: transparent;
  border: none;
}}
.strip .c {{
  flex: 1;
  min-width: 130px;
  padding: 0.8rem 1rem;
  border: 1px solid var(--border);
  border-radius: 10px;
  background: var(--bg-card);
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
  font-size: 0.78rem;
  font-weight: 500;
  color: var(--text-muted);
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}}
.strip .c b {{
  font-family: var(--font-family) !important;
  font-weight: 700;
  font-size: 1.65rem;
  line-height: 1.1;
  color: var(--text-dark);
}}
.strip .c.wide {{
  flex: 2;
  min-width: 220px;
  background: var(--primary-light);
  border-color: #C7D2FE;
}}
.strip .c.wide b {{
  font-size: 2rem;
  color: var(--primary);
}}
.strip .c.b-critical {{
  background: #FEF2F2;
  border-color: #FECACA;
}}
.strip .c.b-critical b {{
  color: #DC2626;
}}
.strip .c.b-high {{
  background: #FFF7ED;
  border-color: #FFEDD5;
}}
.strip .c.b-high b {{
  color: #EA580C;
}}
.strip .c.b-medium {{
  background: #FEFCE8;
  border-color: #FEF08A;
}}
.strip .c.b-medium b {{
  color: #CA8A04;
}}

/* System Analysis Card */
.brief {{
  border: 1px solid var(--border);
  background: var(--bg-card);
  border-radius: 12px;
  padding: 1.25rem 1.4rem;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04);
}}
.brief .sum {{
  font-size: 1.02rem;
  font-weight: 500;
  color: var(--text-dark);
  line-height: 1.6;
  margin: 0 0 1rem;
  padding-bottom: 0.85rem;
  border-bottom: 1px solid #F1F5F9;
}}
.brief h4 {{
  font-family: var(--font-family) !important;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--primary);
  background: var(--primary-light);
  border: 1px solid #C7D2FE;
  border-radius: 6px;
  padding: 0.25rem 0.6rem;
  display: inline-block;
  margin: 0.9rem 0 0.35rem;
}}
.brief ul {{
  margin: 0.3rem 0 0.6rem;
  padding-left: 1.25rem;
  font-size: 0.88rem;
  line-height: 1.6;
  color: #334155;
}}
.brief ul.q li::marker {{
  color: #EF4444;
}}

/* Scenario Ledger: Clean Expandable Cards */
details.case {{
  border: 1px solid var(--border);
  background: var(--bg-card);
  border-radius: 10px;
  margin-bottom: 0.75rem;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
  transition: all 0.15s ease;
  overflow: hidden;
}}
details.case:hover {{
  border-color: #CBD5E1;
  box-shadow: 0 3px 6px -1px rgba(0, 0, 0, 0.05);
}}
details.case[open] {{
  border-color: #C7D2FE;
  box-shadow: 0 6px 12px -2px rgba(0, 0, 0, 0.06);
  margin-bottom: 1.25rem;
}}
details.case > summary {{
  list-style: none;
  cursor: pointer;
  display: grid;
  grid-template-columns: 5.5rem 3.8rem 1fr 11rem 5rem;
  align-items: center;
  padding: 0;
  background: var(--bg-card);
  transition: background 0.15s ease;
}}
details.case > summary::-webkit-details-marker {{
  display: none;
}}
details.case > summary > span {{
  padding: 0.8rem 0.95rem;
  border-right: 1px solid #F1F5F9;
  display: flex;
  align-items: center;
}}
details.case > summary > span:last-child {{
  border-right: 0;
}}
details.case > summary:hover {{
  background: #F8FAFC;
}}
details.case > summary:focus-visible {{
  outline: 2px solid var(--primary);
  outline-offset: -2px;
}}
.case .id {{
  font-weight: 700;
  font-size: 0.82rem;
  background: #F1F5F9;
  color: var(--text-muted);
  justify-content: center;
}}
.case .sc {{
  font-weight: 700;
  font-size: 1.15rem;
  justify-content: center;
}}
.case .ttl {{
  font-weight: 600;
  font-size: 0.92rem;
  color: var(--text-dark);
}}
.case .cat {{
  font-size: 0.8rem;
  font-weight: 500;
  color: var(--text-muted);
}}
.case .sl {{
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--text-muted);
  justify-content: center;
  background: #F8FAFC;
}}
.case .body {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  border-top: 1px solid var(--border);
  background: var(--bg-card);
}}
.case .col {{
  padding: 1.25rem 1.4rem;
}}
.case .col + .col {{
  border-left: 1px solid #F1F5F9;
  background: #F8FAFC;
}}
.case h5 {{
  font-family: var(--font-family) !important;
  font-weight: 600;
  font-size: 0.82rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--text-muted);
  margin: 1.1rem 0 0.35rem;
}}
.case h5:first-child {{
  margin-top: 0;
}}
.case p, .case li {{
  font-size: 0.88rem;
  line-height: 1.6;
  color: #334155;
  margin: 0 0 0.4rem;
}}
.case ol {{
  margin: 0.3rem 0 0.6rem;
  padding-left: 1.3rem;
}}
.case .pass, .case .fail {{
  border-radius: 8px;
  padding: 0.65rem 0.85rem;
  margin-top: 0.75rem;
  font-size: 0.85rem;
  line-height: 1.5;
}}
.case .pass {{
  background: #ECFDF5;
  border: 1px solid #A7F3D0;
  color: #065F46;
}}
.case .fail {{
  background: #FFF1F2;
  border: 1px solid #FECDD3;
  color: #9F1239;
}}
.case .pass b {{
  display: block;
  font-size: 0.74rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: #059669;
  margin-bottom: 0.2rem;
  font-weight: 600;
}}
.case .fail b {{
  display: block;
  font-size: 0.74rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: #E11D48;
  margin-bottom: 0.2rem;
  font-weight: 600;
}}
.empty {{
  border: 1px dashed var(--border);
  border-radius: 12px;
  background: var(--bg-card);
  padding: 2.2rem 1.5rem;
  text-align: center;
  color: var(--text-muted);
  font-size: 0.92rem;
  line-height: 1.6;
}}
.shown {{
  font-weight: 600;
  font-size: 0.88rem;
  color: var(--text-dark);
  padding-top: 0.6rem;
}}

/* Sidebar: Clean, Modern, Minimal */
section[data-testid="stSidebar"] {{
  background: #FFFFFF !important;
  border-right: 1px solid var(--border) !important;
}}
section[data-testid="stSidebar"] * {{
  color: #334155;
}}
section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {{
  font-family: var(--font-family) !important;
  font-weight: 600 !important;
  color: var(--text-dark) !important;
  font-size: 1.1rem !important;
  margin-top: 0.5rem;
}}
section[data-testid="stSidebar"] input {{
  color: var(--text-dark) !important;
  background: #FFFFFF !important;
}}
section[data-testid="stSidebar"] .stButton > button {{
  background: #FFFFFF !important;
  color: var(--text-dark) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.04) !important;
  padding: 0.4rem 0.75rem !important;
  font-size: 0.8rem !important;
}}
section[data-testid="stSidebar"] .stButton > button:hover {{
  background: #F8FAFC !important;
  border-color: #CBD5E1 !important;
  color: var(--primary) !important;
}}
section[data-testid="stSidebar"] a {{
  color: var(--primary) !important;
  text-decoration: none !important;
}}
section[data-testid="stSidebar"] a:hover {{
  text-decoration: underline !important;
}}
.hist {{
  border-left: 3px solid var(--primary);
  background: #F8FAFC;
  border-radius: 0 8px 8px 0;
  border-top: 1px solid #F1F5F9;
  border-right: 1px solid #F1F5F9;
  border-bottom: 1px solid #F1F5F9;
  padding: 0.5rem 0.75rem;
  margin-top: 0.75rem;
  font-size: 0.8rem;
  line-height: 1.45;
}}
.hist b {{
  color: var(--text-dark) !important;
  font-weight: 600;
  font-size: 0.86rem;
}}
.keystate {{
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.78rem;
  font-weight: 500;
  color: #15803D;
  background: #F0FDF4;
  border: 1px solid #BBF7D0;
  border-radius: 8px;
  padding: 0.5rem 0.75rem;
  margin-bottom: 0.75rem;
}}
.keystate-warn {{
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.78rem;
  font-weight: 500;
  color: #B45309;
  background: #FFFBEB;
  border: 1px solid #FDE68A;
  border-radius: 8px;
  padding: 0.5rem 0.75rem;
  margin-bottom: 0.75rem;
}}

@media (max-width: 900px) {{
  details.case > summary {{
    grid-template-columns: 4.5rem 3.5rem 1fr;
  }}
  details.case > summary > .cat, details.case > summary > .sl {{
    display: none;
  }}
  .case .body {{
    grid-template-columns: 1fr;
  }}
  .case .col + .col {{
    border-left: 0;
    border-top: 1px solid var(--border);
  }}
}}
@media (prefers-reduced-motion: reduce) {{
  * {{
    transition: none !important;
  }}
}}
"""


def inject() -> None:
    st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)
