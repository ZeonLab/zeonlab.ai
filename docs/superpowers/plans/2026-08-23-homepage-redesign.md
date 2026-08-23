# ZeonLab Homepage Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the dense research essay with a concise, distinctive, accessible corporate homepage for ZeonLab's applied-AI and investment-research work.

**Architecture:** Keep the existing one-document static architecture: semantic HTML and inline CSS in `site/index.html`, enforced by the Python served-bytes contract and Cloudflare `_headers`. Add no JavaScript, fetched assets, build system, or deploy mechanism.

**Tech Stack:** HTML5, modern CSS, Python 3.12, pytest, Cloudflare Pages static hosting

**Spec:** `docs/superpowers/specs/2026-08-23-homepage-redesign-design.md`

## Global Constraints

- English only.
- No AUM, performance, return, customer, partner, regulatory, or product maturity claims without repository-backed evidence.
- No testimonials, fake dashboards, fabricated data, or implied live capital.
- Keep visible copy between roughly 250 and 700 words.
- Preserve the no-script, no-fetch, self-contained static architecture and strict CSP.
- Production deployment is out of scope; stop at branch, review, and local preview evidence.

---

### Task 1: Extend the Public-Surface Contract

**Files:**
- Modify: `tests/test_site.py`
- Test: `tests/test_site.py`

**Interfaces:**
- Consumes: the served `site/index.html` fixture and existing colour-token parser.
- Produces: structural, honesty, brevity, and accessibility gates that the new page must satisfy.

- [ ] **Step 1: Add failing information-architecture and honesty tests**

Add tests that require the new section IDs, resolved navigation targets, compact
copy, reduced-motion handling, and honest investment boundary:

```python
def _visible_copy(served: str) -> str:
    body = re.sub(r"<style.*?</style>", " ", served, flags=re.I | re.S)
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.S)
    body = re.sub(r"<[^>]+>", " ", body)
    return re.sub(r"\s+", " ", body).strip()


def test_corporate_information_architecture(served: str) -> None:
    for section_id in ("capabilities", "method", "principles", "contact"):
        assert f'id="{section_id}"' in served
    for heading in ("AI Applications", "Investment Research", "Observe",
                    "Reason", "Verify"):
        assert heading in served


def test_internal_navigation_targets_resolve(served: str) -> None:
    targets = re.findall(r'<a[^>]+href="#([^"]+)"', served)
    assert {"main", "capabilities", "method", "contact"}.issubset(targets)
    for target in targets:
        assert re.search(rf'id="{re.escape(target)}"', served)


def test_homepage_copy_is_concise(served: str) -> None:
    words = re.findall(r"[A-Za-z][A-Za-z'-]*", _visible_copy(served))
    assert 250 <= len(words) <= 700, len(words)


def test_investment_boundary_is_explicit(served: str) -> None:
    copy = _visible_copy(served).lower()
    assert "not investment advice" in copy
    assert "no performance offer" in copy


def test_reduced_motion_is_supported(served: str) -> None:
    assert re.search(r"@media\s*\(prefers-reduced-motion:\s*reduce\)", served)
```

- [ ] **Step 2: Run the focused tests and verify RED**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
& 'C:\Users\colin\AppData\Local\Programs\Python\Python312\python.exe' -m pytest tests/test_site.py -q -p no:randomly
```

Expected: the existing page fails the new information-architecture, navigation,
brevity/boundary, and reduced-motion requirements while the prior contract stays
green.

- [ ] **Step 3: Update colour-pair coverage for the planned tokens**

Replace `TEXT_PAIRS` with:

```python
TEXT_PAIRS = [
    ("ink", "bg"),
    ("muted", "bg"),
    ("soft", "bg"),
    ("accent", "bg"),
    ("ink", "panel"),
    ("muted", "panel"),
    ("paper-ink", "paper"),
    ("paper-muted", "paper"),
    ("accent-ink", "accent"),
]
```

- [ ] **Step 4: Commit the failing contract**

```powershell
git add tests/test_site.py
git -c user.name=Codex -c user.email=codex@localhost commit -m "test: define homepage experience contract"
```

### Task 2: Build the Corporate Homepage

**Files:**
- Modify: `site/index.html`
- Test: `tests/test_site.py`

**Interfaces:**
- Consumes: the contract introduced in Task 1 and the existing CSP in `site/_headers`.
- Produces: a single semantic, responsive, no-script HTML document.

- [ ] **Step 1: Replace metadata and design tokens**

Use the title `ZeonLab — Applied AI & Investment Research` and the description
`ZeonLab builds focused AI applications and research systems for consequential financial decisions.` Define the exact light tokens below and override all of them
in the dark media query:

```css
:root {
  --bg:#f2f0e9; --panel:#e7e4da; --paper:#faf9f5;
  --ink:#111815; --muted:#4b5852; --soft:#65716b;
  --paper-ink:#111815; --paper-muted:#4b5852;
  --accent:#b9f33d; --accent-ink:#111815; --line:#aab1aa;
}
@media (prefers-color-scheme:dark) {:root {
  --bg:#0b110f; --panel:#111a17; --paper:#e9e8e1;
  --ink:#f3f4ef; --muted:#b3bdb7; --soft:#96a19b;
  --paper-ink:#111815; --paper-muted:#4b5852;
  --accent:#b9f33d; --accent-ink:#111815; --line:#35413c;
}}
```

- [ ] **Step 2: Implement the semantic content structure**

Build a header with the ZeonLab wordmark and anchors to `#capabilities`,
`#method`, and `#contact`; a split hero containing the proposition “AI for
decisions that carry weight.” and a CSS-only decorative signal map; capability
cards headed `AI Applications` and `Investment Research`; a numbered
Observe/Reason/Verify method; a principles band; and a contact CTA using the
existing `admin@zeonlab.ai` address.

