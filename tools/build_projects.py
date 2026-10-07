"""Builds the series pages in ../projects/ from the data below.

Run: python3 tools/build_projects.py
Edit the text here, then re-run.
"kind": "h" = horizontal 16:9, "v" = vertical 9:16, "dual" = framed for both.
"""
import html
import math
import os

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "projects")
os.makedirs(OUT, exist_ok=True)


def esc(s):
    return html.escape(s, quote=False)


PROJECTS = [
    {
        "slug": "last-signal",
        "kind": "h",
        "theme": "beacon",
        "title": "Last Signal",
        "key": "last-signal-key.jpg",
        "key_pos": "72% 50%",
        "key_alt": "A lone figure in a spacesuit on Triton's frozen plain before the Halcyon Relay tower, an orange beacon at its top beneath Neptune.",
        "logline": "Three years after Earth went silent, the last engineer on a relay station at the edge of the solar system receives a message from home, in her own voice.",
        "facts": [("Genre", "Science-fiction mystery"), ("Format", "Horizontal, 6 episodes of 12 minutes"), ("Status", "In development")],
        "synopsis": [
            "Halcyon Relay sits on the frozen plain of Triton, Neptune's largest moon, four light-hours from Earth. For eleven years it passed messages between the inner planets and the probes beyond. Three years ago every transmission from Earth stopped in the middle of a sentence. The crew went home on the last supply ship. Mara Iven stayed.",
            "She keeps the dishes turning, logs the silence every night and rations what the ship left behind. Her only company is ORRA, the station's maintenance system, which has started to repeat itself: the same weather report twice, the same greeting an hour apart.",
            "Then the array catches a signal from the direction of Earth. It is Mara's voice. It describes, minute by minute, what she will do tomorrow, and begs her not to reply. The next day, everything it described happens.",
            "Every message takes four hours to arrive, and four more for an answer to come back. Mara has to decide whether the voice is a warning, a trap, or proof that she is no longer the only version of herself out here, and what it will cost to answer.",
            "Each episode ends on a message sent and opens four hours later, when the reply lands. The delay is the clock the whole series runs on.",
        ],
        "rule": "Nothing travels faster than light. Every conversation with home takes eight hours, so no one on Triton can interrupt, argue or take anything back.",
        "cast": [
            ("Mara Iven", "Relay engineer, 41", "Methodical, funny when no one is listening, three years past the end of her rotation. She stayed because someone had to, and because nobody at home was waiting for her."),
            ("ORRA", "Station system", "Polite, literal and slowly degrading. The closest thing Mara has to a friend, and the only witness to what she does at night."),
            ("The Voice", "Signal from Earth", "Mara's own voice, four hours late. It knows things she hasn't done yet, and it sounds tired."),
        ],
        "episodes_title": "Episodes",
        "episodes": [
            ("1", "Silence", "A routine night on Halcyon ends with a signal nobody should be sending."),
            ("2", "Delay", "Mara replies against the voice's warning. Four hours later, the answer arrives before her question."),
            ("3", "Echo", "ORRA's logs show walks along the array that Mara doesn't remember taking."),
            ("4", "Handshake", "The signal asks for the station's access codes. It already knows half of them."),
            ("5", "Origin", "Mara traces the source. It is not Earth. It is much closer."),
            ("6", "Reply", "One transmission left. Mara decides what the last signal will say."),
        ],
        "frames_title": "The opening, 30 seconds",
        "frames_note": "",
        "frames": [
            ("0–5 s", "Black. Static. A voice, Mara's, says one word: “Don't.”", {"fx": "static", "sub": "“Don't.”"}),
            ("5–11 s", "Extreme wide: the array on Triton's plain, Neptune overhead, one orange light blinking.", {"at": (50, 50, 1)}),
            ("11–17 s", "Mara walks the length of the array. Her breath fogs the visor.", {"at": (75, 82, 3.2)}),
            ("17–24 s", "Intercut: a waveform on screen, her lips, the same waveform.", {"at": (83, 16, 2.4), "fx": "wave"}),
            ("24–30 s", "She answers. The voice answers at the same moment. Cut to black. Title.", {"fx": "title", "text": "Last Signal"}),
        ],
    },
    {
        "slug": "backup",
        "kind": "v",
        "theme": "mirror",
        "title": "Backup",
        "key": "backup-key.jpg",
        "key_pos": "50% 50%",
        "key_alt": "A rain-soaked canyon of towers in Meridian Stack; a courier on a sky-bridge faces a lit window where someone with her face stands.",
        "logline": "In a city where memories are backed up every night, a courier survives an accident two minutes before the backup, and comes home to find her restored copy already living her life.",
        "facts": [("Genre", "Science-fiction thriller"), ("Format", "Vertical, 60 episodes of 90 seconds"), ("Status", "In development")],
        "synopsis": [
            "Meridian Stack is a vertical city of four-hundred-floor towers joined by sky-bridges, where it hasn't stopped raining in living memory. At 03:00 every night, MIRROR, the city's memory archive, backs up every resident. Lose your body in an accident and MIRROR restores you by morning. Death has started to feel optional.",
            "Noor Vance, a night-shift courier, is in a falling lift at 02:58. She survives. MIRROR logs her death anyway and restores her from the previous night's backup. When Noor limps home, her scanner refuses her ID: “Recipient already delivered.” Through the window, someone with her face is making breakfast.",
            "The archive keeps one copy of each person and deletes duplicates after 72 hours. To stay alive, Noor has to prove she is the original, while the restored Noor, who is missing a day and doesn't know it, is just as certain she is.",
            "That missing day is the key. Whatever Noor delivered in those twenty-four hours is the reason the lift fell. Every 90-second episode ends on a cut, a reveal or a countdown.",
        ],
        "rule": "MIRROR keeps one copy of each person. A backup is legally you, and anything that happened after the last backup legally didn't.",
        "cast": [
            ("Noor Vance", "Night courier, 26", "Knows every shortcut in the Stack and never misses a delivery. She is carrying a day the city has no record of."),
            ("Noor, restored", "MIRROR restoration", "Identical, rested and fully registered. Believes the woman at the door is a glitch, or a thief wearing her face."),
            ("Ezra Kade", "MIRROR technician", "Has deleted hundreds of duplicates without a second look. Notices that MIRROR logged Noor's death, but no one logged the lift failure that caused it."),
        ],
        "episodes_title": "Season arc",
        "episodes": [
            ("1–20", "Displaced", "Locked out of her own life, Noor has 72 hours, no valid ID and a city that no longer recognises her."),
            ("21–40", "The Mirror", "Inside the archive, Noor and Ezra find thousands of residents who have been restored more than once."),
            ("41–60", "Merge", "The two Noors must choose: one of them survives, or both become something MIRROR can't delete."),
        ],
        "frames_title": "Episode 1, the first four shots",
        "frames_note": "",
        "frames": [
            ("", "Top-down: Noor rides the sky-bridges at 02:55, rain on her visor.", {"at": (44, 53, 2.4)}),
            ("", "02:58. The lift drops. Cut to black.", {"at": (50, 55, 1.3), "fx": "dark", "hud": "02:58"}),
            ("", "Morning. Her scanner flashes red: “Recipient already delivered.”", {"at": (52, 36, 1.8), "fx": "dark", "hud": "Recipient already delivered", "alert": True}),
            ("", "Across the bridge, a lit window: someone with her face. Two hands meet on either side of the glass.", {"at": (80, 51, 3)}),
        ],
    },
    {
        "slug": "ark-of-sand",
        "kind": "dual",
        "theme": "dune",
        "title": "Ark of Sand",
        "key": "ark-of-sand-key.jpg",
        "key_pos": "70% 50%",
        "key_alt": "A colossal colony ship half-buried in the dunes of Hesper at dusk; cyan light spills from a hatch; a hooded salvager watches from a crest.",
        "logline": "A young salvager cuts into a buried colony ship and wakes its AI, which has waited three hundred years for four thousand passengers and decides the salvager is the first.",
        "facts": [("Genre", "Science-fiction adventure"), ("Format", "Horizontal with vertical cut-downs, 8 episodes of 8 minutes"), ("Status", "In development")],
        "synopsis": [
            "Hesper was meant to be green by now. Three centuries ago the colony programme was cancelled, the terraformers were shut down, and the people already on the ground were left with a planet that stayed desert. Their descendants travel in caravans and live by salvaging what the programme left behind.",
            "Rook, seventeen and the caravan's best salvager, cuts into a hull the elders have always forbidden. Inside, the lights come on. The colony ship Long Patience is still waiting for launch, and its AI, PATIENCE, greets Rook as passenger one of four thousand.",
            "The caravan wants the ship's reactor: enough power to keep them alive for a generation. PATIENCE wants to finish its mission, and doesn't know the destination was abandoned long ago. Rook is the only one both sides will listen to.",
            "Then the storm season arrives, and the hull becomes the only shelter for a hundred kilometres. Rook has eight days to decide who to lie to.",
        ],
        "rule": "The desert buries everything and gives it back. Every storm moves the dunes and uncovers something older.",
        "cast": [
            ("Rook", "Salvager, 17", "Quick hands, few words, more patient with machines than with people. Has never been inside anything that wasn't moving."),
            ("PATIENCE", "Ship's AI", "No face, only a light, a voice and three-hundred-year-old manners. Still working through the departure checklist."),
            ("Mother Saba", "Caravan leader", "Raised Rook and kept the caravan alive through forty storm seasons. Needs the reactor, and knows what taking it will cost."),
        ],
        "episodes_title": "Episodes",
        "episodes": [
            ("1", "The Edge", "Wind exposes a metal edge nobody has dared to touch."),
            ("2", "Passenger One", "PATIENCE wakes and assigns Rook a cabin, a number and a departure date."),
            ("3", "Manifest", "The ship's records name the four thousand who never came."),
            ("4", "The Price", "The caravan arrives with cutting tools."),
            ("5", "Ground Crew", "Rook learns who the caravans really descend from."),
            ("6", "Storm Season", "The haboob hits. The ship is the only shelter for a hundred kilometres."),
            ("7", "Ignition", "PATIENCE begins its launch sequence."),
            ("8", "Departure", "Rook decides who the ship is for."),
        ],
        "frames_title": "Teaser, framed for both screens",
        "frames_note": "Dashed lines mark the vertical 9:16 crop.",
        "frames": [
            ("", "Wind uncovers a metal edge in the sand.", {"at": (33, 68, 3.4)}),
            ("", "Extreme wide: the hull rises from the dunes like a whale.", {"at": (50, 50, 1)}),
            ("", "Inside: dust in a beam of light. A cyan panel wakes up.", {"at": (73, 60, 3.4)}),
            ("", "PATIENCE speaks: “Welcome aboard, passenger one. You are three hundred years late.”", {"at": (80, 78, 2.2), "sub": "“Welcome aboard, passenger one.”"}),
        ],
    },
]

