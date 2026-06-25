# Will You Go On A Date With Me? 💕

A cheeky single-page site: the **No** button waddles away whenever you try to
catch it, the **Yes** button grows + slams onto the screen a little more every
time, and Robin (Teen Titans Go) goes from heart-eyes → straight-face → crying
the longer you dodge. Say yes and it rains confetti — and (optionally) emails you.

**Live:** https://jakeeup.github.io/for-you/

Pure HTML/CSS/JS, no build step. Just open `index.html` or host the folder anywhere static.

---

## 1) Get the "email me when she says yes" working

GitHub Pages can't send email on its own (no server), so the page uses the free
**Web3Forms** service. Your email address stays private — only a public "access
key" goes in the code.

1. Go to **https://web3forms.com**
2. Type your email (`fjacob31@yahoo.com`) into the **Create Access Key** box.
3. Check your inbox — Web3Forms emails you an **access key** (looks like
   `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`).
4. In `index.html`, find `web3formsKey` in the `CONFIG` block and paste it in:
   ```js
   web3formsKey: "PASTE-YOUR-KEY-HERE",
   ```
5. Save, commit, and push (see step 3). Done — when she clicks **Yes** you get an
   email titled *"She said YES! 💍"*.

> Until a real key is added, the page works perfectly — it just skips the email.

---

## 2) Make it yours

Edit the `CONFIG` block near the top of the `<script>` in `index.html`:

```js
const CONFIG = {
  question:       "Will you go on a date with me?",
  subtitle:       "(please say yes 💕)",
  yesText:        "Yes 💖",
  successTitle:   "YAYYY! I knew it! 💖",
  successMessage: "You just made my whole day 🥰",
  web3formsKey:   "YOUR_ACCESS_KEY_HERE",
  notifySubject:  "She said YES! 💍",
  notifyMessage:  "{name} said yes 🥰",
  noTexts: [ "No", "Are you sure?", "Really sure??", /* ...the taunts... */ ]
};
```

- `noTexts` — what the No button says as it runs (cycles through the list).
- `FULL_SAD_AT` (further down) — how many No-dodges until Robin is fully crying.
- Colors live in the `:root { ... }` CSS variables.

## How the chase works
- **Desktop:** the No button bolts when your cursor gets within ~130px.
- **Mobile:** tapping it makes it jump — it never lands.
- Every dodge grows the Yes button (capped at 6×) with a slam + screen shake,
  and nudges Robin one step sadder.

## The Robin images
`images/love.jpg`, `neutral.png`, `cry.jpg` are the originals. `make-transparent.py`
removes their backgrounds (AI `isnet-anime` model) into the transparent
`robin-love.png` / `robin-neutral.png` / `robin-cry.png` the site uses. To redo them:

```bash
pip install "rembg[cpu]" pillow
python make-transparent.py
```

---

## 3) Update the live site
It's already on GitHub Pages. Any push to `main` rebuilds it automatically:

```bash
git add -A
git commit -m "update"
git push
```
