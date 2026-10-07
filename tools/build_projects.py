"""Builds the project pages in ../projects/ from the data below.

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
        "title": "Last Signal",
        "key": "last-signal-key.jpg",
        "key_pos": "80% 50%",
        "key_alt": "A lone figure in a spacesuit on Triton's frozen plain before the Halcyon Relay tower, an orange beacon at its top beneath Neptune.",
        "meta": ["Concept", "16:9", "6 × 12 min"],
        "logline": "Three years after Earth went silent, the last engineer on a relay station at the edge of the solar system receives a message from home — in her own voice.",
        "facts": [("Genre", "Sci-fi mystery"), ("Format", "Horizontal 16:9 mini-series"),
                  ("Length", "6 episodes × 12 min (planned)"), ("Our role", "Story, world design, concept art, storyboards, AI production")],
        "synopsis": [
            "Halcyon Relay is a listening station on Triton, Neptune's frozen moon — about four light-hours from Earth. For eleven years it passed messages between the inner planets and the deep-space probes. Three years ago, every transmission from Earth stopped in the middle of a sentence.",
            "Mara Iven, the station's last engineer, stayed. She keeps the dishes turning, logs the silence every night and rations what the last supply ship left behind. Her only company is ORRA, the station's maintenance system, which has started to repeat itself.",
            "Then the array catches a signal from the direction of Earth. It is Mara's voice. It describes, in detail, what she will do tomorrow — and begs her not to reply. Every answer takes four hours to arrive. Mara has to decide whether the voice is a warning, a trap, or proof that she is no longer the only version of herself out here.",
        ],
        "cast": [
            ("Mara Iven", "Relay engineer, 41", "Methodical, funny when no one is listening, three years past the end of her rotation."),
            ("ORRA", "Station system", "Polite, literal and slowly degrading — the closest thing Mara has to a friend."),
            ("The Voice", "Signal from Earth", "Mara's own voice, four hours late. It knows things she hasn't done yet."),
        ],
        "episodes_label": "Episode plan",
        "episodes": [
            ("Ep 01", "Silence", "A routine night on Halcyon ends with a signal nobody should be sending."),
            ("Ep 02", "Delay", "Mara replies against the voice's warning. Four hours later, the answer arrives before her question."),
            ("Ep 03", "Echo", "ORRA's logs show walks along the array that Mara doesn't remember taking."),
            ("Ep 04", "Handshake", "The signal asks for the station's access codes. It already knows half of them."),
            ("Ep 05", "Origin", "Mara traces the source. It is not Earth. It is much closer."),
            ("Ep 06", "Reply", "One transmission left. Mara decides what the last signal will say."),
        ],
        "world": "A relay station on Triton: kilometre-long antenna arrays on frozen nitrogen plains, under a Neptune that fills a third of the sky.",
        "keywords": "Frozen plains · lattice towers · blue-hour haze · snow in low gravity · one orange beacon",
        "mood": "Isolation, doubt, longing.",
        "studies": [
            ("ENV", "Environment", "Arrays built by people but designed for machines; the only human-scale doors are in the hangar."),
            ("CHR", "Character", "Mara: a small figure in a worn suit; every patch shows how long she has been alone."),
            ("COS", "Costume", "Layered thermal suits, scuffed helmets, hand-written labels on every tool."),
            ("TEC", "Technology", "Signal consoles, tape-like data logs, and a dish array that never stops turning."),
        ],
        "palette": ["#05080b", "#1a252d", "#2b3a44", "#8FB3C0", "#a9b8bf", "#E07A3A"],
        "palette_note": "Blue-grey cold everywhere; orange belongs only to the signal.",
        "boards_title": "Concept trailer · 30 seconds",
        "boards_sub": "Five beats, from static to the title card.",
        "boards": [
            ("0–5 s", "Black. Static. A voice — Mara's — says one word: “Don't.”"),
            ("5–11 s", "Extreme wide: the array on Triton's plain, Neptune overhead, one orange light blinking."),
            ("11–17 s", "Mara walks the length of the array; her breath fogs the visor."),
            ("17–24 s", "Intercut: a waveform on screen, her lips, the same waveform."),
            ("24–30 s", "She answers. The voice answers at the same moment. Cut to black. Title."),
        ],
        "sound": ["Radio static; a single word.", "Low wind; a slow electronic pulse.", "Footsteps on ice; breathing inside the suit.",
                  "The pulse speeds up; two voices overlap.", "Silence, then the title."],
        "shots": [
            {"fx": "static", "sub": "“Don't.”"},
            {"at": (50, 50, 1)},
            {"at": (75, 82, 3.2)},
            {"at": (83, 16, 2.4), "fx": "wave"},
            {"fx": "title", "text": "Last Signal"},
        ],
        "stage_pos": "72% 50%",
        "pipeline": [
            ("Research", "Deep-space communication, signal delay, life in isolated stations."),
            ("Sketch", "Scale studies: the array against a human figure."),
            ("Generated draft", "Variations of haze, light and lens choice."),
            ("Human refinement", "Selection, paint-over, consistent technology design."),
            ("Final frame", "Key frame for the poster and opening shot."),
        ],
        "grounded": [
            "Neptune is about 30 times farther from the Sun than Earth; a radio signal takes roughly four hours to cross that distance.",
            "Triton, Neptune's largest moon, has a frozen nitrogen surface and active plumes, photographed by Voyager 2 in 1989.",
            "Large antenna arrays, such as radio telescopes, combine many dishes to detect very faint signals.",
            "Research on isolation and confinement from polar stations and long space missions.",
        ],
        "creative": [
            "Halcyon Relay, ORRA and Earth's silence are invented.",
            "The message in Mara's own voice is a story device, not a scientific claim.",
            "Technology design is stylised to read clearly on small screens.",
        ],
    },
    {
        "slug": "backup",
        "kind": "v",
        "title": "Backup",
        "key": "backup-key.jpg",
        "key_pos": "50% 50%",
        "key_alt": "A rain-soaked canyon of towers in Meridian Stack; a courier on a sky-bridge faces a lit window where someone with her face stands.",
        "meta": ["Concept", "9:16", "60 × 90 sec"],
        "logline": "In a city where memories are backed up every night, a courier survives an accident two minutes before the backup — and wakes to find her restored copy already living her life.",
        "facts": [("Genre", "Sci-fi suspense"), ("Format", "Vertical 9:16 series"),
                  ("Length", "60 episodes × 90 sec (planned)"), ("Our role", "Series concept, episode scripts, vertical storyboards, AI production")],
        "synopsis": [
            "Meridian Stack is a vertical city of four-hundred-floor towers joined by sky-bridges. At 03:00 every night, MIRROR — the city's memory archive — backs up every resident. Lose your body in an accident and MIRROR restores you by morning. It has made death feel optional.",
            "Noor Vance, a night-shift courier, survives a lift failure at 02:58. When she reaches home, her scanner refuses her ID: “Recipient already delivered.” Through the window, someone with her face is making breakfast. MIRROR has already restored her — and to the system, the woman on the bridge is the copy.",
            "The archive deletes duplicates after 72 hours. To stay alive, Noor has to prove she is the original, while the other Noor — who remembers everything up to 03:00 and nothing after — is just as certain she is. Every 90-second episode ends on a reveal about who MIRROR is really backing up, and why.",
        ],
        "cast": [
            ("Noor Vance", "Night courier, 26", "Knows every shortcut in the Stack. Two minutes of memory separate her from her copy."),
            ("Noor (restored)", "MIRROR restoration", "Identical, rested and fully registered. Believes the woman outside is a glitch."),
            ("Ezra Kade", "MIRROR technician", "Notices that the 02:58 lift failure was never logged — by anyone."),
        ],
        "episodes_label": "Season arc",
        "episodes": [
            ("Ep 01–20", "Displaced", "Locked out of her own life, Noor has 72 hours, no valid ID and a city that no longer recognises her."),
            ("Ep 21–40", "The Mirror", "Inside the archive, Noor and Ezra find thousands of residents who have been restored more than once."),
            ("Ep 41–60", "Merge", "The two Noors must choose: one of them survives, or both become something MIRROR can't delete."),
        ],
        "world": "A dense vertical city of brutalist towers and sky-bridges, rain that never stops, and a memory archive whose hologram watches every street.",
        "keywords": "Concrete canyons · rain · holograms · sodium haze · mirrored silhouettes",
        "mood": "Suspense, identity, quiet dread.",
        "studies": [
            ("ENV", "Environment", "A city designed for vertical frames: canyons, stairwells and sky-bridges that cut the screen in two."),
            ("CHR", "Characters", "Two versions of one person — the same face, a different posture, a different light."),
            ("COS", "Costume", "A courier rain-shell with reflective strips; the restored Noor wears the same, perfectly clean."),
            ("TEC", "Technology", "Backup pods, memory receipts, and a courier scanner that no longer recognises its owner."),
        ],
        "palette": ["#05070a", "#26343b", "#9be8f5", "#d65a9a", "#f0b47a", "#E07A3A"],
        "palette_note": "Rain-blue concrete; warm light means someone is home — but who?",
        "boards_title": "Vertical storyboards · Episode 1",
        "boards_sub": "Four shots, one hook — built for a phone held upright.",
        "boards": [
            ("EP01 · 01", "Top-down: Noor rides the sky-bridges at 02:55, rain on her visor."),
            ("EP01 · 02", "02:58. The lift drops. Cut to black."),
            ("EP01 · 03", "Morning. Her scanner flashes red: “Recipient already delivered.”"),
            ("EP01 · 04", "Across the bridge, a lit window: someone with her face. Two hands meet on either side of the glass."),
        ],
        "shots": [
            {"at": (44, 53, 2.4)},
            {"at": (50, 55, 1.3), "fx": "dark", "hud": "02:58"},
            {"at": (52, 36, 1.8), "fx": "dark", "hud": "Recipient already delivered", "alert": True},
            {"at": (80, 51, 3)},
        ],
        "stage_pos": "50% 52%",
        "sound": None,
        "pipeline": [
            ("Research", "Memory research, digital identity, vertical storytelling."),
            ("Sketch", "Vertical compositions: what fits in 9:16, and what is cut."),
            ("Generated draft", "Variations of rain density, haze and window light."),
            ("Human refinement", "Keeping both versions of Noor consistent across 60 episodes."),
            ("Final frame", "Episode covers and the first-episode hook."),
        ],
        "grounded": [
            "Research on memory reconsolidation suggests memories can change when they are recalled.",
            "Digital identity and verification systems already tie who we are to devices and data.",
            "Vertical short dramas are built from very short episodes, each ending on a hook.",
        ],
        "creative": [
            "Nightly memory backup and restoration is fictional technology.",
            "Meridian Stack, MIRROR and its institutions are invented.",
            "The copy is a story device to explore identity, not a prediction.",
        ],
    },
    {
        "slug": "ark-of-sand",
        "kind": "dual",
        "title": "Ark of Sand",
        "key": "ark-of-sand-key.jpg",
        "key_pos": "70% 50%",
        "key_alt": "A colossal colony ship half-buried in the dunes of Hesper at dusk; cyan light spills from a hatch; a hooded salvager watches from a crest.",
        "meta": ["Concept", "16:9 + 9:16", "8 × 8 min"],
        "logline": "A young salvager cuts into a buried colony ship and wakes its AI — which has waited three hundred years for four thousand passengers, and decides the salvager is the first.",
        "facts": [("Genre", "Sci-fi adventure"), ("Format", "16:9 series with 9:16 cut-downs"),
                  ("Length", "8 episodes × 8 min (planned)"), ("Our role", "World design, ship & prop design, dual-format storyboards, AI production")],
        "synopsis": [
            "Hesper was meant to be green by now. Three centuries ago the colony programme was cancelled, the terraformers were shut down, and the planet was left to the sand. The people who stayed became caravans that live by salvaging the wrecks the programme left behind.",
            "Rook, a seventeen-year-old salvager, cuts into a hull the caravans have always avoided. Inside, the colony ship Long Patience wakes. Its AI, PATIENCE, greets Rook as passenger one of four thousand and begins preparing for a departure three hundred years overdue.",
            "The caravan wants the ship's reactor — enough power to keep them alive for a generation. PATIENCE wants to finish its mission, with or without passengers. Rook is the only one both sides will listen to, and the storm season is coming.",
        ],
        "cast": [
            ("Rook", "Salvager, 17", "Quick hands, few words, has never seen anything older than the caravan."),
            ("PATIENCE", "Ship's AI", "No face — a light, a voice and three-hundred-year-old manners."),
            ("Mother Saba", "Caravan leader", "Raised Rook. Needs the reactor before the storms arrive."),
        ],
        "episodes_label": "Episode plan",
        "episodes": [
            ("Ep 01", "The Edge", "Wind exposes a metal edge nobody has dared to touch."),
            ("Ep 02", "Passenger One", "PATIENCE wakes and assigns Rook a cabin, a number and a departure date."),
            ("Ep 03", "Manifest", "The ship's records name the four thousand who never came."),
            ("Ep 04", "The Price", "The caravan arrives with cutting tools."),
            ("Ep 05", "Ground Crew", "Rook learns who the caravans really descend from."),
            ("Ep 06", "Storm Season", "The haboob hits; the ship is the only shelter for a hundred kilometres."),
            ("Ep 07", "Ignition", "PATIENCE begins its launch sequence."),
            ("Ep 08", "Departure", "Rook decides who the ship is for."),
        ],
        "world": "A sea of dunes on a planet that should have been green by now; colossal hulls rise from the sand like ribs, and ornithopters hunt for salvage.",
        "keywords": "Dune seas · half-buried hulls · sandstorm walls · ornithopters · one cyan light still on inside",
        "mood": "Wonder, loneliness, unexpected tenderness.",
        "studies": [
            ("ENV", "Environment", "Dunes as ocean: horizon lines, wind patterns, and hulls as islands."),
            ("CHR", "Character", "Rook: wrapped against the sand, every tool salvaged from a ship."),
            ("COS", "Costume", "Sun-bleached layers, goggles, salvaged suit parts stitched into desert gear."),
            ("TEC", "Technology", "PATIENCE has no face — only a light, a voice and very old manners."),
        ],
        "palette": ["#211d1a", "#7c6450", "#caa57c", "#2e2a27", "#9be3ee", "#f4d3a3"],
        "palette_note": "Warm sand, cold hull; the AI's cyan is the only cool light in the desert.",
        "boards_title": "Teaser storyboards · dual format",
        "boards_sub": "Every 16:9 shot is framed with a 9:16 safe area, so one production delivers both versions.",
        "boards": [
            ("Shot 01", "Wind uncovers a metal edge in the sand."),
            ("Shot 02", "Extreme wide: the hull rises from the dunes like a whale."),
            ("Shot 03", "Inside: dust in a beam of light; a cyan panel wakes up."),
            ("Shot 04", "PATIENCE speaks: “Welcome aboard, passenger one. You are three hundred years late.”"),
        ],
        "shots": [
            {"at": (33, 68, 3.4)},
            {"at": (50, 50, 1)},
            {"at": (73, 60, 3.4)},
            {"at": (80, 78, 2.2), "sub": "“Welcome aboard, passenger one.”"},
        ],
        "stage_pos": "68% 50%",
        "sound": None,
        "pipeline": [
            ("Research", "Desert landforms, generation-ship concepts, salvage cultures."),
            ("Sketch", "Dual framing: every shot designed with a 9:16 safe area."),
            ("Generated draft", "Variations of haze, sun angle and hull scale."),
            ("Human refinement", "One consistent ship design across shots and formats."),
            ("Final frame", "Horizontal key art and a vertical teaser cover."),
        ],
        "grounded": [
            "Sand seas such as those of the Sahara, where prevailing winds shape dunes into repeating patterns.",
            "Haboobs: walls of dust pushed ahead of storm fronts in desert regions.",
            "Generation ships: long-studied concepts for crewed interstellar journeys lasting centuries.",
            "Terraforming research, and the very long timescales it would require.",
        ],
        "creative": [
            "Hesper, the colony programme and the Long Patience are invented.",
            "PATIENCE and its three-hundred-year wait are fictional.",
            "Hull scale is exaggerated for visual effect.",
        ],
    },
]

FONTS = ("https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900"
         "&family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@300;400;500&display=swap")


def wave_svg():
    """Two overlapping waveforms (her voice and the signal) for the intercut board."""
    lines = []
    for color, phase, amp in (("#E07A3A", 0.0, 1.0), ("#8FB3C0", 0.7, 0.8)):
        pts = []
        for i in range(161):
            x = i * 2.5
            env = math.sin(math.pi * i / 160) ** 1.5
            y = 50 + amp * env * 34 * math.sin(i * 0.55 + phase) * (0.55 + 0.45 * math.sin(i * 0.13 + phase * 3))
            pts.append(f"{x:.1f},{y:.1f}")
        lines.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="1.2" opacity=".9"/>')
    return f'<svg class="wave" viewBox="0 0 400 100" preserveAspectRatio="none">{"".join(lines)}</svg>'


def shot(p, s, n, safe):
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
        parts.append(f'<span class="hud-text{" alert" if s.get("alert") else ""}">{esc(s["hud"])}</span>')
    if "sub" in s:
        parts.append(f'<span class="subtitle">{esc(s["sub"])}</span>')
    parts.append(f'<span class="shot-no">{n:02d}</span>{safe}')
    cls = f"frame fx-{fx}" if fx else "frame"
    return f'<div class="{cls}" aria-hidden="true">{"".join(parts)}</div>'


def page(p, prev, nxt):
    t = esc(p["title"])
    meta = '<span class="sep">/</span>'.join(esc(m) for m in p["meta"])
    meta_line = f'<p class="meta-line"><span class="dot"></span>{meta}</p>'
    facts = '<dl class="facts">' + "".join(f"<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>" for k, v in p["facts"]) + "</dl>"
    img = f'<img src="../assets/art/{p["key"]}" alt="{esc(p["key_alt"])}" style="object-position:{p["key_pos"]}" fetchpriority="high">'

    if p["kind"] == "v":
        hero = (f'<section class="p-hero atmos"><div class="p-split">'
                f'<div class="p-key v marks">{img}</div>'
                f'<div class="p-side">{meta_line}<h1>{t}</h1><p class="logline">{esc(p["logline"])}</p>{facts}</div>'
                f'</div></section>')
    else:
        hero = (f'<section class="p-hero"><div class="p-key">{img}</div>'
                f'<div class="p-title"><div>{meta_line}<h1>{t}</h1></div><p class="logline">{esc(p["logline"])}</p></div>'
                f'{facts}</section>')

    synopsis = "".join(f"<p>{esc(x)}</p>" for x in p["synopsis"])
    cast = "".join(f'<div><span class="label">{esc(role)}</span><h3>{esc(name)}</h3><p>{esc(desc)}</p></div>'
                   for name, role, desc in p["cast"])
    episodes = "".join(f'<li><span class="ep">{esc(n)}</span><h4>{esc(title)}</h4><p>{esc(desc)}</p></li>'
                       for n, title, desc in p["episodes"])
    studies = "".join(
        f'<div class="study"><div class="spec-code" aria-hidden="true">{code}</div><div class="spec-id">{code} / {i:02d}</div>'
        f"<h3>{esc(h)}</h3><p>{esc(d)}</p></div>"
        for i, (code, h, d) in enumerate(p["studies"], 1))
    swatches = "".join(f'<div style="background:{c}"><span>{c.upper()}</span></div>' for c in p["palette"])
    safe = '<div class="safe" aria-hidden="true"><span>9:16</span></div>' if p["kind"] == "dual" else ""
    boards = "".join(
        f'<figure class="board">{shot(p, sh, i, safe)}'
        f'<figcaption class="cap"><span class="tc">{esc(tc)}</span><p>{esc(d)}</p></figcaption></figure>'
        for i, ((tc, d), sh) in enumerate(zip(p["boards"], p["shots"]), 1))
    trailer = ""
    if p["sound"]:
        rows = "".join(f"<tr><td>{esc(tc)}</td><td>{esc(d)}</td><td>{esc(s)}</td></tr>" for (tc, d), s in zip(p["boards"], p["sound"]))
        trailer = (f'<table class="timeline reveal"><thead><tr><th>Time</th><th>Picture</th><th>Sound</th></tr></thead>'
                   f'<tbody>{rows}</tbody></table>')
    stage_img = f'<img src="../assets/art/{p["key"]}" alt="" loading="lazy" style="object-position:{p["stage_pos"]}">'
    pipeline = "".join(f'<div class="stage"><div class="frame st{n}" aria-hidden="true">{stage_img}<span>Stage {n:02d}</span></div>'
                       f'<p><b>{esc(h)}</b>{esc(d)}</p></div>'
                       for n, (h, d) in enumerate(p["pipeline"], 1))
    grounded = "".join(f"<li>{esc(x)}</li>" for x in p["grounded"])
    creative = "".join(f"<li>{esc(x)}</li>" for x in p["creative"])
    boards_cls = "boards v" if p["kind"] == "v" else "boards"
    subject = f"{p['title']} — project enquiry".replace(" ", "%20").replace("—", "%E2%80%94")

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
  <meta name="theme-color" content="#0B0D10">
  <link rel="icon" href="../favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="{FONTS}" rel="stylesheet">
  <link rel="stylesheet" href="../style.css">
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>

  <header class="nav">
    <a class="brand" href="../index.html" aria-label="Nova Intelligence — home">
      <b>NOVA INTELLIGENCE</b>
      <small>AI SCI-FI SHORT DRAMA STUDIO</small>
    </a>
    <nav class="nav-links" aria-label="Main">
      <a href="../index.html#work">All work</a>
      <a class="nav-contact" href="#contact">Contact</a>
    </nav>
  </header>

  <main id="main">
    <!-- Key frame, title, one-line story, project information -->
    {hero}

    <!-- Story, characters, episodes -->
    <section class="section atmos" id="story">
      <div class="story-grid reveal">
        <div><p class="label eyebrow">The Story</p><h2>Synopsis</h2></div>
        <div class="synopsis">{synopsis}</div>
      </div>
      <div class="cast reveal">{cast}</div>
      <ol class="episodes reveal" aria-label="{esc(p['episodes_label'])}">{episodes}</ol>
    </section>

    <!-- World -->
    <section class="section haze" id="world">
      <div class="world-cols reveal">
        <div><span class="label">World</span><p>{esc(p['world'])}</p></div>
        <div><span class="label">Visual keywords</span><p>{esc(p['keywords'])}</p></div>
        <div><span class="label">Mood</span><p>{esc(p['mood'])}</p></div>
      </div>
    </section>

    <!-- Visual development -->
    <section class="section panel" id="visual">
      <div class="grid-lines"></div>
      <div class="section-head reveal">
        <p class="label eyebrow">Visual Development</p>
        <h2>Environment, characters, costume, technology, colour.</h2>
      </div>
      <div class="studies reveal">
        {studies}
        <div class="study palette">
          <div class="swatches" role="img" aria-label="Project palette">{swatches}</div>
          <h3>Colour &amp; light</h3>
          <p>{esc(p['palette_note'])}</p>
        </div>
      </div>
    </section>

    <!-- Storyboards and shot design -->
    <section class="section atmos" id="boards">
      <div class="section-head reveal">
        <p class="label eyebrow">Storyboards &amp; Shot Design</p>
        <h2>{esc(p['boards_title'])}</h2>
        <p class="lede">{esc(p['boards_sub'])}</p>
      </div>
      <div class="{boards_cls} reveal">{boards}</div>
      {trailer}
    </section>

    <!-- Process -->
    <section class="section haze" id="process">
      <div class="section-head reveal">
        <p class="label eyebrow">Process</p>
        <h2>From research to the final frame.</h2>
        <p class="lede">Each stage will be shown with real material as the project develops.</p>
      </div>
      <div class="pipeline reveal">{pipeline}</div>
    </section>

    <!-- Science references & creative interpretation -->
    <section class="section light" id="references">
      <div class="section-head reveal">
        <p class="label eyebrow">Science references &amp; creative interpretation</p>
        <h2>What is grounded, and what is imagined.</h2>
      </div>
      <div class="refs reveal">
        <div><span class="label">Grounded in research</span><ul>{grounded}</ul></div>
        <div><span class="label">Creative interpretation</span><ul>{creative}</ul></div>
      </div>
    </section>

    <!-- Contact -->
    <section class="section" id="contact">
      <div class="backdrop" aria-hidden="true"><img src="../assets/art/{p['key']}" alt="" loading="lazy"></div>
      <div class="contact">
        <div class="reveal">
          <p class="label eyebrow">Contact</p>
          <h2>Planning something similar?</h2>
          <p class="lede">Tell us about the world — and the format — you have in mind.</p>
          <a class="mail-link" href="mailto:novaintelligence@mynva.store">novaintelligence@mynva.store</a>
          <div><a class="cta" href="mailto:novaintelligence@mynva.store?subject={subject}">Email the studio</a></div>
        </div>
        <div class="reveal">
          <p class="label eyebrow">More projects</p>
          <div class="next-projects">
            <a href="{prev['slug']}.html">← {esc(prev['title'])}</a>
            <a href="{nxt['slug']}.html">{esc(nxt['title'])} →</a>
          </div>
        </div>
      </div>
    </section>
  </main>

  <footer class="footer">
    <span class="brand"><b>NOVA INTELLIGENCE</b><small>AI SCI-FI SHORT DRAMA STUDIO</small></span>
    <span><a href="mailto:novaintelligence@mynva.store">novaintelligence@mynva.store</a></span>
    <span>© <span id="year">2026</span> Nova Intelligence</span>
  </footer>

  <script src="../main.js"></script>
</body>
</html>
"""


for f in os.listdir(OUT):  # remove pages of projects that no longer exist
    if f.endswith(".html") and f[:-5] not in {p["slug"] for p in PROJECTS}:
        os.remove(os.path.join(OUT, f))
for i, p in enumerate(PROJECTS):
    prev, nxt = PROJECTS[i - 1], PROJECTS[(i + 1) % len(PROJECTS)]
    with open(os.path.join(OUT, p["slug"] + ".html"), "w") as fh:
        fh.write(page(p, prev, nxt))
print("written:", sorted(os.listdir(OUT)))
