# Setting up your GitHub profile

1. On GitHub, create a **public** repository named exactly like your username
   (`ZoolCoder/ZoolCoder`). GitHub shows its README on your profile.
2. Copy everything from this folder into it.
3. Put a front-facing photo at `assets/me.jpg` (plain background works best).
4. Open `scripts/config.py` and check `GITHUB_USER`, `PORTFOLIO`, `NOW`, `SINCE`.
5. Run:
   ```
   pip install pillow
   python scripts/build.py
   ```
6. Commit and push. Then go to **Actions → Snake contribution graph → Run workflow**
   once; after that it updates itself every 12 hours.

Re-run `build.py` whenever you change `config.py`.
