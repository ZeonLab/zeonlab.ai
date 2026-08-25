# ZeonLab North Star Homepage Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refresh zeonlab.ai into a production-quality North Star homepage for ZeonLab's trustworthy AI-native investment operating system.

**Architecture:** Retain the one-file, zero-JavaScript static architecture and existing Cloudflare Pages contract. Add contract tests first, then replace the page's narrative and visual system while preserving CSP, no-fetch behavior, accessibility, and honest maturity language.

**Tech Stack:** Semantic HTML5, inline CSS, inline SVG, pytest, Cloudflare Pages direct upload

**Spec:** `docs/superpowers/specs/2026-08-24-north-star-homepage-design.md`

## Global Constraints

- Current state is `research-only SHADOW/NON_ACTIONABLE`.
- IBKR Paper and small-capital live are future gates, not delivered states.
- No performance, customer, AUM, production-investment-product, Paper-execution, live-trading, or profitability claim.
- No JavaScript, external assets, analytics, runtime dependencies, or fetched subresources.
- Preserve `site/_headers` and `.github/workflows/publish.yml`.
- Every normal-size text/background pair clears WCAG AA 4.5:1 in light and dark schemes.

---

### Task 1: Public North Star contract

**Files:**
- Modify: `tests/test_site.py`

**Interfaces:**
- Consumes: the served `site/index.html` text fixture.
- Produces: regression tests for product vocabulary, maturity truth, and in-page navigation.

- [ ] Add a test requiring the exact public concepts: AI-native investment operating system,
  point-in-time, EventEpisode, Brain + Quant, Decision Packet, portfolio construction, SHADOW,
  IBKR Paper, and small-capital live.
- [ ] Add a test requiring the current-state sentence to bind research-only, SHADOW, NON_ACTIONABLE,
  and no capital or orders.
- [ ] Add a test resolving every fragment navigation link to an element ID.
- [ ] Run the three tests and confirm they fail because the old page lacks the North Star contract.
- [ ] Commit the red tests only together with the implementation that makes them green.

### Task 2: Static homepage implementation

**Files:**
- Modify: `site/index.html`

**Interfaces:**
- Consumes: the existing canonical/contact/CSP constraints and Task 1 assertions.
- Produces: a self-contained responsive homepage with hero, causal ledger, Brain + Quant, operating
  loop, validation ladder, and contact surface.

- [ ] Replace the document metadata with accurate North Star title, description, and Open Graph
  copy while retaining the canonical URL and data-URI favicon.
- [ ] Define light/dark design tokens and responsive layout primitives; retain token names consumed
  by contrast tests.
- [ ] Build semantic header/navigation/hero markup with one H1, current maturity badge, and an
  accessible inline causal-ledger graphic.
- [ ] Build the credibility rail, Brain + Quant comparison, five-step governed loop, maturity ladder,
  truth note, and contact/footer.
- [ ] Run the focused tests, then the full 15-test baseline plus new tests until green.

### Task 3: Release-quality verification

**Files:**
- Modify only if verification finds a defect: `site/index.html`, `tests/test_site.py`
- Create: `artifacts/qa/*.png` screenshots, kept outside `site/`

**Interfaces:**
- Consumes: the completed static page.
- Produces: automated-test output, visual evidence, exact git diff, and review receipt.

- [ ] Serve `site/` locally with a bounded static server.
- [ ] Inspect 1440x1100 desktop and 390x844 mobile in light and dark schemes; capture screenshots.
- [ ] Verify one document request, zero console errors, zero horizontal overflow, keyboard focus,
  visible skip link, and semantic heading order.
- [ ] Run the full pytest contract, whitespace check, served-file inventory, and byte-size report.
- [ ] Commit with the non-colingwuyu repository identity and record the exact head.
- [ ] Request independent exact-diff review against `origin/main`; repair all Critical/Important
  findings and re-run verification.
- [ ] Push and open a PR only if the authenticated GitHub identity is not `colingwuyu` and repository
  authority is available.
- [ ] Let the existing merge-to-main workflow deploy; report PR, check, merge, deploy, and live
  observation as separate truths. Do not infer deployment from a passing local test or open PR.

