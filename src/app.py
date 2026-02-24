from flask import Flask, request, Response, render_template
from xml.sax.saxutils import escape

app = Flask(__name__)

THEMES = {
    "midnight": {
        "page_bg": "#1f1f1f",  # outer dark background
        "card_bg": "#031126",  # deep navy
        "border": "#2b3340",  # inner border stroke
        "fg": "#d7dbe2",  # bright text
        "muted": "#7b8494",  # medium gray labels
        "muted2": "#5e6674",  # darker muted numbers
        "accent": "#76d9f4",  # cyan numbers/name
        "accent2": "#f1c40f",  # logo yellow
    }
}


@app.get("/")
@app.get("/builder")
def builder():
    return render_template("builder.html")


@app.get("/api/monkeytype.svg")
def monkeytype_svg():
    username = request.args.get("username", "guest").strip()
    theme_name = request.args.get("theme", "midnight").strip()
    wordValue = request.args.get("wordValue", "10")
    timeValue = request.args.get("timeValue", "15")

    # basic validation
    if not username:
        username = "user"

    if theme_name not in THEMES:
        theme_name = "dark"

    if not timeValue.isdigit() or not wordValue.isdigit():
        return Response("Invalid time or word value", status=400)

    # fake data for now
    wpm1 = 128
    wpm2 = 166
    left_acc = 98.4
    right_acc = 100

    theme = THEMES[theme_name]
    username_esc = escape(username)

    svg = render_monkeytype_card(
        username=username,
        mode_label="time typing",
        left_stat=128,
        right_stat=166,
        left_acc=100,
        right_acc=100,
        secondCount=timeValue,
        wordCount=wordValue,
        theme=THEMES["midnight"],
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

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="980" height="360" viewBox="0 0 980 360">
  <!-- Outer background -->
  <rect x="0" y="0" width="980" height="360" rx="34" fill="{theme["page_bg"]}"/>

  <!-- Main card -->
  <rect x="26" y="26" width="928" height="308" rx="28" fill="{theme["card_bg"]}" stroke="{theme["border"]}" stroke-width="4"/>

  <!-- Header -->
  <g>
    <!-- Simple logo pill placeholder -->
    <rect x="290" y="56" width="88" height="44" rx="12" fill="none" stroke="{theme["accent2"]}" stroke-width="4"/>
    <text x="392" y="89" fill="{theme["muted2"]}" font-size="34" font-weight="700"
          font-family="Inter, Segoe UI, Arial, sans-serif">monkeytype</text>
  </g>

  <!-- Left profile section -->
  <g>
    <text x="96" y="192" fill="{theme["accent"]}" font-size="72" font-weight="700"
          font-family="Inter, Segoe UI, Arial, sans-serif">{username_esc}</text>

    <text x="98" y="232" fill="{theme["muted"]}" font-size="28"
          font-family="Inter, Segoe UI, Arial, sans-serif">{mode_esc}</text>

    <text x="98" y="288" fill="{theme["fg"]}" font-size="54" font-weight="600"
          font-family="Inter, Segoe UI, Arial, sans-serif">21:27:19</text>
  </g>

  <!-- Middle stat column -->
  <g>
    <text x="460" y="142" fill="{theme["muted"]}" font-size="30"
          font-family="Inter, Segoe UI, Arial, sans-serif">{secondCount} seconds</text>

    <text x="450" y="232" fill="{theme["accent"]}" font-size="92" font-weight="700"
          font-family="Inter, Segoe UI, Arial, sans-serif">{left_stat}</text>

    <text x="476" y="304" fill="{theme["muted2"]}" font-size="58" font-weight="500"
          font-family="Inter, Segoe UI, Arial, sans-serif">{left_acc}%</text>
  </g>

  <!-- Right stat column -->
  <g>
    <text x="706" y="142" fill="{theme["muted"]}" font-size="30"
          font-family="Inter, Segoe UI, Arial, sans-serif">{wordCount} words</text>

    <text x="690" y="232" fill="{theme["accent"]}" font-size="92" font-weight="700"
          font-family="Inter, Segoe UI, Arial, sans-serif">{right_stat}</text>

    <text x="706" y="304" fill="{theme["muted"]}" font-size="58" font-weight="500"
          font-family="Inter, Segoe UI, Arial, sans-serif">{right_acc}%</text>
  </g>
</svg>'''
    return svg


if __name__ == "__main__":
    app.run(debug=True)