Use this exact boundary copy in the footer:

```html
<p>Research and software work. Not investment advice. No performance offer.</p>
```

- [ ] **Step 3: Implement responsive and accessible behaviour**

Use CSS grid for desktop and collapse the hero, cards, method, and footer below
`760px`. Ensure `html, body { overflow-x: clip; }`, maintain visible
`:focus-visible`, preserve the skip link, label every section, add
`aria-hidden="true"` to the signal map, and disable animation and transitions:

```css
@media (prefers-reduced-motion:reduce) {
  *,*::before,*::after { animation-duration:.01ms!important;
    animation-iteration-count:1!important; transition-duration:.01ms!important; }
}
```

- [ ] **Step 4: Run the complete contract and verify GREEN**

Run:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
& 'C:\Users\colin\AppData\Local\Programs\Python\Python312\python.exe' -m pytest tests/ -q -p no:randomly
```

Expected: all tests pass, with no skip because the existing real contact address
remains in place.

- [ ] **Step 5: Commit the implementation**

```powershell
git add site/index.html
git -c user.name=Codex -c user.email=codex@localhost commit -m "feat: redesign ZeonLab corporate homepage"
```

### Task 3: Align Repository Documentation

**Files:**
- Modify: `README.md`
- Modify: `DEPLOY.md`

**Interfaces:**
- Consumes: the final site architecture and unchanged publish workflow.
- Produces: accurate local-development and deployment handoff instructions.

- [ ] **Step 1: Update the README description and local commands**

Describe the page as ZeonLab's corporate homepage for applied AI and investment
research, keep the no-script/no-fetch statement, and document the explicit
Windows Python path fallback plus a local server command:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
& 'C:\Users\colin\AppData\Local\Programs\Python\Python312\python.exe' -m pytest tests/ -q -p no:randomly
& 'C:\Users\colin\AppData\Local\Programs\Python\Python312\python.exe' -m http.server 4173 --directory site
```

- [ ] **Step 2: Correct stale deployment prose**

Remove the obsolete placeholder-fill and historical staging-repository language
from `DEPLOY.md`. State the current observed mechanism only: merge-to-`main`
after review runs the contract, deploy, and external byte verification jobs.
Preserve the rollback and outside-verification instructions.

- [ ] **Step 3: Run documentation and contract checks**

Run `git diff --check` and the complete pytest command from Task 2.

- [ ] **Step 4: Commit documentation**

```powershell
git add README.md DEPLOY.md
git -c user.name=Codex -c user.email=codex@localhost commit -m "docs: align homepage publishing guidance"
```

### Task 4: Browser and Branch Verification

**Files:**
- Verify: `site/index.html`
- Verify: repository branch and commit history

**Interfaces:**
- Consumes: the completed branch.
- Produces: desktop/mobile screenshots and exact handoff evidence.

- [ ] **Step 1: Start a local static server**

Run the Python HTTP server from Task 3 on `127.0.0.1:4173`. Do not bind to a
public interface.

- [ ] **Step 2: Inspect desktop and mobile layouts**

At 1440×1000 and 390×844, capture full-page screenshots and verify:

```text
horizontalScroll = 0
documentRequests = 1
consoleErrors = 0
```

Use DOM checks for unique H1, section labels, native anchors, and the visible
contact action. Inspect the screenshots for overlap, awkward wrapping, empty
areas, visual imbalance, and illegible copy.

- [ ] **Step 3: Verify keyboard and reduced-motion behaviour**

Use the browser to focus the skip link and navigation/CTA links; confirm the
focus indicator is visible. Emulate or inspect the reduced-motion stylesheet and
confirm decorative animation is disabled.

- [ ] **Step 4: Run final deterministic checks**

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
& 'C:\Users\colin\AppData\Local\Programs\Python\Python312\python.exe' -m pytest tests/ -q -p no:randomly
git diff --check origin/main...HEAD
git status --short --branch
git log --oneline --decorate origin/main..HEAD
```

- [ ] **Step 5: Prepare the review handoff**

Report the exact branch, head SHA, files changed, contract count, visual QA
dimensions, screenshot paths, and local preview URL. Do not push with the
forbidden `colingwuyu` credential. If no authorized GitHub identity is
available, provide the exact push/PR blocker and leave the independently
reviewable local branch intact.
