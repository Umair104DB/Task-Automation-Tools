from pathlib import Path
import re
import shutil
import requests
from bs4 import BeautifulSoup


def move_jpg_files():
    source = Path(input("Folder containing JPG files: ").strip()).expanduser()
    if not source.is_dir():
        print("Folder does not exist.")
        return
    destination = source / "organized_jpg"
    destination.mkdir(exist_ok=True)
    moved = 0
    for file in source.iterdir():
        if file.is_file() and file.suffix.lower() in {".jpg", ".jpeg"}:
            target = destination / file.name
            if target.exists():
                print(f"Skipped duplicate name: {file.name}")
                continue
            shutil.move(str(file), str(target)); moved += 1
    print(f"Moved {moved} image(s) to {destination}")


def extract_emails():
    source = Path(input("Path to text file: ").strip()).expanduser()
    if not source.is_file():
        print("Input file not found."); return
    text = source.read_text(encoding="utf-8", errors="ignore")
    emails = sorted(set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)))
    output = source.with_name("extracted_emails.txt")
    output.write_text("\n".join(emails), encoding="utf-8")
    print(f"Found {len(emails)} unique email address(es). Saved to {output}")


def save_webpage_title():
    url = input("Public webpage URL: ").strip()
    if not url.startswith(("http://", "https://")):
        print("Enter a valid http or https URL."); return
    try:
        response = requests.get(url, headers={"User-Agent": "CodeAlphaLearningScript/1.0"}, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.get_text(" ", strip=True) if soup.title else "(No title found)"
        Path("webpage_title.txt").write_text(f"URL: {url}\nTitle: {title}\n", encoding="utf-8")
        print(f"Saved title: {title}")
    except requests.RequestException as exc:
        print(f"Could not fetch webpage: {exc}")


def main():
    actions = {"1": move_jpg_files, "2": extract_emails, "3": save_webpage_title}
    while True:
        print("\nPYTHON TASK AUTOMATION")
        print("1. Move JPG/JPEG files")
        print("2. Extract email addresses from a text file")
        print("3. Save a public webpage title")
        print("0. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "0": break
        action = actions.get(choice)
        if action: action()
        else: print("Choose 0, 1, 2 or 3.")


if __name__ == "__main__":
    main()
