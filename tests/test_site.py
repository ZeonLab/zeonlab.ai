"""Served-bytes contract for the zeonlab.ai homepage.

The page is a public, static, self-contained artefact. Everything asserted here
is asserted against the bytes a visitor's browser receives -- not against the
build, not against intent. Three separable concerns, one authoritative home:

  1. LEAK       nothing internal, nothing non-English, nothing fetched.
  2. HONESTY    the contact slot is either an unreplaced placeholder or a real
                address; an invented-looking address is a failure.
  3. LEGIBILITY every foreground/background text pair clears WCAG AA in both
                colour schemes, computed from the page's own tokens.

Run:  python -m pytest tests/ -q
"""

from __future__ import annotations

import json
import os
import re
import unicodedata
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]

# By default the built site in this repo. ZEONLAB_SITE points the same contract
# at any directory holding an index.html -- in particular a copy pulled down
# from the live origin after deploy, so the checks below can be run against the
# bytes Cloudflare actually serves rather than only against the build.
SITE = Path(os.environ.get("ZEONLAB_SITE") or (REPO / "site"))
INDEX = SITE / "index.html"


# --------------------------------------------------------------------------
# The served bytes. One read, one decode, shared by every check.
# --------------------------------------------------------------------------

@pytest.fixture(scope="module")
def served() -> str:
    assert INDEX.is_file(), f"no page at {INDEX}"
    raw = INDEX.read_bytes()
    # The page declares utf-8; if it does not decode as utf-8 the browser is
    # receiving something other than what the meta charset promises.
    return raw.decode("utf-8")


@pytest.fixture(scope="module")
def site_files() -> list[Path]:
    return sorted(p for p in SITE.rglob("*") if p.is_file())


# --------------------------------------------------------------------------
# 1. LEAK
# --------------------------------------------------------------------------

# Outbound URLs the page is allowed to contain. Each needs a reason, because an
# allowlist without reasons is a place to hide a leak.
ALLOWED_URLS = {
    # The page's own canonical origin (rel=canonical, og:url). Declared
    # outbound; it is the domain this page is served from.
    "https://zeonlab.ai/": "self / canonical origin",
    # XML namespace inside the inline SVG favicon data URI. A namespace is an
    # identifier, never a request: no user agent fetches it.
    "http://www.w3.org/2000/svg": "SVG XML namespace, not a request",
}

# Tokens that must never reach a public byte. Tailnet and loopback hostnames,
# repository paths, and the private-plane vocabulary.
FORBIDDEN_TOKENS = [
    "ts.net",
    "tailscale",
    "tailnet",
    "127.0.0.1",
    "0.0.0.0",
    "localhost",
    "src/",
    "deploy/",
    "dev/pm",
    "cbrain",
    "investbrain",
    "box-a",
    "finhub-share",
    ".env",
    "BEGIN PRIVATE KEY",
    "BEGIN RSA",
    "-----BEGIN",
]

# Service names an English page may legitimately use as ordinary words. Each is
# excluded on that ground alone; nothing hyphenated or coined is excluded.
ENGLISH_COLLISIONS = {"phoenix", "tempo", "alloy", "core", "dashboard"}


def _service_names() -> tuple[set[str], str]:
    """Internal-service vocabulary the page must not mention.

    This repository is PUBLIC, so the authoritative list of internal service
    names cannot be checked in here -- that would publish the very names it
    guards against. Instead: a small literal set of infrastructure product
    names that appear in our stack (public knowledge, harmless to name), plus
    an optional private list supplied at test time via ZEONLAB_INTERNAL_NAMES
    (one name per line) so the product repository's CI can run this same test
    with the full vocabulary. Provenance is returned so a failure says which.
    """
    names = {"intel-mcp", "falkordb", "graphiti", "grafana", "prometheus",
             "loki", "tempo", "nats", "phoenix", "zitadel", "alloy"}
    sources = ["public literal set"]
    extra = os.environ.get("ZEONLAB_INTERNAL_NAMES")
    if extra and Path(extra).is_file():
        for line in Path(extra).read_text(encoding="utf-8").splitlines():
            line = line.strip().lower()
            if line and not line.startswith("#"):
                names.add(line)
        sources.append("ZEONLAB_INTERNAL_NAMES (private, not in this repo)")
    return names, " + ".join(sources)


