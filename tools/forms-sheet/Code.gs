/**
 * Axe Connect: website forms -> Google Sheet + Gmail.
 *
 * Paste into Extensions > Apps Script of a Google Sheet and deploy as a web app
 * (Execute as: Me, Who has access: Anyone). Every form on axeconnect.co.za posts here:
 * the submission is saved in its own tab, you get an email, and the customer gets an
 * automatic reply. Setup steps: tools/forms-sheet/README.md
 */

const OWNER_EMAIL = 'carvenmaceke9@gmail.com';   // where new enquiries are emailed
const BUSINESS = 'Axe Connect';
const SITE = 'https://axeconnect.co.za';
const WHATSAPP = '060 795 0837';

const TABS = {
  quote:      { name: 'Quotes',      cols: ['Received', 'Name', 'Phone', 'Email', 'Service', 'Business', 'Type', 'Pages', 'Features / problem', 'Budget', 'Deadline', 'Message', 'Status'] },
  contact:    { name: 'Messages',    cols: ['Received', 'Name', 'Phone', 'Email', 'Service', 'Message', 'Status'] },
  review:     { name: 'Reviews',     cols: ['Received', 'Name', 'Rating', 'Service', 'Review', 'JSON for reviews.json', 'Published?'] },
  newsletter: { name: 'Subscribers', cols: ['Subscribed', 'Email', 'Page', 'Status'] }
};

