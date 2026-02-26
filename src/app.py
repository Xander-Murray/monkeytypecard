import json
import os
from flask import Flask, request, Response, render_template, jsonify
from xml.sax.saxutils import escape
import services.monkeytype

app = Flask(__name__)

THEMES_PATH = os.path.join(app.static_folder, "themes.json")
with open(THEMES_PATH) as f:
    THEMES_LIST = json.load(f)

THEMES = {t["name"]: t for t in THEMES_LIST}


def theme_to_card_colors(t):
    """Map a monkeytype theme to SVG card colors."""
    return {
        "page_bg": t.get("subAltColor", t["bgColor"]),
        "card_bg": t["bgColor"],
        "border": t.get("subColor", "#2b3340"),
        "fg": t["textColor"],
        "muted": t.get("subColor", "#7b8494"),
        "accent": t["mainColor"],
        "accent2": t.get("caretColor", t["mainColor"]),
    }


@app.get("/")
@app.get("/builder")
def builder():
    return render_template("builder.html")


@app.get("/api/themes")
def api_themes():
    """Return the list of themes for the frontend."""
    compact = [
        {
            "name": t["name"],
            "bgColor": t["bgColor"],
            "mainColor": t["mainColor"],
            "subColor": t.get("subColor", "#666"),
            "textColor": t["textColor"],
            "subAltColor": t.get("subAltColor", t["bgColor"]),
        }
        for t in THEMES_LIST
    ]
    return jsonify(compact)


@app.get("/monkeytype.svg")
def monkeytype_svg():
    username = request.args.get("username", "guest").strip()
    theme_name = request.args.get("theme", "serika_dark").strip()
    wordValue = request.args.get("wordValue", "10")
    timeValue = request.args.get("timeValue", "15")

    if not username:
        username = "user"

    if theme_name not in THEMES:
        theme_name = "serika_dark"

    if not timeValue.isdigit() or not wordValue.isdigit():
        return Response("Invalid time or word value", status=400)

    theme = theme_to_card_colors(THEMES[theme_name])

    svg = render_monkeytype_card(
        username=username,
        mode_label="time typing",
        left_stat=128,
        right_stat=166,
        left_acc=100,
        right_acc=100,
        secondCount=timeValue,
        wordCount=wordValue,
        theme=theme,
    )
    resp = Response(svg, mimetype="image/svg+xml")
    resp.headers["Cache-Control"] = "public, max-age=300"
    return resp