def test_no_cjk_codepoints(served: str) -> None:
    """English only on the served bytes. Standing rule for external surfaces."""
    offenders = []
    for i, ch in enumerate(served):
        if ord(ch) < 0x2E80:
            continue
        name = unicodedata.name(ch, "")
        if any(k in name for k in ("CJK", "HIRAGANA", "KATAKANA", "HANGUL",
                                   "BOPOMOFO", "IDEOGRAPH")):
            offenders.append((i, ch, name))
    assert not offenders, f"CJK codepoints in served bytes: {offenders[:8]}"


def test_no_internal_tokens(served: str) -> None:
    low = served.lower()
    hits = [t for t in FORBIDDEN_TOKENS if t.lower() in low]
    assert not hits, f"internal tokens in served bytes: {hits}"


def test_no_service_names(served: str) -> None:
    names, provenance = _service_names()
    assert names, f"service vocabulary resolved empty (source: {provenance})"
    low = served.lower()
    hits = sorted(n for n in names if re.search(rf"(?<![a-z0-9-]){re.escape(n)}(?![a-z0-9-])", low))
    assert not hits, f"service names in served bytes: {hits} (checked {len(names)} from {provenance})"


def test_every_servable_file_is_public_safe(site_files: list[Path]) -> None:
    """The scan must cover the whole build, not just the page.

    A static host serves every file in the directory it is given. The deploy
    note lives here and is therefore reachable at /DEPLOY.md by anyone -- so it
    is held to the same standard as the page. Checking only index.html would
    leave the most likely leak surface unread.
    """
    names, provenance = _service_names()
    leaks: dict[str, list[str]] = {}
    for path in site_files:
        rel = path.relative_to(SITE).as_posix()
        low = path.read_text(encoding="utf-8", errors="replace").lower()
        hits = [t for t in FORBIDDEN_TOKENS if t.lower() in low]
        hits += [n for n in names
                 if re.search(rf"(?<![a-z0-9-]){re.escape(n)}(?![a-z0-9-])", low)]
        if hits:
            leaks[rel] = sorted(set(hits))
    assert not leaks, (
        f"internal tokens in publicly servable files: {leaks} "
        f"(service vocabulary from {provenance})"
    )


def test_no_external_url_outside_allowlist(served: str) -> None:
    found = set(re.findall(r"https?://[^\s\"'<>)]+", served))
    unexpected = sorted(u for u in found if u.rstrip("/") not in
                        {a.rstrip("/") for a in ALLOWED_URLS})
    assert not unexpected, (
        f"undeclared external URLs: {unexpected}. "
        f"Allowed: {json.dumps(ALLOWED_URLS, indent=2)}"
    )


def test_no_script_tag(served: str) -> None:
    """No JavaScript at all -- the page must work with scripting off."""
    assert "<script" not in served.lower(), "page carries a <script> tag"


def test_no_fetched_subresource(served: str) -> None:
    """Every href/src is a data URI, a fragment, a mailto, or the declared
    canonical origin. Nothing is fetched to render this page."""
    # Quote-aware: a double-quoted value may legitimately contain single quotes
    # (the inline SVG favicon does). A naive ["'] class truncates the capture
    # there and would wave a later leak straight through.
    refs = [d or s for d, s in re.findall(
        r"""\b(?:href|src|srcset|poster)\s*=\s*(?:"([^"]*)"|'([^']*)')""",
        served, flags=re.I)]
    allowed_prefixes = ("data:", "#", "mailto:")
    allowed_exact = {a.rstrip("/") for a in ALLOWED_URLS}
    bad = [r for r in refs
           if not r.startswith(allowed_prefixes)
           and r.rstrip("/") not in allowed_exact]
    assert not bad, f"page fetches subresources: {bad}"
    assert "@import" not in served, "CSS @import would fetch a stylesheet"
    assert not re.search(r"url\(\s*['\"]?https?:", served), \
        "CSS url() points at a network resource"