function doPost(e) {
  try {
    const d = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    const kind = d.kind;
    if (!TABS[kind]) return json_({ ok: false, error: 'Unknown form' });
    if (d.website) return json_({ ok: true });                 // honeypot: pretend success for bots
    const f = d.fields || {};
    const email = String(f.email || '').trim();
    if (email && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return json_({ ok: false, error: 'Invalid email' });

    const now = new Date();
    const row = rowFor_(kind, f, now);
    if (kind === 'newsletter' && isSubscribed_(email)) return json_({ ok: true, already: true });
    sheet_(kind).appendRow(row);

    // Email you
    const body = (d.msg || JSON.stringify(f, null, 2)) + '\n\n— Saved in the "' + TABS[kind].name + '" tab of your Axe Connect forms sheet.';
    const opts = { name: BUSINESS + ' website' };
    if (email) opts.replyTo = email;
    MailApp.sendEmail(OWNER_EMAIL, clip_(d.subject || ('New ' + kind + ' from the website'), 250), body, opts);

    // Automatic reply to the customer
    if (email && kind !== 'review') autoReply_(kind, email, f);
    return json_({ ok: true });
  } catch (err) {
    return json_({ ok: false, error: String(err) });
  }
}

/** Unsubscribe link in newsletter emails. */
function doGet(e) {
  const p = (e && e.parameter) || {};
  if (p.unsubscribe) {
    const sh = sheet_('newsletter'), data = sh.getDataRange().getValues();
    for (let i = 1; i < data.length; i++) {
      if (String(data[i][1]).toLowerCase() === String(p.unsubscribe).toLowerCase()) sh.getRange(i + 1, 4).setValue('Unsubscribed');
    }
    return HtmlService.createHtmlOutput('<p style="font-family:sans-serif">You have been unsubscribed from ' + BUSINESS + ' emails.</p>');
  }
  return json_({ ok: true, service: BUSINESS + ' forms' });
}

function rowFor_(kind, f, now) {
  const c = s => clip_(s == null ? '' : String(s), 5000);
  if (kind === 'quote') return [now, c(f.name), c(f.phone), c(f.email), c(f.service), c(f.business), c(f.websiteType), c(f.pages), c(f.features), c(f.budget), c(f.deadline), c(f.extra), 'New'];
  if (kind === 'contact') return [now, c(f.name), c(f.phone), c(f.email), c(f.service), c(f.msg), 'New'];
  if (kind === 'review') return [now, c(f.name), Number(f.rating) || '', c(f.service), c(f.text), c(f.snippet), 'No'];
  return [now, c(f.email), c(f.page), 'Subscribed'];
}

function autoReply_(kind, email, f) {
  const first = String(f.name || '').trim().split(' ')[0];
  const hi = first ? 'Hi ' + first + ',' : 'Hi,';
  const subjects = {
    quote: 'We received your quote request – ' + BUSINESS,
    contact: 'Thanks for your message – ' + BUSINESS,
    newsletter: "You're subscribed to " + BUSINESS
  };
  const lines = {
    quote: 'Thanks for your quote request' + (f.service ? ' for ' + f.service : '') + '. We are looking at the details and will come back to you with a clear quote soon.',
    contact: 'Thanks for getting in touch. We received your message and will reply as soon as possible.',
    newsletter: 'Thanks for subscribing. We will only email you occasionally, with specials and useful updates.'
  };
  const text = hi + '\n\n' + lines[kind] + '\n\nNeed us sooner? WhatsApp or call ' + WHATSAPP + ' (available 24/7).\n\n' + BUSINESS + '\n' + SITE;
  const html = '<div style="font-family:Arial,sans-serif;max-width:560px;margin:auto;border:1px solid #eee;border-radius:12px;overflow:hidden">' +
    '<div style="background:#0B0B0E;color:#fff;padding:18px 22px;font-size:18px;font-weight:bold"><span style="color:#E5372B">Axe</span> Connect</div>' +
    '<div style="padding:22px;color:#222;line-height:1.6"><p>' + hi + '</p><p>' + lines[kind] + '</p>' +
    '<p>Need us sooner? WhatsApp or call <b>' + WHATSAPP + '</b> (available 24/7).</p>' +
    '<p style="margin-top:22px"><a href="' + SITE + '" style="background:#E5372B;color:#fff;padding:10px 16px;border-radius:8px;text-decoration:none">Visit axeconnect.co.za</a></p></div></div>';
  MailApp.sendEmail(email, subjects[kind], text, { name: BUSINESS, htmlBody: html, replyTo: OWNER_EMAIL });
}

/** Menu in the Sheet: Axe Connect > Send newsletter. */
function onOpen() {
  SpreadsheetApp.getUi().createMenu('Axe Connect').addItem('Send newsletter to subscribers', 'sendNewsletter').addToUi();
}

/** Write the subject in B1 and the message in B2 of the "Newsletter" tab, then run this. */
function sendNewsletter() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const nl = ss.getSheetByName('Newsletter') || ss.insertSheet('Newsletter');
  if (!nl.getRange('A1').getValue()) { nl.getRange('A1:A2').setValues([['Subject'], ['Message']]); }
  const subject = String(nl.getRange('B1').getValue()).trim(), message = String(nl.getRange('B2').getValue()).trim();
  if (!subject || !message) { SpreadsheetApp.getUi().alert('Type the subject in B1 and the message in B2 of the "Newsletter" tab first.'); return; }
  const url = ScriptApp.getService().getUrl();
  const subs = sheet_('newsletter').getDataRange().getValues().slice(1).filter(r => r[3] === 'Subscribed' && r[1]);
  if (subs.length > MailApp.getRemainingDailyQuota()) { SpreadsheetApp.getUi().alert('Gmail allows ' + MailApp.getRemainingDailyQuota() + ' more emails today; you have ' + subs.length + ' subscribers. Try again tomorrow.'); return; }
  subs.forEach(r => {
    const unsub = url + '?unsubscribe=' + encodeURIComponent(r[1]);
    MailApp.sendEmail(r[1], subject, message + '\n\n' + BUSINESS + ' · ' + SITE + '\nUnsubscribe: ' + unsub, { name: BUSINESS, replyTo: OWNER_EMAIL });
  });
  SpreadsheetApp.getUi().alert('Sent to ' + subs.length + ' subscribers.');
}

function isSubscribed_(email) {
  if (!email) return false;
  return sheet_('newsletter').getDataRange().getValues().slice(1).some(r => String(r[1]).toLowerCase() === email.toLowerCase() && r[3] === 'Subscribed');
}

function sheet_(kind) {
  const ss = SpreadsheetApp.getActiveSpreadsheet(), t = TABS[kind];
  let sh = ss.getSheetByName(t.name);
  if (!sh) { sh = ss.insertSheet(t.name); sh.appendRow(t.cols); sh.setFrozenRows(1); sh.getRange(1, 1, 1, t.cols.length).setFontWeight('bold'); }
  return sh;
}

function clip_(s, n) { return s.length > n ? s.slice(0, n) : s; }
function json_(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }

/** Run once from the editor to create the tabs and approve permissions. */
function setup() { Object.keys(TABS).forEach(sheet_); onOpen(); }
