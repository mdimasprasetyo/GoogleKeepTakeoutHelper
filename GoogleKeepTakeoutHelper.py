import os
import json
import glob
from bs4 import BeautifulSoup
import html2text
from datetime import datetime
from config import INPUT_DIR

# ✅ OUTPUT FOLDER
OUTPUT_DIR = os.path.join(INPUT_DIR, "output_md")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def micros_to_datetime(micros):
    if not micros:
        return None
    return datetime.fromtimestamp(micros / 1_000_000).isoformat()

def load_json_metadata(json_path):
    if not os.path.exists(json_path):
        return {}

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return {
        "created": micros_to_datetime(data.get("createdTimestampUsec")),
        "updated": micros_to_datetime(data.get("userEditedTimestampUsec")),
        "archived": data.get("isArchived"),
        "pinned": data.get("isPinned"),
        "labels": [label["name"] for label in data.get("labels", [])],
        "color": data.get("color")
    }

def html_to_markdown(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    title = soup.title.text.strip() if soup.title else "Untitled"

    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.body_width = 0

    content_md = h.handle(str(soup.body)) if soup.body else ""
    return title, content_md.strip()

def write_markdown(note_name, title, metadata, content):
    safe_name = note_name.replace("/", "_")
    output_path = os.path.join(OUTPUT_DIR, f"{safe_name}.md")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(f"title: \"{title}\"\n")

        for key, value in metadata.items():
            if value is None:
                continue
            if isinstance(value, list):
                f.write(f"{key}:\n")
                for item in value:
                    f.write(f"  - {item}\n")
            else:
                f.write(f"{key}: {value}\n")

        f.write("---\n\n")
        f.write(content)

def main():
    html_files = glob.glob(os.path.join(INPUT_DIR, "*.html"))

    if not html_files:
        print("❌ No HTML files found. Check your path.")
        return

    for html_path in html_files:
        base_name = os.path.splitext(os.path.basename(html_path))[0]
        json_path = os.path.join(INPUT_DIR, base_name + ".json")

        print(f"Processing: {base_name}")

        title, content_md = html_to_markdown(html_path)
        metadata = load_json_metadata(json_path)

        write_markdown(base_name, title, metadata, content_md)

    print("\n✅ Done!")
    print("📁 Markdown files saved in:")
    print(OUTPUT_DIR)

if __name__ == "__main__":
    main()