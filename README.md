# zeonlab.ai

The ZeonLab homepage. One static page, its CSS inline, no JavaScript, no
fetched subresources of any kind. Served by Cloudflare Pages.

- `site/` — the whole site: `index.html` and the `_headers` file that makes
  the browser enforce the no-external-fetch claim (`default-src 'none'`).
- `tests/` — the contract every servable file must pass before it ships:
  English only, no internal paths or hostnames, no scripts, no fetched fonts
  or images, a contact address that is real rather than a stand-in, and a
  Content-Security-Policy that agrees with the page.
- `.github/workflows/publish.yml` — a merge to `main` that touches `site/`
  runs the contract, deploys `site/` to Cloudflare Pages, and then fetches
  `https://zeonlab.ai/` from outside and requires the served bytes to hash to
  the committed file. See `DEPLOY.md` for what that needs and how to check it.

To change the page: edit `site/index.html`, run `python -m pytest tests/ -q`,
open a pull request. Nothing is uploaded by hand.
