# Firebase Google sign-in

1. Open the project in Firebase Console, add a Web app, and copy the app settings into the `config` object in `index.html` (replace the four `YOUR_...` placeholders).
2. Go to **Authentication → Sign-in method** and enable **Google**.
3. Under **Authentication → Settings → Authorized domains**, add `115707002-boop.github.io`.
4. Commit and push `index.html` to `main`; GitHub Pages will redeploy. The dashboard is hidden unless Firebase confirms a signed-in user.

This is a static-site sign-in gate, not server-side access control. The repository and static HTML are public; do not store confidential data here. Existing task data remains in browser localStorage. To protect data, use a trusted backend and enforce Firebase token verification/database security rules.
