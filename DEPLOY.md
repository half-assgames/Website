# Putting half-assgames.com online

This guide takes the website in this folder live at **https://half-assgames.com**, hosted
free on GitHub Pages. You do the sign-ups and DNS changes. It takes about 30 minutes,
plus some waiting while the internet catches up.

**What changes:** the "Coming Soon" page goes away and your site appears.
**What doesn't change:** your `joshua@half-assgames.com` email and Google Search Console.
Their DNS records stay exactly as they are.

Where you see `half-assgames` as a GitHub name below, use whatever organisation name you end
up with in step 2.

---

## 1. Find where you manage the domain

The domain's DNS is run by **Squarespace**, so the DNS changes happen in Squarespace Domains.
You just need to know how you log in there.

1. Go to <https://lookup.icann.org>, search `half-assgames.com`, and look at **Registrar**.
   It will almost certainly say **Squarespace Domains**. (Google Domains customers were moved
   to Squarespace in 2023, and domains bought during Google Workspace sign-up live there too.)
2. Try signing in at <https://account.squarespace.com/domains>:
   - If you made a Squarespace account, use that.
   - Otherwise choose **Continue with Google** and pick `joshua@half-assgames.com`.
3. Still can't find it? Go to <https://admin.google.com> (signed in as `joshua@half-assgames.com`)
   > **Account** > **Domains** > **Manage domains**. Your domain's **Manage** or
   **DNS** link hands you over to Squarespace.

You're in the right place when you can see **half-assgames.com** and a **DNS** page with
records like `MX smtp.google.com`. Leave that tab open for step 4.

---

## 2. Make a GitHub organisation for the studio

The repo has to be public for free hosting. An organisation keeps your personal GitHub
account out of it: the site's commits are signed just "Josh" with the studio email.

1. Sign in to GitHub with your normal account.
2. Go to <https://github.com/organizations/plan> and pick **Free**.
3. **Organization name:** `half-assgames` (if it's taken, try `halfassgames`).
   **Contact email:** `joshua@half-assgames.com`. **Belongs to:** My personal account.
4. Skip inviting anyone.
5. Check your membership is hidden: open the organisation > **People**. Your name should
   say **Private**. If it says Public, change it to Private.

---

## 3. Put the website on GitHub

### Upload it

**With GitHub Desktop** (already on your PC):

1. **File** > **Add local repository** > choose this folder
   (`Documents\Half-Ass Games\Website`) > **Add repository**.
2. Click **Publish repository**.
   - **Name:** `website`
   - **Untick** "Keep this code private"
   - **Organization:** `half-assgames`
3. Click **Publish repository**.

**Or in a terminal** (create an empty public repo called `website` in the organisation first,
without a README):

```bash
git remote add origin https://github.com/half-assgames/website.git
```

```bash
git push -u origin main
```

### Turn on GitHub Pages

1. On GitHub, open the `website` repo > **Settings** > **Pages**.
2. Under **Build and deployment**: **Source** = Deploy from a branch,
   **Branch** = `main`, folder = **/docs**. Click **Save**.
3. **Custom domain** should fill in as `half-assgames.com` by itself (the `docs/CNAME` file
   tells it). If it's empty, type `half-assgames.com` and click **Save**.

It will say the DNS check failed. That's expected until step 4 is done.

### Verify the domain (stops anyone else using it on GitHub)

1. Open the **organisation** (not the repo) > **Settings** > **Pages** > **Add a domain**.
2. Type `half-assgames.com` and click **Add domain**.
3. GitHub shows a TXT record to add, something like
   `_github-pages-challenge-half-assgames` with a long code. Copy both; you'll add them in
   step 4. Leave this page open.

---

## 4. Change the DNS at Squarespace

In Squarespace Domains > **half-assgames.com** > **DNS** (sometimes **DNS Settings**).

### Leave these alone

| Host | Type | Data | What it is |
|---|---|---|---|
| @ | MX | smtp.google.com | Your email |
| @ | TXT | google-site-verification=... | Search Console |
| google._domainkey | TXT | v=DKIM1; ... | Email signing |

These might sit in a **Google Workspace** preset. Keep that preset.

### Delete the Squarespace parking records

Delete the **Squarespace Defaults** preset (or these records one by one):

| Host | Type | Data |
|---|---|---|
| @ | A | 198.185.159.144 |
| @ | A | 198.185.159.145 |
| @ | A | 198.49.23.144 |
| @ | A | 198.49.23.145 |
| www | CNAME | ext-sq.squarespace.com |

### Add the GitHub Pages records

Under **Custom records**, add each of these (leave TTL at its default):

| Host | Type | Data |
|---|---|---|
| @ | A | 185.199.108.153 |
| @ | A | 185.199.109.153 |
| @ | A | 185.199.110.153 |
| @ | A | 185.199.111.153 |
| @ | AAAA | 2606:50c0:8000::153 |
| @ | AAAA | 2606:50c0:8001::153 |
| @ | AAAA | 2606:50c0:8002::153 |
| @ | AAAA | 2606:50c0:8003::153 |
| www | CNAME | half-assgames.github.io |
| _github-pages-challenge-half-assgames | TXT | *the code GitHub gave you in step 3* |

The `www` record points at your **organisation's** github.io address, with no `/website` on
the end.

### Optional, while you're there: help your emails avoid spam folders

Your domain has no SPF record yet. Adding one tells other mail servers that Google sends
your email. Add it only if there's no other TXT record starting with `v=spf1`:

| Host | Type | Data |
|---|---|---|
| @ | TXT | v=spf1 include:_spf.google.com ~all |

---

## 5. Wait, then switch on HTTPS

1. DNS changes usually show up within an hour, but can take up to a day.
2. Back on the organisation's **Settings** > **Pages**, click **Verify** next to the domain.
3. In the repo's **Settings** > **Pages**, the custom domain should now say
   **DNS check successful**.
4. Once GitHub has made the certificate (minutes, sometimes a few hours), tick
   **Enforce HTTPS**.

### Check it all works

- <https://half-assgames.com> shows the site
- <https://www.half-assgames.com> jumps to the same site
- <https://half-assgames.com/deep-sea-panic/privacy/> shows the privacy policy
- Send yourself an email at `joshua@half-assgames.com` from another account to check
  email still arrives

---

## 6. Hook it up

- **Google Play Console** > your app > **Policy and programs** > **App content** >
  **Privacy policy**: `https://half-assgames.com/deep-sea-panic/privacy/`
- **Play Console** > **Store presence** > **Store settings** > **Website**:
  `https://half-assgames.com/deep-sea-panic/`
- **Google Search Console** (already verified for the domain) > **Sitemaps** > add
  `https://half-assgames.com/sitemap.xml`
- **itch.io:** add `https://half-assgames.com` to your profile's links, if you like

---

## If something goes wrong

- **"DNS check unsuccessful" after a day:** make sure the four old `198.x` A records and the
  `ext-sq.squarespace.com` CNAME are gone, and the four `185.199.x.153` A records are there.
  Squarespace can't show the "Coming Soon" page and your site at the same time.
- **"Enforce HTTPS" stays greyed out for more than a day:** in the repo's Settings > Pages,
  remove the custom domain, save, add it back, save. That asks GitHub for a new certificate.
- **Email stops arriving:** check the `MX smtp.google.com` record is still there.
- **The site looks old after a change:** GitHub takes about a minute to publish. Then
  refresh with Ctrl+F5.
