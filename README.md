# Half-Ass Games website

The studio website at **https://half-assgames.com**: plain HTML and CSS, hosted free on
GitHub Pages. To put it online the first time, follow [DEPLOY.md](DEPLOY.md).

## What's where

| Path | What it is |
|---|---|
| `docs/` | **The website.** GitHub publishes everything in this folder (that's why it's called docs) |
| `docs/index.html` | Home page: the studio, all the games, why "Half-Ass", say hi |
| `docs/deep-sea-panic/index.html` | The Deep Sea Panic! page |
| `docs/deep-sea-panic/privacy/index.html` | The privacy policy Google Play links to |
| `docs/404.html` | The "Lost at sea!" page for broken links |
| `docs/css/site.css` | All the colours, fonts and layout |
| `docs/img/`, `docs/fonts/` | Images and fonts, made by the build script below |
| `docs/CNAME` | Tells GitHub the site's address. Don't delete it |
| `preview.cmd`, `serve.ps1` | Preview the site on your PC |
| `tools/build-assets.py` | Turns the store art, logo and game fonts into small web files |

## Preview it on your PC

Double-click **`preview.cmd`**. Your browser opens at <http://localhost:8080/>. Close the
black window to stop it.

## Change some words

Open the page's `index.html` in any text editor (VS Code is great), change the text between
the tags, save, and refresh the preview.

## The games on the home page

Each game is a card in the **Games** section of `docs/index.html`, under **Out now** or
**In development**. To add a game, copy a whole `<article class="card project ...">...</article>`
block, change the words, and give it a little tag like `Playable prototype` or `On itch.io`.

Each card's colour stripe comes from its class (`p-arcane`, `p-channel`), set in
`docs/css/site.css`. Copy one of those lines to give a new game its own colours.

## Two looks

Studio pages (home, 404) use the donkey's colours: pink-red, purple and cream on dark plum.
Deep Sea Panic!'s pages have `<body class="theme-sea">`, which switches them to the game's
deep-sea colours. A future game page can get its own look the same way: copy the
`.theme-sea { ... }` block in `site.css`, rename it, and change the colours.

## Change the screenshots, key art or logo

The images come from these originals:

- Key art, icon and screenshots: `C:\UnityProjects\Submarine_Game\Store\Graphics`
- Studio logo: `Documents\Half-Ass Games\Brand\Half-Ass-Games-logo.png`

Replace the original, then run this in this folder to remake the web versions:

```bash
uv run --no-project --with pillow --with fonttools --with brotli python tools/build-assets.py
```

To show different screenshots, change the `SCREENSHOTS` list at the top of the script and
the matching `<img>` lines in `docs/deep-sea-panic/index.html`.

## Publish a change

**GitHub Desktop:** type a short summary of the change, click **Commit to main**, then
**Push origin**. The live site updates in about a minute.

## When Deep Sea Panic! launches on Google Play

1. In `docs/deep-sea-panic/index.html`, find the two `ANDROID` comments in the "Get it"
   section. Delete the tester card and un-comment the "Get it on Google Play" card.
2. In the same file, change the top button `Android: help test it` (`href="#android"`) to
   say `Get it on Google Play`.
3. In `docs/index.html`, change the line "On Android? It's coming to Google Play soon..." to
   point to Google Play.
4. Optional: swap the text button for Google's official badge from
   <https://play.google.com/intl/en_us/badges/>. Google asks that you use the badge as-is.
5. Preview, then publish.

## Good to know

- **Privacy:** the site has no cookies, analytics or trackers, and loads nothing from other
  websites. The YouTube trailer only loads when someone presses play. If that ever changes,
  update the "About this website" part of the privacy page.
- **Privacy policy changes:** if the game starts collecting anything (ads, analytics,
  purchases, accounts), update `docs/deep-sea-panic/privacy/index.html` and its date
  **before** releasing that version.
- **Fonts:** Bungee and Nunito, the same fonts the game uses. Both are free under the
  SIL Open Font License; the licence files are in `docs/fonts/`.