def test_site_is_self_contained(site_files: list[Path]) -> None:
    """The whole build is the page plus its deploy note. No stray assets that
    could quietly carry a font, a tracker, or an internal artefact."""
    names = sorted(p.relative_to(SITE).as_posix() for p in site_files)
    assert "index.html" in names, names
    unexpected = [n for n in names
                  if not (n == "index.html" or n.endswith(".md")
                          or n in {"_headers", "_redirects", "robots.txt"})]
    assert not unexpected, f"unexpected files in the build: {unexpected}"


# --------------------------------------------------------------------------
# 2. HONESTY -- the contact slot
# --------------------------------------------------------------------------

PLACEHOLDER = "{{CONTACT}}"
EMAIL = re.compile(r"^[^@\s<>\"']+@[A-Za-z0-9]([A-Za-z0-9-]*[A-Za-z0-9])?"
                   r"(\.[A-Za-z0-9]([A-Za-z0-9-]*[A-Za-z0-9])?)+$")

# Addresses that are shaped like an email but are stand-ins. An invented address
# is worse than an empty one: it silently fails for whoever writes to it.
FAKE_LOCALPARTS = {"example", "test", "foo", "bar", "tbd", "todo", "changeme",
                   "placeholder", "you", "your-email", "email", "noreply",
                   "no-reply", "someone", "user", "name"}
FAKE_DOMAINS = {"example.com", "example.org", "example.net", "test.com",
                "domain.com", "email.com", "yourdomain.com", "tbd.com",
                "localhost", "invalid"}


def _contact_slot(served: str) -> str:
    m = re.search(r'<span class="slot">(.*?)</span>', served, flags=re.S)
    assert m, "contact slot markup not found -- the page must carry one"
    return m.group(1).strip()


def test_contact_slot_is_placeholder_or_real_address(served: str) -> None:
    value = _contact_slot(served)

    if value == PLACEHOLDER:
        # Allowed, and reported. The principal supplies the address at deploy
        # time; shipping the placeholder is honest, shipping a fake is not.
        pytest.skip(f"contact slot still the unreplaced placeholder {PLACEHOLDER} "
                    f"-- allowed; see DEPLOY.md step 5")

    assert EMAIL.match(value), (
        f"contact slot holds {value!r}, which is neither the {PLACEHOLDER} "
        f"placeholder nor a valid email address"
    )
    local, _, domain = value.partition("@")
    assert local.lower() not in FAKE_LOCALPARTS, \
        f"contact slot holds a stand-in local part: {value!r}"
    assert domain.lower() not in FAKE_DOMAINS, \
        f"contact slot holds a stand-in domain: {value!r}"


def test_placeholder_appears_at_most_once(served: str) -> None:
    assert served.count(PLACEHOLDER) <= 1, \
        "the contact placeholder appears more than once; one slot, one home"


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


# --------------------------------------------------------------------------
# 3. LEGIBILITY -- contrast, computed from the page's own tokens
# --------------------------------------------------------------------------

def _relative_luminance(hex_colour: str) -> float:
    h = hex_colour.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    chan = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    chan = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
            for c in chan]
    return 0.2126 * chan[0] + 0.7152 * chan[1] + 0.0722 * chan[2]


