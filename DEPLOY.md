# Deploying zeonlab.ai

`site/` is the whole site: one `index.html` with its CSS inline, one
`_headers` file, and this note. There is no build step, no dependency, no
JavaScript, and nothing fetched from a network at render time.

**This step needs Cloudflare account access that the engineering lane does not
hold and should not hold.** Everything below is written to be done by the
account owner.

Note also that this file is written to be safe to publish. A static host serves
every file in the directory it is handed, so whatever ends up here is reachable
at `/DEPLOY.md`. Keep it free of anything you would not put on the page itself;
a test enforces that, and it is easier to keep than to repair.

Budget: about ten minutes, most of it waiting for the certificate.

---

## 0. Before uploading: fill the contact slot

`index.html` ships with a deliberate placeholder:

```html
<span class="slot">{{CONTACT}}</span>
```

Replace `{{CONTACT}}` with the address you want to receive mail at. The
placeholder was left unfilled on purpose: an invented address looks finished and
silently discards everyone who writes to it, so the build refuses to guess one.

Shipping the placeholder as-is is survivable — it is visibly a placeholder — but
shipping a fake address is not. The test in step 6 enforces exactly that
distinction, and only that one.

## 1. Create the Pages project

Cloudflare dashboard → **Workers & Pages** → **Create** → **Pages**.

**Use direct upload.** Choose *Upload assets* and name the project
`zeonlab-site`. Drag in the two files this site consists of — `index.html` and
`_headers` — rather than the folder that contains them; Pages serves what you
give it from the root, and a nested folder would put the page at
`/zeonlab-site/index.html` instead of `/`.

Direct upload is the recommendation and not merely the easier option. The
alternative, connecting the project to the source repository, grants Cloudflare
standing read access to that whole repository in order to publish two files that
never change on their own. That is a large permission for a small job. If you
connect it anyway, set the framework preset to *None*, leave the build command
empty, set the build output directory to `/`, and set the advanced *root
directory* to the directory containing this file.

Leave every build variable unset. There is nothing to build.

## 2. Confirm the preview

Pages gives the project a `*.pages.dev` address as soon as the first deployment
finishes. Open it and confirm the page renders before touching DNS — a problem
is far easier to see here than behind a domain.

## 3. Attach the domain

Project → **Custom domains** → **Set up a custom domain**. Add both, one at a
time:

- `zeonlab.ai`
- `www.zeonlab.ai`

Because the zone is already on this Cloudflare account, Pages writes the DNS
records itself and the certificate is Cloudflare-managed — you are not asked to
supply one. If you would rather place or check the records by hand, these are
the two Pages wants:

| Type | Name | Target | Proxy |
|---|---|---|---|
| CNAME | `zeonlab.ai` (entered as `@`) | `zeonlab-site.pages.dev` | Proxied (orange cloud) |
| CNAME | `www` | `zeonlab-site.pages.dev` | Proxied (orange cloud) |

Substitute the project's real `*.pages.dev` hostname if you named the project
something other than `zeonlab-site`.

**Delete the record that is there now.** `www.zeonlab.ai` currently answers
`525`, which is Cloudflare reporting that its TLS handshake to the origin behind
that record failed — something is still pointed at an origin that cannot serve
it. That record must be removed or replaced by the CNAME above, or it will keep
winning and the `525` will survive the Pages deployment. Check the apex for a
stale `A` record and delete that too.

Certificate issuance is the slow part: usually a minute or two, occasionally up
to about fifteen. The custom domain reads *Active* when it is done.

## 4. Verify from outside

Run these from an ordinary internet connection with no relationship to our own
network — a phone on cellular is a perfectly good check, because it proves the
page is reachable from the public internet rather than from somewhere
privileged.

```sh
curl -sI https://zeonlab.ai     | head -1     # expect: HTTP/2 200
curl -sI https://www.zeonlab.ai | head -1     # expect: HTTP/2 200
```

`200` is the pass. `525` means step 3 is unfinished: either the old origin
record is still winning, or the certificate has not issued yet. `522` and `523`
are the same class of problem. A `301` or `308` from `www` to the apex is fine
if you chose to redirect one to the other.

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
between light and dark. The page was verified at 390, 768 and 1280 px in both
schemes with zero console errors, zero horizontal overflow and exactly one
network request, but that verification was against the build. This one is
against what Cloudflare serves.

## 6. Re-run the contract against the live bytes

The test that guards this page can be pointed at the deployed site instead of at
the build: set the `ZEONLAB_SITE` environment variable to a directory holding a
copy of the served page, and run the suite from the source repository. The exact
command is in the accompanying design note.

```sh
mkdir -p /tmp/zeonlab-live
curl -s https://zeonlab.ai > /tmp/zeonlab-live/index.html
```

That is the check worth keeping, because it sees an edit made in the Cloudflare
dashboard, which no repository test ever will. It fails on any CJK character,
any private hostname or path, any internal component name, any undeclared
external URL, any `<script>` tag, any fetched subresource, a contrast regression
in either colour scheme, and a contact slot holding something that is neither
the untouched placeholder nor a valid address. An untouched placeholder is
reported rather than failed.

## Rolling back

Pages keeps every deployment. Project → **Deployments** → the one you want →
**Rollback to this deployment**. It is instant and needs no rebuild.

## How it publishes now (2026-08-16)

A merge to the staging repository's `staging` branch that touches this
directory runs the `publish-site` job of the collection workflow: the
public-safety contract first,
then `wrangler pages deploy` with a Pages-only token held as a repository
secret, then a fetch of `https://zeonlab.ai/` from outside comparing the served
bytes to the committed file (the Cloudflare beacon injection alone is stripped
before comparing, and the pass line says whether that was needed). A merge that
does not touch the site skips all three steps and stays green. No hand upload.

Observed: the first real page change published itself (`b2382ddb5`, live and
byte-identical from outside); the verifier's own defects were fixed after and
prove themselves on the next page change.
