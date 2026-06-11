#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Daily Creative Intel Report Generator
Generates a new daily skin report and pushes to GitHub.

Usage:
  python daily_report.py              # Generate for today
  python daily_report.py --dry-run    # Preview without saving
  python daily_report.py --force      # Force regenerate even if today exists
"""
import json, os, sys, time, urllib2, urllib, re, subprocess, io
from datetime import datetime

reload(sys)
sys.setdefaultencoding("utf-8")

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_DIR, "data")
LOG_FILE = os.path.join(REPO_DIR, "tools", "daily_report.log")

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = u"[{}] {}".format(timestamp, msg)
    print(line.encode("utf-8") if isinstance(line, unicode) else line)
    try:
        with io.open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + u"\n")
    except:
        pass

def clean_html(text):
    """Remove HTML tags from text."""
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()

SEARCH_QUERIES = [
    (u"Valorant", u"Valorant 新皮肤"),
    (u"CS2", u"CS2 新皮肤"),
    (u"Apex Legends", u"Apex 新皮肤"),
    (u"Marvel Rivals", u"漫威争锋 新皮肤"),
    (u"CODM", u"使命召唤手游 新皮肤"),
    (u"Fortnite", u"Fortnite 新皮肤"),
    (u"PUBG", u"PUBG 新皮肤"),
    (u"Overwatch 2", u"守望先锋2 新皮肤"),
    (u"Rainbow Six Siege", u"彩虹六号围攻 新皮肤"),
    (u"The Finals", u"THE FINALS 新皮肤"),
    (u"Delta Force", u"三角洲行动 新皮肤"),
    (u"Naraka", u"永劫无间 新皮肤"),
]

def bilibili_search(keyword, limit=2):
    encoded = urllib.quote(keyword.encode("utf-8"))
    url = "https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword={}&order=pubdate&page=1".format(encoded)
    headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.bilibili.com/"}
    req = urllib2.Request(url, headers=headers)
    try:
        resp = urllib2.urlopen(req, timeout=10)
        data = json.loads(resp.read().decode("utf-8"))
        if data.get("code") == 0:
            results = data.get("data", {}).get("result", [])
            entries = []
            for v in results[:limit]:
                pic = v.get("pic", "")
                if pic.startswith("//"):
                    pic = "https:" + pic
                entries.append({
                    "bvid": v.get("bvid", ""),
                    "title": clean_html(v.get("title", "")),
                    "description": clean_html(v.get("description", "")),
                    "pic": pic,
                    "author": v.get("author", ""),
                    "url": "https://www.bilibili.com/video/" + v.get("bvid", ""),
                })
            return entries
    except Exception as e:
        log(u"  Search error for '{}': {}".format(keyword, str(e)[:100]))
    return []

def generate_entry(game, keyword, result):
    skin = result["title"]
    if len(skin) > 60:
        skin = skin[:57] + "..."
    desc = result.get("description", "")
    if desc and len(desc) > 120:
        desc = desc[:117] + "..."
    
    search_url = "https://search.bilibili.com/all?keyword={}&order=pubdate".format(
        urllib.quote(keyword.encode("utf-8"))
    )
    
    return {
        "game": game,
        "skinName": skin,
        "type": u"B站最新",
        "releaseDate": datetime.now().strftime("%Y.%m.%d"),
        "brief": desc if desc else u"B站最新游戏皮肤相关视频",
        "sourceUrl": result["url"],
        "biliSearch": search_url,
        "imageUrl": result.get("pic", ""),
    }

def main():
    dry_run = "--dry-run" in sys.argv
    force = "--force" in sys.argv
    
    today = datetime.now().strftime("%Y-%m-%d")
    log(u"=" * 50)
    log(u"Daily Report Generator - {}".format(today))
    
    # Load existing data
    skins_path = os.path.join(DATA_DIR, "skins.json")
    with io.open(skins_path, "r", encoding="utf-8") as f:
        skins_data = json.loads(f.read())
    
    if today in [d["date"] for d in skins_data] and not force:
        log(u"SKIP: {} already has entries (use --force to override)".format(today))
        return
    
    if force and today in [d["date"] for d in skins_data]:
        log(u"FORCE: removing existing entries for {}".format(today))
        skins_data = [d for d in skins_data if d["date"] != today]
    
    # Search Bilibili
    log(u"Searching Bilibili...")
    new_entries = []
    seen = set()
    
    for game, keyword in SEARCH_QUERIES:
        results = bilibili_search(keyword, limit=2)
        log(u"  {}: {} results".format(game, len(results)))
        for r in results:
            entry = generate_entry(game, keyword, r)
            key = (entry["game"], entry["skinName"])
            if key not in seen:
                seen.add(key)
                new_entries.append(entry)
        time.sleep(0.3)
    
    if not new_entries:
        log(u"WARN: No content found, creating placeholder")
        new_entries.append({
            "game": u"待更新",
            "skinName": u"今日暂无新皮肤内容",
            "type": u"自动日报",
            "releaseDate": today,
            "brief": u"请在B站搜索最新游戏皮肤资讯后手动更新",
            "sourceUrl": "https://www.bilibili.com/",
            "biliSearch": "https://search.bilibili.com/all?keyword=%E6%B8%B8%E6%88%8F+%E6%96%B0%E7%9A%AE%E8%82%A4&order=pubdate",
            "imageUrl": "",
        })
    
    log(u"Generated {} unique entries".format(len(new_entries)))
    
    if dry_run:
        log(u"*** DRY RUN - would add: ***")
        for e in new_entries:
            log(u"  [{}] {}".format(e["game"], e["skinName"][:60]))
        return
    
    # Update skins.json
    new_day = {"date": today, "entries": new_entries}
    skins_data.insert(0, new_day)
    
    with io.open(skins_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(skins_data, ensure_ascii=False, indent=2))
    log(u"Updated skins.json")
    
    # Git commit and push
    log(u"Committing and pushing...")
    os.chdir(REPO_DIR)
    safe = REPO_DIR.replace("\\", "/")
    git = ["git", "-c", "safe.directory=" + safe]
    
    try:
        subprocess.check_call(git + ["add", "data/skins.json"])
        subprocess.check_call(git + ["commit", "-m", "daily: auto report for {}".format(today)])
        subprocess.check_call(git + ["push", "origin", "main"])
        log(u"DONE: Report generated and pushed!")
    except Exception as e:
        log(u"ERROR: Git failed - {}".format(str(e)[:100]))
        log(u"File updated locally. Manual push needed.")

if __name__ == "__main__":
    main()
