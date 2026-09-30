#!/usr/bin/env python3
"""Google Drive + Docs helper for the Rossen v2 workflow (runs in Claude Code).

Why this exists: the Show Plan is a shared Google Doc that producers edit live.
Rebuilding it would erase their edits, so every change after creation is made
IN PLACE — targeted text replacement and comment replies — never a rewrite.

One-time setup (see SETUP.md at the package root):
    pip install google-api-python-client google-auth-oauthlib
    Put your OAuth desktop-client file at ~/.rossen/credentials.json
    First run opens a browser to sign in; the token is cached at ~/.rossen/token.json

Commands:
    folder   --parent ID --name NAME            find-or-create a subfolder, print its ID
    find     --name TEXT [--parent ID]          list files whose title contains TEXT
    create   --folder ID --title T --html FILE  create a Google Doc from HTML, print its ID
    read     --doc ID [--out FILE]              export the doc as Markdown (plain text fallback)
    comments --doc ID [--all]                   list open comments (or all) with quoted text
    reply    --doc ID --comment CID --text T [--resolve]
    replace  --doc ID --find TEXT --with TEXT [--allow-many]
    upload   --folder ID FILE [FILE ...]        upload files (clips, stills), print IDs + links

`replace` is the edit primitive. It uses the Docs API replaceAllText, which
changes only the matched text and leaves every other character — including a
producer's edits — untouched. It refuses to run if the text matches zero times
(the anchor was edited away; re-read the doc) or more than once (the anchor is
ambiguous) unless --allow-many is passed.
"""
from __future__ import annotations

import argparse
import io
import json
import mimetypes
import sys
from pathlib import Path

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
]
HOME = Path.home() / ".rossen"
CREDS = HOME / "credentials.json"
TOKEN = HOME / "token.json"
DOC_MIME = "application/vnd.google-apps.document"
FOLDER_MIME = "application/vnd.google-apps.folder"


def _services():
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except ImportError:
        sys.exit("Missing libraries. Run: pip install google-api-python-client google-auth-oauthlib")
    creds = None
    if TOKEN.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDS.exists():
                sys.exit(f"No OAuth client file at {CREDS}. See SETUP.md, step 'Connect Google'.")
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDS), SCOPES)
            creds = flow.run_local_server(port=0)
        HOME.mkdir(parents=True, exist_ok=True)
        TOKEN.write_text(creds.to_json())
    drive = build("drive", "v3", credentials=creds)
    docs = build("docs", "v1", credentials=creds)
    return drive, docs


def _q(s: str) -> str:
    return s.replace("\\", "\\\\").replace("'", "\\'")


def cmd_folder(a):
    drive, _ = _services()
    q = (f"'{a.parent}' in parents and name = '{_q(a.name)}' "
         f"and mimeType = '{FOLDER_MIME}' and trashed = false")
    hits = drive.files().list(q=q, fields="files(id,name)").execute().get("files", [])
    if hits:
        print(hits[0]["id"])
        return
    f = drive.files().create(body={"name": a.name, "mimeType": FOLDER_MIME, "parents": [a.parent]},
                             fields="id").execute()
    print(f["id"])


def cmd_find(a):
    drive, _ = _services()
    q = f"name contains '{_q(a.name)}' and trashed = false"
    if a.parent:
        q += f" and '{a.parent}' in parents"
    for f in drive.files().list(q=q, fields="files(id,name,mimeType,modifiedTime,webViewLink)",
                                orderBy="modifiedTime desc").execute().get("files", []):
        print(json.dumps(f))


def cmd_create(a):
    from googleapiclient.http import MediaIoBaseUpload
    drive, _ = _services()
    html = Path(a.html).read_bytes()
    media = MediaIoBaseUpload(io.BytesIO(html), mimetype="text/html", resumable=False)
    f = drive.files().create(body={"name": a.title, "mimeType": DOC_MIME, "parents": [a.folder]},
                             media_body=media, fields="id,webViewLink").execute()
    print(json.dumps(f))


def cmd_read(a):
    drive, _ = _services()
    try:
        data = drive.files().export(fileId=a.doc, mimeType="text/markdown").execute()
    except Exception:
        data = drive.files().export(fileId=a.doc, mimeType="text/plain").execute()
    text = data.decode("utf-8") if isinstance(data, bytes) else data
    if a.out:
        Path(a.out).write_text(text)
        print(f"wrote {a.out} ({len(text)} chars)")
    else:
        print(text)