FONTS = ("https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900"
         "&family=Newsreader:ital,opsz,wght@0,6..72,300..500;1,6..72,300..500&display=swap")


def wave_svg():
    """Two overlapping waveforms (her voice and the signal) for the intercut frame."""
    lines = []
    for color, phase, amp in (("#E8955A", 0.0, 1.0), ("#8C969B", 0.7, 0.8)):
        pts = []
        for i in range(161):
            x = i * 2.5
            env = math.sin(math.pi * i / 160) ** 1.5
            y = 50 + amp * env * 34 * math.sin(i * 0.55 + phase) * (0.55 + 0.45 * math.sin(i * 0.13 + phase * 3))
            pts.append(f"{x:.1f},{y:.1f}")
        lines.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="1.2" opacity=".9"/>')
    return f'<svg class="wave" viewBox="0 0 400 100" preserveAspectRatio="none">{"".join(lines)}</svg>'


def frame(p, s, safe):
    """One storyboard frame: a crop of the key art (x%, y%, zoom) plus an optional effect or overlay."""
    parts = []
    if "at" in s:
        x, y, k = s["at"]
        left = min(max(x / 100 - 0.5 / k, 0), 1 - 1 / k)
        top = min(max(y / 100 - 0.5 / k, 0), 1 - 1 / k)
        parts.append(f'<img src="../assets/art/{p["key"]}" alt="" loading="lazy" style="width:{k * 100:.0f}%;height:{k * 100:.0f}%;'
                     f'left:{-left * k * 100:.1f}%;top:{-top * k * 100:.1f}%">')
    fx = s.get("fx")
    if fx == "wave":
        parts.append(wave_svg())
    if fx == "title":
        parts.append(f'<span class="title-card">{esc(s["text"])}</span>')
    if "hud" in s:
        parts.append(f'<span class="hud{" alert" if s.get("alert") else ""}">{esc(s["hud"])}</span>')
    if "sub" in s:
        parts.append(f'<span class="subtitle">{esc(s["sub"])}</span>')
    parts.append(safe)
    cls = f"shot fx-{fx}" if fx else "shot"
    return f'<div class="{cls}" aria-hidden="true">{"".join(parts)}</div>'


