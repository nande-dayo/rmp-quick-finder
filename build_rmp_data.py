import json
from pathlib import Path
import re
import shutil
from bs4 import BeautifulSoup

# ダウンロードフォルダのパス（Windows / Mac 両対応）
DOWNLOAD_DIR = Path.home() / "Downloads"
TARGET_FILE_NAME = "rmp_rendered.html"

source_path = DOWNLOAD_DIR / TARGET_FILE_NAME
local_path = Path(TARGET_FILE_NAME)

# 1. ダウンロードフォルダに最新ファイルがあれば、作業フォルダへ自動移動/上書き
if source_path.exists():
    print(f"ダウンロードフォルダから {TARGET_FILE_NAME} を移動中...")
    shutil.move(str(source_path), str(local_path))
    print("移動完了！")

# 2. ファイルの存在チェック
if not local_path.exists():
    print(
        f"エラー: {TARGET_FILE_NAME} が見つかりません。ブックマークレットで保存してください。"
    )
    exit(1)

print(f"{local_path} を解析中...")

with open(local_path, "r", encoding="utf-8", errors="ignore") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

drugs = []
seen_names = set()

for tr in soup.find_all("tr"):
    tds = tr.find_all("td")
    if len(tds) < 6:
        continue

    drug_name = tds[0].get_text(strip=True)
    if not drug_name or drug_name in seen_names:
        continue

    company = tds[1].get_text(strip=True)
    generic_name = tds[2].get_text(strip=True)

    detail_link = tds[5].find("a")
    if detail_link and "href" in detail_link.attrs:
        href = detail_link["href"]
        match = re.search(r"GeneralList/(\d+)", href)
        yj7 = match.group(1) if match else ""
        detail_url = href if href.startswith("http") else f"https://www.pmda.go.jp{href}"
    else:
        yj7 = ""
        detail_url = ""

    drugs.append(
        {
            "name": drug_name,
            "generic": generic_name,
            "company": company,
            "yj7": yj7,
            "detailUrl": detail_url,
        }
    )
    seen_names.add(drug_name)

print(f"抽出完了: {len(drugs)} 件のデータを取得しました。")

with open("rmp_data.json", "w", encoding="utf-8") as f:
    json.dump(drugs, f, ensure_ascii=False, indent=2)

print("rmp_data.json を作成しました。")