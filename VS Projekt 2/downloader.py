import json
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

ARCHIVE_FILE = "scp_archive.json"


def download_one(num_int: int):
    num_str = f"{num_int:03d}"
    url = f"https://scp-wiki.wikidot.com/scp-{num_str}"
    try:
        res = requests.get(url, timeout=8)
        if res.status_code != 200:
            return num_str, None
        soup = BeautifulSoup(res.text, "html.parser")
        content = soup.find("div", id="page-content")
        if not content:
            return num_str, None
        paragraphs = [
            p.get_text().strip()
            for p in content.find_all(["p", "blockquote"])
            if p.get_text().strip()
        ]
        return num_str, paragraphs
    except Exception:
        return num_str, None


if __name__ == "__main__":
    print("Starting download of SCP-002 through SCP-999 (Series 1)...")
    archive = {}
    with ThreadPoolExecutor(max_workers=12) as executor:
        for num_str, paragraphs in executor.map(download_one, range(2, 1000)):
            if paragraphs:
                archive[num_str] = paragraphs
                if int(num_str) % 50 == 0:
                    print(f"Progress: saved through SCP-{num_str}...")

    with open(ARCHIVE_FILE, "w", encoding="utf-8") as f:
        json.dump(archive, f, ensure_ascii=False)
    print(f"Done! Saved {len(archive)} entries to {ARCHIVE_FILE}.")