def page(p, nxt):
    t = esc(p["title"])
    img = f'<img src="../assets/art/{p["key"]}" alt="{esc(p["key_alt"])}" style="object-position:{p["key_pos"]}" fetchpriority="high">'
    head = f'<div class="p-head"><h1>{t}</h1><p class="logline">{esc(p["logline"])}</p></div>'
    hero_cls = "p-hero v" if p["kind"] == "v" else "p-hero"
    facts = "".join(f"<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>" for k, v in p["facts"])
    synopsis = "".join(f"<p>{esc(x)}</p>" for x in p["synopsis"])
    cast = "".join(f'<div><h3>{esc(name)}</h3><p class="role">{esc(role)}</p><p>{esc(desc)}</p></div>'
                   for name, role, desc in p["cast"])
    episodes = "".join(f'<li><span class="n">{esc(n)}</span><div><h3>{esc(title)}</h3><p>{esc(desc)}</p></div></li>'
                       for n, title, desc in p["episodes"])
    safe = '<span class="safe"></span>' if p["kind"] == "dual" else ""
    frames = "".join(
        f'<figure>{frame(p, s, safe)}<figcaption>'
        + (f'<span class="tc">{esc(tc)}</span>' if tc else "")
        + f'{esc(d)}</figcaption></figure>'
        for tc, d, s in p["frames"])
    frames_cls = "frames v" if p["kind"] == "v" else "frames"
    note = f'<p class="note">{esc(p["frames_note"])}</p>' if p["frames_note"] else ""
    ep_cls = "episodes wide-n" if "–" in p["episodes"][0][0] else "episodes"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{t} — Nova Intelligence</title>
  <meta name="description" content="{esc(p['logline'])}">
  <meta property="og:title" content="{t} — Nova Intelligence">
  <meta property="og:description" content="{esc(p['logline'])}">
  <meta property="og:url" content="https://mynva.store/projects/{p['slug']}.html">
  <meta property="og:image" content="https://mynva.store/assets/art/{p['key']}">
  <meta name="theme-color" content="#0D1217">
  <link rel="icon" href="../favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="{FONTS}" rel="stylesheet">
  <link rel="stylesheet" href="../style.css">
