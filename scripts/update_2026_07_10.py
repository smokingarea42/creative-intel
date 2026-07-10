#!/usr/bin/env python3
"""Daily update script for 2026-07-10"""
import json
import os

DATA_DIR = r"C:\Users\xuyiqing03\Documents\creative-intel\data"

# === 1. REPORTS ===
new_reports = [
    {
        "id": "2026-07-10-01",
        "date": "2026-07-10",
        "game": "和平精英 (Tencent)",
        "title": "【今日D-Day】和平精英新神装【幻音九尾·璃】7.10零点上线：九尾狐主题+娜扎Cos大使+璀璨转盘变现",
        "highlights": "- 7月10日0点正式上线，射击BR品类7周年活动矩阵最高端付费出口（射击BR品类）\n- 九尾狐主题神装含全套特效+专属动作+语音，配套璀璨转盘同步开启\n- 演员娜扎出任Cos大使，7.6悬念海报→7.8 CG动画→7.10上线，3天预热节奏\n- 继帕修斯/龙鳞之后的第N款神装，单价天花板级定价",
        "designAnalysis": "- 明星Cos大使=借用明星流量做游戏内容破圈，非代言但效果接近\n- 悬念海报→CG→上线的3天节奏：信息释放节奏快，保持讨论热度不断层\n- 璀璨转盘=独立付费通道，与常规军需分离避免蚕食\n- 九尾狐主题在国风审美中认知度极高，降低玩家理解成本",
        "bsInsight": "核心学习：①明星Cos大使比传统代言轻量但传播效果接近，成本可控；②神装级产品的预热应该是递进式信息释放（悬念→细节→上线），而非一次性曝光；③独立转盘通道避免与日常商城互相干扰。",
        "sourceUrl": "https://news.qq.com/rain/a/20260709A053SN00",
        "imageUrl": ""
    },
    {
        "id": "2026-07-10-02",
        "date": "2026-07-10",
        "game": "Square Enix (FF7 Ever Crisis)",
        "title": "【FF7 Ever Crisis 10月关服】$1亿/3年的GaaS产品被放弃——SE对手游ROI标准的残酷裁决",
        "highlights": "- 7月8日官宣10月7日永久关服，370万下载/$1亿累计收入/近3年运营（RPG品类）\n- 最近30天收入仅$68万，月收入从峰值骤降至不足百万\n- 无离线模式无资产迁移，停止Red Crystal Sales充值\n- 日本占1/3下载，北美占1/4；SE全移动端矩阵累计$68.8亿",
        "designAnalysis": "- $1亿/3年≈年均$3300万对SE而言ROI不达标，但对多数公司已是成功\n- 月收入$68万=日均$2.3万，运维成本可能已倒挂\n- 继Mario Kart Tour后一周内第二个大IP手游宣布关服=行业趋势信号\n- SE移动端$68.8亿说明整体盘子够大，单品ROI不够就砍",
        "bsInsight": "一周内两个大IP关服（Mario Kart+FF7EC）释放明确信号：大厂对手游的ROI容忍度在快速收紧。对BS的启示：①收入曲线下行时必须有止损线；②$1亿级产品都会被砍说明IP不是护身符——持续运营能力才是；③无离线模式再次成为玩家痛点，应考虑账号资产跨产品可迁移性。",
        "sourceUrl": "https://mobilegamer.biz/final-fantasy-7-ever-crisis-closes-in-october/",
        "imageUrl": ""
    },
    {
        "id": "2026-07-10-03",
        "date": "2026-07-10",
        "game": "行业数据 (Sensor Tower/AppMagic)",
        "title": "【6月全球手游收入榜】Whiteout Survival登顶，PUBG Mobile/Candy Crush/LastWar骤降——世界杯效应+暑期档重塑格局",
        "highlights": "- Sensor Tower数据：Whiteout Survival(SLG)夺得6月全球手游收入冠军，eFootball因世界杯强势上升\n- Honor of Kings因Unbound Destiny版本表现良好，Gossip Harbor叙事活动驱动增长\n- PUBG Mobile/Candy Crush Saga/LastWar三款产品月收入出现明显骤降\n- 下载榜：Roblox第一，Arrows系列3款进入Top10，Block Blast持续下滑",
        "designAnalysis": "- Whiteout Survival登顶=SLG品类头部集中度进一步提升\n- eFootball世界杯期间强势=体育赛事窗口对足球类产品有决定性影响\n- PUBG Mobile骤降可能与火影联动7.9上线前的观望期有关\n- Arrows系列3款进入下载Top10=超休闲品类仍有爆发空间",
        "bsInsight": "核心观察：①世界杯窗口期足球类产品收入暴增（eFootball），BS应预判体育赛事对竞品的影响并做错峰策略；②PUBG Mobile骤降后紧接火影联动=经典的【低谷蓄力→联动爆发】节奏，BS的版本节奏也应有意制造期待窗口；③SLG登顶说明高ARPU品类在头部效应下仍在增长。",
        "sourceUrl": "https://mobilegamer.biz/data-digest-pokemon-go-turns-10-junes-top-performers-funding-news-supercity-stats-more/",
        "imageUrl": ""
    }
]

