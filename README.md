# 日序 Daymark

個人行程與任務管理單頁原型，使用 HTML、CSS 與 JavaScript。任務留存在目前瀏覽器的 localStorage，並依登入的提供者與使用者 ID 分開保存；不使用 Firebase、資料庫或 API Key。

## 啟用 Google 登入

1. 在 Google Cloud Console 建立 Web OAuth Client ID。
2. 將 `https://115707002-boop.github.io` 加入 Authorized JavaScript origins。
3. 將 Web Client ID 填入 `index.html` 的 `GOOGLE_CLIENT_ID`。

Google Identity Services 會回傳登入憑證供此原型辨識使用者。頁面不會把憑證送到伺服器；正式產品應由伺服器驗證 ID token。

## 啟用 LINE 登入

1. 在 LINE Developers 建立 LINE Login channel 和 LIFF app，並啟用 `profile` scope。
2. 將 Endpoint URL 設為 `https://115707002-boop.github.io/20261030/`。
3. 將 LIFF ID 填入 `index.html` 的 `LINE_LIFF_ID`。

此靜態頁面只在瀏覽器取得 LINE profile。不要在前端放 LINE Channel Secret。Google 與 LINE 帳戶不會自動合併。

## 限制

登入畫面適合原型展示，不能保護靜態頁面或本機資料。使用者可以直接讀取或修改頁面與 localStorage；沒有雲端同步、帳號資料庫或伺服器端授權。

