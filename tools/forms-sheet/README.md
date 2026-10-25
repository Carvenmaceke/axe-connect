# Website forms -> Google Sheet

Quote requests, contact messages, reviews and newsletter sign-ups from axeconnect.co.za
are saved in a Google Sheet, emailed to you, and (except reviews) answered with an
automatic reply to the customer. EmailJS stays as a backup if the Sheet can't be reached.

## Setup (about 10 minutes, once)
1. Create a Google Sheet called **Axe Connect forms** (signed in as carvenmaceke9@gmail.com).
2. **Extensions > Apps Script**. Delete what's there, paste everything from `Code.gs`, save.
3. Choose **setup** in the function menu and click **Run**. Allow the permissions
   (Google shows "unverified app" for your own scripts: Advanced > Go to project).
   The tabs Quotes, Messages, Reviews and Subscribers appear in the Sheet.
4. **Deploy > New deployment > Web app**. Execute as **Me**, Who has access **Anyone**.
   Click **Deploy** and copy the **Web app URL** (ends in `/exec`).
5. Send the URL to Claude, or paste it into `index.html`: `const FORMS_URL = '';`
   then run `python3 tools/build_pages.py`.

## Using it
- New enquiries: a row in the right tab plus an email to you (reply goes straight to the customer).
- Track progress in the **Status** column (New, Quoted, Won, Lost...).
- Reviews: copy the JSON from the Reviews tab into `reviews.json` to publish one.
- Newsletter: in the **Newsletter** tab type the subject in B1 and the message in B2, then
  **Axe Connect > Send newsletter to subscribers**. Each email has an unsubscribe link.
- Gmail limit: about 100 emails a day on a free account.
- After editing `Code.gs`: **Deploy > Manage deployments > Edit > New version** (keeps the same URL).
