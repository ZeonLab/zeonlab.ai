# ZeonLab Homepage Redesign

## Purpose

Replace the current research essay with a concise corporate homepage that
positions ZeonLab at the intersection of applied AI and investment research.
The page should feel credible to an institutional audience without implying
customers, assets under management, investment returns, regulatory status, or
product maturity that the company has not substantiated.

## Direction

The visual direction is an “institutional intelligence studio”: editorial
clarity, financial precision, and a small amount of technical energy. The page
uses an ink-black canvas, warm off-white surfaces, muted teal, and a restrained
acid accent. A CSS-only signal map in the hero supplies a distinctive visual
without introducing images, JavaScript, or network requests.

The experience remains a single static document with inline CSS. It preserves
the repository's strict no-fetch and no-script privacy posture, works without a
build step, respects the system colour scheme, and is suitable for the existing
Cloudflare Pages direct-upload workflow.

## Information Architecture

1. A compact header gives the wordmark, two in-page navigation links, and a
   direct contact action.
2. The hero states the company proposition in one sentence: ZeonLab builds AI
   systems for decisions that carry weight. Supporting copy names the two
   domains—AI applications and investment research—without making maturity or
   performance claims.
3. A two-pillar section explains the company through “AI Applications” and
   “Investment Research”. Each card describes a category of work, not a product
   claimed to be production-ready.
4. A methodology section presents Observe → Reason → Verify as the common
   operating loop across both pillars.
5. A principles band states the commitments that can be demonstrated on the
   page: evidence before assertion, explicit uncertainty, and human
   accountability.
6. A final contact section invites research, product, and partnership
   conversations through the existing `admin@zeonlab.ai` mailbox.
7. The footer carries the company name, year, and an explicit boundary: the
   site presents research and software work, not investment advice or a
   performance offer.

## Content Rules

- English only.
- No AUM, performance, return, customer, partner, regulatory, or product
  maturity claims without repository-backed evidence.
- No testimonials, fake dashboards, fabricated data, or implied live capital.
- Keep visible copy between roughly 250 and 700 words.
- Describe investment work as research and decision systems. State that the
  page is not investment advice and makes no performance offer.
- Use the verified contact address already present in the repository.

## Interaction and Responsive Behaviour

The page is deliberately JavaScript-free. In-page navigation and the mail link
are native anchors. Desktop uses an asymmetric hero and two-column content
blocks. Tablet and mobile collapse to one column, reduce decorative density,
and keep all copy readable without horizontal scrolling. The visual signal map
is decorative and hidden from assistive technology.

Keyboard focus remains conspicuous. A skip link targets the main landmark.
Every section is labelled, decorative elements are ignored by screen readers,
and motion is limited to a subtle CSS ambient treatment that is fully disabled
under `prefers-reduced-motion: reduce`.

## Quality Gates

- Extend the served-bytes contract before changing the page so the new
  information architecture, concise copy, honest boundary language, navigation
  targets, reduced-motion support, CSP, and WCAG AA colour tokens are tested.
- Run the complete Python contract suite.
- Serve `site/` locally and inspect desktop and mobile layouts in a browser.
- Verify one document request, no console errors, no horizontal overflow,
  resolved navigation targets, and visible keyboard focus.
- Compare the final branch to `origin/main` and preserve the existing publish
  workflow. Do not merge or trigger the production workflow in this task.

## Deployment Boundary

The deliverable is an independently reviewable feature branch and draft-PR
handoff with local preview evidence. Production deployment remains the existing
merge-to-`main` workflow and is explicitly outside this task's authority. No
Cloudflare account setting, token, DNS record, project setting, or production
deployment is changed.