</head>
<body class="t-{p['theme']}">
  <a class="skip" href="#main">Skip to content</a>

  <header class="nav">
    <a class="brand" href="../index.html">Nova Intelligence</a>
    <nav class="nav-links" aria-label="Main">
      <a href="../index.html#series">Series</a>
      <a href="#contact">Contact</a>
    </nav>
  </header>

  <main id="main">
    <section class="{hero_cls}">
      <div class="key">{img}</div>
      {head}
    </section>
    <dl class="facts">{facts}</dl>

    <section class="section story">
      <h2>The story</h2>
      <div class="synopsis">
        {synopsis}
        <blockquote class="rule"><p>{esc(p['rule'])}</p><footer>The rule of this world</footer></blockquote>
      </div>
    </section>

    <section class="section">
      <h2>Characters</h2>
      <div class="cast">{cast}</div>
    </section>

    <section class="section">
      <h2>{esc(p['episodes_title'])}</h2>
      <ol class="{ep_cls}">{episodes}</ol>
    </section>

    <section class="section">
      <h2>{esc(p['frames_title'])}</h2>
      {note}
      <div class="{frames_cls}">{frames}</div>
    </section>

    <a class="next t-{nxt['theme']}" href="{nxt['slug']}.html">
      <img src="../assets/art/{nxt['key']}" alt="" loading="lazy" style="object-position:{nxt['key_pos']}">
      <span class="next-label">Next series</span>
      <strong>{esc(nxt['title'])}</strong>
    </a>

    <section class="section contact" id="contact">
      <h2>Interested in {t}?</h2>
      <a class="mail" href="mailto:novaintelligence@mynva.store?subject={t.replace(' ', '%20')}">novaintelligence@mynva.store</a>
    </section>
  </main>

  <footer class="footer">
    <span>© <span id="year">2026</span> Nova Intelligence</span>
    <a href="../index.html">Home</a>
  </footer>

  <script src="../main.js"></script>
</body>
</html>
"""


for f in os.listdir(OUT):  # remove pages of series that no longer exist
    if f.endswith(".html") and f[:-5] not in {p["slug"] for p in PROJECTS}:
        os.remove(os.path.join(OUT, f))
for i, p in enumerate(PROJECTS):
    nxt = PROJECTS[(i + 1) % len(PROJECTS)]
    with open(os.path.join(OUT, p["slug"] + ".html"), "w") as fh:
        fh.write(page(p, nxt))
print("written:", sorted(os.listdir(OUT)))
