from __future__ import annotations

import base64
import html
import io
import json
import random
from pathlib import Path
from typing import Any

import streamlit as st

try:
    from PIL import Image, ImageOps
except Exception:  # Pillow ships with Streamlit, but the app should never crash without it.
    Image = None  # type: ignore[assignment]
    ImageOps = None  # type: ignore[assignment]

BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(
    page_title="Chapter 20 — A Little Universe",
    page_icon="💌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@500;600;700&family=Noto+Sans+Kannada:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,500;1,600&family=Quicksand:wght@400;500;600;700&display=swap');

:root {
    --ink: #3c2940;
    --ink-soft: #5f4860;
    --muted: #755b72;
    --rose: #d77f9f;
    --rose-deep: #a94e72;
    --pink: #f7c9d9;
    --lavender: #cbb4ef;
    --cream: #fffaf2;
    --paper: #fffdf8;
    --gold: #a8752f;
    --gold-bright: #c9984c;
    --gold-soft: #ecd19a;
    --gold-pale: #f7ebd1;
    --shadow: 0 24px 70px -34px rgba(92, 54, 96, 0.45);
    --radius: 30px;
    --serif: "Playfair Display", Georgia, "Times New Roman", serif;
    --sans: "Quicksand", "Segoe UI", system-ui, -apple-system, sans-serif;
    --script: "Caveat", "Segoe Script", cursive;
    --kannada: "Noto Sans Kannada", "Nirmala UI", "Tunga", sans-serif;
}

*,
*::before,
*::after {
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
}

html, body, .stApp {
    font-family: var(--sans);
    color: var(--ink);
}

.stApp {
    background:
        radial-gradient(circle at 8% 8%, rgba(247, 201, 217, 0.55), transparent 40%),
        radial-gradient(circle at 94% 3%, rgba(203, 180, 239, 0.48), transparent 38%),
        radial-gradient(circle at 50% 104%, rgba(236, 209, 154, 0.34), transparent 46%),
        linear-gradient(158deg, #fffaf5 0%, #fdf0f6 32%, #f5efff 66%, #fffaf2 100%);
    background-attachment: fixed;
    overflow-x: hidden;
}

header[data-testid="stHeader"],
#MainMenu,
footer,
[data-testid="stDecoration"],
[data-testid="stToolbar"],
[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}

.block-container {
    position: relative;
    z-index: 2;
    max-width: 1160px;
    padding: 1.4rem 1.25rem 0;
}

.stApp a {
    color: var(--rose-deep);
}

.stApp a:hover {
    color: var(--gold);
}

.stApp ::selection {
    background: rgba(247, 201, 217, 0.8);
    color: var(--ink);
}

/* ---------- Fixed dreamy background ---------- */

.cosmic-bg {
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    overflow: hidden;
}

.cosmic-bg span {
    position: absolute;
    color: rgba(169, 78, 114, 0.24);
    font-size: 1rem;
    animation: drift 14s ease-in-out infinite;
    text-shadow: 0 0 18px rgba(255, 255, 255, 0.9);
}

.cosmic-bg span:nth-child(1)  { left: 4%;  top: 12%;  font-size: 1.5rem; animation-delay: -1s; }
.cosmic-bg span:nth-child(2)  { left: 10%; top: 64%;  color: rgba(168, 117, 47, 0.24); animation-delay: -5s; }
.cosmic-bg span:nth-child(3)  { left: 18%; top: 32%;  font-size: 0.8rem; animation-delay: -9s; }
.cosmic-bg span:nth-child(4)  { left: 27%; top: 82%;  color: rgba(123, 89, 164, 0.22); animation-delay: -3s; }
.cosmic-bg span:nth-child(5)  { left: 37%; top: 8%;   animation-delay: -7s; }
.cosmic-bg span:nth-child(6)  { left: 48%; top: 92%;  font-size: 0.75rem; animation-delay: -11s; }
.cosmic-bg span:nth-child(7)  { left: 58%; top: 18%;  color: rgba(168, 117, 47, 0.22); animation-delay: -4s; }
.cosmic-bg span:nth-child(8)  { left: 67%; top: 72%;  animation-delay: -8s; }
.cosmic-bg span:nth-child(9)  { left: 76%; top: 38%;  font-size: 1.7rem; animation-delay: -2s; }
.cosmic-bg span:nth-child(10) { left: 84%; top: 88%;  color: rgba(123, 89, 164, 0.2); animation-delay: -6s; }
.cosmic-bg span:nth-child(11) { left: 91%; top: 22%;  font-size: 0.85rem; animation-delay: -10s; }
.cosmic-bg span:nth-child(12) { left: 96%; top: 56%;  color: rgba(168, 117, 47, 0.24); animation-delay: -12s; }
.cosmic-bg span:nth-child(13) { left: 31%; top: 52%;  font-size: 0.7rem; animation-delay: -13s; }
.cosmic-bg span:nth-child(14) { left: 72%; top: 6%;   font-size: 1.1rem; animation-delay: -5.5s; }

/* ---------- Shared pieces ---------- */

.glass {
    background: linear-gradient(145deg, rgba(255, 255, 255, 0.74), rgba(255, 255, 255, 0.4));
    border: 1px solid rgba(255, 255, 255, 0.88);
    -webkit-backdrop-filter: blur(18px) saturate(120%);
    backdrop-filter: blur(18px) saturate(120%);
    box-shadow: var(--shadow);
}

.section-anchor {
    scroll-margin-top: 22px;
}

.section-head {
    max-width: 760px;
    margin: 0 auto 1.9rem;
    text-align: center;
}

.eyebrow {
    display: inline-block;
    font-size: 0.69rem;
    font-weight: 700;
    letter-spacing: 0.26em;
    text-transform: uppercase;
    color: #7c5065;
}

.section-title {
    margin: 0.45rem 0 0.7rem;
    font-family: var(--serif);
    font-size: clamp(1.95rem, 4.3vw, 3.15rem);
    font-weight: 600;
    line-height: 1.08;
    letter-spacing: -0.015em;
    color: var(--ink);
}

.section-sub {
    max-width: 640px;
    margin: 0 auto;
    font-size: 0.99rem;
    line-height: 1.7;
    color: var(--ink-soft);
}

.mini-note {
    margin: 0.8rem 0 0;
    font-size: 0.78rem;
    letter-spacing: 0.04em;
    color: #6f4e64;
}

.section-space {
    margin-top: clamp(4rem, 9vw, 7rem);
}

.count-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    margin-top: 1rem;
    padding: 0.4rem 0.85rem;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.62);
    border: 1px solid rgba(168, 117, 47, 0.28);
    color: var(--ink-soft);
    font-size: 0.76rem;
    font-weight: 600;
    letter-spacing: 0.05em;
}

.reveal-up {
    animation: fade-up 0.9s cubic-bezier(0.2, 0.7, 0.2, 1) both;
}

/* ---------- Streamlit widgets ---------- */

.stButton > button,
.stLinkButton > a {
    min-height: 2.9rem;
    padding: 0.78rem 1.55rem;
    border: 1px solid rgba(255, 255, 255, 0.85);
    border-radius: 999px;
    background: linear-gradient(120deg, #f6b7ce 0%, #eaa6c1 42%, #e3b87b 125%);
    color: #3a1f2f !important;
    font-family: var(--sans);
    font-size: 0.92rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    box-shadow: 0 14px 30px -16px rgba(169, 78, 114, 0.75);
    transition: transform 0.25s ease, box-shadow 0.25s ease, filter 0.25s ease;
}

.stButton > button:hover,
.stLinkButton > a:hover {
    transform: translateY(-2px);
    filter: saturate(1.06);
    box-shadow: 0 18px 36px -16px rgba(169, 78, 114, 0.8);
    color: #2e1725 !important;
}

.stButton > button:focus-visible,
.stLinkButton > a:focus-visible {
    outline: 3px solid #7b59a4;
    outline-offset: 3px;
}

.stButton > button[kind="secondary"] {
    background: rgba(255, 253, 248, 0.84);
    border: 1px solid rgba(168, 117, 47, 0.38);
    color: var(--ink) !important;
    box-shadow: 0 10px 25px -18px rgba(92, 54, 96, 0.5);
}

.stTabs [data-baseweb="tab-list"] {
    gap: 0.35rem;
    justify-content: center;
    padding: 0.35rem;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.58);
    border: 1px solid rgba(255, 255, 255, 0.88);
    width: fit-content;
    margin: 0 auto 1rem;
}

.stTabs [data-baseweb="tab"] {
    height: auto;
    padding: 0.55rem 1.15rem;
    border-radius: 999px;
    color: var(--ink-soft);
    font-family: var(--sans);
    font-size: 0.82rem;
    font-weight: 700;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(120deg, rgba(247, 201, 217, 0.9), rgba(236, 209, 154, 0.72)) !important;
    color: var(--ink) !important;
}

.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] {
    display: none;
}

video.stVideo {
    display: block;
    width: min(100%, 430px) !important;
    height: auto !important;
    margin: 0 auto;
    background: #140b1a;
    border-radius: 24px;
    box-shadow: var(--shadow);
}

.stAudio audio {
    width: 100%;
}

[data-testid="stExpander"] {
    margin-top: 1rem;
    border-radius: 18px;
    background: rgba(255, 253, 248, 0.54);
    border: 1px solid rgba(255, 255, 255, 0.85);
}

[data-testid="stExpander"] summary {
    font-family: var(--sans);
    font-weight: 700;
    color: var(--ink-soft);
}

.st-key-welcome_cta {
    max-width: 380px;
    margin: 1.3rem auto 0.25rem;
}

.st-key-video_cta,
.st-key-letter_cta,
.st-key-letter_close {
    max-width: 390px;
    margin: 1.15rem auto 0.3rem;
}

