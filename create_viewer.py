import json

# 先ほど作成したJSONを読み込み
with open("rmp_data.json", "r", encoding="utf-8") as f:
    drugs_data = json.load(f)

json_str = json.dumps(drugs_data, ensure_ascii=False)

html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>RMP資材クイックファインダー</title>
  <style>
    * {{ box-sizing: border-box; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      max-width: 760px;
      margin: 40px auto;
      padding: 0 20px;
      color: #333;
      background-color: #f7f9fa;
    }}
    .header {{
      text-align: center;
      margin-bottom: 24px;
    }}
    h1 {{
      font-size: 22px;
      color: #1a535c;
      margin-bottom: 6px;
    }}
    .sub {{
      font-size: 13px;
      color: #666;
    }}
    .search-box {{
      position: sticky;
      top: 15px;
      z-index: 10;
      background: #f7f9fa;
      padding-bottom: 12px;
    }}
    input {{
      width: 100%;
      font-size: 18px;
      padding: 14px 16px;
      border: 2px solid #1a535c;
      border-radius: 8px;
      outline: none;
      box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }}
    input:focus {{
      box-shadow: 0 0 0 3px rgba(26,83,92,0.2);
    }}
    .count {{
      font-size: 13px;
      color: #777;
      margin-top: 8px;
      text-align: right;
    }}
    .list {{
      list-style: none;
      padding: 0;
      margin: 10px 0 0 0;
    }}
    .item {{
      background: #fff;
      padding: 16px;
      border-radius: 8px;
      margin-bottom: 12px;
      border: 1px solid #e1e8ed;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }}
    .info {{
      max-width: 68%;
    }}
    .name {{
      font-size: 17px;
      font-weight: bold;
      color: #222;
      margin-bottom: 4px;
    }}
    .meta {{
      font-size: 12px;
      color: #666;
      line-height: 1.4;
    }}
    .actions {{
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}
    .btn {{
      display: inline-block;
      text-align: center;
      background-color: #ff6b6b;
      color: #fff;
      text-decoration: none;
      padding: 9px 16px;
      font-size: 14px;
      font-weight: bold;
      border-radius: 6px;
      transition: background-color 0.15s ease;
      white-space: nowrap;
    }}
    .btn:hover {{
      background-color: #ee5253;
    }}
    .no-data {{
      text-align: center;
      color: #999;
      padding: 40px 0;
      font-size: 15px;
    }}
    .footer {{
      margin-top: 40px;
      padding: 24px 12px 30px;
      border-top: 1px solid #e1e8ed;
      font-size: 11px;
      color: #777;
      line-height: 1.6;
      text-align: center;
    }}
    .footer a {{
      color: #1a535c;
      text-decoration: underline;
    }}
  </style>
</head>
<body>

  <div class="header">
    <h1>💊 RMP資材クイックファインダー</h1>
    <div class="sub">調剤室用 / PMDA詳細ページ直結ツール（全 {len(drugs_data)} 品目収録）</div>
  </div>

  <div class="search-box">
    <input type="text" id="q" placeholder="商品名または一般名を入力（例：アイクルシグ、フォシーガ、ダパグリフロジン）" autofocus>
    <div class="count" id="count"></div>
  </div>

  <ul class="list" id="list"></ul>
  <div class="no-data" id="empty" style="display:none;">該当するRMP対象品目が見つかりません。</div>

  <footer class="footer">
    <p>
      出典：独立行政法人医薬品医療機器総合機構（PMDA）「<a href="https://www.pmda.go.jp/safety/info-services/drugs/items-information/rmp/0001.html" target="_blank" rel="noopener noreferrer">RMP提出品目一覧</a>」をもとに加工・作成<br>
      ※本ツールは個人による非公式の業務支援ツールであり、独立行政法人医薬品医療機器総合機構（PMDA）が提供・推奨するものではありません。<br>
      ※医薬品の最新情報や適正使用に関する最新資材は、リンク先のPMDA公式サイトにて必ず一次情報をご確認ください。
    </p>
  </footer>

  <script>
    const data = {json_str};
    const input = document.getElementById('q');
    const list = document.getElementById('list');
    const empty = document.getElementById('empty');
    const count = document.getElementById('count');

    function render(items) {{
      list.innerHTML = '';
      if (items.length === 0) {{
        empty.style.display = 'block';
        count.textContent = '';
        return;
      }}
      empty.style.display = 'none';
      count.textContent = `表示件数: ${{items.length}} 件`;

      items.slice(0, 50).forEach(item => {{
        const li = document.createElement('li');
        li.className = 'item';
        li.innerHTML = `
          <div class="info">
            <div class="name">${{item.name}}</div>
            <div class="meta">
              <strong>一般名:</strong> ${{item.generic}}<br>
              <strong>会社名:</strong> ${{item.company}} / <strong>YJ7桁:</strong> ${{item.yj7 || '-'}}
            </div>
          </div>
          <div class="actions">
            <a href="${{item.detailUrl}}" target="_blank" rel="noopener noreferrer" class="btn">
              📄 PMDA資材ページを開く
            </a>
          </div>
        `;
        list.appendChild(li);
      }});
    }}

    input.addEventListener('input', (e) => {{
      const val = e.target.value.trim().toLowerCase();
      if (!val) {{
        list.innerHTML = '';
        empty.style.display = 'none';
        count.textContent = '';
        return;
      }}
      const res = data.filter(d => 
        (d.name && d.name.toLowerCase().includes(val)) ||
        (d.generic && d.generic.toLowerCase().includes(val))
      );
      render(res);
    }});
  </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("index.html を生成しました。ダブルクリックしてブラウザで開いてみてください！")