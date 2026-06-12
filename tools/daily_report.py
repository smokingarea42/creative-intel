#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Daily Creative Intel Report Generator
Auto-generates skin report from Bilibili search and pushes to GitHub.
Scheduled via Windows Task Scheduler: weekdays 10:30 AM.
"""
import json, os, sys, time, urllib2, urllib, re, subprocess, io
from datetime import datetime

reload(sys)
sys.setdefaultencoding("utf-8")

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_DIR, "data")
LOG_FILE = os.path.join(REPO_DIR, "tools", "daily_report.log")

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = u"[{}] {}".format(ts, msg)
    print(line.encode("utf-8") if isinstance(line, unicode) else line)
    try:
        with io.open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + u"\n")
    except:
        pass

def clean_html(text):
    if not text:
        return ""
    return re.sub(r"<[^>]+>", "", text).strip()

def notify_done(today, count):
    """Show Windows toast notification."""
    try:
        ps_script = (
            u'Add-Type -AssemblyName System.Windows.Forms; '
            u'$b = New-Object System.Windows.Forms.NotifyIcon; '
            u'$b.Icon = [System.Drawing.SystemIcons]::Information; '
            u'$b.BalloonTipIcon = "Info"; '
            u'$b.BalloonTipTitle = "Creative Intel 日报已生成"; '
            u'$b.BalloonTipText = "{} 日报已生成并推送! 共 {} 条新皮肤"; '
            u'$b.Visible = $true; '
            u'$b.ShowBalloonTip(10000); '
            u'Start-Sleep -Seconds 12; '
            u'$b.Dispose()'
        ).format(today, count)
        subprocess.call(
            ["powershell", "-Command", ps_script.encode("utf-8")],
            shell=True
        )
    except Exception as e:
        log(u"Notification failed: {}".format(str(e)[:80]))

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
    """Search Bilibili with retry for 412 errors."""
    encoded = urllib.quote(keyword.encode("utf-8"))
    url = ("https://api.bilibili.com/x/web-interface/search/type"
           "?search_type=video&keyword={}&order=pubdate&page=1").format(encoded)
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Referer": "https://www.bilibili.com/",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    
    for attempt in range(3):
        try:
            req = urllib2.Request(url, headers=headers)
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
            else:
                log(u"  API error for {}: code={}".format(keyword, data.get("code")))
                return []
        except urllib2.HTTPError as e:
            if e.code == 412 and attempt < 2:
                time.sleep(2)
                continue
            log(u"  HTTP {} for {}: {}".format(e.code, keyword, str(e)[:60]))
            return []
        except Exception as e:
            if attempt < 2:
                time.sleep(2)
                continue
            log(u"  Error for {}: {}".format(keyword, str(e)[:80]))
            return []
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
    
    skins_path = os.path.join(DATA_DIR, "skins.json")
    with io.open(skins_path, "r", encoding="utf-8") as f:
        skins_data = json.loads(f.read())
    
    if today in [d["date"] for d in skins_data] and not force:
        log(u"SKIP: {} already exists (use --force to override)".format(today))
        return
    
    if force:
        skins_data = [d for d in skins_data if d["date"] != today]
    
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
        time.sleep(0.5)
    
    if not new_entries:
        log(u"WARN: No content found, creating placeholder")
        new_entries.append({
            "game": u"待更新",
            "skinName": u"今日暂无新皮肤内容",
            "type": u"自动日报",
            "releaseDate": today,
            "brief": u"请在B站搜索最新游戏皮肤资讯后手动更新",
            "sourceUrl": "https://www.bilibili.com/",
            "biliSearch": "https://search.bilibili.com/all?keyword=游戏+新皮肤&order=pubdate",
            "imageUrl": "",
        })
    
    log(u"Generated {} unique entries".format(len(new_entries)))
    
    if dry_run:
        log(u"*** DRY RUN ***")
        for e in new_entries:
            log(u"  [{}] {}".format(e["game"], e["skinName"][:60]))
        return
    
    new_day = {"date": today, "entries": new_entries}
    skins_data.insert(0, new_day)
    
    with io.open(skins_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(skins_data, ensure_ascii=False, indent=2))
    log(u"Updated skins.json")
    
    log(u"Committing and pushing...")
    os.chdir(REPO_DIR)
    safe = REPO_DIR.replace("\\", "/")
    git = ["git", "-c", "safe.directory=" + safe]
    
    try:
        subprocess.check_call(git + ["add", "data/skins.json"])
        subprocess.check_call(git + ["commit", "-m", "daily: auto report for {}".format(today)])
        subprocess.check_call(git + ["push", "origin", "main"])
        log(u"DONE: Report generated and pushed!")
        notify_done(today, len(new_entries))
    except Exception as e:
        log(u"ERROR: Git failed - {}".format(str(e)[:100]))
        log(u"File updated locally, manual push needed.")

if __name__ == "__main__":
    main()