.st-key-finale_controls {
    position: relative;
    z-index: 3;
    width: 100vw !important;
    max-width: 100vw !important;
    margin: -1rem calc(50% - 50vw) 0 !important;
    padding: 1.5rem 1rem 2.7rem;
    background:
        radial-gradient(circle at 50% 0%, rgba(236, 209, 154, 0.14), transparent 55%),
        linear-gradient(180deg, #27132e 0%, #1b0f25 100%);
    text-align: center;
}

.st-key-finale_controls [data-testid="stButton"] {
    display: flex;
    justify-content: center;
}

.st-key-finale_controls .stButton > button {
    min-height: 3rem;
    padding: 0.82rem 1.65rem;
    background: linear-gradient(120deg, #f5dfa8, #d9ad5e 55%, #f3c7d8);
    border: 1px solid rgba(255, 255, 255, 0.55);
    box-shadow: 0 16px 36px -16px rgba(0, 0, 0, 0.6);
    color: #2a1430 !important;
}

.st-key-finale_controls .stButton > button:hover {
    box-shadow: 0 22px 44px -16px rgba(0, 0, 0, 0.65);
    color: #2a1430 !important;
}

.replay-kicker {
    margin: 0 0 0.85rem;
    font-size: 0.66rem;
    font-weight: 700;
    letter-spacing: 0.24em;
    text-transform: uppercase;
    color: rgba(255, 248, 238, 0.72);
}

.st-key-video_panel {
    padding: clamp(1rem, 3.2vw, 2rem);
    border-radius: 34px;
    background: linear-gradient(150deg, rgba(255, 255, 255, 0.68), rgba(255, 247, 251, 0.42));
    border: 1px solid rgba(255, 255, 255, 0.9);
    box-shadow: var(--shadow);
}

.st-key-anthem_panel {
    padding: clamp(1.1rem, 3.5vw, 2.6rem);
    border-radius: 34px;
    background:
        radial-gradient(circle at 12% 12%, rgba(247, 201, 217, 0.45), transparent 38%),
        radial-gradient(circle at 88% 0%, rgba(203, 180, 239, 0.42), transparent 40%),
        linear-gradient(155deg, rgba(255, 253, 248, 0.85), rgba(250, 238, 245, 0.66));
    border: 1px solid rgba(255, 255, 255, 0.92);
    box-shadow: var(--shadow);
}

.st-key-letter_panel {
    border-radius: 34px;
}

/* ---------- Welcome ---------- */

.welcome {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 88vh;
    padding: clamp(2.2rem, 6vw, 4.2rem) clamp(1.1rem, 4vw, 2.5rem);
    border-radius: clamp(26px, 4vw, 46px);
    text-align: center;
    overflow: hidden;
}

.welcome::before {
    content: "";
    position: absolute;
    inset: 8% 10% auto;
    height: 58%;
    background: radial-gradient(circle, rgba(247, 201, 217, 0.62), transparent 68%);
    filter: blur(24px);
    pointer-events: none;
}

.welcome-kicker {
    position: relative;
    z-index: 1;
    margin: 0 0 1rem;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.32em;
    text-transform: uppercase;
    color: #7c5065;
}

.welcome-title {
    position: relative;
    z-index: 1;
    max-width: 760px;
    margin: 0;
    font-family: var(--serif);
    font-size: clamp(1.75rem, 4.4vw, 3.1rem);
    font-weight: 500;
    line-height: 1.22;
    color: var(--ink);
}

.envelope-stage {
    position: relative;
    z-index: 2;
    width: min(330px, 78vw);
    aspect-ratio: 1.5 / 1;
    margin: 2.5rem auto 1.4rem;
    perspective: 900px;
    filter: drop-shadow(0 30px 35px rgba(150, 84, 116, 0.3));
    animation: bob 5.5s ease-in-out infinite;
}

.envelope-stage:hover .env-flap {
    transform: rotateX(32deg);
}

.env-body {
    position: absolute;
    inset: 0;
    overflow: hidden;
    border-radius: 15px;
    background: linear-gradient(160deg, #fde8f0 0%, #f5c9da 58%, #efb2ca 100%);
    border: 1px solid rgba(255, 255, 255, 0.85);
}

.env-body::before {
    content: "";
    position: absolute;
    inset: 0;
    z-index: 2;
    background:
        linear-gradient(135deg, transparent 49.5%, rgba(255, 255, 255, 0.58) 50%, transparent 50.5%),
        linear-gradient(-135deg, transparent 49.5%, rgba(255, 255, 255, 0.58) 50%, transparent 50.5%);
}

.env-letter {
    position: absolute;
    left: 7%;
    right: 7%;
    top: 11%;
    height: 73%;
    z-index: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.1rem;
    border-radius: 8px;
    background:
        repeating-linear-gradient(180deg, rgba(201, 168, 112, 0.12) 0, rgba(201, 168, 112, 0.12) 1px, transparent 1px, transparent 27px),
        #fffdf7;
    box-shadow: 0 8px 24px rgba(126, 70, 96, 0.16);
    color: #a8752f;
}

.env-letter span:first-child {
    font-family: var(--serif);
    font-size: 2.5rem;
    font-weight: 600;
    line-height: 1;
}

.env-letter span:last-child {
    font-family: var(--script);
    font-size: 1.15rem;
    color: #8b657a;
}

.env-flap {
    position: absolute;
    top: 0;
    left: 0;
    z-index: 3;
    width: 100%;
    height: 58%;
    border-radius: 15px 15px 0 0;
    background: linear-gradient(160deg, #fbe0ea 0%, #f2bdd2 100%);
    clip-path: polygon(0 0, 100% 0, 50% 100%);
    transform-origin: top center;
    transition: transform 0.7s cubic-bezier(0.2, 0.7, 0.2, 1);
}

.env-seal {
    position: absolute;
    left: 50%;
    top: 52%;
    z-index: 5;
    display: grid;
    place-items: center;
    width: 62px;
    height: 62px;
    transform: translate(-50%, -50%);
    border-radius: 50%;
    background: radial-gradient(circle at 32% 28%, #f7e7ba, #d4ac62 62%, #a97d36);
    border: 2px solid rgba(255, 255, 255, 0.45);
    box-shadow: 0 6px 16px rgba(105, 66, 40, 0.35), inset 0 2px 4px rgba(255, 255, 255, 0.5);
    font-family: var(--serif);
    font-size: 1.35rem;
    font-weight: 700;
    color: #5b3a2b;
}

.welcome-spark {
    position: absolute;
    z-index: 1;
    color: var(--gold-bright);
    opacity: 0.75;
    animation: twinkle 3.2s ease-in-out infinite;
}

.welcome-spark:nth-of-type(1) { top: 17%; left: 18%; font-size: 1.1rem; }
.welcome-spark:nth-of-type(2) { top: 26%; right: 17%; font-size: 0.8rem; animation-delay: -1.1s; }
.welcome-spark:nth-of-type(3) { bottom: 30%; left: 12%; font-size: 0.9rem; animation-delay: -2s; }
.welcome-spark:nth-of-type(4) { bottom: 22%; right: 13%; font-size: 1.3rem; animation-delay: -0.7s; }

.welcome-hint {
    position: relative;
    z-index: 1;
    margin: 1.1rem 0 0;
    font-family: var(--script);
    font-size: 1.3rem;
    color: #8b657a;
}

/* ---------- Hero ---------- */

.hero {
    position: relative;
    isolation: isolate;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 85vh;
    padding: clamp(2.5rem, 7vw, 5rem) clamp(1.1rem, 4vw, 3rem);
    overflow: hidden;
    border-radius: clamp(26px, 4vw, 46px);
    text-align: center;
    background:
        radial-gradient(circle at 15% 18%, rgba(247, 201, 217, 0.64), transparent 46%),
        radial-gradient(circle at 86% 12%, rgba(203, 180, 239, 0.54), transparent 44%),
        radial-gradient(circle at 50% 102%, rgba(236, 209, 154, 0.35), transparent 48%),
        linear-gradient(150deg, rgba(255, 253, 248, 0.92), rgba(255, 246, 250, 0.74) 45%, rgba(248, 241, 255, 0.84));
    border: 1px solid rgba(255, 255, 255, 0.92);
    box-shadow: var(--shadow);
}

.hero::before {
    content: "";
    position: absolute;
    inset: 0;
    z-index: 0;
    background-image: radial-gradient(rgba(168, 117, 47, 0.22) 1px, transparent 1px);
    background-size: 30px 30px;
    opacity: 0.42;
    -webkit-mask-image: radial-gradient(circle at center, #000 20%, transparent 78%);
    mask-image: radial-gradient(circle at center, #000 20%, transparent 78%);
    pointer-events: none;
}

.hero-age {
    position: absolute;
    top: 50%;
    left: 50%;
    z-index: 0;
    transform: translate(-52%, -55%);
    font-family: var(--serif);
    font-size: clamp(12rem, 35vw, 27rem);
    font-weight: 700;
    line-height: 0.7;
    letter-spacing: -0.07em;
    color: transparent;
    -webkit-text-stroke: 1.5px rgba(168, 117, 47, 0.17);
    pointer-events: none;
    user-select: none;
}

.orbit {
    position: absolute;
    top: 50%;
    left: 50%;
    z-index: 1;
    width: min(78vw, 580px);
    aspect-ratio: 1;
    border-radius: 50%;
    border: 1px dashed rgba(168, 117, 47, 0.34);
    animation: orbit-spin 52s linear infinite;
    pointer-events: none;
}

.orbit--two {
    width: min(60vw, 440px);
    border-style: solid;
    border-color: rgba(150, 112, 188, 0.3);
    animation-direction: reverse;
    animation-duration: 38s;
}

.orbit-dot {
    position: absolute;
    top: -5px;
    left: 50%;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: #d9a84e;
    box-shadow: 0 0 16px rgba(217, 168, 78, 0.9);
}

.orbit--two .orbit-dot {
    top: auto;
    bottom: 12%;
    left: 12%;
    width: 7px;
    height: 7px;
    background: #b99adf;
    box-shadow: 0 0 14px rgba(185, 154, 223, 0.9);
}

.hero-inner {
    position: relative;
    z-index: 3;
    display: flex;
    flex-direction: column;
    align-items: center;
    max-width: 900px;
}

.hero-kicker {
    margin: 0;
    font-size: 0.66rem;
    font-weight: 700;
    letter-spacing: 0.32em;
    text-transform: uppercase;
    color: #7c5065;
}

.hero-title {
    margin: 0.7rem 0 0;
    font-family: var(--serif);
    font-weight: 600;
    line-height: 1.02;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--ink);
}

.hero-title-line {
    display: block;
    font-size: clamp(1.35rem, 3.7vw, 2.6rem);
    letter-spacing: 0.1em;
}

.hero-name {
    display: block;
    margin-top: 0.2rem;
    font-family: var(--script);
    font-size: clamp(3.2rem, 11vw, 7rem);
    font-weight: 700;
    line-height: 0.98;
    letter-spacing: 0;
    text-transform: none;
    background: linear-gradient(115deg, #8c5c22 8%, #c9984c 48%, #9b5a6f 95%);
    -webkit-background-clip: text;
    background-clip: text;
    color: #8c5c22;
    -webkit-text-fill-color: transparent;
    filter: drop-shadow(0 5px 16px rgba(168, 117, 47, 0.18));
}

.hero-bang {
    -webkit-text-fill-color: #9b5a6f;
    color: #9b5a6f;
}

.hero-sub {
    max-width: 560px;
    margin: 1rem auto 0;
    font-size: clamp(0.92rem, 1.9vw, 1.08rem);
    line-height: 1.65;
    color: var(--ink-soft);
}

.hero-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem;
    justify-content: center;
    margin-top: 1.3rem;
}

.chip {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.4rem 0.85rem;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.66);
    border: 1px solid rgba(168, 117, 47, 0.32);
    color: #6b4c5d;
    font-size: 0.76rem;
    font-weight: 600;
    letter-spacing: 0.04em;
}

.hero-nav {
    display: flex;
    flex-wrap: wrap;
    gap: 0.2rem;
    justify-content: center;
    margin-top: 1.7rem;
}

.hero-nav a {
    padding: 0.42rem 0.7rem;
    border: 1px solid transparent;
    border-radius: 999px;
    color: #5d4459;
    font-size: 0.76rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    text-decoration: none;
    transition: background 0.25s ease, border-color 0.25s ease, transform 0.25s ease;
}

.hero-nav a:hover {
    background: rgba(255, 255, 255, 0.72);
    border-color: rgba(168, 117, 47, 0.32);
    transform: translateY(-1px);
}

.scroll-cue {
    display: inline-flex;
    flex-direction: column;
    align-items: center;
    gap: 0.25rem;
    margin-top: 2rem;
    color: #8b657a;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.22em;
    text-transform: uppercase;
}

.scroll-cue span:last-child {
    font-size: 1.15rem;
    letter-spacing: 0;
    animation: bob 2.2s ease-in-out infinite;
}

.confetti {
    position: absolute;
    inset: 0;
    z-index: 4;
    pointer-events: none;
    overflow: hidden;
}

.confetti-piece {
    position: absolute;
    top: -12%;
    left: var(--left);
    width: var(--size);
    height: calc(var(--size) * 0.5);
    border-radius: var(--round);
    background: var(--color);
    opacity: 0.92;
    animation: confetti-fall var(--duration) cubic-bezier(0.3, 0.6, 0.4, 1) var(--delay) forwards;
}

/* ---------- Spotlight ---------- */

.spotlight {
    display: grid;
    grid-template-columns: minmax(0, 1.15fr) minmax(0, 0.85fr);
    margin-top: 1.8rem;
    overflow: hidden;
    border-radius: 30px;
    background: rgba(255, 253, 248, 0.74);
    border: 1px solid rgba(255, 255, 255, 0.9);
    box-shadow: var(--shadow);
}

.spotlight-media {
    position: relative;
    min-height: 380px;
    background: #f4e8f1;
}

.spotlight-media img {
    display: block;
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.spotlight-media::after {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, transparent 72%, rgba(255, 253, 248, 0.22));
    pointer-events: none;
}

.spotlight-copy {
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: clamp(1.5rem, 3.6vw, 3rem);
}

.spotlight-label {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.24em;
    text-transform: uppercase;
    color: #7b4f1c;
}

.spotlight-quote {
    margin: 0.8rem 0 0.9rem;
    font-family: var(--serif);
    font-style: italic;
    font-size: clamp(1.55rem, 3.1vw, 2.35rem);
    line-height: 1.24;
    color: var(--ink);
}

.spotlight-note {
    margin: 0;
    max-width: 34ch;
    font-size: 0.86rem;
    line-height: 1.65;
    color: var(--muted);
}

.spotlight-placeholder {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 2rem;
    text-align: center;
    background:
        radial-gradient(circle at 30% 20%, rgba(255, 255, 255, 0.85), transparent 45%),
        linear-gradient(145deg, #fbeaf2, #eee3fb 62%, #fbf1dc);
}

.spotlight-placeholder .sun {
    font-size: 3.4rem;
    filter: drop-shadow(0 8px 20px rgba(168, 117, 47, 0.25));
}

.spotlight-placeholder strong {
    font-family: var(--serif);
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--ink);
}

.spotlight-placeholder small {
    max-width: 30ch;
    font-size: 0.78rem;
    line-height: 1.55;
    color: var(--muted);
}

/* ---------- Scrapbook gallery ---------- */

.scrapbook {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(225px, 1fr));
    gap: clamp(1.1rem, 2.5vw, 1.8rem);
    align-items: start;
    margin-top: 2rem;
}

.photo-card {
    position: relative;
    margin: 0;
    padding: 10px 10px 0;
    border-radius: 18px;
    background: #fffdf9;
    box-shadow: 0 20px 44px -28px rgba(97, 59, 92, 0.6);
    transform: rotate(var(--tilt, 0deg));
    transition: transform 0.45s cubic-bezier(0.2, 0.7, 0.2, 1), box-shadow 0.45s ease;
}

.photo-card.wide {
    grid-column: span 2;
}

.photo-card::before {
    content: "";
    position: absolute;
    top: -9px;
    left: 50%;
    z-index: 2;
    width: 74px;
    height: 20px;
    transform: translateX(-50%) rotate(-2deg);
    background: rgba(247, 201, 217, 0.68);
    border-left: 1px dashed rgba(255, 255, 255, 0.8);
    border-right: 1px dashed rgba(255, 255, 255, 0.8);
    box-shadow: 0 2px 6px rgba(134, 84, 110, 0.12);
}

.photo-card:nth-child(4n + 1) { --tilt: -1.7deg; }
.photo-card:nth-child(4n + 2) { --tilt: 1.2deg; }
.photo-card:nth-child(4n + 3) { --tilt: -0.8deg; }
.photo-card:nth-child(4n + 4) { --tilt: 1.9deg; }

.photo-card:hover {
    z-index: 3;
    transform: rotate(0deg) translateY(-7px);
    box-shadow: 0 30px 58px -26px rgba(97, 59, 92, 0.56);
}

.photo-card img {
    display: block;
    width: 100%;
    height: 265px;
    border-radius: 11px;
    object-fit: cover;
    background: #f5e9f1;
}

.photo-card.wide img {
    height: 300px;
}

.photo-card figcaption {
    padding: 0.65rem 0.45rem 0.8rem;
    font-family: var(--script);
    font-size: 1.32rem;
    line-height: 1.12;
    color: #56404f;
    text-align: center;
}

.photo-empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.45rem;
    height: 265px;
    padding: 1.2rem;
    border: 1.5px dashed rgba(154, 103, 136, 0.38);
    border-radius: 11px;
    background:
        radial-gradient(circle at 25% 20%, rgba(255, 255, 255, 0.85), transparent 45%),
        linear-gradient(145deg, #fbeaf2, #f0e6fa 62%, #fbf1dc);
    text-align: center;
}

.photo-empty .empty-emoji {
    font-size: 2.4rem;
}

.photo-empty .empty-title {
    font-family: var(--serif);
    font-size: 1.02rem;
    font-weight: 600;
    color: var(--ink);
}

.photo-empty .empty-note {
    max-width: 24ch;
    font-size: 0.72rem;
    line-height: 1.5;
    color: var(--muted);
}

/* ---------- Video ---------- */

.video-poster {
    position: relative;
    aspect-ratio: 16 / 9;
    overflow: hidden;
    border-radius: 26px;
    background:
        radial-gradient(circle at 78% 22%, rgba(236, 209, 154, 0.38), transparent 28%),
        radial-gradient(circle at 18% 82%, rgba(247, 201, 217, 0.32), transparent 34%),
        linear-gradient(145deg, #24132d 0%, #432142 48%, #1f1029 100%);
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 30px 70px -34px rgba(45, 19, 48, 0.8);
}

.poster-img {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.video-veil {
    position: absolute;
    inset: 0;
    background:
        linear-gradient(180deg, rgba(24, 12, 30, 0.34) 0%, transparent 38%, rgba(24, 12, 30, 0.78) 100%),
        radial-gradient(circle at 50% 45%, transparent 20%, rgba(24, 12, 30, 0.3) 78%);
}

.poster-content {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: clamp(1.1rem, 3vw, 2rem);
    color: #fff8ee;
}

.poster-top {
    display: flex;
    flex-wrap: wrap;
    gap: 0.55rem;
    align-items: center;
    justify-content: space-between;
}

.poster-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.35rem 0.7rem;
    border-radius: 999px;
    background: rgba(255, 248, 238, 0.14);
    border: 1px solid rgba(255, 248, 238, 0.3);
    -webkit-backdrop-filter: blur(8px);
    backdrop-filter: blur(8px);
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
}

.poster-genre {
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: rgba(255, 248, 238, 0.68);
}

.poster-bottom {
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 1rem;
    align-items: end;
}

.poster-play {
    display: grid;
    place-items: center;
    width: clamp(58px, 10vw, 82px);
    aspect-ratio: 1;
    border-radius: 50%;
    background: rgba(255, 248, 238, 0.16);
    border: 1px solid rgba(255, 248, 238, 0.55);
    -webkit-backdrop-filter: blur(8px);
    backdrop-filter: blur(8px);
    box-shadow: 0 0 0 8px rgba(255, 248, 238, 0.06), 0 0 38px rgba(236, 209, 154, 0.25);
    font-size: clamp(1.1rem, 2.5vw, 1.5rem);
    color: #fff8ee;
    animation: play-glow 4.5s ease-in-out infinite;
}

.poster-title {
    margin: 0;
    font-family: var(--serif);
    font-size: clamp(1.45rem, 4vw, 2.7rem);
    font-weight: 600;
    line-height: 1.04;
    letter-spacing: -0.01em;
}

.poster-sub {
    max-width: 52ch;
    margin: 0.4rem 0 0;
    font-size: clamp(0.76rem, 1.6vw, 0.9rem);
    line-height: 1.55;
    color: rgba(255, 248, 238, 0.82);
}

.video-missing .poster-play {
    animation: none;
    border-style: dashed;
    font-size: 1.3rem;
}

.video-missing .poster-sub {
    color: #f3d9ae;
}

.mini-label {
    margin: 1.2rem 0 0.35rem;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #94677e;
}

/* ---------- Anthem / lyrics ---------- */

.anthem-meta {
    margin: 0 0 1.1rem;
    text-align: center;
}

.anthem-title {
    margin: 0;
    font-family: var(--serif);
    font-size: clamp(1.3rem, 2.8vw, 1.8rem);
    font-weight: 600;
    color: var(--ink);
}

.anthem-artist {
    margin: 0.25rem 0 0;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #7c5065;
}

.anthem-intro {
    max-width: 620px;
    margin: 0 auto 1.4rem;
    font-size: 0.9rem;
    line-height: 1.7;
    text-align: center;
    color: var(--ink-soft);
}

.lyrics {
    max-width: 740px;
    margin: 0 auto;
    padding: 0.6rem 0 1.3rem;
    text-align: center;
}

.lyric-stanza {
    margin: 1.15rem 0;
}

.lyric-line {
    margin: 0.2rem 0;
    font-family: var(--kannada);
    font-size: clamp(1.18rem, 2.8vw, 1.7rem);
    font-weight: 500;
    line-height: 1.85;
    color: var(--ink);
}

.lyrics.translit .lyric-line {
    font-family: var(--serif);
    font-style: italic;
    font-size: clamp(1.05rem, 2.3vw, 1.4rem);
    line-height: 1.7;
}

.chorus-box {
    position: relative;
    margin: 1.3rem 0;
    padding: 1.3rem 1rem 1rem;
    overflow: hidden;
    border-radius: 24px;
    background:
        radial-gradient(circle at 15% 10%, rgba(255, 255, 255, 0.72), transparent 40%),
        linear-gradient(135deg, rgba(255, 240, 203, 0.7), rgba(247, 201, 217, 0.55));
    border: 1px solid rgba(168, 117, 47, 0.42);
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.85), 0 14px 34px -26px rgba(140, 84, 60, 0.55);
    animation: soft-glow 6s ease-in-out infinite;
}

.chorus-box::before,
.chorus-box::after {
    content: "♪";
    position: absolute;
    color: rgba(168, 117, 47, 0.28);
    font-family: var(--serif);
    font-size: 1.7rem;
    animation: note-float 5s ease-in-out infinite;
}

.chorus-box::before {
    top: 12px;
    left: 14px;
}

.chorus-box::after {
    right: 16px;
    bottom: 12px;
    animation-delay: -2.2s;
}

.chorus-label {
    display: inline-block;
    margin-bottom: 0.35rem;
    font-size: 0.58rem;
    font-weight: 700;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: #6f4716;
}

.chorus-box .lyric-line {
    position: relative;
    z-index: 1;
    color: #4b2f3c;
}

.lyrics-empty {
    padding: 1.5rem;
    border: 1px dashed rgba(154, 103, 136, 0.4);
    border-radius: 20px;
    color: var(--muted);
    font-size: 0.88rem;
    line-height: 1.65;
    text-align: center;
}

/* ---------- Reasons ---------- */

.reasons-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 0.85rem;
}

.reason-card {
    position: relative;
    min-height: 154px;
    padding: 1rem 1rem 0.95rem;
    overflow: hidden;
    border-radius: 20px;
    background: linear-gradient(150deg, rgba(255, 255, 255, 0.86), rgba(252, 232, 240, 0.6));
    border: 1px solid rgba(255, 255, 255, 0.92);
    box-shadow: 0 14px 32px -24px rgba(120, 70, 120, 0.68);
    transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease, background 0.3s ease;
}

.reason-card:nth-child(3n + 2) {
    background: linear-gradient(150deg, rgba(255, 253, 247, 0.9), rgba(245, 236, 255, 0.66));
}

.reason-card:nth-child(3n + 3) {
    background: linear-gradient(150deg, rgba(255, 254, 249, 0.9), rgba(251, 240, 211, 0.58));
}

.reason-card summary {
    display: flex;
    flex-direction: column;
    gap: 0.45rem;
    align-items: flex-start;
    list-style: none;
    cursor: pointer;
    outline: none;
}

.reason-card summary::-webkit-details-marker {
    display: none;
}

.reason-card summary:focus-visible {
    border-radius: 10px;
    outline: 3px solid #7b59a4;
    outline-offset: 5px;
}

.reason-num {
    font-family: var(--serif);
    font-size: 1.9rem;
    font-weight: 600;
    line-height: 1;
    color: #b07a8f;
}

.reason-hint {
    font-size: 0.58rem;
    font-weight: 700;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #755b72;
}

.reason-heart {
    position: absolute;
    top: 0.8rem;
    right: 0.9rem;
    color: rgba(169, 78, 114, 0.45);
    font-size: 0.95rem;
    transition: transform 0.3s ease, color 0.3s ease;
}

.reason-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 20px 40px -24px rgba(120, 70, 120, 0.65);
}

.reason-card[open] {
    border-color: rgba(168, 117, 47, 0.5);
    background: linear-gradient(150deg, #fffaf1, #f8e4ee);
    transform: translateY(-2px);
    box-shadow: 0 22px 44px -24px rgba(120, 70, 120, 0.6);
}

.reason-card[open] .reason-heart {
    transform: scale(1.2) rotate(-8deg);
    color: #a94e72;
}

.reason-text {
    margin: 0.7rem 0 0;
    font-size: 0.88rem;
    line-height: 1.55;
    color: #4b3448;
    animation: fade-up 0.4s ease both;
}

/* ---------- Timeline ---------- */

.timeline {
    position: relative;
    max-width: 900px;
    margin: 2.2rem auto 0;
    padding: 0.4rem 0;
}

.timeline::before {
    content: "";
    position: absolute;
    top: 0;
    bottom: 0;
    left: 50%;
    width: 2px;
    transform: translateX(-50%);
    background: linear-gradient(180deg, rgba(236, 209, 154, 0.2), rgba(168, 117, 47, 0.65) 18%, rgba(203, 180, 239, 0.7) 72%, rgba(236, 209, 154, 0.1));
}

.timeline-item {
    position: relative;
    width: 50%;
    padding: 0 2.7rem 2rem 0;
}

.timeline-item:nth-child(even) {
    margin-left: 50%;
    padding: 0 0 2rem 2.7rem;
}

.timeline-dot {
    position: absolute;
    top: 0.5rem;
    right: -20px;
    z-index: 2;
    display: grid;
    place-items: center;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: linear-gradient(145deg, #fffaf1, #f7e6f0);
    border: 1px solid rgba(168, 117, 47, 0.45);
    box-shadow: 0 6px 18px rgba(126, 70, 96, 0.2);
    font-size: 1.1rem;
}

.timeline-item:nth-child(even) .timeline-dot {
    right: auto;
    left: -20px;
}

.timeline-card {
    padding: 1.15rem 1.2rem 1.2rem;
    border-radius: 20px;
    background: rgba(255, 253, 248, 0.78);
    border: 1px solid rgba(255, 255, 255, 0.9);
    box-shadow: 0 16px 36px -28px rgba(97, 59, 92, 0.62);
}

.timeline-date {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.25rem 0.65rem;
    border-radius: 999px;
    background: rgba(247, 201, 217, 0.4);
    border: 1px solid rgba(168, 117, 47, 0.24);
    color: #6f4716;
    font-size: 0.61rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
}

.timeline-title {
    margin: 0.55rem 0 0.4rem;
    font-family: var(--serif);
    font-size: 1.25rem;
    font-weight: 600;
    line-height: 1.22;
    color: var(--ink);
}

.timeline-text {
    margin: 0;
    font-size: 0.85rem;
    line-height: 1.65;
    color: var(--ink-soft);
}

.one-more {
    position: relative;
    max-width: 640px;
    margin: 1.2rem auto 0;
    padding: 1.5rem 1.6rem;
    border: 1.5px dashed rgba(168, 117, 47, 0.48);
    border-radius: 24px;
    background: linear-gradient(145deg, rgba(255, 251, 243, 0.85), rgba(250, 236, 244, 0.6));
    text-align: center;
}

.one-more .sun {
    display: inline-block;
    margin-bottom: 0.25rem;
    font-size: 1.8rem;
    animation: bob 4s ease-in-out infinite;
}

.one-more h3 {
    margin: 0 0 0.45rem;
    font-family: var(--serif);
    font-size: 1.35rem;
    font-weight: 600;
    color: var(--ink);
}

.one-more p {
    margin: 0;
    font-size: 0.86rem;
    line-height: 1.7;
    color: var(--ink-soft);
}

/* ---------- Letter ---------- */

.letter-closed {
    position: relative;
    max-width: 760px;
    margin: 0 auto;
    padding: clamp(2rem, 5vw, 3.8rem) clamp(1.2rem, 4vw, 3rem);
    overflow: hidden;
    border: 1.5px dashed rgba(168, 117, 47, 0.5);
    border-radius: 32px;
    background:
        radial-gradient(circle at 20% 10%, rgba(255, 255, 255, 0.8), transparent 45%),
        linear-gradient(145deg, rgba(255, 252, 246, 0.9), rgba(247, 226, 238, 0.62));
    text-align: center;
    box-shadow: var(--shadow);
}

.letter-wax {
    display: grid;
    place-items: center;
    width: 74px;
    height: 74px;
    margin: 0 auto 1rem;
    border-radius: 50%;
    background: radial-gradient(circle at 32% 28%, #e8b7c7, #b65f7f 62%, #8f3f5e);
    border: 2px solid rgba(255, 255, 255, 0.38);
    box-shadow: 0 8px 22px rgba(126, 62, 88, 0.32), inset 0 2px 5px rgba(255, 255, 255, 0.35);
    font-size: 1.6rem;
}

.letter-closed h3 {
    margin: 0 0 0.5rem;
    font-family: var(--serif);
    font-size: clamp(1.35rem, 3vw, 1.85rem);
    font-weight: 600;
    color: var(--ink);
}

.letter-closed p {
    max-width: 46ch;
    margin: 0 auto;
    font-size: 0.86rem;
    line-height: 1.7;
    color: var(--ink-soft);
}

.letter-paper {
    position: relative;
    max-width: 700px;
    margin: 0 auto;
    padding: clamp(1.6rem, 5vw, 3.4rem);
    border-radius: 10px;
    background:
        repeating-linear-gradient(180deg, transparent 0, transparent 39px, rgba(201, 168, 112, 0.09) 39px, rgba(201, 168, 112, 0.09) 40px),
        linear-gradient(180deg, #fffdf5, #fff9ef);
    border: 1px solid rgba(168, 117, 47, 0.32);
    box-shadow: 0 36px 80px -34px rgba(96, 60, 85, 0.5);
    animation: letter-open 0.8s cubic-bezier(0.2, 0.7, 0.2, 1) both;
}

.letter-paper::before {
    content: "";
    position: absolute;
    inset: 13px;
    border: 1px solid rgba(168, 117, 47, 0.22);
    border-radius: 4px;
    pointer-events: none;
}

.letter-paper::after {
    content: "🌻";
    position: absolute;
    top: -17px;
    right: 8%;
    font-size: 2rem;
    transform: rotate(12deg);
    filter: drop-shadow(0 5px 10px rgba(96, 60, 85, 0.2));
}

.letter-salutation {
    margin: 0 0 1.1rem;
    font-family: var(--script);
    font-size: clamp(1.8rem, 4vw, 2.5rem);
    font-weight: 600;
    color: #6f4154;
}

.letter-body p {
    margin: 0 0 1rem;
    font-family: var(--script);
    font-size: clamp(1.22rem, 2.4vw, 1.48rem);
    line-height: 1.68;
    color: #3f2f43;
    opacity: 0;
    animation: fade-up 0.7s ease forwards;
    animation-delay: calc(var(--i) * 0.1s);
}

.letter-signoff {
    margin-top: 1.5rem;
    font-family: var(--script);
    font-size: clamp(1.25rem, 2.6vw, 1.55rem);
    line-height: 1.45;
    color: #5f4860;
}

.letter-signature {
    margin-top: 0.15rem;
    font-family: var(--script);
    font-size: clamp(1.7rem, 3.8vw, 2.35rem);
    font-weight: 600;
    color: #8c5c22;
}

/* ---------- Wish wall ---------- */

.wish-wall {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(235px, 1fr));
    gap: 1rem;
    align-items: start;
}

.wish-card {
    position: relative;
    padding: 1.2rem 1.25rem 1.1rem;
    border-radius: 20px 20px 20px 5px;
    background: rgba(255, 253, 248, 0.82);
    border: 1px solid rgba(255, 255, 255, 0.92);
    box-shadow: 0 16px 34px -28px rgba(97, 59, 92, 0.6);
    transform: rotate(var(--tilt, 0deg));
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.wish-card:nth-child(3n + 1) { --tilt: -1.1deg; }
.wish-card:nth-child(3n + 2) { --tilt: 1deg; }
.wish-card:nth-child(3n + 3) { --tilt: -0.4deg; }

.wish-card:hover {
    transform: rotate(0deg) translateY(-3px);
    box-shadow: 0 22px 44px -28px rgba(97, 59, 92, 0.6);
}

.wish-quote {
    position: absolute;
    top: 0.5rem;
    right: 0.85rem;
    font-family: var(--serif);
    font-size: 2.6rem;
    line-height: 1;
    color: rgba(169, 78, 114, 0.18);
}

.wish-card p {
    margin: 0 0 0.85rem;
    font-family: var(--serif);
    font-style: italic;
    font-size: 0.98rem;
    line-height: 1.6;
    color: var(--ink);
}

.wish-from {
    display: inline-block;
    font-size: 0.61rem;
    font-weight: 700;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #7c5065;
}

.wish-empty {
    max-width: 640px;
    margin: 0 auto;
    padding: 1.5rem;
    border: 1px dashed rgba(154, 103, 136, 0.4);
    border-radius: 20px;
    text-align: center;
    color: var(--muted);
    font-size: 0.88rem;
}

/* ---------- Finale ---------- */

.finale {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100vw;
    min-height: 92vh;
    margin: clamp(4rem, 9vw, 7rem) calc(50% - 50vw) 0;
    padding: clamp(3rem, 8vw, 5rem) clamp(1.2rem, 4vw, 2rem);
    overflow: hidden;
    background:
        radial-gradient(circle at 18% 16%, rgba(201, 152, 76, 0.25), transparent 38%),
        radial-gradient(circle at 82% 24%, rgba(233, 138, 168, 0.23), transparent 42%),
        radial-gradient(circle at 52% 94%, rgba(139, 102, 180, 0.3), transparent 48%),
        linear-gradient(155deg, #1b0f25 0%, #3a1c3e 46%, #27132e 100%);
    color: #fff8ee;
    text-align: center;
}

.finale::before {
    content: "";
    position: absolute;
    inset: 0;
    background-image:
        radial-gradient(rgba(255, 248, 238, 0.55) 1px, transparent 1px),
        radial-gradient(rgba(236, 209, 154, 0.35) 1px, transparent 1px);
    background-size: 110px 110px, 170px 170px;
    background-position: 12px 18px, 60px 80px;
    opacity: 0.3;
    -webkit-mask-image: radial-gradient(circle at center, #000 18%, transparent 76%);
    mask-image: radial-gradient(circle at center, #000 18%, transparent 76%);
    pointer-events: none;
}

.finale-content {
    position: relative;
    z-index: 3;
    max-width: 880px;
}

.finale-sigil {
    display: grid;
    place-items: center;
    width: 72px;
    height: 72px;
    margin: 0 auto 1.2rem;
    border-radius: 50%;
    border: 1px solid rgba(236, 209, 154, 0.5);
    background: rgba(255, 248, 238, 0.05);
    box-shadow: 0 0 46px rgba(236, 209, 154, 0.16);
    color: #ecd19a;
    font-family: var(--serif);
    font-size: 1.8rem;
}

.finale-kicker {
    margin: 0 0 1rem;
    font-size: 0.64rem;
    font-weight: 700;
    letter-spacing: 0.32em;
    text-transform: uppercase;
    color: #ecd19a;
}

.finale-title {
    margin: 0;
    font-family: var(--serif);
    font-size: clamp(2.35rem, 7vw, 5.3rem);
    font-weight: 600;
    line-height: 0.98;
    letter-spacing: 0.02em;
    text-transform: uppercase;
}

.finale-title span {
    display: block;
    color: #f0d9a5;
}

.finale-closing {
    max-width: 640px;
    margin: 1.5rem auto 0;
    font-family: var(--script);
    font-size: clamp(1.5rem, 4vw, 2.5rem);
    line-height: 1.25;
    color: #ffe7f0;
}

.finale-name {
    display: block;
    margin-top: 0.2rem;
    font-size: 0.86em;
    color: #f0d9a5;
}

.finale-note {
    max-width: 500px;
    margin: 1rem auto 0;
    font-size: 0.8rem;
    line-height: 1.6;
    color: rgba(255, 248, 238, 0.68);
}

.finale-star {
    position: absolute;
    z-index: 1;
    color: #f6e5b8;
    animation: twinkle var(--twinkle, 3.4s) ease-in-out infinite;
    animation-delay: var(--delay, 0s);
    opacity: 0.8;
    text-shadow: 0 0 14px rgba(246, 229, 184, 0.75);
}

.finale-sunflower {
    position: absolute;
    z-index: 1;
    font-size: var(--size, 1.6rem);
    opacity: 0.55;
    animation: sway var(--sway, 6s) ease-in-out infinite;
    animation-delay: var(--delay, 0s);
    filter: drop-shadow(0 8px 18px rgba(0, 0, 0, 0.25));
}

.gold-confetti {
    position: absolute;
    top: -10%;
    left: var(--left);
    z-index: 2;
    width: var(--size, 7px);
    height: calc(var(--size, 7px) * 0.45);
    border-radius: 2px;
    background: var(--color, #ecd19a);
    opacity: 0.8;
    animation: confetti-fall var(--duration, 9s) linear var(--delay, 0s) infinite;
}

.footer {
    position: relative;
    z-index: 2;
    padding: 2.2rem 1rem 2.6rem;
    text-align: center;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #6f4e64;
}

/* ---------- Typography hardening ---------- */

html body .stApp,
html body .stApp p,
html body .stApp li,
html body .stApp label,
html body .stApp input,
html body .stApp textarea,
html body .stApp summary,
html body .stApp button {
    font-family: var(--sans) !important;
}

html body .stApp .welcome-title,
html body .stApp .hero-title,
html body .stApp .section-title,
html body .stApp .spotlight-quote,
html body .stApp .poster-title,
html body .stApp .anthem-title,
html body .stApp .timeline-title,
html body .stApp .one-more h3,
html body .stApp .letter-closed h3,
html body .stApp .wish-card p {
    font-family: var(--serif) !important;
}

html body .stApp .hero-name,
html body .stApp .welcome-hint,
html body .stApp .photo-card figcaption,
html body .stApp .letter-salutation,
html body .stApp .letter-body p,
html body .stApp .letter-signoff,
html body .stApp .letter-signature,
html body .stApp .finale-closing {
    font-family: var(--script) !important;
}

html body .stApp .lyric-line {
    font-family: var(--kannada) !important;
}

html body .stApp .lyrics.translit .lyric-line {
    font-family: var(--serif) !important;
    font-style: italic;
}

/* ---------- Animations ---------- */

@keyframes fade-up {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes drift {
    0%, 100% { transform: translate3d(0, 0, 0) rotate(0deg); opacity: 0.55; }
    50%      { transform: translate3d(7px, -16px, 0) rotate(8deg); opacity: 0.9; }
}

@keyframes bob {
    0%, 100% { transform: translateY(0); }
    50%      { transform: translateY(-8px); }
}

@keyframes twinkle {
    0%, 100% { opacity: 0.25; transform: scale(0.85); }
    50%      { opacity: 0.95; transform: scale(1.08); }
}

@keyframes orbit-spin {
    from { transform: translate(-50%, -50%) rotate(0deg); }
    to   { transform: translate(-50%, -50%) rotate(360deg); }
}

@keyframes confetti-fall {
    0%   { transform: translate3d(0, -8vh, 0) rotate(0deg); opacity: 0; }
    8%   { opacity: 0.95; }
    100% { transform: translate3d(var(--drift, 30px), 92vh, 0) rotate(760deg); opacity: 0; }
}

@keyframes play-glow {
    0%, 100% { box-shadow: 0 0 0 8px rgba(255, 248, 238, 0.06), 0 0 30px rgba(236, 209, 154, 0.18); }
    50%      { box-shadow: 0 0 0 12px rgba(255, 248, 238, 0.08), 0 0 48px rgba(236, 209, 154, 0.34); }
}

@keyframes soft-glow {
    0%, 100% { box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.85), 0 14px 34px -26px rgba(140, 84, 60, 0.55); }
    50%      { box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.9), 0 18px 44px -22px rgba(168, 117, 47, 0.55); }
}

@keyframes note-float {
    0%, 100% { transform: translateY(0) rotate(-6deg); opacity: 0.28; }
    50%      { transform: translateY(-8px) rotate(7deg); opacity: 0.55; }
}

@keyframes letter-open {
    from { opacity: 0; transform: translateY(26px) scale(0.985); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
}

@keyframes sway {
    0%, 100% { transform: translateY(0) rotate(-4deg); }
    50%      { transform: translateY(-10px) rotate(5deg); }
}

/* ---------- Responsive ---------- */

@media (max-width: 1000px) {
    .reasons-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
}

@media (max-width: 820px) {
    .spotlight { grid-template-columns: 1fr; }
    .spotlight-media { min-height: 320px; }
    .spotlight-media::after { background: linear-gradient(180deg, transparent 74%, rgba(255, 253, 248, 0.28)); }
    .spotlight-copy { padding-top: 1.5rem; }
}

@media (max-width: 760px) {
    .block-container { padding-left: 0.9rem; padding-right: 0.9rem; }
    .hero { min-height: 78vh; }
    .hero-age { font-size: clamp(10rem, 50vw, 18rem); }
    .photo-card.wide { grid-column: span 1; }
    .photo-card { transform: none; }
    .photo-card img { height: 300px; }
    .reasons-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .timeline::before { left: 19px; }
    .timeline-item,
    .timeline-item:nth-child(even) {
        width: 100%;
        margin-left: 0;
        padding: 0 0 1.8rem 3.3rem;
    }
    .timeline-dot,
    .timeline-item:nth-child(even) .timeline-dot {
        top: 0.4rem;
        left: -1px;
        right: auto;
    }
    .poster-bottom { grid-template-columns: 1fr; gap: 0.75rem; }
    .poster-play { width: 54px; }
    .letter-paper::after { right: 5%; }
}

@media (max-width: 560px) {
    .block-container { padding: 0.8rem 0.7rem 0; }
    .welcome { min-height: 86vh; border-radius: 24px; }
    .welcome-hint { font-size: 1.1rem; }
    .envelope-stage { margin-top: 2rem; }
    .hero { border-radius: 24px; }
    .hero-title-line { font-size: 1.1rem; }
    .hero-name { font-size: clamp(2.8rem, 15vw, 4.4rem); }
    .hero-nav { gap: 0; }
    .hero-nav a { font-size: 0.7rem; padding: 0.38rem 0.5rem; }
    .scrapbook { grid-template-columns: 1fr; }
    .photo-card img { height: 320px; }
    .reasons-grid { grid-template-columns: 1fr; }
    .reason-card { min-height: 120px; }
    .stTabs [data-baseweb="tab-list"] { width: 100%; }
    .stTabs [data-baseweb="tab"] { padding: 0.5rem 0.7rem; font-size: 0.74rem; }
    .finale { min-height: 88vh; }
    .st-key-finale_controls { padding-bottom: 2.2rem; }
    .footer { padding-bottom: 2rem; }
}

@media (prefers-reduced-motion: reduce) {
    html { scroll-behavior: auto; }
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
    }
}
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def load_json(relative_path: str, default: Any) -> Any:
    path = BASE_DIR / relative_path
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (FileNotFoundError, json.JSONDecodeError, OSError, TypeError, ValueError):
        return default


def show(markup: str) -> None:
    """Render HTML without letting Markdown turn indented tags into code blocks."""
    cleaned = "\n".join(line.strip() for line in markup.strip().splitlines())
    st.markdown(cleaned, unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def image_payload(path_string: str, modified: float, max_side: int = 1100, quality: int = 84) -> dict[str, Any]:
    """Load, downscale and encode an image as a data URI for the scrapbook."""
    path = Path(path_string)
    raw = path.read_bytes()
    mime = {
        ".jpg": "jpeg",
        ".jpeg": "jpeg",
        ".png": "png",
        ".webp": "webp",
        ".gif": "gif",
        ".bmp": "bmp",
    }.get(path.suffix.lower(), "jpeg")

    if Image is not None:
        try:
            with Image.open(io.BytesIO(raw)) as opened:
                image = ImageOps.exif_transpose(opened) if ImageOps is not None else opened
                image = image.convert("RGB")
                width, height = image.size
                resample = getattr(Image, "Resampling", Image).LANCZOS
                image.thumbnail((max_side, max_side), resample)
                buffer = io.BytesIO()
                image.save(buffer, format="WEBP", quality=quality, method=4)
                encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
                return {"uri": "data:image/webp;base64," + encoded, "w": width, "h": height}
        except Exception:
            pass

    encoded = base64.b64encode(raw).decode("ascii")
    return {"uri": f"data:image/{mime};base64," + encoded, "w": 0, "h": 0}


def media_source(value: Any) -> str | None:
    """Return a usable local path or remote URL, or None when the asset is absent."""
    if not value:
        return None
    value = str(value)
    if value.startswith(("http://", "https://")):
        return value
    path = (BASE_DIR / value).resolve()
    try:
        if path.is_file() and path.stat().st_size > 0:
            return str(path)
    except OSError:
        return None
    return None


def section_config(content: dict[str, Any], key: str) -> dict[str, str]:
    defaults: dict[str, dict[str, str]] = {
        "photos": {"kicker": "01 · The scrapbook", "title": "Her Photo Universe", "subtitle": "Every frame holds a version of you we never want to forget."},
        "video": {"kicker": "02 · The premiere", "title": "The Birthday Film", "subtitle": "A little film for a very big day."},
        "reasons": {"kicker": "03 · The evidence", "title": "20 Reasons We Love You", "subtitle": "Twenty tiny truths. Tap each card to open it."},
        "letter": {"kicker": "04 · Sealed with love", "title": "A Letter From Your Sister", "subtitle": "From Anu, with all her love."},
        "wishes": {"kicker": "05 · The wish wall", "title": "Birthday Wish Wall", "subtitle": "A little constellation of voices from the people who adore you."},
        "finale": {"kicker": "06 · The last page (for now)", "title": "Grand Finale", "subtitle": ""},
    }
    result = defaults.get(key, {"kicker": "", "title": "", "subtitle": ""}).copy()
    custom = as_dict(as_dict(content.get("sections")).get(key))
    result.update({k: str(v) for k, v in custom.items() if isinstance(v, (str, int, float))})
    return result


def section_head(content: dict[str, Any], key: str, extra: str = "") -> str:
    config = section_config(content, key)
    return f"""
    <div class="section-head reveal-up">
        <span class="eyebrow">{esc(config.get("kicker", ""))}</span>
        <h2 class="section-title">{esc(config.get("title", ""))}</h2>
        <p class="section-sub">{esc(config.get("subtitle", ""))}</p>
        {extra}
    </div>
    """


def confetti_pieces(count: int = 44) -> str:
    colors = ["#f2b8cf", "#cbb4ef", "#ecd19a", "#e98aa8", "#fff4d6", "#bda2e8", "#d9a84e"]
    rng = random.Random(20)
    pieces = []
    for _ in range(count):
        left = rng.uniform(1, 99)
        size = rng.uniform(6, 12)
        delay = rng.uniform(0, 1.4)
        duration = rng.uniform(3.2, 5.2)
        drift = rng.uniform(-90, 90)
        color = rng.choice(colors)
        radius = "50%" if rng.random() > 0.55 else "2px"
        pieces.append(
            f'<span class="confetti-piece" style="--left:{left:.1f}%;--size:{size:.0f}px;'
            f'--delay:{delay:.2f}s;--duration:{duration:.2f}s;--drift:{drift:.0f}px;'
            f'--color:{color};--round:{radius};"></span>'
        )
    return "".join(pieces)


def welcome_markup(birthday: dict[str, Any]) -> str:
    note = birthday.get("welcome", "Psst... someone very special turns 20 today 💌")
    nickname = birthday.get("nickname", "[NICKNAME]")
    return f"""
    <section class="welcome glass" id="top">
        <span class="welcome-spark" aria-hidden="true">✦</span>
        <span class="welcome-spark" aria-hidden="true">✧</span>
        <span class="welcome-spark" aria-hidden="true">♡</span>
        <span class="welcome-spark" aria-hidden="true">✦</span>
        <p class="welcome-kicker">A secret letter · Chapter 20</p>
        <h1 class="welcome-title">{esc(note)}</h1>
        <div class="envelope-stage" aria-hidden="true">
            <div class="env-body">
                <div class="env-letter">
                    <span>20</span>
                    <span>for {esc(nickname)}</span>
                </div>
            </div>
            <div class="env-flap"></div>
            <div class="env-seal">♡</div>
        </div>
        <p class="welcome-hint">A little universe is waiting inside. No peeking before you are ready.</p>
    </section>
    """


def hero_markup(content: dict[str, Any]) -> str:
    birthday = as_dict(content.get("birthday"))
    name = birthday.get("name", "[SISTER'S NAME]")
    prefix = birthday.get("headline_prefix", "HAPPY 20TH BIRTHDAY,")
    subtitle = birthday.get("subtitle", "20 years of magic, mischief, smiles and memories")
    date_text = birthday.get("date", "[BIRTHDAY DATE]")
    sign_note = birthday.get("sign_note", "a little Libra magic")
    age = birthday.get("age", 20)
    confetti = confetti_pieces() if st.session_state.get("just_opened") else ""
    st.session_state.just_opened = False

    return f"""
    <section class="hero glass" id="top">
        {confetti}
        <div class="hero-age" aria-hidden="true">{esc(age)}</div>
        <div class="orbit" aria-hidden="true"><span class="orbit-dot"></span></div>
        <div class="orbit orbit--two" aria-hidden="true"><span class="orbit-dot"></span></div>
        <div class="hero-inner">
            <p class="hero-kicker">Chapter 20 · A little universe made just for you</p>
            <h1 class="hero-title">
                <span class="hero-title-line">{esc(prefix)}</span>
                <span class="hero-name">{esc(name)}<span class="hero-bang">!</span></span>
            </h1>
            <p class="hero-sub">{esc(subtitle)}</p>
            <div class="hero-chips">
                <span class="chip">♎ {esc(sign_note)}</span>
                <span class="chip">✦ {esc(date_text)}</span>
                <span class="chip">☾ {esc(age)} trips around the sun</span>
            </div>
            <nav class="hero-nav" aria-label="Birthday page sections">
                <a href="#photos">Photos</a>
                <a href="#video">The film</a>
                <a href="#reasons">20 reasons</a>
                <a href="#letter">The letter</a>
                <a href="#wishes">Wishes</a>
            </nav>
            <div class="scroll-cue" aria-hidden="true"><span>Scroll gently</span><span>⌄</span></div>
        </div>
    </section>
    """


def discover_photos(config: dict[str, Any]) -> tuple[list[Path], Path | None]:
    folder = (BASE_DIR / str(config.get("folder", "assets/photos"))).resolve()
    allowed = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp"}
    if not folder.is_dir():
        return [], None
    files = sorted(
        path for path in folder.iterdir()
        if path.is_file() and path.suffix.lower() in allowed and not path.name.startswith(".")
    )
    spotlight_name = str(config.get("spotlight", "") or "")
    spotlight = next((path for path in files if path.name == spotlight_name), None)
    if spotlight is None and files:
        spotlight = files[0]
    return files, spotlight


def caption_for(path: Path, config: dict[str, Any], index: int) -> str:
    captions = config.get("captions", {}) or {}
    if isinstance(captions, dict) and path.name in captions:
        return str(captions[path.name])
    fallbacks = config.get("fallback_captions", []) or []
    if not isinstance(fallbacks, list) or not fallbacks:
        fallbacks = ["Our little sunshine", "The smile that lights up our home", "Queen of our hearts", "Chapter 20 begins"]
    return str(fallbacks[index % len(fallbacks)])


def photo_section_markup(content: dict[str, Any]) -> str:
    config = as_dict(content.get("photos"))
    birthday = as_dict(content.get("birthday"))
    name = str(birthday.get("name", "[SISTER'S NAME]"))
    files, spotlight = discover_photos(config)
    if len(files) == 1:
        count_text = "1 memory & counting"
    else:
        count_text = f"{len(files)} memories & counting" if files else "Waiting for the first memory"
    extra = f'<span class="count-chip">✧ {esc(count_text)}</span>'
    markup = [section_head(content, "photos", extra)]

    if spotlight is not None:
        try:
            payload = image_payload(str(spotlight), spotlight.stat().st_mtime, 1600, 85)
            caption = caption_for(spotlight, config, files.index(spotlight))
            label = config.get("spotlight_label", "Spotlight memory")
            note = config.get("spotlight_note", "Some photos don't just show a moment. They bring it all back.")
            markup.append(f"""
            <div class="spotlight">
                <div class="spotlight-media">
                    <img src="{payload['uri']}" alt="{esc(caption)}" loading="eager">
                </div>
                <div class="spotlight-copy">
                    <span class="spotlight-label">✦ {esc(label)}</span>
                    <p class="spotlight-quote">“{esc(caption)}”</p>
                    <p class="spotlight-note">{esc(note)}</p>
                </div>
            </div>
            """)
        except OSError:
            spotlight = None

    if spotlight is None:
        spotlight_caption = config.get("spotlight_caption", "The one we keep coming back to")
        markup.append(f"""
        <div class="spotlight">
            <div class="spotlight-media spotlight-placeholder">
                <span class="sun" aria-hidden="true">🌻</span>
                <strong>Your spotlight memory</strong>
                <small>Add a photo to assets/photos and name it in content.json — this frame is waiting for her.</small>
            </div>
            <div class="spotlight-copy">
                <span class="spotlight-label">✦ Spotlight memory</span>
                <p class="spotlight-quote">“{esc(spotlight_caption)}”</p>
                <p class="spotlight-note">The one we keep coming back to. Add your favourite photograph and it will live here.</p>
            </div>
        </div>
        """)

    grid_photos = [path for path in files if path != spotlight]
    cards = []
    for index, path in enumerate(grid_photos):
        try:
            payload = image_payload(str(path), path.stat().st_mtime, 1100, 83)
        except OSError:
            continue
        caption = caption_for(path, config, files.index(path))
        wide = " wide" if payload["w"] and payload["w"] > payload["h"] * 1.12 else ""
        cards.append(f"""
        <figure class="photo-card{wide}">
            <img src="{payload['uri']}" alt="{esc(caption)}" loading="lazy">
            <figcaption>{esc(caption)}</figcaption>
        </figure>
        """)

    if not files:
        placeholders = [
            ("🌻", "Our little sunshine", "A favourite photo lives here"),
            ("✨", "The smile that lights up our home", "Drop a photo into assets/photos"),
            ("🌙", "Queen of our hearts", "This frame is waiting for her"),
            ("💌", "Chapter 20 begins", "Add the first memory of the new chapter"),
        ]
        for emoji, caption, note in placeholders:
            cards.append(f"""
            <figure class="photo-card">
                <div class="photo-empty">
                    <span class="empty-emoji" aria-hidden="true">{emoji}</span>
                    <span class="empty-title">{esc(note)}</span>
                    <span class="empty-note">{esc(caption)}</span>
                </div>
                <figcaption>{esc(caption)}</figcaption>
            </figure>
            """)

    if cards:
        markup.append(f'<div class="scrapbook">{"".join(cards)}</div>')

    if files:
        markup.append(
            '<p class="mini-note">Photos are optimised automatically for a quick, gentle load — '
            f'every memory of {esc(name)} stays exactly as it is.</p>'
        )
    else:
        markup.append(
            '<p class="mini-note">Only real photographs belong here — add hers to assets/photos '
            'and update the captions in content.json.</p>'
        )

    return "".join(markup)


def poster_markup(content: dict[str, Any]) -> str:
    video = as_dict(content.get("video"))
    title = video.get("title", "Chapter 20: The Film")
    intro = video.get("intro", "A little film for a very big day.")
    poster_path = media_source(video.get("poster", "assets/video_poster.jpg"))
    poster_img = ""
    if poster_path:
        try:
            payload = image_payload(poster_path, Path(poster_path).stat().st_mtime, 1600, 85)
            poster_img = f'<img class="poster-img" src="{payload["uri"]}" alt="Poster artwork for the birthday music video" loading="lazy">'
        except OSError:
            poster_img = ""
    return f"""
    <div class="video-poster">
        {poster_img}
        <div class="video-veil"></div>
        <div class="poster-content">
            <div class="poster-top">
                <span class="poster-badge">A little film · Chapter 20</span>
                <span class="poster-genre">Kannada hip-hop · birthday edition</span>
            </div>
            <div class="poster-bottom">
                <div class="poster-play" aria-hidden="true">▶</div>
                <div>
                    <h3 class="poster-title">{esc(title)}</h3>
                    <p class="poster-sub">{esc(intro)}</p>
                </div>
            </div>
        </div>
    </div>
    """


def missing_video_markup(content: dict[str, Any]) -> str:
    video = as_dict(content.get("video"))
    title = video.get("missing_title", "The film is still warming up")
    text = video.get("missing_text", "Add your birthday music video at assets/birthday_video.mp4 and this stage will come alive.")
    return f"""
    <div class="video-poster video-missing">
        <div class="video-veil"></div>
        <div class="poster-content">
            <div class="poster-top">
                <span class="poster-badge">A little film · Chapter 20</span>
                <span class="poster-genre">Waiting for the premiere</span>
            </div>
            <div class="poster-bottom">
                <div class="poster-play" aria-hidden="true">♫</div>
                <div>
                    <h3 class="poster-title">{esc(title)}</h3>
                    <p class="poster-sub">{esc(text)}</p>
                </div>
            </div>
        </div>
    </div>
    """


def reasons_markup(content: dict[str, Any]) -> str:
    reasons = content.get("reasons", [])
    if not isinstance(reasons, list):
        reasons = []
    cards = []
    for index, reason in enumerate(reasons[:20], start=1):
        cards.append(f"""
        <details class="reason-card">
            <summary>
                <span class="reason-num">{index:02d}</span>
                <span class="reason-hint">Tap to reveal</span>
                <span class="reason-heart" aria-hidden="true">♡</span>
            </summary>
            <p class="reason-text">{esc(reason)}</p>
        </details>
        """)
    if not cards:
        cards.append('<div class="wish-empty">Add your 20 reasons in content.json.</div>')
    return (
        section_head(content, "reasons")
        + f'<div class="reasons-grid">{"".join(cards)}</div>'
        + '<p class="mini-note">Twenty cards, twenty small truths. Open them slowly.</p>'
    )


def wishes_markup(content: dict[str, Any]) -> str:
    wishes = content.get("wishes", [])
    if not isinstance(wishes, list):
        wishes = []
    cards = []
    for wish in wishes:
        if not isinstance(wish, dict):
            continue
        cards.append(f"""
        <article class="wish-card">
            <span class="wish-quote" aria-hidden="true">“</span>
            <p>{esc(wish.get("message", ""))}</p>
            <span class="wish-from">— {esc(wish.get("from", "Someone who loves you"))}</span>
        </article>
        """)
    if not cards:
        cards.append('<div class="wish-empty">Wishes are stored safely in content.json — add as many as you like.</div>')
    return section_head(content, "wishes") + f'<div class="wish-wall">{"".join(cards)}</div>'


def letter_markup(letter: dict[str, Any]) -> str:
    paragraphs = letter.get("paragraphs", []) or []
    if not isinstance(paragraphs, list):
        paragraphs = [str(paragraphs)]
    body = "".join(
        f'<p style="--i:{index}">{esc(paragraph)}</p>'
        for index, paragraph in enumerate(paragraphs)
        if str(paragraph).strip()
    )
    return f"""
    <article class="letter-paper">
        <p class="letter-salutation">{esc(letter.get("salutation", "My dearest [NICKNAME],"))}</p>
        <div class="letter-body">{body}</div>
        <p class="letter-signoff">{esc(letter.get("signoff", "Forever your biggest fan,"))}<br>
        <span class="letter-signature">{esc(letter.get("signature", "[YOUR NAME] ♡"))}</span></p>
    </article>
    """


def closed_letter_markup(letter: dict[str, Any]) -> str:
    note = letter.get("envelope_note", "For your eyes only, [NICKNAME]")
    return f"""
    <div class="letter-closed">
        <div class="letter-wax" aria-hidden="true">🕊</div>
        <h3>{esc(note)}</h3>
        <p>There is a letter in here with your name on it. It is a little long, a little sentimental, and entirely yours.</p>
    </div>
    """


def finale_markup(content: dict[str, Any]) -> str:
    finale = as_dict(content.get("finale"))
    birthday = as_dict(content.get("birthday"))
    name = birthday.get("name", "[SISTER'S NAME]")
    rng = random.Random(20)

    stars = []
    for _ in range(26):
        stars.append(
            f'<span class="finale-star" style="left:{rng.uniform(2, 98):.1f}%;top:{rng.uniform(2, 96):.1f}%;'
            f'font-size:{rng.uniform(0.5, 1.15):.2f}rem;--twinkle:{rng.uniform(2.4, 5.4):.1f}s;'
            f'--delay:{rng.uniform(-5, 0):.1f}s;" aria-hidden="true">✦</span>'
        )
    sunflowers = []
    for _ in range(6):
        sunflowers.append(
            f'<span class="finale-sunflower" style="left:{rng.uniform(3, 94):.1f}%;top:{rng.uniform(8, 90):.1f}%;'
            f'--size:{rng.uniform(1.2, 2.2):.1f}rem;--sway:{rng.uniform(4.5, 8):.1f}s;'
            f'--delay:{rng.uniform(-6, 0):.1f}s;" aria-hidden="true">🌻</span>'
        )
    gold = []
    for _ in range(30):
        gold.append(
            f'<span class="gold-confetti" style="--left:{rng.uniform(0, 100):.1f}%;'
            f'--size:{rng.uniform(4, 9):.0f}px;--duration:{rng.uniform(7, 13):.1f}s;'
            f'--delay:{rng.uniform(-12, 0):.1f}s;'
            f'--color:{rng.choice(["#ecd19a", "#f5dfa8", "#d9ad5e", "#f3c7d8"])};"></span>'
        )

    return f"""
    <section class="finale" id="finale" aria-labelledby="finale-title">
        {"".join(stars)}
        {"".join(sunflowers)}
        {"".join(gold)}
        <div class="finale-content">
            <div class="finale-sigil" aria-hidden="true">♎</div>
            <p class="finale-kicker">{esc(finale.get("kicker", "The last page is only the beginning"))}</p>
            <h2 class="finale-title" id="finale-title">
                {esc(finale.get("line_one", "THIS IS YOUR CHAPTER 20."))}
                <span>{esc(finale.get("line_two", "MAKE IT UNFORGETTABLE."))}</span>
            </h2>
            <p class="finale-closing">
                {esc(finale.get("closing", "You will always be our little girl."))}
                <span class="finale-name">{esc(finale.get("closing_name", "Happy Birthday, " + name + " ❤️"))}</span>
            </p>
            <p class="finale-note">Keep this page bookmarked. Come back whenever you need reminding how loved you are.</p>
        </div>
    </section>
    """


def footer_markup(content: dict[str, Any]) -> str:
    footer = content.get("footer", "Made with love · Chapter 20")
    return f'<div class="footer">{esc(footer)}</div>'


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

content = load_json("content.json", {})
if not isinstance(content, dict):
    content = {}
birthday_info = as_dict(content.get("birthday"))

st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

# Decorative fixed backdrop
show("""
<div class="cosmic-bg" aria-hidden="true">
    <span>✦</span><span>♡</span><span>✧</span><span>♡</span><span>✦</span><span>✧</span><span>♡</span>
    <span>✦</span><span>♡</span><span>✧</span><span>✦</span><span>♡</span><span>✧</span><span>♡</span>
</div>
""")

if "revealed" not in st.session_state:
    st.session_state.revealed = False


# ---------------------------------------------------------------------------
# Section 1 — Secret welcome
# ---------------------------------------------------------------------------

if not st.session_state.revealed:
    show(welcome_markup(birthday_info))
    with st.container(key="welcome_cta"):
        if st.button("Open Your Surprise  ✨", type="primary", use_container_width=True):
            st.session_state.revealed = True
            st.session_state.just_opened = True
            st.rerun()
    st.stop()


# ---------------------------------------------------------------------------
# Section 1 continued — Hero
# ---------------------------------------------------------------------------

show(hero_markup(content))


# ---------------------------------------------------------------------------
# Section 2 — Photo universe
# ---------------------------------------------------------------------------

show('<div id="photos" class="section-anchor"></div>')
show(photo_section_markup(content))


# ---------------------------------------------------------------------------
# Section 3 — Birthday music video
# ---------------------------------------------------------------------------

show('<div id="video" class="section-anchor section-space"></div>')
show(section_head(content, "video"))

video_config = as_dict(content.get("video"))
video_src = media_source(video_config.get("path", "assets/birthday_video.mp4"))
audio_src = media_source(video_config.get("audio", "assets/birthday_audio.mp3"))

with st.container(key="video_panel"):
    if video_src:
        if st.session_state.get("play_video"):
            st.video(video_src)
            st.caption("Best with the volume up and someone you love nearby. 🎧")
        else:
            show(poster_markup(content))
            with st.container(key="video_cta"):
                if st.button(
                    video_config.get("button_label", "Play the Video 🎬"),
                    type="primary",
                    use_container_width=True,
                    key="play_video_button",
                ):
                    st.session_state.play_video = True
                    st.rerun()
    else:
        show(missing_video_markup(content))

    if audio_src:
        with st.expander(video_config.get("audio_label", "Prefer just the song? 🎵")):
            st.audio(audio_src)


# ---------------------------------------------------------------------------
# Section 4 — 20 reasons
# ---------------------------------------------------------------------------

show('<div id="reasons" class="section-anchor section-space"></div>')
show(reasons_markup(content))


# ---------------------------------------------------------------------------
# Section 5 — Letter
# ---------------------------------------------------------------------------

show('<div id="letter" class="section-anchor section-space"></div>')
show(section_head(content, "letter"))

letter_config = as_dict(content.get("letter"))
if st.session_state.get("letter_open"):
    show(letter_markup(letter_config))
    with st.container(key="letter_close"):
        if st.button("Fold the letter back  ✦", type="secondary", use_container_width=True):
            st.session_state.letter_open = False
            st.rerun()
else:
    show(closed_letter_markup(letter_config))
    with st.container(key="letter_cta"):
        if st.button("Open the Letter  💌", type="primary", use_container_width=True):
            st.session_state.letter_open = True
            st.rerun()


# ---------------------------------------------------------------------------
# Section 6 — Wish wall
# ---------------------------------------------------------------------------

show('<div id="wishes" class="section-anchor section-space"></div>')
show(wishes_markup(content))


# ---------------------------------------------------------------------------
# Section 7 — Grand finale
# ---------------------------------------------------------------------------

show(finale_markup(content))

finale_config = as_dict(content.get("finale"))
with st.container(key="finale_controls"):
    show('<p class="replay-kicker">One more spin through your little universe?</p>')
    if st.button(
        finale_config.get("replay_label", "Replay the surprise ↺"),
        type="primary",
        key="replay_button",
    ):
        for _key in ("revealed", "just_opened", "play_video", "letter_open"):
            st.session_state.pop(_key, None)
        st.session_state.revealed = False
        st.rerun()

show(footer_markup(content))
