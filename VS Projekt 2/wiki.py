import json
import os
import requests
from bs4 import BeautifulSoup
import textwrap

ARCHIVE_FILE = "scp_archive.json"
LOCAL_ARCHIVE = {}

if os.path.exists(ARCHIVE_FILE):
    try:
        with open(ARCHIVE_FILE, "r", encoding="utf-8") as f:
            LOCAL_ARCHIVE = json.load(f)
    except Exception:
        LOCAL_ARCHIVE = {}

SCP_001_PROPOSALS = {
    "clef": ("Dr. Clef's Proposal - The Gate Guardian", "code-name-dr-clef-s-proposal"),
    "locke": ("S. D. Locke's Proposal - When Day Breaks", "shaggydredlocks-proposal"),
    "factory": ("Bright's Proposal - The Factory", "scp-001-o5"),
    "scarlet": ("Tufto's Proposal - The Scarlet King", "tuftos-proposal"),
}


def fetch_scp_article(query: str, user: dict, lang: str = "en") -> list[str]:
    clean_q = query.lower().replace("scp-", "").strip()
    if clean_q.isdigit():
        clean_q = clean_q.zfill(3)

    base_url = (
        "https://scp-wiki-de.wikidot.com"
        if lang == "de"
        else "https://scp-wiki.wikidot.com"
    )

    # 1. Special access check for SCP-001.
    if clean_q == "001":
        if not user.get("is_o5"):
            return [
                "==================================================================",
                " [ACCESS DENIED] MEMETIC KILL AGENT ARMED",
                " ACCESS TO SCP-001 IS RESTRICTED TO O5 COUNCIL MEMBERS (LEVEL 5).",
                f" CURRENT CLEARANCE: LEVEL {user.get('clearance')} ({user.get('name')})",
                "==================================================================",
            ]
        return [
            "=== [O5 OVERRIDE ACCEPTED] SCP-001 ARCHIVE UNLOCKED ===",
            "Choose a proposal command:",
            "  scp 001 clef     -> The Gate Guardian",
            "  scp 001 locke    -> When Day Breaks",
            "  scp 001 factory  -> The Factory",
            "  scp 001 scarlet  -> The Scarlet King",
            "============================================================",
        ]

    if clean_q.startswith("001 "):
        if not user.get("is_o5"):
            return ["[ACCESS DENIED] LEVEL 5 (O5) REQUIRED."]
        parts = clean_q.split(" ", 1)
        key = parts[1].strip() if len(parts) > 1 else ""
        if key not in SCP_001_PROPOSALS:
            return ["UNKNOWN PROPOSAL. USE: clef, locke, factory, scarlet"]
        title, slug = SCP_001_PROPOSALS[key]
        url = f"{base_url}/{slug}"
    else:
        # 2. Check whether the entry is in the local English archive.
        if lang == "en" and clean_q in LOCAL_ARCHIVE:
            lines = [f"=== [LOCAL ARCHIVE] SCP-{clean_q} FILE ===", ""]
            for p in LOCAL_ARCHIVE[clean_q]:
                lines.extend(textwrap.wrap(p, width=82))
                lines.append("")
            return lines
        url = f"{base_url}/scp-{clean_q}"

    # 3. Fetch the article from the live wiki.
    try:
        res = requests.get(url, timeout=8)
        if res.status_code != 200:
            return [f"[HTTP ERROR {res.status_code}] FILE UNAVAILABLE: {url}"]

        soup = BeautifulSoup(res.text, "html.parser")
        content = soup.find("div", id="page-content")
        if not content:
            return ["[ERROR] COULD NOT READ PAGE CONTENT."]

        lines = [f"=== [LIVE SCiPNET] DATEI ABRUF: {url.upper()} ===", ""]
        for p in content.find_all(["p", "blockquote"]):
            text = p.get_text().strip()
            if text:
                lines.extend(textwrap.wrap(text, width=82))
                lines.append("")
        return lines
    except Exception as e:
        return [f"[NETWORK ERROR] {e}"]
