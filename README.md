# zeonlab.ai

ZeonLab's corporate homepage for applied AI and investment research. It is one
static page with inline CSS, no JavaScript, and no fetched subresources of any
kind. It is served by Cloudflare Pages.

- `site/` — the whole site: `index.html` and the `_headers` file that makes
  the browser enforce the no-external-fetch claim (`default-src 'none'`).
- `tests/` — the contract every servable file must pass before it ships:
  English only, no internal paths or hostnames, no scripts, no fetched fonts
  or images, a valid contact-address policy, and a Content-Security-Policy that
  agrees with the page.
- `.github/workflows/publish.yml` — pull requests that touch the public surface
  run the contract without deployment authority. After review, a merge to
  `main` runs the same contract, deploys `site/` to Cloudflare Pages, and then
  fetches `https://zeonlab.ai/` from outside and requires the served bytes to
  hash to the committed file. See `DEPLOY.md` for the account setup and
  verification guidance.

## Local development

From the repository root, edit `site/index.html` and run the contract with a
portable Python command:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m pytest tests/ -q -p no:randomly
python -m http.server 4173 --bind 127.0.0.1 --directory site
```

On Windows, use the `py` launcher with the same `-m` arguments if `python` is
not on `PATH`. Open <http://127.0.0.1:4173> to inspect the local page. Nothing
is uploaded by hand.
