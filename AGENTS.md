# İlan Pilotu legal pages — project rules (Claude Code, Codex, Cursor, Antigravity)

Static GitHub Pages site that hosts the privacy policy and terms of use of the
"İlan Pilotu" browser extension. The store listings (Chrome Web Store, Edge
Add-ons) link to these pages. The repo is public; the product source is in a
separate private repo. No framework, no dependencies, no build server.

## Commands
- `python3 build.py <path-to-docs/store>`  regenerate the HTML from the policy
  markdown (`privacy-tr.md`, `terms-tr.md`) kept in the product repo.
- Preview: `python3 -m http.server 4174 --bind 127.0.0.1`, open the pages.
- There is no test suite. After a change, read the generated page text.

## Hard rules
1. Published URLs never change: `index.html`, `gizlilik.html` and
   `kosullar.html` are referenced by store listings. Do not rename, move or
   delete them.
2. Never hand-edit `gizlilik.html` or `kosullar.html`. The source of truth is
   the markdown in the product repo; change it there, then run `build.py`.
   `build.py` itself may be changed when the markdown needs a new construct.
3. The repo is public: no secrets, no licence keys, no personal data, no
   private paths or repo contents. Only the support address already printed on
   the pages may appear.
4. Page text is Turkish (`lang="tr"`). Code and comments in English.
5. No external scripts, fonts, trackers or network requests on the pages.
   The CSS stays inline.
6. No dependency: `build.py` uses the Python standard library only.
7. The pages must say what the extension really does. If the product's data
   handling or permissions change, the policy changes first, then the release.
   A legal review of the wording is still advised; do not present the text as
   legal advice.

## File map
| File | Responsibility |
|---|---|
| `build.py` | Markdown → static HTML (also writes `index.html`) |
| `index.html` | Landing page with links to the two policies (generated) |
| `gizlilik.html` | Privacy policy (generated) |
| `kosullar.html` | Terms of use (generated) |

## Working efficiently
- One task per session. Open only the files above.
- After editing the markdown in the product repo, regenerate here and commit
  the generated HTML in one commit.

## Git
- Branch `main` is what GitHub Pages publishes; a push goes live within
  minutes. Check the diff of the generated HTML before pushing.
- Conventional Commits in English (`docs:` for wording, `chore:` for tooling).