# Read existing reports
reports_path = os.path.join(DATA_DIR, "reports.json")
with open(reports_path, 'r', encoding='utf-8') as f:
    reports = json.load(f)

# Check for duplicates by id
existing_ids = {r["id"] for r in reports}
added_reports = []
for r in new_reports:
    if r["id"] not in existing_ids:
        added_reports.append(r)

# Prepend new reports (newest first)
reports = added_reports + reports

# Write back
with open(reports_path, 'w', encoding='utf-8') as f:
    json.dump(reports, f, ensure_ascii=False, indent=2)
print(f"Reports: added {len(added_reports)}, total {len(reports)}")

# === 2. SKINS ===
new_skins_entry = {
    "date": "2026-07-10",
    "entries": [
        {
            "game": "和平精英",
            "skinName": "新神装【幻音九尾·璃】今日0点正式上线（九尾狐主题全套特效+娜扎Cos大使+璀璨转盘）",
            "type": "神装级·今日D-Day",
            "releaseDate": "2026.7.10",
            "brief": "射击BR品类7周年活动矩阵最高端付费出口，九尾狐主题含全套特效+专属动作，配套璀璨转盘同步开启",
            "sourceUrl": "https://news.qq.com/rain/a/20260709A053SN00",
            "biliSearch": "https://search.bilibili.com/all?keyword=%E5%92%8C%E5%B9%B3%E7%B2%BE%E8%8B%B1+%E5%B9%BB%E9%9F%B3%E4%B9%9D%E5%B0%BE+%E7%92%83+%E7%A5%9E%E8%A3%85+7.10&order=pubdate",
            "imageUrl": ""
        },
        {
            "game": "三角洲行动",
            "skinName": "彩虹六号联动今日正式开启：蜂医×Doc金皮+无名×Vigil红皮+深蓝×Montagne红皮+2款墨冰武器（3选2+1免费）",
            "type": "FPS同品类联动·今日D-Day·限时绝版",
            "releaseDate": "2026.7.10",
            "brief": "FPS撤离品类×R6联动今日正式开启，3款传说干员自选2款免费+2款墨冰武器自选1款免费，限时绝版不返场",
            "sourceUrl": "https://www.bilibili.com/video/BV1Ce7A6tEfs/",
            "biliSearch": "https://search.bilibili.com/all?keyword=%E4%B8%89%E8%A7%92%E6%B4%B2%E8%A1%8C%E5%8A%A8+%E5%BD%A9%E8%99%B9%E5%85%AD%E5%8F%B7+%E8%81%94%E5%8A%A8+%E4%BB%8A%E6%97%A5%E5%BC%80%E5%90%AF+7.10&order=pubdate",
            "imageUrl": "http://i2.hdslb.com/bfs/archive/3d749e1d3a6092ef4a5648a7ad1318f970dda1c9.jpg"
        },
        {
            "game": "CODM (国际版)",
            "skinName": "S6 Persona 5 Royal联动第二周：Violet(菫)Armory新一轮角色解锁+Mythic FSS Hurricane Draw持续中",
            "type": "JRPG联动赛季·第二周运营",
            "releaseDate": "2026.7.1",
            "brief": "FPS品类×P5R联动进入第二周运营，Violet角色Armory本周解锁，Mythic Draw限时继续中",
            "sourceUrl": "https://gamemarket.gg/news/call-of-duty-mobile/call-of-duty-mobile-season-6-launch-persona-5-royal-complete-overview",
            "biliSearch": "https://search.bilibili.com/all?keyword=CODM+S6+Persona+5+%E7%AC%AC%E4%BA%8C%E5%91%A8+Violet&order=pubdate",
            "imageUrl": ""
        },
        {
            "game": "Fortnite",
            "skinName": "DC Summer Event确认7.16上线（夏日版Batman/Harley Quinn/Catwoman/Poison Ivy+Batman Sprite新品类道具+Batmobile载具）",
            "type": "DC夏日IP联动·7.16上线确认",
            "releaseDate": "2026.7.16",
            "brief": "BR品类DC主题夏日活动确认7.16上线，四款经典DC角色沙滩休闲版重绘+首款Batman Sprite追踪型宠物+Batmobile",
            "sourceUrl": "https://beebom.com/fortnite-leak-reveals-dc-summer-event-with-new-skins-and-a-batman-sprite-to-terrify-your-enemies/",
            "biliSearch": "https://search.bilibili.com/all?keyword=Fortnite+DC+Summer+Batman+Sprite+%E5%A4%8F%E6%97%A5+7.16&order=pubdate",
            "imageUrl": ""
        }
    ]
}

