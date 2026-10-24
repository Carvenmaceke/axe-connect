/**
 * Axe Connect: Google reviews for the website.
 *
 * Paste this into Extensions > Apps Script of a Google Sheet. Once a day it reads the
 * rating, review count and latest reviews of the Axe Connect Business Profile from the
 * Google Places API, saves them in the Sheet, emails you when a new review arrives, and
 * serves them to axeconnect.co.za as JSON. Setup steps: tools/google-reviews/README.md
 */

// Your Google Place ID. Leave empty and run findPlaceId() once to look it up.
const PLACE_ID = '';
// Where "new review" alerts go.
const ALERT_EMAIL = 'carvenmaceke9@gmail.com';
// Used by findPlaceId() only.
const SEARCH_TEXT = 'Axe Connect Pretoria';

function apiKey_() {
  const key = PropertiesService.getScriptProperties().getProperty('PLACES_API_KEY');
  if (!key) throw new Error('Add your API key: Project Settings > Script properties > PLACES_API_KEY');
  return key;
}

/** Run once if you don't know your Place ID. The matches appear in the Execution log. */
function findPlaceId() {
  const res = UrlFetchApp.fetch('https://places.googleapis.com/v1/places:searchText', {
    method: 'post', contentType: 'application/json', muteHttpExceptions: true,
    headers: { 'X-Goog-Api-Key': apiKey_(), 'X-Goog-FieldMask': 'places.id,places.displayName,places.formattedAddress' },
    payload: JSON.stringify({ textQuery: SEARCH_TEXT })
  });
  const places = (JSON.parse(res.getContentText()).places || []);
  places.forEach(p => Logger.log(p.id + '  |  ' + (p.displayName || {}).text + '  |  ' + p.formattedAddress));
  if (!places.length) Logger.log('No match. Response: ' + res.getContentText());
}

/** Fetches the latest reviews and stores them in the Sheet. Runs daily once setup() has run. */
function refreshReviews() {
  if (!PLACE_ID) throw new Error('Set PLACE_ID at the top of the script (run findPlaceId() to get it).');
  const res = UrlFetchApp.fetch('https://places.googleapis.com/v1/places/' + PLACE_ID + '?languageCode=en', {
    muteHttpExceptions: true,
    headers: { 'X-Goog-Api-Key': apiKey_(), 'X-Goog-FieldMask': 'displayName,rating,userRatingCount,googleMapsUri,reviews' }
  });
  if (res.getResponseCode() !== 200) throw new Error('Places API ' + res.getResponseCode() + ': ' + res.getContentText());
  const d = JSON.parse(res.getContentText());
  const data = {
    updated: new Date().toISOString(),
    rating: d.rating || null,
    count: d.userRatingCount || 0,
    mapsUri: d.googleMapsUri || '',
    reviews: (d.reviews || []).map(r => {
      const a = r.authorAttribution || {};
      return {
        name: a.displayName || 'Google user', profile: a.uri || '', photo: a.photoUri || '',
        rating: r.rating || 0, text: ((r.originalText || r.text || {}).text) || '',
        when: r.relativePublishTimeDescription || '', time: r.publishTime || ''
      };
    })
  };

  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const store = ss.getSheetByName('data') || ss.insertSheet('data');
  const before = JSON.parse(store.getRange('A1').getValue() || '{"count":0,"reviews":[]}');
  store.getRange('A1').setValue(JSON.stringify(data));

  const table = ss.getSheetByName('Google reviews') || ss.insertSheet('Google reviews', 0);
  table.clear();
  table.appendRow(['Updated', data.updated, 'Rating', data.rating, 'Total reviews', data.count]);
  table.appendRow(['Name', 'Stars', 'When', 'Review']);
  data.reviews.forEach(r => table.appendRow([r.name, r.rating, r.when, r.text]));

  // Email an alert when Google reports more reviews than last time
  if (before.count && data.count > before.count && ALERT_EMAIL) {
    const known = (before.reviews || []).map(r => r.name + r.time);
    const fresh = data.reviews.filter(r => known.indexOf(r.name + r.time) === -1);
    const lines = fresh.map(r => '★'.repeat(r.rating) + '  ' + r.name + '\n' + r.text).join('\n\n');
    MailApp.sendEmail(ALERT_EMAIL, 'New Google review for Axe Connect (' + data.count + ' total)',
      (lines || 'You have a new Google review.') + '\n\nIt now shows on axeconnect.co.za automatically.\n' + data.mapsUri);
  }
  return data;
}

/** The website reads this (Deploy > New deployment > Web app, access: Anyone). */
function doGet() {
  const store = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('data');
  let json = store ? store.getRange('A1').getValue() : '';
  if (!json) json = JSON.stringify(refreshReviews());
  return ContentService.createTextOutput(json).setMimeType(ContentService.MimeType.JSON);
}

/** Run once: fetches reviews now and schedules a daily refresh at about 6am. */
function setup() {
  ScriptApp.getProjectTriggers().forEach(t => { if (t.getHandlerFunction() === 'refreshReviews') ScriptApp.deleteTrigger(t); });
  ScriptApp.newTrigger('refreshReviews').timeBased().everyDays(1).atHour(6).create();
  refreshReviews();
}
