# Sign-in setup: Firebase + LINE LIFF

- Google uses Firebase Authentication and provides the Firebase UID.
- LINE uses LIFF SDK and provides the LINE user profile and LIFF login status.
- Current Firebase project: `daymark-20261030-ncu`; current Firebase Web app: `Daymark Web`.

## Configure LINE
1. Create a LINE Login channel in LINE Developers and a LIFF app in that channel.
2. Set the LIFF Endpoint URL to `https://115707002-boop.github.io/20261030/` and enable the profile scope.
3. Copy the LIFF ID and replace `YOUR_LINE_LIFF_ID` in `index.html`.
4. Add the same endpoint to the channel's allowed callback/login URL settings if requested by LINE.
5. Deploy `index.html` to GitHub Pages, then test login from the HTTPS Pages URL, not from a `file://` URL.

The LINE button calls LIFF `init`, starts LINE login, and retrieves the LIFF profile when logged in. It deliberately does **not** treat a LINE profile as a Firebase user. The dashboard remains gated on Firebase Auth; to provide one shared account/UID for both providers, implement a trusted backend that verifies the LINE ID token and mints a Firebase custom token, or configure an appropriate Firebase Identity Platform OIDC provider. Do not put a LINE Channel Secret in the static HTML or GitHub.

Firebase config is public Web app configuration; it is not an authorization secret. Static-site UI gating does not protect public repository contents or private data. Enforce access on a trusted backend/database before storing sensitive user data.