def render_monkeytype_card(
    username,
    mode_label,
    left_stat,
    right_stat,
    left_acc,
    right_acc,
    secondCount,
    wordCount,
    theme,
):
    username_esc = escape(username)
    mode_esc = escape(mode_label)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="495" height="180" viewBox="0 0 990 360">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Lexend+Deca:wght@300;400;500;600;700&amp;display=swap');
    </style>
  </defs>

  <!-- Outer background -->
  <rect width="990" height="360" rx="20" fill="{theme["page_bg"]}"/>

  <!-- Main card -->
  <rect x="16" y="16" width="958" height="328" rx="16" fill="{theme["card_bg"]}" stroke="{theme["border"]}" stroke-width="2" stroke-opacity="0.5"/>

  <!-- Header: logo + wordmark -->
  <g transform="translate(56, 48)">
    <g transform="scale(0.12) translate(680, 1030)" fill="{theme["accent2"]}">
      <path d="M -430 -910 L -430 -910 C -424.481 -910 -420 -905.519 -420 -900 L -420 -900 C -420 -894.481 -424.481 -890 -430 -890 L -430 -890 C -435.519 -890 -440 -894.481 -440 -900 L -440 -900 C -440 -905.519 -435.519 -910 -430 -910 Z"/>
      <path d="M -570 -910 L -510 -910 C -504.481 -910 -500 -905.519 -500 -900 L -500 -900 C -500 -894.481 -504.481 -890 -510 -890 L -570 -890 C -575.519 -890 -580 -894.481 -580 -900 L -580 -900 C -580 -905.519 -575.519 -910 -570 -910 Z"/>
      <path d="M -590 -970 L -590 -970 C -584.481 -970 -580 -965.519 -580 -960 L -580 -940 C -580 -934.481 -584.481 -930 -590 -930 L -590 -930 C -595.519 -930 -600 -934.481 -600 -940 L -600 -960 C -600 -965.519 -595.519 -970 -590 -970 Z"/>
      <path d="M -639.991 -960.515 C -639.72 -976.836 -626.385 -990 -610 -990 L -610 -990 C -602.32 -990 -595.31 -987.108 -590 -982.355 C -584.69 -987.108 -577.68 -990 -570 -990 L -570 -990 C -553.615 -990 -540.28 -976.836 -540.009 -960.515 C -540.001 -960.345 -540 -960.172 -540 -960 L -540 -960 L -540 -940 C -540 -934.481 -544.481 -930 -550 -930 L -550 -930 C -555.519 -930 -560 -934.481 -560 -940 L -560 -960 L -560 -960 C -560 -965.519 -564.481 -970 -570 -970 C -575.519 -970 -580 -965.519 -580 -960 L -580 -960 L -580 -960 L -580 -940 C -580 -934.481 -584.481 -930 -590 -930 L -590 -930 C -595.519 -930 -600 -934.481 -600 -940 L -600 -960 L -600 -960 L -600 -960 L -600 -960 L -600 -960 L -600 -960 L -600 -960 L -600 -960 C -600 -965.519 -604.481 -970 -610 -970 C -615.519 -970 -620 -965.519 -620 -960 L -620 -960 L -620 -940 C -620 -934.481 -624.481 -930 -630 -930 L -630 -930 C -635.519 -930 -640 -934.481 -640 -940 L -640 -960 L -640 -960 C -640 -960.172 -639.996 -960.344 -639.991 -960.515 Z"/>
      <path d="M -460 -930 L -460 -900 C -460 -894.481 -464.481 -890 -470 -890 L -470 -890 C -475.519 -890 -480 -894.481 -480 -900 L -480 -930 L -508.82 -930 C -514.99 -930 -520 -934.481 -520 -940 L -520 -940 C -520 -945.519 -514.99 -950 -508.82 -950 L -431.18 -950 C -425.01 -950 -420 -945.519 -420 -940 L -420 -940 C -420 -934.481 -425.01 -930 -431.18 -930 L -460 -930 Z"/>
      <path d="M -470 -990 L -430 -990 C -424.481 -990 -420 -985.519 -420 -980 L -420 -980 C -420 -974.481 -424.481 -970 -430 -970 L -470 -970 C -475.519 -970 -480 -974.481 -480 -980 L -480 -980 C -480 -985.519 -475.519 -990 -470 -990 Z"/>
      <path d="M -630 -910 L -610 -910 C -604.481 -910 -600 -905.519 -600 -900 L -600 -900 C -600 -894.481 -604.481 -890 -610 -890 L -630 -890 C -635.519 -890 -640 -894.481 -640 -900 L -640 -900 C -640 -905.519 -635.519 -910 -630 -910 Z"/>
      <path d="M -515 -990 L -510 -990 C -504.481 -990 -500 -985.519 -500 -980 L -500 -980 C -500 -974.481 -504.481 -970 -510 -970 L -515 -970 C -520.519 -970 -525 -974.481 -525 -980 L -525 -980 C -525 -985.519 -520.519 -990 -515 -990 Z"/>
      <path d="M -660 -910 L -680 -910 L -680 -980 C -680 -1007.596 -657.596 -1030 -630 -1030 L -430 -1030 C -402.404 -1030 -380 -1007.596 -380 -980 L -380 -900 C -380 -872.404 -402.404 -850 -430 -850 L -630 -850 C -657.596 -850 -680 -872.404 -680 -900 L -680 -920 L -660 -920 L -660 -900 C -660 -883.443 -646.557 -870 -630 -870 L -430 -870 C -413.443 -870 -400 -883.443 -400 -900 L -400 -980 C -400 -996.557 -413.443 -1010 -430 -1010 L -630 -1010 C -646.557 -1010 -660 -996.557 -660 -980 L -660 -910 Z"/>
    </g>
    <text x="46" y="20" fill="{theme["muted"]}" font-size="26" font-weight="400" letter-spacing="1"
          font-family="Lexend Deca, Inter, Segoe UI, sans-serif" opacity="0.8">monkeytype</text>
  </g>

  <!-- Thin divider under header -->
  <line x1="56" y1="88" x2="934" y2="88" stroke="{theme["border"]}" stroke-width="1" stroke-opacity="0.3"/>

  <!-- Left: username -->
  <g>
    <text x="56" y="142" fill="{theme["accent"]}" font-size="52" font-weight="700" letter-spacing="-1"
          font-family="Lexend Deca, Inter, Segoe UI, sans-serif">{username_esc}</text>
  </g>

  <!-- Vertical divider -->
  <line x1="420" y1="100" x2="420" y2="330" stroke="{theme["border"]}" stroke-width="1" stroke-opacity="0.3"/>

  <!-- Time stat column -->
  <g>
    <text x="468" y="130" fill="{theme["muted"]}" font-size="18" font-weight="400" letter-spacing="2"
          font-family="Lexend Deca, Inter, Segoe UI, sans-serif" opacity="0.6">{secondCount} seconds</text>

    <text x="468" y="210" fill="{theme["accent"]}" font-size="80" font-weight="700" letter-spacing="-2"
          font-family="Lexend Deca, Inter, Segoe UI, sans-serif">{left_stat}</text>
    <text x="470" y="240" fill="{theme["muted"]}" font-size="18" font-weight="400" letter-spacing="1"
          font-family="Lexend Deca, Inter, Segoe UI, sans-serif" opacity="0.5">wpm</text>

    <text x="468" y="300" fill="{theme["fg"]}" font-size="38" font-weight="500" letter-spacing="-1"
          font-family="Lexend Deca, Inter, Segoe UI, sans-serif" opacity="0.9">{left_acc}%</text>
    <text x="470" y="326" fill="{theme["muted"]}" font-size="16" font-weight="400" letter-spacing="1"
          font-family="Lexend Deca, Inter, Segoe UI, sans-serif" opacity="0.5">acc</text>
  </g>

  <!-- Vertical divider -->
  <line x1="700" y1="100" x2="700" y2="330" stroke="{theme["border"]}" stroke-width="1" stroke-opacity="0.3"/>

  <!-- Words stat column -->
  <g>
    <text x="748" y="130" fill="{theme["muted"]}" font-size="18" font-weight="400" letter-spacing="2"
          font-family="Lexend Deca, Inter, Segoe UI, sans-serif" opacity="0.6">{wordCount} words</text>

    <text x="748" y="210" fill="{theme["accent"]}" font-size="80" font-weight="700" letter-spacing="-2"
          font-family="Lexend Deca, Inter, Segoe UI, sans-serif">{right_stat}</text>
    <text x="750" y="240" fill="{theme["muted"]}" font-size="18" font-weight="400" letter-spacing="1"
          font-family="Lexend Deca, Inter, Segoe UI, sans-serif" opacity="0.5">wpm</text>

    <text x="748" y="300" fill="{theme["fg"]}" font-size="38" font-weight="500" letter-spacing="-1"
          font-family="Lexend Deca, Inter, Segoe UI, sans-serif" opacity="0.9">{right_acc}%</text>
    <text x="750" y="326" fill="{theme["muted"]}" font-size="16" font-weight="400" letter-spacing="1"
          font-family="Lexend Deca, Inter, Segoe UI, sans-serif" opacity="0.5">acc</text>
  </g>

  <!-- Bottom-left joined time -->
    <text x="58" y="280" fill="{theme["muted"]}" font-size="20" font-weight="400" letter-spacing="2"
          font-family="Lexend Deca, Inter, Segoe UI, sans-serif" opacity="0.7">{mode_esc}</text>
  <text x="58" y="316" fill="{theme["fg"]}" font-size="32" font-weight="300" letter-spacing="1" opacity="0.4"
        font-family="Lexend Deca, Inter, Segoe UI, sans-serif">21:27:19</text>
</svg>'''
    return svg


if __name__ == "__main__":
    app.run(debug=True)
