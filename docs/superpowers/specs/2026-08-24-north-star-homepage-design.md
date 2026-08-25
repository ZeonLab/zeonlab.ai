# ZeonLab North Star Homepage Design

Date: 2026-08-24  
Status: Approved architectural refresh  
Surface: `https://zeonlab.ai/`

## Decision

Refresh the existing ZeonLab company homepage around the product North Star: ZeonLab builds a
trustworthy AI-native investment operating system. The page should make the product legible without
presenting planned capabilities as delivered results.

The implementation retains the repository's strongest architectural property: the public surface
is one static HTML document with inline CSS, no JavaScript, no third-party assets, no analytics, and
no fetched subresources. The existing Cloudflare Pages publish and served-byte verification
contract remains unchanged.

## Audience and job

The primary visitor is an investment or AI-research professional deciding whether ZeonLab's work is
distinctive and credible. In one scan they should understand:

1. the destination is an AI-native investment operating system, not a generic research lab;
2. evidence is frozen point-in-time and replayable;
3. EventEpisodes, rather than snapshots, are the longitudinal unit;
4. Brain and Quant remain independently observable and meet through governed ledgers;
5. reviewed research becomes forecasts, Decision Packets, and portfolio-construction candidates;
6. validation advances prospectively from SHADOW to IBKR Paper to a separately authorized bounded
   live pilot; and
7. today's state is research-only SHADOW/NON_ACTIONABLE, with no performance or live-capital claim.

## Information architecture

The page uses a compact six-part narrative:

- **Hero:** the North Star, one-sentence product definition, explicit current-state marker, and a
  decision-ledger visual that communicates evidence, causality, and review.
- **Credibility rail:** three invariants—point-in-time by construction, episode over snapshot, and
  separated authority classes.
- **Brain + Quant:** Brain organizes causal evidence and falsifiers; Quant contributes typed signal
  and nonlinear model decisions; agreement, tension, and residual remain visible.
- **Governed loop:** evidence freeze, EventEpisode, forecast, independent review/Decision Packet,
  and portfolio construction.
- **Validation ladder:** preregistered PIT replay and held-out evaluation precede prospective SHADOW;
  IBKR Paper and small-capital live remain future, separately gated states.
- **Contact/footer:** one real receiving mailbox, no signup funnel, and concise status language.

## Visual system

The page should feel calm, exact, and premium rather than like a trading terminal. A warm light
canvas and deep midnight dark canvas use pine/teal as the evidence accent and restrained amber for
decision boundaries. Typography uses the system sans stack for editorial clarity and the system
monospace stack for clocks, states, and ledger labels.

The hero's visual is a CSS/SVG causal path and decision ledger, not a dashboard screenshot. Fine
rules, nodes, time stamps, and a review seal create a distinctive evidence-led motif. There are no
stock photography, generic neural-network clouds, candlesticks, crypto neon, or decorative charts.

Responsive behavior:

- desktop: two-column hero, two-column system explanation, five-step loop, horizontal validation
  ladder;
- tablet: proportional two-column layouts with wrapped cards;
- mobile: single-column reading order, stacked process steps, compact navigation, no horizontal
  overflow;
- print: white background, hidden navigation actions, intact content hierarchy.

Both light and dark schemes must preserve WCAG AA contrast. Focus rings, a skip link, semantic
landmarks, resolvable section labels, and reduced-motion handling are release requirements.

## Copy and truth contract

Allowed language describes the destination, product method, and governed sequence. Current claims
must stay within implemented/research truth:

- use `research-only`, `SHADOW`, and `NON_ACTIONABLE` for the current operating state;
- describe PIT/replay mechanics and product methodology without claiming connected data coverage or
  economic validation;
- describe IBKR Paper and bounded live capital only as future gates;
- keep broker writes behind separate explicit approval;
- make profitability an empirical objective, never a promise.

The page must not claim returns, alpha, customers, assets under management, production deployment of
the investment product, observed Paper execution, live trading, or strategy profitability.

## Technical and release contract

- Modify only `site/index.html` and focused tests, plus non-servable repository documentation.
- Keep `site/_headers` and `.github/workflows/publish.yml` unchanged unless a verified defect is
  discovered.
- Keep the existing canonical URL and contact mailbox.
- Add no build system, runtime dependency, JavaScript, external font, image, CDN, analytics, or
  network request.
- Preserve the current Cloudflare Pages direct-upload workflow and outside served-byte SHA-256 gate.
- Automated tests must lock the North Star concepts, honest maturity ladder, internal-name safety,
  self-contained rendering, semantic structure, and contrast contract.
- Before publication, render and inspect desktop and mobile in light and dark modes, run the full
  contract, obtain independent exact-diff review, and repair every Critical or Important finding.

## Acceptance criteria

The refresh is ready to publish when:

1. the full repository contract passes from a clean exact head;
2. desktop and mobile renders have no clipping, overlap, horizontal overflow, or illegible text;
3. the page exposes the North Star and all six public concepts without overstating maturity;
4. no external request or JavaScript is introduced;
5. an independent reviewer reports zero open Critical or Important findings; and
6. the repository publication path either produces a reviewable PR with exact-head checks or is
   reported as blocked with the precise identity/gate limitation.

