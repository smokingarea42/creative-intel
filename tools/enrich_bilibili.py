# -*- coding: utf-8 -*-
import json, re, os, sys, time, urllib2
reload(sys)
sys.setdefaultencoding("utf-8")

DATA_DIR = r"C:\Users\xuyiqing03\Documents\Codex\2026-06-11\https-smokingarea42-github-io-creative-intel\repo\data"

def bilibili_api(bvid):
    url = "https://api.bilibili.com/x/web-interface/view?bvid={}".format(bvid)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.bilibili.com/"
    }
    req = urllib2.Request(url, headers=headers)
    try:
        resp = urllib2.urlopen(req, timeout=10)
        data = json.loads(resp.read().decode("utf-8"))
        if data.get("code") == 0:
            d = data["data"]
            return {
                "title": d.get("title", ""),
                "desc": d.get("desc", ""),
                "pic": d.get("pic", ""),
                "owner": d.get("owner", {}).get("name", ""),
                "duration": d.get("duration", 0),
                "view": d.get("stat", {}).get("view", 0)
            }
    except Exception as e:
        print("  API error for {}: {}".format(bvid, str(e)[:80]))
    return None

def enrich_file(fname):
    path = os.path.join(DATA_DIR, fname)
    with open(path, "rb") as f:
        data = json.loads(f.read().decode("utf-8"))
    
    modified = False
    enriched = 0
    
    if fname == "skins.json":
        for day in data:
            for e in day.get("entries", []):
                url = e.get("sourceUrl", "")
                if "bilibili.com/video/" in url:
                    m = re.search(r'(BV[a-zA-Z0-9]+|av\d+)', url)
                    if not m:
                        continue
                    bvid = m.group(1)
                    
                    if e.get("_bilibili_enriched"):
                        continue
                    
                    skin_name = e.get("skinName", "")[:60]
                    print("  Enriching: {} - {}".format(bvid, skin_name.encode("utf-8") if isinstance(skin_name, unicode) else skin_name))
                    info = bilibili_api(bvid)
                    if info and info["pic"]:
                        if not e.get("imageUrl") or e["imageUrl"].startswith("http://"):
                            e["imageUrl"] = info["pic"].replace("http://", "https://")
                            modified = True
                        e["_bilibili_enriched"] = True
                        if info.get("owner"):
                            e["_bilibili_author"] = info["owner"]
                        enriched += 1
                        time.sleep(0.3)
                    elif info and not info["pic"]:
                        print("    No cover image returned")
    
    elif fname in ("activities.json", "reports.json"):
        for e in data:
            url = e.get("sourceUrl", "")
            if "bilibili.com/video/" in url:
                m = re.search(r'(BV[a-zA-Z0-9]+|av\d+)', url)
                if not m:
                    continue
                bvid = m.group(1)
                
                if e.get("_bilibili_enriched"):
                    continue
                
                title = e.get("title", e.get("activityName", ""))[:60]
                print("  Enriching: {} - {}".format(bvid, title.encode("utf-8") if isinstance(title, unicode) else title))
                info = bilibili_api(bvid)
                if info and info["pic"]:
                    if not e.get("imageUrl") or e["imageUrl"].startswith("http://"):
                        e["imageUrl"] = info["pic"].replace("http://", "https://")
                        modified = True
                    e["_bilibili_enriched"] = True
                    if info.get("owner"):
                        e["_bilibili_author"] = info["owner"]
                    enriched += 1
                    time.sleep(0.3)
    
    if modified:
        with open(path, "wb") as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"))
        print("  Saved: {} entries enriched".format(enriched))
    else:
        print("  No changes needed")
    return enriched

if __name__ == "__main__":
    total = 0
    for fname in ["skins.json", "activities.json", "reports.json"]:
        print("\n=== {} ===".format(fname))
        total += enrich_file(fname)
    print("\nTotal entries enriched: {}".format(total))
