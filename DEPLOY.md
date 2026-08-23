# Deploying zeonlab.ai

`site/` is the whole deployed site: one `index.html` with its CSS inline and
one `_headers` file. There is no build step, no dependency, no JavaScript, and
nothing fetched from a network at render time. `DEPLOY.md` stays in the
repository; the publish workflow uploads `site/` only.

**This step needs Cloudflare account access that the engineering lane does not
hold and should not hold.** Everything below is written to be done by the
account owner.

---

## 1. Create the Pages project

Cloudflare dashboard → **Workers & Pages** → **Create** → **Pages**.

Choose **Direct Upload**, name the project `zeonlab-site`, and leave the build
command and framework preset empty. The workflow uploads the `site/` directory
with Wrangler after an approved merge; do not connect the repository to a
second Cloudflare build integration.

Add the repository secrets expected by the workflow: `CLOUDFLARE_PAGES_TOKEN`
with permission to publish this Pages project, and `CLOUDFLARE_ACCOUNT_ID` for
the owning account. Leave build variables unset; there is nothing to build.

## 2. Attach the domain

Project → **Custom domains** → **Set up a custom domain**. Add both, one at a
time:

- `zeonlab.ai`
- `www.zeonlab.ai`

If the zone is already on this Cloudflare account, Pages writes the DNS records
itself and manages the certificate. If you place or check the records by hand,
the Pages targets are:

| Type | Name | Target | Proxy |
|---|---|---|---|
| CNAME | `zeonlab.ai` (entered as `@`) | `zeonlab-site.pages.dev` | Proxied (orange cloud) |
| CNAME | `www` | `zeonlab-site.pages.dev` | Proxied (orange cloud) |

Substitute the project's real `*.pages.dev` hostname if you named the project
something other than `zeonlab-site`.

Remove any stale record that conflicts with the Pages targets above. Wait for
the custom domain to read *Active* before relying on the domain.

## 3. How publishing works

For the normal publish path, after review merge the page change to `main`. A
push to `main` that touches `site/`, `tests/`, or this workflow runs three gates
in order:

1. The public-surface contract runs against the servable files.
2. Wrangler directly uploads `site/` to the `zeonlab-site` Cloudflare Pages
   project.
3. A runner outside the deployment fetches `https://zeonlab.ai/` and compares
   the served bytes with the committed `site/index.html` bytes. The verifier
   permits only the documented Cloudflare beacon injection; any other mismatch
   fails.

Changes outside those paths do not trigger the normal publish path. There is no
hand upload step.

## 4. Verify from outside

Run these from an ordinary internet connection with no relationship to our own
network — a phone on cellular is a perfectly good check, because it proves the
page is reachable from the public internet rather than from somewhere
privileged.

```sh
curl -sI https://zeonlab.ai     | head -1     # expect: HTTP/2 200
curl -sI https://www.zeonlab.ai | head -1     # expect: HTTP/2 200
```

`200` is the pass. `522` and `523` indicate that the domain or origin is not
ready. A `301` or `308` from `www` to the apex is fine if you chose to redirect
one to the other.

Confirm the response headers arrived as well, since they are what stops the page
from ever fetching anything:

```sh
curl -sI https://zeonlab.ai | grep -i 'content-security-policy'
```

The policy denies everything by default and permits only an inline stylesheet
and a `data:` image. If a later edit introduces a web font, a CDN script or an
analytics beacon, the browser will block it and the console will go red — which
is the intended failure mode, because a silent external request on this page is
the defect.

## 5. Look at it

Open the live URL on a phone and on a desktop, and switch the system appearance
between light and dark. Check for zero console errors, zero horizontal overflow,
and no unexpected network requests. This check is against what Cloudflare
serves.

## 6. Re-run the contract against the live bytes

The test that guards this page can be pointed at the deployed site instead of at
the build: set the `ZEONLAB_SITE` environment variable to a directory holding a
copy of the served page, and run the suite from the source repository.

```sh
mkdir -p /tmp/zeonlab-live
curl -s https://zeonlab.ai > /tmp/zeonlab-live/index.html
ZEONLAB_SITE=/tmp/zeonlab-live python -m pytest tests/ -q -p no:randomly
```

That check sees what Cloudflare serves, rather than only what is in the
repository. It fails on any CJK character, private hostname or path, internal
component name, undeclared external URL, `<script>` tag, fetched subresource,
contrast regression in either colour scheme, or an invalid contact address.

## Rolling back

Pages keeps every deployment. Project → **Deployments** → the one you want →
**Rollback to this deployment**. It is instant and needs no rebuild.