def cmd_comments(a):
    drive, _ = _services()
    token = None
    while True:
        r = drive.comments().list(
            fileId=a.doc, pageToken=token, pageSize=100,
            fields="nextPageToken,comments(id,author/displayName,content,resolved,"
                   "quotedFileContent/value,createdTime,replies(author/displayName,content))",
        ).execute()
        for c in r.get("comments", []):
            if c.get("resolved") and not a.all:
                continue
            print(json.dumps({
                "id": c["id"],
                "author": c.get("author", {}).get("displayName"),
                "on": (c.get("quotedFileContent") or {}).get("value"),
                "comment": c.get("content"),
                "resolved": c.get("resolved", False),
                "replies": [x.get("content") for x in c.get("replies", [])],
            }, ensure_ascii=False))
        token = r.get("nextPageToken")
        if not token:
            break


def cmd_reply(a):
    drive, _ = _services()
    body = {"content": a.text}
    if a.resolve:
        body["action"] = "resolve"
    drive.replies().create(fileId=a.doc, commentId=a.comment, body=body, fields="id").execute()
    print("replied" + (" and resolved" if a.resolve else ""))


def _count(text: str, needle: str) -> int:
    return text.count(needle)


def cmd_replace(a):
    drive, docs = _services()
    # Count first against the live doc so an edited-away or ambiguous anchor is caught.
    data = drive.files().export(fileId=a.doc, mimeType="text/plain").execute()
    text = data.decode("utf-8") if isinstance(data, bytes) else data
    n = _count(text, a.find)
    if n == 0:
        sys.exit(f"NOT FOUND: {a.find!r} — a producer may have edited this line. "
                 f"Re-read the doc and use the current text.")
    if n > 1 and not a.allow_many:
        sys.exit(f"AMBIGUOUS: {a.find!r} appears {n} times. Use a longer, unique anchor "
                 f"(include the clip ID), or pass --allow-many.")
    r = docs.documents().batchUpdate(documentId=a.doc, body={"requests": [{
        "replaceAllText": {"containsText": {"text": a.find, "matchCase": True},
                           "replaceText": getattr(a, "with")}}]}).execute()
    changed = r["replies"][0].get("replaceAllText", {}).get("occurrencesChanged", 0)
    print(f"replaced {changed}")


def cmd_upload(a):
    from googleapiclient.http import MediaFileUpload
    drive, _ = _services()
    for p in a.files:
        p = Path(p)
        mime = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
        media = MediaFileUpload(str(p), mimetype=mime, resumable=True)
        f = drive.files().create(body={"name": p.name, "parents": [a.folder]},
                                 media_body=media, fields="id,webViewLink").execute()
        print(json.dumps({"file": p.name, **f}))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("folder"); p.add_argument("--parent", required=True); p.add_argument("--name", required=True); p.set_defaults(fn=cmd_folder)
    p = sp.add_parser("find"); p.add_argument("--name", required=True); p.add_argument("--parent"); p.set_defaults(fn=cmd_find)
    p = sp.add_parser("create"); p.add_argument("--folder", required=True); p.add_argument("--title", required=True); p.add_argument("--html", required=True); p.set_defaults(fn=cmd_create)
    p = sp.add_parser("read"); p.add_argument("--doc", required=True); p.add_argument("--out"); p.set_defaults(fn=cmd_read)
    p = sp.add_parser("comments"); p.add_argument("--doc", required=True); p.add_argument("--all", action="store_true"); p.set_defaults(fn=cmd_comments)
    p = sp.add_parser("reply"); p.add_argument("--doc", required=True); p.add_argument("--comment", required=True); p.add_argument("--text", required=True); p.add_argument("--resolve", action="store_true"); p.set_defaults(fn=cmd_reply)
    p = sp.add_parser("replace"); p.add_argument("--doc", required=True); p.add_argument("--find", required=True); p.add_argument("--with", required=True); p.add_argument("--allow-many", action="store_true"); p.set_defaults(fn=cmd_replace)
    p = sp.add_parser("upload"); p.add_argument("--folder", required=True); p.add_argument("files", nargs="+"); p.set_defaults(fn=cmd_upload)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