skins_path = os.path.join(DATA_DIR, "skins.json")
with open(skins_path, 'r', encoding='utf-8') as f:
    skins = json.load(f)

# Check if 2026-07-10 already exists
existing_dates = {s["date"] for s in skins}
if "2026-07-10" not in existing_dates:
    skins.insert(0, new_skins_entry)
    print(f"Skins: added 2026-07-10 entry with {len(new_skins_entry['entries'])} skins")
else:
    print("Skins: 2026-07-10 already exists, skipping")

with open(skins_path, 'w', encoding='utf-8') as f:
    json.dump(skins, f, ensure_ascii=False, indent=2)
print(f"Skins: total {len(skins)} date entries")

# === 3. ACTIVITIES ===
new_activities = [
    {
        "id": "2026-07-10-act-01",
        "date": "2026-07-10",
        "game": "和平精英 (Tencent)",
        "title": "【和平精英7.10幻音九尾·璃神装上线：璀璨转盘+明星Cos大使+递进式预热营销】",
        "heat": "\U0001f525 今日0点上线 | 九尾狐国风主题 | 娜扎Cos大使 | 7周年活动天花板",
        "tag": "\U0001f31f 最新活动",
        "mechanismType": "璀璨转盘+明星营销+递进式预热",
        "mechanism": "- 璀璨转盘独立通道：与常规军需分离，专属付费入口不蚕食日常流水\n- 娜扎Cos大使（非代言）：轻量级明星合作，成本<代言但传播效果接近\n- 3天递进预热：7.6悬念海报→7.8 CG动画→7.10上线，信息不断层",
        "whyHot": "- 神装是和平精英付费天花板，每次上线都是社区级事件\n- 九尾狐主题在国风审美中认知度极高，玩家共鸣强\n- 娜扎明星效应带动破圈传播，非游戏用户也会关注",
        "insight": "- 独立转盘通道=不影响日常军需节奏，做增量而非替代\n- 明星Cos≠代言：规避代言合规风险但保留流量价值\n- 递进预热保持话题热度：对BS的启示是旗舰皮肤上线应有3-5天预热窗口",
        "sourceUrl": "https://news.qq.com/rain/a/20260709A053SN00",
        "imageUrl": ""
    },
    {
        "id": "2026-07-10-act-02",
        "date": "2026-07-10",
        "game": "三角洲行动 x 彩虹六号 (腾讯/育碧)",
        "title": "【三角洲行动×彩虹六号联动今日正式开启：免费自选传说+墨冰付费天花板+限时绝版FOMO】",
        "heat": "\U0001f525 今日正式上线 | 3选2免费传说 | 墨冰绝版 | FPS同品类联动",
        "tag": "\U0001f3c6 讨论度高",
        "mechanismType": "免费自选+限时绝版+同品类联动",
        "mechanism": "- 3款传说干员自选2款免费：玩家有选择权=满意度远高于随机发放\n- 2款墨冰武器自选1款免费：零氪也能获得传说级联动内容\n- 限时绝版不返场：制造极强FOMO，犹豫=永久错过\n- Doc金皮做最高付费天花板：免费层做体量，付费层做深度",
        "whyHot": "- 两个FPS头部产品联动=行业事件，话题性天然爆棚\n- 免费自选两款传说的慷慨度让社区一致好评\n- 限时绝版=FOMO最大化，窗口期付费冲动极强",
        "insight": "- 免费自选是最高级的联动慷慨度表达：用户选择权>随机赠送\n- 限时绝版FOMO+免费入口=全层级玩家都有理由登录和消费\n- 核心学习：联动的免费内容越慷慨，付费天花板的转化率越高",
        "sourceUrl": "https://www.bilibili.com/video/BV1Ce7A6tEfs/",
        "imageUrl": "http://i2.hdslb.com/bfs/archive/3d749e1d3a6092ef4a5648a7ad1318f970dda1c9.jpg"
    }
]

activities_path = os.path.join(DATA_DIR, "activities.json")
with open(activities_path, 'r', encoding='utf-8') as f:
    activities = json.load(f)

existing_act_ids = {a["id"] for a in activities}
added_acts = []
for a in new_activities:
    if a["id"] not in existing_act_ids:
        added_acts.append(a)

activities = added_acts + activities

with open(activities_path, 'w', encoding='utf-8') as f:
    json.dump(activities, f, ensure_ascii=False, indent=2)
print(f"Activities: added {len(added_acts)}, total {len(activities)}")

# === VALIDATION ===
for name in ["reports.json", "skins.json", "activities.json"]:
    path = os.path.join(DATA_DIR, name)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    try:
        json.loads(content)
        print(f"  {name}: VALID JSON")
    except json.JSONDecodeError as e:
        print(f"  {name}: INVALID JSON - {e}")

print("\nDone!")
