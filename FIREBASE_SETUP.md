# Firebase & LINE login setup

## Firebase project
Project: `daymark-20261030-ncu` (Spark plan), web app nickname: `Daymark Web`.

## LINE Login
1. In LINE Developers, create a LINE Login channel and configure the callback URL as `https://<your-auth-domain>/__/auth/handler` (use the Firebase `authDomain` value).
2. Copy the LINE Channel ID and Channel Secret from the LINE Developers console.
3. Firebase Authentication does **not** offer LINE as a native provider. Its OpenID Connect (OIDC) provider is only available after upgrading to Firebase Authentication with Identity Platform. Do not paste the LINE channel secret into the static site. Use a trusted backend/Identity Platform integration to exchange and verify tokens.
4. When an OIDC provider/backend is configured, add `115707002-boop.github.io` as an authorized domain and wire that provider into the sign-in UI.

The page gates its dashboard until Firebase confirms an authenticated user. This static-site gate alone does not protect public repository contents or provide server-side authorization; do not store confidential data here.
