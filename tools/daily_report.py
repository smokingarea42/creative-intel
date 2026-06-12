#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Daily Creative Intel Report Generator
Auto-generates skin reports, intelligence reports, and activity analysis.
Scheduled via Windows Task Scheduler: weekdays 10:30 AM.
"""
import json, os, sys, time, urllib2, urllib, re, subprocess, io, hashlib
from datetime import datetime

reload(sys)
sys.setdefaultencoding("utf-8")

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_DIR, "data")
LOG_FILE = os.path.join(REPO_DIR, "tools", "daily_report.log")
MAX_PER_SECTION = 3

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

def short_id(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()[:8]

def notify_done(today, skins_n, reports_n, activities_n):
    try:
        msg = u"{} 日报已生成! 皮肤{}条 情报{}条 活动{}条".format(
            today, skins_n, reports_n, activities_n
        )
        ps = (
            u'Add-Type -AssemblyName System.Windows.Forms; '
            u'$b = New-Object System.Windows.Forms.NotifyIcon; '
            u'$b.Icon = [System.Drawing.SystemIcons]::Information; '
            u'$b.BalloonTipIcon = "Info"; '
            u'$b.BalloonTipTitle = "Creative Intel 日报已生成"; '
            u'$b.BalloonTipText = "{}"; '
            u'$b.Visible = $true; '
            u'$b.ShowBalloonTip(10000); '
            u'Start-Sleep -Seconds 12; '
            u'$b.Dispose()'
        ).format(msg)
        subprocess.call(["powershell", "-Command", ps.encode("utf-8")], shell=True)
    except:
        pass

# === Search queries for each section ===
SKIN_QUERIES = [
    (u"Valorant", u"Valorant 新皮肤 评测"),
    (u"Apex Legends", u"Apex 新皮肤 活动"),
    (u"Marvel Rivals", u"漫威争锋 新皮肤"),
    (u"CODM", u"使命召唤手游 新皮肤 神话"),
    (u"Fortnite", u"Fortnite 新皮肤"),
    (u"PUBG", u"PUBG 新皮肤"),
    (u"Overwatch 2", u"守望先锋2 新皮肤"),
    (u"CS2", u"CS2 新皮肤 武器箱"),
    (u"The Finals", u"THE FINALS 新皮肤"),
    (u"Delta Force", u"三角洲行动 新皮肤"),
    (u"Naraka", u"永劫无间 新皮肤"),
    (u"Rainbow Six Siege", u"彩虹六号 新皮肤"),
]

REPORT_QUERIES = [
    (u"FPS", u"FPS游戏 商业化 拆解 分析"),
    (u"MOBA", u"MOBA游戏 皮肤 商业化分析"),
    (u"射击游戏", u"射击游戏 皮肤设计 商业化"),
    (u"游戏运营", u"游戏运营 商业化 案例分析"),
    (u"手游", u"手游 商业化 活动设计 拆解"),
    (u"游戏皮肤", u"游戏皮肤 设计分析 商业化"),
    (u"赛季通行证", u"赛季通行证 BattlePass 分析"),
    (u"抽奖活动", u"游戏抽奖 活动机制 分析"),
]

ACTIVITY_QUERIES = [
    (u"游戏活动", u"游戏活动 运营 机制拆解"),
    (u"手游活动", u"手游 活动设计 案例分析"),
    (u"FPS活动", u"FPS游戏 活动 运营分析"),
    (u"限时活动", u"游戏限时活动 设计 拆解"),
    (u"充值活动", u"游戏充值活动 商业化 分析"),
    (u"联动活动", u"游戏IP联动 活动设计"),
    (u"签到活动", u"游戏签到 日常活动 机制"),
    (u"战令", u"游戏战令 通行证 设计分析"),
]

def bilibili_search(keyword, limit=3):
    encoded = urllib.quote(keyword.encode("utf-8"))
    url = ("https://api.bilibili.com/x/web-interface/search/type"
           "?search_type=video&keyword={}&order=pubdate&page=1").format(encoded)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
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
                        "play": v.get("play", 0),
                        "url": "https://www.bilibili.com/video/" + v.get("bvid", ""),
                    })
                return entries
            return []
        except urllib2.HTTPError as e:
            if e.code == 412 and attempt < 2:
                time.sleep(2)
                continue
            return []
        except:
            if attempt < 2:
                time.sleep(2)
                continue
            return []
    return []

def generate_skin_entry(game, keyword, result):
    skin = result["title"]
    if len(skin) > 60:
        skin = skin[:57] + "..."
    desc = result.get("description", "")
    if desc and len(desc) > 120:
        desc = desc[:117] + "..."
    kw_enc = urllib.quote(keyword.encode("utf-8"))
    return {
        "game": game,
        "skinName": skin,
        "type": u"B站最新",
        "releaseDate": datetime.now().strftime("%Y.%m.%d"),
        "brief": desc if desc else u"最新游戏皮肤资讯",
        "sourceUrl": result["url"],
        "biliSearch": "https://search.bilibili.com/all?keyword={}&order=pubdate".format(kw_enc),
        "imageUrl": result.get("pic", ""),
    }

def generate_report_entry(game, keyword, result, today):
    title = result["title"]
    if len(title) > 80:
        title = title[:77] + "..."
    desc = result.get("description", "")
    if desc and len(desc) > 200:
        desc = desc[:197] + "..."
    uid = short_id(result["bvid"] + today)
    return {
        "id": uid,
        "date": today,
        "game": game,
        "title": title,
        "category": u"商业化分析",
        "highlights": desc if desc else u"游戏商业化/皮肤设计深度分析",
        "designAnalysis": u"来源: B站UP主 {} | 播放: {}".format(
            result.get("author", "未知"), result.get("play", 0)
        ),
        "bsInsight": u"自动聚合B站最新商业化分析内容",
        "sourceUrl": result["url"],
        "imageUrl": result.get("pic", ""),
    }

def generate_activity_entry(game, keyword, result, today):
    title = result["title"]
    if len(title) > 80:
        title = title[:77] + "..."
    desc = result.get("description", "")
    if desc and len(desc) > 200:
        desc = desc[:197] + "..."
    uid = short_id(result["bvid"] + today + "act")
    return {
        "id": uid,
        "date": today,
        "game": game,
        "activityName": title,
        "activityType": u"运营活动分析",
        "title": title,
        "highlights": desc if desc else u"游戏活动机制深度拆解",
        "designAnalysis": u"来源: B站UP主 {} | 播放: {}".format(
            result.get("author", "未知"), result.get("play", 0)
        ),
        "sourceUrl": result["url"],
        "biliSearch": "https://search.bilibili.com/all?keyword={}&order=pubdate".format(
            urllib.quote(keyword.encode("utf-8"))
        ),
        "imageUrl": result.get("pic", ""),
    }

def search_and_collect(queries, entry_generator, today, max_entries=MAX_PER_SECTION):
    """Search across queries and collect unique entries."""
    entries = []
    seen = set()
    
    for game, keyword in queries:
        if len(entries) >= max_entries:
            break
        results = bilibili_search(keyword, limit=1)
        for r in results:
            key = r["bvid"]
            if key not in seen:
                seen.add(key)
                entry = entry_generator(game, keyword, r, today) if today else entry_generator(game, keyword, r)
                entries.append(entry)
        time.sleep(0.5)
    
    return entries[:max_entries]

def load_json(fname):
    path = os.path.join(DATA_DIR, fname)
    with io.open(path, "r", encoding="utf-8") as f:
        return json.loads(f.read())

def save_json(fname, data):
    path = os.path.join(DATA_DIR, fname)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=2))

def main():
    dry_run = "--dry-run" in sys.argv
    force = "--force" in sys.argv
    today = datetime.now().strftime("%Y-%m-%d")
    
    log(u"=" * 50)
    log(u"Daily Report Generator - {}".format(today))
    
    # Load all data files
    skins_data = load_json("skins.json")
    reports_data = load_json("reports.json")
    activities_data = load_json("activities.json")
    
    existing_dates = {
        "skins": [d["date"] for d in skins_data],
        "reports": [d["date"] for d in reports_data],
        "activities": [d["date"] for d in activities_data],
    }
    
    skins_n = reports_n = activities_n = 0
    
    # === SKINS ===
    if today in existing_dates["skins"] and not force:
        log(u"[SKINS] {} already exists, skipping".format(today))
        # Count existing entries for today
        for d in skins_data:
            if d["date"] == today:
                skins_n = len(d["entries"])
    else:
        if force:
            skins_data = [d for d in skins_data if d["date"] != today]
        log(u"[SKINS] Searching {} queries...".format(len(SKIN_QUERIES)))
        new_skins = search_and_collect(
            SKIN_QUERIES,
            lambda g, k, r, t: generate_skin_entry(g, k, r),
            today,
            MAX_PER_SECTION
        )
        if new_skins and not dry_run:
            skins_data.insert(0, {"date": today, "entries": new_skins})
            save_json("skins.json", skins_data)
            skins_n = len(new_skins)
            log(u"[SKINS] Generated {} entries".format(skins_n))
        else:
            log(u"[SKINS] No results found")
    
    # === REPORTS ===
    if today in existing_dates["reports"] and not force:
        log(u"[REPORTS] {} already exists, skipping".format(today))
        reports_n = sum(1 for d in reports_data if d["date"] == today)
    else:
        if force:
            reports_data = [d for d in reports_data if d["date"] != today]
        log(u"[REPORTS] Searching analysis content...")
        new_reports = search_and_collect(
            REPORT_QUERIES,
            lambda g, k, r, t: generate_report_entry(g, k, r, t),
            today,
            MAX_PER_SECTION
        )
        if new_reports and not dry_run:
            reports_data = new_reports + reports_data
            reports_data.sort(key=lambda x: x["date"], reverse=True)
            save_json("reports.json", reports_data)
            reports_n = len(new_reports)
            log(u"[REPORTS] Generated {} entries".format(reports_n))
        else:
            log(u"[REPORTS] No results found")
    
    # === ACTIVITIES ===
    if today in existing_dates["activities"] and not force:
        log(u"[ACTIVITIES] {} already exists, skipping".format(today))
        activities_n = sum(1 for d in activities_data if d["date"] == today)
    else:
        if force:
            activities_data = [d for d in activities_data if d["date"] != today]
        log(u"[ACTIVITIES] Searching event analysis...")
        new_activities = search_and_collect(
            ACTIVITY_QUERIES,
            lambda g, k, r, t: generate_activity_entry(g, k, r, t),
            today,
            MAX_PER_SECTION
        )
        if new_activities and not dry_run:
            activities_data = new_activities + activities_data
            activities_data.sort(key=lambda x: x["date"], reverse=True)
            save_json("activities.json", activities_data)
            activities_n = len(new_activities)
            log(u"[ACTIVITIES] Generated {} entries".format(activities_n))
        else:
            log(u"[ACTIVITIES] No results found")
    
    if dry_run:
        log(u"*** DRY RUN - no changes saved ***")
        return
    
    # Check if anything was generated
    if skins_n == 0 and reports_n == 0 and activities_n == 0:
        log(u"Nothing new to commit")
        return
    
    # Git commit and push
    log(u"Committing and pushing (S:{} R:{} A:{})...".format(skins_n, reports_n, activities_n))
    os.chdir(REPO_DIR)
    safe = REPO_DIR.replace("\\", "/")
    git = ["git", "-c", "safe.directory=" + safe]
    
    try:
        subprocess.check_call(git + ["add", "data/skins.json", "data/reports.json", "data/activities.json"])
        subprocess.check_call(git + ["commit", "-m",
            "daily: {} | skins:{} reports:{} activities:{}".format(today, skins_n, reports_n, activities_n)])
        subprocess.check_call(git + ["push", "origin", "main"])
        log(u"DONE: Pushed successfully!")
        notify_done(today, skins_n, reports_n, activities_n)
    except Exception as e:
        log(u"ERROR: Git failed - {}".format(str(e)[:100]))

if __name__ == "__main__":
    main()
