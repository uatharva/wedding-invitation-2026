from flask import Flask, render_template_string, request, redirect, url_for, jsonify
import csv
import os
import secrets
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", secrets.token_hex(16))

CSV_FILE = "rsvp_responses.csv"

WEDDING = {
    "couple_names": "Nehal & Atharva",
    "headline": "A modern Seattle wedding with subtle Indian warmth",
    "subheadline": "An intimate white wedding celebration — elevated, playful, stylish, and full of joy.",
    "date": "Friday, July 24, 2026",
    "time": "4:30 PM Ceremony · Dinner, Desserts & Toasts to Follow",
    "venue": "Apartment Community Lounge, Seattle, WA",
    "address": "14633 NE 37th Pl, Seattle, WA 98101",
    "officiant": "Animesh Soni",
    "rsvp_by": "Friday, June 26, 2026",
    "parking_note": "Guest parking and building access instructions will be shared closer to the date.",
    "dress_code_title": "Pastels & Formals",
    "women_attire": "Sarees, lehengas, gowns, elegant cocktail dresses, or formal dresses in pastel tones.",
    "men_attire": "Suits, bandhgalas, kurta-jacket sets, or dress shirts with blazers and formal trousers in pastel tones.",
    "no_gifts": "No gifts, please — your presence is the only present we would love.",
    "our_note": "We are keeping things intentionally intimate — no elaborate itinerary and no multiple functions, just one beautiful evening with the people we love most.",
    "schedule": [
        {"time": "4:00 PM", "title": "Guest Arrival", "desc": "Welcome drinks, mingling, and cozy pre-ceremony energy."},
        {"time": "4:30 PM", "title": "Ceremony", "desc": "A modern white wedding ceremony officiated by our friend."},
        {"time": "5:15 PM", "title": "Photos & Toasts", "desc": "A few pictures, warm wishes, and celebratory toasts."},
        {"time": "6:00 PM", "title": "Dinner & Desserts", "desc": "Good food, sweet endings, music, and time together."},
    ],
    "faq": [
        {"q": "What should I wear?", "a": "Formal attire in pastel tones. Indian and Western formalwear are both perfect."},
        {"q": "Will there be multiple events?", "a": "No — we are keeping the celebration simple with one main ceremony and dinner."},
        {"q": "Are gifts expected?", "a": "No gifts, please. We truly just want to celebrate with you."},
        {"q": "Can I bring a plus one?", "a": "Please follow the invitation details you received, or reach out to us if unsure."},
        {"q": "Parking and building access?", "a": "You can add guest parking, building entry, and elevator instructions here."},
    ],
    "stickers": ["just married", "save the date", "soft launch forever", "Seattle love club", "pastels only", "dancing encouraged"],
    "moments": ["ceremony", "toasts", "dessert table", "playlist", "dance floor", "late-night chai vibes"],
    "playlist": ["Golden Hour", "Kesariya (acoustic vibe)", "Until I Found You", "Raabta", "Perfect", "Tera Hone Laga Hoon"],
    "hero_tags": ["white wedding", "Seattle", "Indian roots", "formal pastels", "intimate celebration"],
}

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{{ wedding.couple_names }} | Wedding Invitation</title>
  <meta name="description" content="Interactive wedding invitation and RSVP website" />
  <style>
    :root {
  --bg-1: #ffe8da; /* warm sunset base (richer) */
  --bg-2: #ffc98a; /* soft gold (richer) */
  --bg-3: #b7e6ff; /* cool sky hint (richer) */
      --paper: rgba(255,255,255,0.72);
      --paper-2: rgba(255,255,255,0.88);
      --text: #2c2725;
      --muted: #776c65;
      --line: rgba(113, 95, 84, 0.14);
      --dark: #241f1d;
      --rose: #ffd6de;
      --peach: #ffd9bf;
      --sage: #d9efd9;
      --lavender: #e5ddff;
      --blue: #d8ebff;
      --gold: #c7a87a;
      --shadow: 0 24px 80px rgba(43, 28, 22, 0.12);
      --radius-xl: 34px;
      --radius-lg: 24px;
      --radius-md: 18px;
    }

    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      min-height: 100vh;
      overflow-x: hidden;
      color: var(--text);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  background: linear-gradient(120deg, var(--bg-1) 0%, var(--bg-2) 45%, var(--bg-3) 100%);
  background-size: 200% 200%;
  animation: gradientShift 24s ease infinite;
    }

    /* subtle vignette to increase contrast for sparkles */
    body::after {
      content: '';
      position: fixed;
      inset: 0;
      pointer-events: none;
      background: radial-gradient(60% 40% at 50% 30%, rgba(255,255,255,0.0), rgba(0,0,0,0.06) 60% , rgba(0,0,0,0.12) 100%);
      mix-blend-mode: multiply;
      z-index: 0;
    }

    @keyframes gradientShift {
      0% { background-position: 0% 50%; }
      50% { background-position: 100% 50%; }
      100% { background-position: 0% 50%; }
    }

    .ambient, .confetti, .stars {
      position: fixed;
      inset: 0;
      pointer-events: none;
      overflow: hidden;
      z-index: 0;
    }

    .blob {
      position: absolute;
      border-radius: 999px;
      filter: blur(14px);
      opacity: 0.75;
      animation: floatBlob 14s ease-in-out infinite;
    }

    .blob.one { width: 360px; height: 360px; background: rgba(255, 214, 222, 0.65); top: -80px; left: -40px; }
    .blob.two { width: 420px; height: 420px; background: rgba(229, 221, 255, 0.55); top: 10%; right: -100px; animation-delay: -3s; }
    .blob.three { width: 340px; height: 340px; background: rgba(217, 239, 217, 0.60); bottom: -60px; left: 10%; animation-delay: -7s; }
    .blob.four { width: 300px; height: 300px; background: rgba(216, 235, 255, 0.55); bottom: 12%; right: 4%; animation-delay: -10s; }

    @keyframes floatBlob {
      0%, 100% { transform: translateY(0) translateX(0) scale(1); }
      25% { transform: translateY(-18px) translateX(12px) scale(1.03); }
      50% { transform: translateY(16px) translateX(-12px) scale(0.98); }
      75% { transform: translateY(-10px) translateX(18px) scale(1.04); }
    }

    .spark, .dot {
      position: absolute;
      border-radius: 999px;
      opacity: 0.65;
      animation: drift linear infinite;
    }

    @keyframes drift {
      0% { transform: translateY(0) rotate(0deg); opacity: 0; }
      12% { opacity: 0.7; }
      100% { transform: translateY(-120vh) rotate(240deg); opacity: 0; }
    }

    .star {
      position: absolute;
      color: rgba(199,168,122,0.55);
      font-size: 14px;
      animation: twinkle 4s ease-in-out infinite;
    }

    @keyframes twinkle {
      0%, 100% { opacity: 0.2; transform: scale(0.8); }
      50% { opacity: 0.9; transform: scale(1.15); }
    }

    .shell {
      width: min(1220px, calc(100% - 28px));
      margin: 0 auto;
      padding: 18px 0 60px;
      position: relative;
      z-index: 2;
    }

    .topbar {
      position: sticky;
      top: 12px;
      z-index: 30;
      display: flex;
      justify-content: center;
      margin-bottom: 16px;
    }

    .nav {
      display: flex;
      gap: 10px;
      align-items: center;
      flex-wrap: wrap;
      padding: 10px 12px;
      border: 1px solid rgba(255,255,255,0.65);
      border-radius: 999px;
      backdrop-filter: blur(20px);
      background: rgba(255,255,255,0.58);
      box-shadow: 0 8px 28px rgba(40, 30, 25, 0.08);
    }

    .nav a, .nav button {
      border: none;
      background: transparent;
      color: var(--text);
      text-decoration: none;
      padding: 10px 14px;
      border-radius: 999px;
      font-size: 14px;
      cursor: pointer;
    }

    .nav .cta {
      background: var(--dark);
      color: white;
      box-shadow: 0 12px 28px rgba(36,31,29,0.18);
    }

    .glass, .card, .panel {
      background: var(--paper);
      border: 1px solid rgba(255,255,255,0.65);
      border-radius: var(--radius-xl);
      backdrop-filter: blur(22px);
      box-shadow: var(--shadow);
    }

    .hero {
      display: grid;
      grid-template-columns: 1.05fr 0.95fr;
      gap: 22px;
      align-items: stretch;
    }

    .hero-left {
      padding: 34px;
      position: relative;
      overflow: hidden;
      isolation: isolate;
    }

    .hero-left::before {
      content: "";
      position: absolute;
      width: 240px;
      height: 240px;
      border-radius: 999px;
      right: -70px;
      top: -60px;
      background: radial-gradient(circle, rgba(255,255,255,0.74), transparent 72%);
      z-index: -1;
    }

    .eyebrow {
      text-transform: uppercase;
      letter-spacing: 0.28em;
      font-size: 12px;
      color: var(--muted);
      margin-bottom: 16px;
    }

    h1 {
      font-family: Georgia, "Times New Roman", serif;
      font-size: clamp(54px, 8vw, 96px);
      line-height: 0.92;
      letter-spacing: -0.04em;
      font-weight: 400;
      margin: 0;
    }

    .headline-wrap {
      position: relative;
    }

    .hero-copy {
      margin-top: 20px;
      max-width: 660px;
      font-size: 18px;
      line-height: 1.8;
      color: #554b46;
    }

    .hero-tags, .stickers-row {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 18px;
    }

    .chip, .sticker {
      padding: 10px 14px;
      border-radius: 999px;
      font-size: 13px;
      background: rgba(255,255,255,0.82);
      border: 1px solid rgba(110, 92, 82, 0.10);
      box-shadow: 0 6px 16px rgba(0,0,0,0.04);
    }

    .sticker {
      font-weight: 700;
      transform: rotate(-2deg);
      animation: bob 4s ease-in-out infinite;
    }
    .sticker:nth-child(2n) { transform: rotate(3deg); animation-delay: -1.2s; }
    .sticker:nth-child(3n) { transform: rotate(-4deg); animation-delay: -2.1s; }

    @keyframes bob {
      0%, 100% { transform: translateY(0) rotate(-2deg); }
      50% { transform: translateY(-8px) rotate(1deg); }
    }

    .hero-actions {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      margin-top: 24px;
    }

    .btn {
      border: none;
      border-radius: 999px;
      padding: 14px 20px;
      font-size: 15px;
      cursor: pointer;
      text-decoration: none;
      transition: transform 180ms ease, box-shadow 180ms ease, background 180ms ease;
      display: inline-flex;
      align-items: center;
      gap: 10px;
    }

    .btn:hover { transform: translateY(-2px) scale(1.01); }
    .btn-primary {
      background: var(--dark);
      color: white;
      box-shadow: 0 14px 26px rgba(36,31,29,0.18);
    }
    .btn-secondary {
      background: rgba(255,255,255,0.88);
      color: var(--text);
      border: 1px solid rgba(110, 92, 82, 0.12);
    }
    .btn-fun {
      background: linear-gradient(135deg, #ffdfec, #efe7ff, #e8fff1);
      color: #322b28;
      border: 1px solid rgba(110,92,82,0.10);
    }

    .countdown {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
      margin-top: 24px;
    }

    .count-box {
      padding: 16px;
      border-radius: 22px;
      text-align: center;
      background: rgba(255,255,255,0.82);
      border: 1px solid rgba(110, 92, 82, 0.10);
    }

    .count-box strong {
      display: block;
      font-size: 28px;
      font-weight: 700;
      margin-bottom: 4px;
    }

    .hero-right {
      display: grid;
      gap: 14px;
    }

    .invite-card {
      padding: 18px;
      border-radius: 32px;
      background: linear-gradient(180deg, rgba(255,255,255,0.96), rgba(255,248,242,0.95));
      border: 1px solid rgba(223,207,196,0.84);
      position: relative;
      overflow: hidden;
      min-height: 420px;
    }

    .invite-card::before, .invite-card::after {
      content: "✦";
      position: absolute;
      color: rgba(199,168,122,0.34);
      font-size: 28px;
      animation: twinkle 4.2s ease-in-out infinite;
    }
    .invite-card::before { top: 18px; left: 18px; }
    .invite-card::after { right: 18px; bottom: 18px; animation-delay: -1.2s; }

    .invite-inner {
      height: 100%;
      padding: 26px;
      border-radius: 24px;
      border: 1px dashed rgba(199,168,122,0.28);
      display: flex;
      flex-direction: column;
      justify-content: center;
      text-align: center;
    }

    .couple {
      font-family: Georgia, "Times New Roman", serif;
      font-size: clamp(36px, 4vw, 52px);
      line-height: 1.05;
      margin: 8px 0 16px;
    }

    .meta {
      font-size: 15px;
      line-height: 1.9;
      color: #5a514c;
    }

    .reactions {
      display: flex;
      gap: 12px;
      align-items: center;
      overflow: auto;
      padding-bottom: 4px;
    }

    .reaction {
      min-width: 96px;
      padding: 14px 12px;
      text-align: center;
      border-radius: 20px;
      background: rgba(255,255,255,0.78);
      border: 1px solid rgba(110,92,82,0.10);
      animation: pulseFloat 4.5s ease-in-out infinite;
    }
    .reaction:nth-child(2n) { animation-delay: -1s; }
    .reaction:nth-child(3n) { animation-delay: -2.1s; }

    @keyframes pulseFloat {
      0%, 100% { transform: translateY(0) scale(1); }
      50% { transform: translateY(-6px) scale(1.04); }
    }

    .reaction .emoji { font-size: 24px; display: block; margin-bottom: 6px; }
    .reaction .label { font-size: 12px; color: var(--muted); }

    .marquee-wrap {
      overflow: hidden;
      border-radius: 22px;
      background: rgba(255,255,255,0.68);
      border: 1px solid rgba(110,92,82,0.10);
      padding: 10px 0;
    }

    .marquee {
      display: flex;
      width: max-content;
      gap: 28px;
      animation: marquee 26s linear infinite;
      padding-left: 18px;
      font-weight: 700;
      color: #5b514c;
      text-transform: lowercase;
    }

    @keyframes marquee {
      from { transform: translateX(0); }
      to { transform: translateX(-50%); }
    }

    section { margin-top: 22px; }
    .grid-3, .grid-2, .masonry { display: grid; gap: 18px; }
    .grid-3 { grid-template-columns: repeat(3, 1fr); }
    .grid-2 { grid-template-columns: repeat(2, 1fr); }
  .grid-1 { grid-template-columns: 1fr; display: grid; gap: 18px; }
    .masonry { grid-template-columns: 1.05fr 0.95fr; }

    .section-card {
      padding: 24px;
      border-radius: 30px;
      background: var(--paper-2);
      border: 1px solid rgba(223, 211, 202, 0.86);
      box-shadow: var(--shadow);
      position: relative;
      overflow: hidden;
    }

    .section-title {
      margin: 0 0 8px;
      font-size: 34px;
      font-family: Georgia, "Times New Roman", serif;
      font-weight: 400;
    }

    .section-copy {
      margin: 0;
      line-height: 1.8;
      color: #5d544f;
    }

    .mini-card {
      padding: 24px;
      border-radius: 24px;
      background: rgba(255,255,255,0.84);
      border: 1px solid rgba(223, 211, 202, 0.84);
      min-height: 200px;
      transition: transform 180ms ease, box-shadow 180ms ease;
    }

    /* Save the date card styling */
    .save-date-card {
      padding: 18px 20px;
      border-radius: 18px;
      background: linear-gradient(180deg, rgba(255,255,255,0.95), rgba(255,252,245,0.92));
      border: 1px solid rgba(199,168,122,0.14);
      box-shadow: 0 18px 40px rgba(30,20,18,0.06);
      display: inline-block;
      margin-top: 12px;
    }
    .save-date-card .save-date-main {
      font-family: Georgia, 'Times New Roman', serif;
      font-size: 36px;
      margin-top: 6px;
      font-weight: 600;
      letter-spacing: -0.01em;
    }
    .save-date-card .save-date-sub {
      color: var(--muted);
      margin-top: 6px;
      font-size: 14px;
    }

    .mini-card:hover { transform: translateY(-4px) rotate(-0.2deg); box-shadow: 0 20px 40px rgba(43, 28, 22, 0.10); }
    .mini-card h3 { margin-top: 0; font-size: 22px; }

    .story-panel {
      padding: 30px;
      border-radius: 32px;
      background: linear-gradient(135deg, rgba(36,31,29,0.98), rgba(69,58,55,0.95));
      color: #fff7f2;
      box-shadow: var(--shadow);
    }
    .story-panel p { color: rgba(255,255,255,0.84); }

    .palette {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-top: 18px;
    }
    .swatch {
      min-width: 110px;
      flex: 1 1 110px;
      border-radius: 20px;
      padding: 12px;
      font-size: 13px;
      border: 1px solid rgba(110,92,82,0.08);
      background: rgba(255,255,255,0.82);
    }
    .swatch span { display: block; width: 100%; height: 42px; border-radius: 14px; margin-bottom: 10px; }
    .swatch.blush span { background: #f4d8d8; }
    .swatch.sage span { background: #d9e4d8; }
    .swatch.blue span { background: #d9e7f4; }
    .swatch.lilac span { background: #e7e0f2; }
    .swatch.champagne span { background: #efe0c7; }
    .swatch.peach span { background: #f4dbc9; }

    .timeline { display: grid; gap: 14px; margin-top: 20px; }
    .timeline-item {
      display: grid;
      grid-template-columns: 110px 1fr;
      gap: 16px;
      align-items: start;
      padding: 18px;
      border-radius: 22px;
      background: rgba(255,255,255,0.86);
      border: 1px solid rgba(223,211,202,0.82);
      transition: transform 180ms ease;
    }
    .timeline-item:hover { transform: translateX(4px); }
    .timeline-time { font-weight: 700; color: #6a5d56; }

    .moments-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      margin-top: 18px;
    }

    .moment {
      padding: 16px;
      border-radius: 18px;
      background: linear-gradient(135deg, rgba(255,255,255,0.86), rgba(255,247,243,0.94));
      border: 1px solid rgba(223,211,202,0.82);
      text-transform: lowercase;
      font-weight: 700;
    }

    .playlist-list { display: grid; gap: 10px; margin-top: 16px; }
    .track {
      display: flex;
      justify-content: space-between;
      gap: 14px;
      padding: 14px 16px;
      border-radius: 18px;
      background: rgba(255,255,255,0.82);
      border: 1px solid rgba(223,211,202,0.82);
    }

    .rsvp-panel { position: relative; overflow: hidden; }
    .rsvp-glow {
      position: absolute;
      width: 220px;
      height: 220px;
      right: -70px;
      bottom: -70px;
      border-radius: 999px;
      background: radial-gradient(circle, rgba(255,214,222,0.58), transparent 70%);
      pointer-events: none;
    }

    .success {
      background: #eef8ef;
      border: 1px solid #c8e3cb;
      color: #255733;
      padding: 14px 16px;
      border-radius: 18px;
      margin-top: 16px;
    }

    .rsvp-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px; margin-top: 18px; }
    .field { display: flex; flex-direction: column; gap: 8px; }
    .field.full { grid-column: 1 / -1; }
    label { font-size: 13px; color: #6e635d; font-weight: 600; }
    input, select, textarea {
      width: 100%;
      padding: 14px 15px;
      border-radius: 18px;
      border: 1px solid rgba(120, 103, 93, 0.16);
      background: rgba(255,255,255,0.94);
      color: var(--text);
      font-size: 15px;
      outline: none;
    }
    input:focus, select:focus, textarea:focus {
      border-color: rgba(78,66,60,0.38);
      box-shadow: 0 0 0 4px rgba(78,66,60,0.08);
    }
    textarea { resize: vertical; min-height: 110px; }

    .rsvp-actions { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 16px; }
    .tiny-note { font-size: 13px; color: #7d716a; margin-top: 10px; }

    .faq-item {
      border-radius: 22px;
      background: rgba(255,255,255,0.90);
      border: 1px solid rgba(223,211,202,0.82);
      overflow: hidden;
      margin-bottom: 12px;
    }
    .faq-button {
      width: 100%;
      text-align: left;
      background: transparent;
      border: none;
      padding: 18px 20px;
      font-size: 16px;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .faq-answer { display: none; padding: 0 20px 18px; color: #5d544f; line-height: 1.75; }
    .faq-item.open .faq-answer { display: block; }

    .footer {
      text-align: center;
      color: #786c65;
      padding: 34px 10px 20px;
    }

    .reveal {
      opacity: 0;
      transform: translateY(22px) scale(0.985);
      transition: opacity 700ms ease, transform 700ms ease;
    }
    .reveal.show { opacity: 1; transform: translateY(0) scale(1); }

    .floating-rsvp {
      position: fixed;
      right: 18px;
      bottom: 18px;
      z-index: 25;
      display: none;
    }

    .music-toggle {
      position: fixed;
      left: 18px;
      bottom: 18px;
      z-index: 25;
      border-radius: 999px;
      background: rgba(255,255,255,0.78);
      backdrop-filter: blur(16px);
      border: 1px solid rgba(223,211,202,0.82);
      padding: 12px 14px;
      cursor: pointer;
      display: flex;
      gap: 8px;
      align-items: center;
      box-shadow: 0 10px 26px rgba(43,28,22,0.10);
    }

    @media (max-width: 980px) {
      .hero, .masonry, .grid-2, .grid-3, .moments-grid { grid-template-columns: 1fr; }
      .countdown, .rsvp-grid { grid-template-columns: repeat(2, 1fr); }
      .topbar { position: static; }
      .floating-rsvp { display: block; }
    }

    @media (max-width: 640px) {
      .countdown, .rsvp-grid { grid-template-columns: 1fr; }
      .timeline-item { grid-template-columns: 1fr; }
      h1 { line-height: 1.02; }
      .hero-left, .section-card, .story-panel, .invite-inner { padding: 22px; }
      .nav { justify-content: center; }
    }
    /* Modal & interactive extras */
    #rsvp-modal { display: none; position: fixed; inset: 0; z-index: 60; }
    .modal-backdrop { position: absolute; inset: 0; background: rgba(24,20,18,0.48); backdrop-filter: blur(6px); }
    .modal-card { position: absolute; left: 50%; top: 50%; transform: translate(-50%,-50%); width: min(720px, calc(100% - 36px)); border-radius: 18px; background: rgba(255,255,255,0.98); padding: 20px; box-shadow: 0 20px 60px rgba(24,20,18,0.28); }
    .modal-close { position: absolute; right: 12px; top: 10px; border: none; background: transparent; font-size: 18px; cursor: pointer; }
    .modal-content { max-height: 72vh; overflow: auto; }
    @media (max-width: 980px) { .modal-card { width: calc(100% - 28px); } }

    /* sparkle elements (bright, high-contrast for summer evening) */
    .sparkle {
      position: fixed;
      z-index: 55;
      pointer-events: none;
      opacity: 0.95;
      border-radius: 999px;
      transform: translate3d(0,0,0);
      will-change: transform, opacity;
      mix-blend-mode: screen;
      pointer-events: none;
    }

    /* dynamic accent variables (JS will update) */
    :root { --accent1: #ffd6de; --accent2: #efe7ff; }
    .btn-fun { background: linear-gradient(135deg, var(--accent1), var(--accent2)); }
  </style>
</head>
<body>
  <div class="ambient">
    <div class="blob one"></div>
    <div class="blob two"></div>
    <div class="blob three"></div>
    <div class="blob four"></div>
  </div>
  <!-- RSVP modal (hidden by default) -->
  <div id="rsvp-modal" aria-hidden="true">
    <div class="modal-backdrop" onclick="closeRsvpModal()"></div>
    <div class="modal-card">
      <button class="modal-close" onclick="closeRsvpModal()">✕</button>
      <div class="modal-content">
        <div class="eyebrow">RSVP</div>
        <h2 class="section-title">Quick RSVP</h2>
        <form id="rsvp-form-ajax">
          <div class="rsvp-grid">
            <div class="field">
              <label for="full_name_ajax">Full name</label>
              <input id="full_name_ajax" type="text" name="full_name" required placeholder="Your full name" />
            </div>
            <div class="field">
              <label for="attending_ajax">Attendance</label>
              <select id="attending_ajax" name="attending" required>
                <option value="">Select one</option>
                <option value="Yes">Yes, happily attending</option>
                <option value="No">Sorry, unable to attend</option>
                <option value="Maybe">Maybe</option>
              </select>
            </div>
            <div class="field">
              <label for="guest_count_ajax">Guest count</label>
              <select id="guest_count_ajax" name="guest_count" required>
                <option value="">Select one</option>
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
              </select>
            </div>
            <div class="field full">
              <label for="message_ajax">Message (optional)</label>
              <textarea id="message_ajax" name="message" placeholder="A note for the couple"></textarea>
            </div>
          </div>
          <div style="display:flex; gap:12px; margin-top:12px;">
            <button class="btn btn-primary" type="submit">Send RSVP</button>
            <button class="btn btn-secondary" type="button" onclick="closeRsvpModal()">Cancel</button>
          </div>
        </form>
        <div id="rsvp-ajax-success" class="success" style="display:none; margin-top:12px;">Thanks — your RSVP has been received.</div>
      </div>
    </div>
  </div>
  <div class="confetti" id="confetti"></div>
  <div class="stars" id="stars"></div>

  <div class="shell">
    <div class="topbar reveal">
      <nav class="nav">
        <a href="#details">Details</a>
        <a href="#dress-code">Dress Code</a>
        <a href="#schedule">Schedule</a>
        <a href="#rsvp">RSVP</a>
        <a href="#faq">FAQ</a>
        <button class="cta" type="button" onclick="scrollToSection('rsvp')">Respond</button>
      </nav>
    </div>

    <header class="hero">
      <div class="glass hero-left reveal">
        <div class="eyebrow">Modern wedding celebration · Seattle</div>
        <div class="headline-wrap">
          <h1>{{ wedding.couple_names }}</h1>
        </div>
        <div class="save-date-card">
          <div class="eyebrow" style="letter-spacing:0.18em;">Save the date</div>
          <div class="save-date-main">{{ wedding.date }}</div>
          <div class="save-date-sub">{{ wedding.time.split('·')[0].strip() }} · {{ wedding.venue }}</div>
          <div style="margin-top:10px;"><a class="btn btn-primary" href="#rsvp">RSVP</a></div>
        </div>
        <p class="hero-copy">{{ wedding.subheadline }} A small gathering of about {{ wedding.guest_count }}, a white wedding ceremony, formal pastels, and quiet Indian touches woven into a fresh Seattle celebration.</p>

        <div class="hero-actions">
          <button type="button" class="btn btn-primary" onclick="scrollToSection('rsvp')">RSVP now</button>
          <a class="btn btn-secondary" href="#schedule">See the evening flow</a>
          <button class="btn btn-fun" type="button" onclick="burst()">celebrate ✦</button>
        </div>

        <div class="countdown" id="countdown">
          <div class="count-box"><strong id="days">--</strong><span>Days</span></div>
          <div class="count-box"><strong id="hours">--</strong><span>Hours</span></div>
          <div class="count-box"><strong id="minutes">--</strong><span>Minutes</span></div>
          <div class="count-box"><strong id="seconds">--</strong><span>Seconds</span></div>
        </div>
      </div>

      <div class="hero-right reveal">
        <div class="invite-card card">
          <div class="invite-inner">
            <div class="eyebrow">Wedding Invitation</div>
            <div class="couple">{{ wedding.couple_names }}</div>
            <p class="section-copy" style="margin-bottom:18px;">request the pleasure of your company as they begin their next chapter together.</p>
            <div class="meta">
              <div><strong>{{ wedding.date }}</strong></div>
              <div>{{ wedding.time }}</div>
              <div>{{ wedding.venue }}</div>
              <div>{{ wedding.address }}</div>
              <div>{{ wedding.officiant }}</div>
            </div>
            <div style="height:1px;background:rgba(199,168,122,0.28);margin:22px 0;"></div>
            <div class="meta">
              <div><strong>RSVP by {{ wedding.rsvp_by }}</strong></div>
              <div style="margin-top:8px;">{{ wedding.no_gifts }}</div>
            </div>
          </div>
        </div>

        <div class="reactions">
          <div class="reaction"><span class="emoji">✨</span><div>soft glam</div><div class="label">wedding energy</div></div>
          <div class="reaction"><span class="emoji">🥂</span><div>toasts</div><div class="label">good company</div></div>
          <div class="reaction"><span class="emoji">💐</span><div>pastels</div><div class="label">formal dress code</div></div>
          <div class="reaction"><span class="emoji">🕊️</span><div>white wedding</div><div class="label">simple & elegant</div></div>
          <div class="reaction"><span class="emoji">🪩</span><div>dance floor</div><div class="label">joy encouraged</div></div>
        </div>

        <div class="marquee-wrap">
          <div class="marquee">
            {% for item in wedding.moments %}
              <span>{{ item }}</span>
            {% endfor %}
            {% for item in wedding.moments %}
              <span>{{ item }}</span>
            {% endfor %}
          </div>
        </div>
      </div>
    </header>

    <section id="details" class="reveal">
      <div class="grid-3">
        <div class="mini-card">
          <div class="eyebrow">Ceremony</div>
          <h3>Intimate white wedding</h3>
          <p class="section-copy">A warm, personal ceremony in our apartment community lounge with our closest people.</p>
        </div>
        <div class="mini-card">
          <div class="eyebrow">Vibe</div>
          <h3>Playful, modern, eventful</h3>
          <p class="section-copy">Less traditional card, more immersive celebration page — stylish, upbeat, and full of movement.</p>
        </div>
        <div class="mini-card">
          <div class="eyebrow">After</div>
          <h3>Dinner, desserts & music</h3>
          <p class="section-copy">Stay for food, desserts, toasts, dancing, and a cozy late-night finish with everyone together.</p>
        </div>
      </div>
    </section>

    <!-- (live guest list removed per preference) -->

    <section class="masonry reveal">
      <div class="section-card">
        <div class="eyebrow">Our celebration</div>
        <h2 class="section-title">Simple, intimate, and full of joy</h2>
        <p class="section-copy">{{ wedding.our_note }}</p>
        <p class="section-copy" style="margin-top:12px;">We wanted our wedding to feel elevated without feeling stiff — more alive, more us, and more like an experience guests can feel the second the page opens.</p>
        <div class="moments-grid">
          {% for item in wedding.moments %}
          <div class="moment">{{ item }}</div>
          {% endfor %}
        </div>
      </div>

      <div class="story-panel">
        <div class="eyebrow" style="color:rgba(255,255,255,0.62);">A note from us</div>
        <h2 class="section-title" style="color:white; margin-bottom:12px;">A little modern, a little traditional, fully us</h2>
        <p>We are celebrating in Seattle with a clean white ceremony, pastel formalwear, and subtle Indian touches that feel warm rather than overdone.</p>
        <p>The goal is simple: one beautiful night, a room full of love, and a website that feels like the party has already started.</p>
        <p>{{ wedding.no_gifts }}</p>
      </div>
    </section>

    <section id="dress-code" class="reveal">
      <div class="grid-2">
        <div class="section-card">
          <div class="eyebrow">Dress code</div>
          <h2 class="section-title">{{ wedding.dress_code_title }}</h2>
          <p class="section-copy"><strong>For women:</strong> {{ wedding.women_attire }}</p>
          <p class="section-copy" style="margin-top:12px;"><strong>For men:</strong> {{ wedding.men_attire }}</p>
          <p class="section-copy" style="margin-top:12px;">Aim for polished pastel looks. Indian and Western formalwear are equally welcome.</p>
        </div>
        <div class="section-card">
          <div class="eyebrow">Color inspiration</div>
          <h2 class="section-title">Pastel palette</h2>
          <div class="palette">
            <div class="swatch blush"><span></span>Blush</div>
            <div class="swatch.sage swatch sage"><span></span>Sage</div>
            <div class="swatch blue"><span></span>Powder Blue</div>
            <div class="swatch lilac"><span></span>Lilac</div>
            <div class="swatch champagne"><span></span>Champagne</div>
            <div class="swatch peach"><span></span>Peach</div>
          </div>
        </div>
      </div>
    </section>

    <section id="schedule" class="reveal">
      <div class="grid-1">
        <div class="section-card">
          <div class="eyebrow">Evening flow</div>
          <h2 class="section-title">A smooth, simple timeline</h2>
          <div class="timeline">
            {% for item in wedding.schedule %}
            <div class="timeline-item">
              <div class="timeline-time">{{ item.time }}</div>
              <div>
                <div style="font-weight:700; margin-bottom:4px;">{{ item.title }}</div>
                <div class="section-copy">{{ item.desc }}</div>
              </div>
            </div>
            {% endfor %}
          </div>
        </div>

        <!-- Playlist / moodboard removed per design preference -->
      </div>
    </section>

    <section id="rsvp" class="reveal">
      <div class="grid-2">
        <div class="section-card rsvp-panel">
          <div class="rsvp-glow"></div>
          <div class="eyebrow">RSVP</div>
          <h2 class="section-title">We can’t wait to celebrate with you</h2>
          <p class="section-copy">Please respond by <strong>{{ wedding.rsvp_by }}</strong>. Share your attendance, guest count, dietary needs, song request, and a note for us.</p>
          {% if success %}
            <div class="success">Thank you! Your RSVP has been submitted successfully.</div>
          {% endif %}
          <form method="POST" action="/rsvp">
            <div class="rsvp-grid">
              <div class="field">
                <label for="full_name">Full name</label>
                <input id="full_name" type="text" name="full_name" required placeholder="Your full name" />
              </div>
              <div class="field">
                <label for="attending">Attendance</label>
                <select id="attending" name="attending" required>
                  <option value="">Select one</option>
                  <option value="Yes">Yes, happily attending</option>
                  <option value="No">Sorry, unable to attend</option>
                  <option value="Maybe">Maybe</option>
                </select>
              </div>
              <div class="field">
                <label for="guest_count">Guest count</label>
                <select id="guest_count" name="guest_count" required>
                  <option value="">Select one</option>
                  <option value="1">1</option>
                  <option value="2">2</option>
                  <option value="3">3</option>
                  <option value="4">4</option>
                </select>
              </div>
              <div class="field">
                <label for="meal_preference">Meal preference</label>
                <select id="meal_preference" name="meal_preference">
                  <option value="">Optional</option>
                  <option value="Vegetarian">Vegetarian</option>
                  <option value="Non-Vegetarian">Non-Vegetarian</option>
                  <option value="Vegan">Vegan</option>
                  <option value="Other">Other</option>
                </select>
              </div>
              <div class="field full">
                <label for="dietary_restrictions">Dietary restrictions</label>
                <input id="dietary_restrictions" type="text" name="dietary_restrictions" placeholder="Allergies, restrictions, or special requests" />
              </div>
              <div class="field full">
                <label for="song_request">Song request</label>
                <input id="song_request" type="text" name="song_request" placeholder="Optional — a song you’d love to hear" />
              </div>
              <div class="field full">
                <label for="message">Message for the couple</label>
                <textarea id="message" name="message" placeholder="Optional"></textarea>
              </div>
            </div>
            <div class="rsvp-actions">
              <button class="btn btn-primary" type="submit">Submit RSVP</button>
              <button class="btn btn-secondary" type="button" onclick="downloadIcs()">Add to calendar</button>
              <button class="btn btn-fun" type="button" onclick="burst()">send sparkle</button>
            </div>
            <div class="tiny-note">{{ wedding.no_gifts }}</div>
          </form>
        </div>

        <div id="faq" class="section-card">
          <div class="eyebrow">Guest information</div>
          <h2 class="section-title">FAQ</h2>
          {% for item in wedding.faq %}
          <div class="faq-item">
            <button class="faq-button" type="button" onclick="toggleFaq(this)">
              <span>{{ item.q }}</span>
              <span>+</span>
            </button>
            <div class="faq-answer">{{ item.a }}</div>
          </div>
          {% endfor %}
          <div style="margin-top:18px; padding:18px; border-radius:20px; background:rgba(255,217,191,0.42); border:1px solid rgba(225,194,171,0.5);">
            <div style="font-weight:700; margin-bottom:6px;">Building note</div>
            <div class="section-copy">{{ wedding.parking_note }}</div>
          </div>
        </div>
      </div>
    </section>

    <footer class="footer reveal">
      <div class="eyebrow">With love</div>
      <div style="font-family: Georgia, 'Times New Roman', serif; font-size: 34px;">{{ wedding.couple_names }}</div>
      <p style="max-width:640px; margin:12px auto 0; line-height:1.8;">Thank you for being part of this chapter. We are excited to celebrate with you.</p>
    </footer>
  </div>

  <div class="floating-rsvp">
    <button type="button" class="btn btn-primary" onclick="scrollToSection('rsvp')">RSVP</button>
  </div>

  <button class="music-toggle" type="button" onclick="toggleMood(this)">
    <span id="music-icon">♪</span>
    <span id="music-text">mood on</span>
  </button>

  <script>
    function scrollToSection(id) {
      document.getElementById(id).scrollIntoView({ behavior: 'smooth' });
    }

    function toggleFaq(button) {
      const item = button.closest('.faq-item');
      item.classList.toggle('open');
      button.querySelector('span:last-child').textContent = item.classList.contains('open') ? '–' : '+';
    }

    function setupReveal() {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) entry.target.classList.add('show');
        });
      }, { threshold: 0.12 });
      document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));
    }

    function setupCountdown() {
      const targetDate = new Date('{{ wedding.date }} {{ wedding.time.split("·")[0].strip() }}');
      const safeTarget = isNaN(targetDate.getTime()) ? new Date(Date.now() + 15 * 24 * 60 * 60 * 1000) : targetDate;
      function tick() {
        const diff = Math.max(0, safeTarget - new Date());
        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
        const minutes = Math.floor((diff / (1000 * 60)) % 60);
        const seconds = Math.floor((diff / 1000) % 60);
        document.getElementById('days').textContent = days;
        document.getElementById('hours').textContent = hours;
        document.getElementById('minutes').textContent = minutes;
        document.getElementById('seconds').textContent = seconds;
      }
      tick();
      setInterval(tick, 1000);
    }

    function setupParticles() {
      const confetti = document.getElementById('confetti');
      const stars = document.getElementById('stars');
      const colors = ['rgba(255,214,222,0.8)', 'rgba(255,217,191,0.8)', 'rgba(217,239,217,0.8)', 'rgba(229,221,255,0.8)', 'rgba(216,235,255,0.8)'];
      for (let i = 0; i < 22; i++) {
        const dot = document.createElement('div');
        dot.className = 'dot';
        const size = Math.random() * 10 + 6;
        dot.style.width = size + 'px';
        dot.style.height = size + 'px';
        dot.style.left = Math.random() * 100 + 'vw';
        dot.style.bottom = (-10 - Math.random() * 80) + 'px';
        dot.style.background = colors[i % colors.length];
        dot.style.animationDuration = (12 + Math.random() * 12) + 's';
        dot.style.animationDelay = (-Math.random() * 20) + 's';
        confetti.appendChild(dot);
      }
      for (let i = 0; i < 30; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.textContent = i % 3 === 0 ? '✦' : '·';
        star.style.left = Math.random() * 100 + 'vw';
        star.style.top = Math.random() * 100 + 'vh';
        star.style.animationDelay = (-Math.random() * 5) + 's';
        star.style.fontSize = (Math.random() * 10 + 10) + 'px';
        stars.appendChild(star);
      }
    }

    function burst() {
      const confetti = document.getElementById('confetti');
      const colors = ['#ffd6de', '#ffd9bf', '#d9efd9', '#e5ddff', '#d8ebff'];
      for (let i = 0; i < 18; i++) {
        const piece = document.createElement('div');
        piece.className = 'dot';
        const size = Math.random() * 12 + 7;
        piece.style.width = size + 'px';
        piece.style.height = size + 'px';
        piece.style.left = (45 + Math.random() * 10) + 'vw';
        piece.style.bottom = '12vh';
        piece.style.background = colors[i % colors.length];
        piece.style.animationDuration = (4 + Math.random() * 3) + 's';
        confetti.appendChild(piece);
        setTimeout(() => piece.remove(), 6500);
      }
    }

    // Interactive: summer fireflies, dynamic accent color, modal RSVP (AJAX)
    function createSparkle() {
      // bright, short-lived sparkle that stands out against the warm background
      const el = document.createElement('div');
      el.className = 'sparkle';
      const size = 14 + Math.random() * 36; // larger sparkles
      el.style.width = size + 'px';
      el.style.height = size + 'px';
      el.style.left = Math.random() * 100 + 'vw';
      el.style.top = Math.random() * 70 + 'vh';
      el.style.background = 'radial-gradient(circle at 30% 30%, rgba(255,255,250,1), rgba(255,235,160,0.98) 40%, rgba(255,200,90,0.25) 70%)';
      el.style.boxShadow = '0 0 44px rgba(255,235,160,0.98), 0 0 12px rgba(255,200,90,0.64)';
      el.style.borderRadius = '50%';
      el.style.opacity = '0';
      document.body.appendChild(el);
      const duration = 800 + Math.random() * 1000; // short and noticeable
      // sparkle pulse + gentle drift
      el.animate([
        { transform: 'translateY(0vh) scale(0.7)', opacity: 0 },
        { transform: `translateY(${6 + Math.random()*8}vh) scale(1.05)`, opacity: 1 },
        { transform: `translateY(${14 + Math.random()*18}vh) scale(0.85)`, opacity: 0 }
      ], { duration: duration, easing: 'cubic-bezier(.2,.9,.3,1)', iterations: 1 });
      setTimeout(() => el.remove(), duration + 80);
      return el;
    }

    function startSparkles(rate = 420) {
      const starter = setInterval(() => createSparkle(), rate);
      return starter;
    }

    // dynamic accent: slow, warm color shift for a summer vibe
    (function startAccentShift(){
      let h = 28; // start warm
      setInterval(() => {
        h = (h + 0.6) % 360;
        const a1 = `hsl(${h} 86% 90%)`;
        const a2 = `hsl(${(h+28)%360} 88% 84%)`;
        document.documentElement.style.setProperty('--accent1', a1);
        document.documentElement.style.setProperty('--accent2', a2);
      }, 1200);
    })();

    // modal helpers
    function openRsvpModal() {
      const modal = document.getElementById('rsvp-modal');
      if (!modal) return;
      modal.style.display = 'block';
      modal.setAttribute('aria-hidden', 'false');
      const first = modal.querySelector('input,textarea,select');
      if (first) first.focus();
    }
    function closeRsvpModal() {
      const modal = document.getElementById('rsvp-modal');
      if (!modal) return;
      modal.style.display = 'none';
      modal.setAttribute('aria-hidden', 'true');
    }

    // AJAX RSVP endpoint: submit the modal form via fetch to /api/rsvp
    document.addEventListener('DOMContentLoaded', () => {
      const ajaxForm = document.getElementById('rsvp-form-ajax');
      if (ajaxForm) {
        ajaxForm.addEventListener('submit', async (ev) => {
          ev.preventDefault();
          const fd = new FormData(ajaxForm);
          try {
            const res = await fetch('/api/rsvp', { method: 'POST', body: fd });
            const json = await res.json();
            if (json && json.success) {
              const success = document.getElementById('rsvp-ajax-success');
              if (success) success.style.display = 'block';
              burst();
              // short sparkle burst for celebration
              for (let i=0;i<20;i++) setTimeout(()=>createSparkle(), i*60);
              setTimeout(() => { if (success) success.style.display = 'none'; closeRsvpModal(); ajaxForm.reset(); }, 1400);
            }
          } catch (e) { console.error('ajax rsvp', e); }
        });
      }

      // convert RSVP buttons to open modal when appropriate
      document.querySelectorAll('.btn.btn-primary').forEach(btn => {
        if (btn.textContent && btn.textContent.toLowerCase().includes('rsvp')) {
          btn.addEventListener('click', (e) => { e.preventDefault(); openRsvpModal(); });
        }
      });

  // start a gentle field of sparkles for ambience
  setTimeout(() => startSparkles(700), 600);
    });

    let moodOn = true;
    function toggleMood(button) {
      moodOn = !moodOn;
      document.body.style.animationPlayState = moodOn ? 'running' : 'paused';
      document.getElementById('music-icon').textContent = moodOn ? '♪' : '⏸';
      document.getElementById('music-text').textContent = moodOn ? 'mood on' : 'mood paused';
    }

    function downloadIcs() {
      const ics = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//Wedding Invite//EN',
        'BEGIN:VEVENT',
        'SUMMARY:{{ wedding.couple_names }} Wedding',
        'LOCATION:{{ wedding.venue }}',
        'DESCRIPTION:Intimate wedding celebration in Seattle',
        'END:VEVENT',
        'END:VCALENDAR'
      ].join('\n');
      const blob = new Blob([ics], { type: 'text/calendar;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'wedding-invitation.ics';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    }

    window.addEventListener('DOMContentLoaded', () => {
      setupReveal();
      setupCountdown();
      setupParticles();
      const firstFaq = document.querySelector('.faq-item');
      if (firstFaq) {
        firstFaq.classList.add('open');
        const icon = firstFaq.querySelector('.faq-button span:last-child');
        if (icon) icon.textContent = '–';
      }
    });
  </script>
</body>
</html>
"""


def initialize_csv() -> None:
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "timestamp",
                "full_name",
                "attending",
                "guest_count",
                "meal_preference",
                "dietary_restrictions",
                "song_request",
                "message",
            ])


@app.route("/", methods=["GET"])
def home():
    success = request.args.get("success") == "1"
    return render_template_string(HTML, wedding=WEDDING, success=success)


@app.route("/rsvp", methods=["POST"])
def rsvp():
    initialize_csv()
    response = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "full_name": request.form.get("full_name", "").strip(),
        "attending": request.form.get("attending", "").strip(),
        "guest_count": request.form.get("guest_count", "").strip(),
        "meal_preference": request.form.get("meal_preference", "").strip(),
        "dietary_restrictions": request.form.get("dietary_restrictions", "").strip(),
        "song_request": request.form.get("song_request", "").strip(),
        "message": request.form.get("message", "").strip(),
    }
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            response["timestamp"],
            response["full_name"],
            response["attending"],
            response["guest_count"],
            response["meal_preference"],
            response["dietary_restrictions"],
            response["song_request"],
            response["message"],
        ])
    return redirect(url_for("home", success="1") + "#rsvp")


@app.route("/api/rsvp", methods=["POST"])
def api_rsvp():
  """Accept RSVP via AJAX (FormData) and return JSON."""
  initialize_csv()
  # support both form and multipart FormData the same way
  response = {
    "timestamp": datetime.now().isoformat(timespec="seconds"),
    "full_name": request.form.get("full_name", "").strip(),
    "attending": request.form.get("attending", "").strip(),
    "guest_count": request.form.get("guest_count", "").strip(),
    "meal_preference": request.form.get("meal_preference", "").strip(),
    "dietary_restrictions": request.form.get("dietary_restrictions", "").strip(),
    "song_request": request.form.get("song_request", "").strip(),
    "message": request.form.get("message", "").strip(),
  }
  with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([
      response["timestamp"],
      response["full_name"],
      response["attending"],
      response["guest_count"],
      response["meal_preference"],
      response["dietary_restrictions"],
      response["song_request"],
      response["message"],
    ])
  return jsonify({"success": True})


@app.route("/api/rsvps", methods=["GET"])
def api_rsvps():
    initialize_csv()
    rows = []
    with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    return jsonify(rows)


if __name__ == "__main__":
    initialize_csv()
    app.run(debug=True)
