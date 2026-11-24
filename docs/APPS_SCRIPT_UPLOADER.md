# Drafts uploader: Google Apps Script (free, runs in your Google account)

**Why:** the Drive connector can't upload files over 10 MB. This tiny web app runs as *your* Google account and lets the cloud studio drop finished drafts (up to ~35 MB each) into `06_DRAFTS_FOR_REVIEW`. It can **only create files inside that one folder**: it cannot read, list, change or delete anything else.

## Setup (≈5 minutes, once). Use the account that owns `cynoimpakt@gmail.com`'s Drive (Editor on the studio folder)
1. Go to **script.google.com** → **New project**. Name it `Studio Draft Uploader`.
2. Delete the sample code and paste the code below. Click **Save**.
3. **Project Settings** (gear icon) → **Script Properties** → **Add property**:
   - Property: `UPLOAD_TOKEN`
   - Value: any long random text (e.g. 30+ random letters/numbers). Keep it; you'll paste it once more in step 6.
4. **Deploy → New deployment** → type **Web app**:
   - Execute as: **Me**
   - Who has access: **Anyone**
   - Click **Deploy** → **Authorize access** → choose your account → *Advanced → Go to Studio Draft Uploader* → **Allow**.
5. Copy the **Web app URL** (ends in `/exec`).
6. In this session's environment settings (title bar → environment menu → **Edit**) add two **environment variables**:
   - `DRAFT_UPLOAD_URL` = the Web app URL
   - `DRAFT_UPLOAD_TOKEN` = the token from step 3

   _(These are read by sessions in this environment. The token only allows creating files in the drafts folder.)_
7. Reply "uploader done". Variables apply from the next session restart; I'll test with a small file.

## Code
```javascript
// Studio Draft Uploader: creates files ONLY inside 06_DRAFTS_FOR_REVIEW (or a subfolder of it).
const DRAFTS_FOLDER_ID = '1WbkqnzdhDU_n8vjRgKONf8XnuN9Lg9Nr';   // GUJARATI_CREATOR_STUDIO/06_DRAFTS_FOR_REVIEW
const ALLOWED = ['video/mp4', 'image/jpeg', 'image/png', 'text/plain', 'text/markdown', 'application/json', 'application/x-subrip'];
const MAX_BYTES = 36 * 1024 * 1024;

function doPost(e) {
  try {
    const req = JSON.parse(e.postData.contents);
    const token = PropertiesService.getScriptProperties().getProperty('UPLOAD_TOKEN');
    if (!token || req.token !== token) return out_({ ok: false, error: 'unauthorized' });
    if (ALLOWED.indexOf(req.mimeType) < 0) return out_({ ok: false, error: 'type not allowed' });
    const bytes = Utilities.base64Decode(req.base64);
    if (bytes.length > MAX_BYTES) return out_({ ok: false, error: 'too large' });
    const name = String(req.name).replace(/[\\/:*?"<>|]/g, '_').slice(0, 120);
    let folder = DriveApp.getFolderById(DRAFTS_FOLDER_ID);
    if (req.subfolder) {
      const sub = String(req.subfolder).replace(/[\\/:*?"<>|]/g, '_').slice(0, 80);
      const it = folder.getFoldersByName(sub);
      folder = it.hasNext() ? it.next() : folder.createFolder(sub);
    }
    const file = folder.createFile(Utilities.newBlob(bytes, req.mimeType, name));
    return out_({ ok: true, id: file.getId(), url: file.getUrl(), size: bytes.length });
  } catch (err) {
    return out_({ ok: false, error: String(err).slice(0, 200) });
  }
}

function out_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}
```

## Security notes
- The web app only ever calls `createFile` / `createFolder` inside the drafts folder. No read, list, edit, share or delete.
- Wrong or missing token → rejected. Rotate by changing `UPLOAD_TOKEN` (and the env variable).
- Remove at any time: script.google.com → project → Deploy → Manage deployments → Archive.
