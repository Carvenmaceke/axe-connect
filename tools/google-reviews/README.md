# Google reviews on axeconnect.co.za

A free Google Apps Script reads the Axe Connect Google Business Profile once a day and
the website shows the Google rating, total reviews and latest Google reviews automatically.
You also get an email whenever a new Google review comes in.

Google's Places API shares the **5 most relevant reviews** plus the overall rating and count.

## Setup (about 15 minutes, once)

### 1. Get a Google API key
1. Go to https://console.cloud.google.com and create a project called **Axe Connect**.
2. Add billing (Google asks for a card; this usage stays inside the free monthly allowance).
3. **APIs & Services > Library**: search **Places API (New)** and click **Enable**.
4. **APIs & Services > Credentials > Create credentials > API key**. Copy the key.
5. Click the key > **API restrictions > Restrict key > Places API (New)** > Save.

### 2. Create the Google Sheet and script
1. Create a new Google Sheet called **Axe Connect reviews**.
2. **Extensions > Apps Script**. Delete what's there and paste everything from `Code.gs`.
3. **Project Settings** (gear icon) > **Script properties > Add**:
   name `PLACES_API_KEY`, value = your key. Save.

### 3. Find your Place ID
1. In the script editor choose **findPlaceId** in the function menu and click **Run**
   (allow the permissions it asks for).
2. Open **Execution log**: copy the ID next to "Axe Connect" (starts with `ChIJ`).
3. Paste it into `const PLACE_ID = '...'` at the top of the script. Save.

### 4. Switch it on
1. Choose **setup** and click **Run**. The sheet fills with your reviews and a daily
   refresh is scheduled.
2. **Deploy > New deployment > Select type: Web app**.
   Execute as: **Me**. Who has access: **Anyone**. Click **Deploy** and copy the
   **Web app URL** (ends in `/exec`).
3. Send that URL to Claude, or paste it into `index.html` here:
   `const GOOGLE_REVIEWS_URL = '';`  then rebuild the pages (`python3 tools/build_pages.py`).