def contrast(a: str, b: str) -> float:
    la, lb = _relative_luminance(a), _relative_luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def _tokens(served: str) -> dict[str, dict[str, str]]:
    """Pull --name:#hex out of the light :root block and the dark override."""
    dark_block = re.search(
        r"@media\s*\(prefers-color-scheme:\s*dark\)\s*\{\s*:root\s*\{(.*?)\}",
        served, flags=re.S)
    assert dark_block, "no prefers-color-scheme:dark override in the page"
    light_block = re.search(r":root\s*\{(.*?)\}", served, flags=re.S)
    assert light_block, "no :root token block in the page"

    def parse(text: str) -> dict[str, str]:
        return {k: v for k, v in re.findall(r"--([a-z0-9-]+)\s*:\s*(#[0-9A-Fa-f]{3,8})",
                                            text)}

    light = parse(light_block.group(1))
    dark = dict(light)
    dark.update(parse(dark_block.group(1)))
    return {"light": light, "dark": dark}


# Every pair the page actually paints, foreground token against the surface it
# sits on. Nothing here is decorative: each one carries body or label text.
TEXT_PAIRS = [
    ("ink", "bg"),
    ("muted", "bg"),
    ("soft", "bg"),
    ("ink", "panel"),
    ("muted", "panel"),
    ("paper-ink", "paper"),
    ("paper-muted", "paper"),
    ("accent-ink", "accent"),
]

AA_NORMAL = 4.5


@pytest.mark.parametrize("scheme", ["light", "dark"])
def test_text_contrast_meets_aa(served: str, scheme: str) -> None:
    tok = _tokens(served)[scheme]
    failures = []
    for fg, bg in TEXT_PAIRS:
        assert fg in tok and bg in tok, f"missing token in {scheme}: {fg}/{bg}"
        ratio = contrast(tok[fg], tok[bg])
        if ratio < AA_NORMAL:
            failures.append(f"--{fg} on --{bg} = {ratio:.2f}:1 "
                            f"({tok[fg]} on {tok[bg]})")
    assert not failures, f"{scheme} scheme below WCAG AA {AA_NORMAL}:1 -> {failures}"


# --------------------------------------------------------------------------
# Structure -- semantics a screen reader depends on
# --------------------------------------------------------------------------

def test_document_structure(served: str) -> None:
    assert re.search(r'<html[^>]*\blang="en"', served), 'missing lang="en"'
    assert re.search(r'<meta[^>]*charset="?utf-8', served, flags=re.I)
    assert re.search(r'<meta[^>]*name="viewport"', served, flags=re.I)
    for landmark in ("<header", "<main", "<footer"):
        assert landmark in served, f"missing landmark {landmark}>"
    assert served.count("<h1") == 1, "a page has exactly one h1"
    assert "&copy; 2026 ZeonLab" in served or "© 2026 ZeonLab" in served, \
        "footer must carry the copyright line"


def test_headers_policy_agrees_with_the_page(served: str) -> None:
    """The _headers CSP and the page must not drift apart. The page fetches
    nothing; the policy that ships with it must say so, or one of the two is
    lying and the reader cannot tell which."""
    headers = SITE / "_headers"
    if not headers.is_file():
        pytest.skip("no _headers file in this build")
    text = headers.read_text(encoding="utf-8")
    csp = next((l for l in text.splitlines()
                if l.strip().lower().startswith("content-security-policy:")), None)
    assert csp, "_headers ships without a Content-Security-Policy"
    assert "default-src 'none'" in csp, f"CSP does not deny by default: {csp}"
    # A script-src allowance would contradict test_no_script_tag.
    assert not re.search(r"script-src\s+(?!'none')", csp), \
        f"CSP permits script sources on a page that carries no script: {csp}"
    assert "<script" not in served.lower()


def test_every_section_is_labelled(served: str) -> None:
    """aria-labelledby on each section must resolve to an id that exists."""
    for target in re.findall(r'<section[^>]*aria-labelledby="([^"]+)"', served):
        assert re.search(rf'id="{re.escape(target)}"', served), \
            f"aria-labelledby={target!r} points at no element"
