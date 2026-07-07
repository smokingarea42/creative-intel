import json
import os

os.chdir(r'C:\Users\xuyiqing03\Documents\creative-intel\data')

# === REPORTS ===
with open('reports.json', 'r', encoding='utf-8') as f:
    reports = json.load(f)

new_reports = [
    {
        "id": "2026-07-07-01",
        "date": "2026-07-07",
        "game": "Xbox / Microsoft",
        "title": "【Xbox裁员3200人：King和Mojang直接向CEO Asha Sharma汇报】—— 手游巨头重组对行业的三层信号",
        "highlights": "- Xbox宣布裁员3200人，4家主机工作室被剥离（Ninja Theory/Double Fine/Compulsion/Undead Labs）\n- King（Candy Crush）和Mojang（Minecraft）将直接向CEO Asha Sharma汇报，被定义为【平台级资产】\n- Sharma明确表示管理层级压缩至3-5层，新COO Helen Chiang拥有端到端P&L权\n- 承诺2027年恢复增长，今年投资规模不减但方向更聚焦",
        "designAnalysis": "- King直接向CEO汇报=手游在微软体系内地位史上最高，不再是边缘业务\n- 4家主机工作室剥离而手游保留=资源向高ROI业务倾斜\n- 管理层级压缩=决策速度加快，对King的Live Ops节奏是利好",
        "bsInsight": "核心信号：手游在平台巨头内的战略地位持续上升。King被定义为【平台级】说明Candy Crush的变现能力已被视为Xbox生态的核心引擎之一。对BS的启示：手游的商业确定性远高于主机游戏，这是行业共识的又一次确认。",
        "sourceUrl": "https://mobilegamer.biz/xbox-axes-3200-jobs-king-and-mojang-to-report-directly-to-boss-asha-sharma/",
        "imageUrl": ""
    },
    {
        "id": "2026-07-07-02",
        "date": "2026-07-07",
        "game": "Scopely / Studio Auknow (日本市场)",
        "title": "【Scopely战略投资赛马娘创始人新工作室Studio Auknow】—— 日本手游市场的【顶级创作者+全球发行】新范式",
        "highlights": "- Scopely（Monopoly Go母公司）宣布战略投资Studio Auknow，由赛马娘前总监创立\n- 赛马娘累计1800万下载、$24亿收入，95%来自日本市场\n- Scopely日本总裁明确表态：长期投资日本市场，支持顶级创作者从日本走向世界\n- 英语版赛马娘美国已获220万下载，证明IP全球化潜力",
        "designAnalysis": "- $24亿/95%来自日本=单一市场ARPU极致化的又一案例（对标eFootball）\n- Scopely投资逻辑：用全球发行能力+日本顶级创作者的组合打破地域限制\n- 赛马娘的成功公式：养成+收集+强叙事=超深度付费",
        "bsInsight": "这笔投资再次证明：日本市场的单用户价值远超全球平均。赛马娘$24亿/1800万下载=$133/下载。对BS的参考：如果日本市场ARPU显著高于其他区域，值得为日本做深度本地化内容和定价策略。",
        "sourceUrl": "https://mobilegamer.biz/scopely-helps-fund-the-new-studio-from-the-mind-behind-umamusume-pretty-derby/",
        "imageUrl": ""
    },
    {
        "id": "2026-07-07-03",
        "date": "2026-07-07",
        "game": "行业数据 (AppMagic/GamingonPhone)",
        "title": "【6月全球手游收入榜：王者荣耀$1.1亿蝉联榜首，Whiteout Survival $1.09亿紧追，足球游戏借世界杯窗口集体上升】",
        "highlights": "- 王者荣耀6月约$1.1亿居收入榜首（MOBA品类），Whiteout Survival $1.09亿紧随其后\n- 下载榜Arrows Puzzle Escape蝉联第一（2520万安装），Roblox升至第四\n- 足球相关游戏（Soccer Superstar/EA FC Mobile/Football League）集体进入下载Top15\n- Free Fire MAX稳居下载第三，证明BR品类在新兴市场依然强劲",
        "designAnalysis": "- 王者+Whiteout差距缩小至$100万：SLG品类持续逼近MOBA霸主\n- 足球游戏集体上升=世界杯窗口效应的实时验证（对标此前+71%下载数据）\n- 下载榜被休闲拼图主导但收入榜全是中重度：获客和变现是两个世界",
        "bsInsight": "两个核心观察：①世界杯窗口正在实时生效，足球游戏集体进入下载榜——BS如果有体育主题活动应该正在运行中；②收入榜头部格局稳定说明存量运营决定一切，新品很难在短期内冲击Top10。",
        "sourceUrl": "https://gamingonphone.com/news/top-15-mobile-games-for-june-2026/",
        "imageUrl": ""
    }
]

reports = new_reports + reports

with open('reports.json', 'w', encoding='utf-8') as f:
    json.dump(reports, f, ensure_ascii=False, indent=2)

print(f"Reports updated: {len(reports)} entries, latest date: {reports[0]['date']}")

# === SKINS ===
with open('skins.json', 'r', encoding='utf-8') as f:
    skins = json.load(f)

# Check existing entries for dedup
existing_skin_names = set()
for day in skins:
    for entry in day.get('entries', []):
        existing_skin_names.add(entry.get('skinName', '')[:30])

new_skins_entries = []

# Fortnite Scooby-Doo - already in 7.6 data as leak, check if already covered
scooby_check = "Scooby-Doo联动皮肤泄露"[:30]
if scooby_check not in existing_skin_names:
    new_skins_entries.append({
        "game": "Fortnite",
        "skinName": "Scooby-Doo联动皮肤已上架Item Shop（Shaggy/Velma/Fred/Daphne+Scooby宠物+Mystery Machine滑翔伞）",
        "type": "动画IP联动·7.4上架",
        "releaseDate": "2026.7.4",
        "brief": "BR品类继American Dad后连续第二周动画IP联动，神秘公司全阵容上架，延续每周一个IP的工业化联动节奏",
        "sourceUrl": "https://fortnite.gg/shop",
        "biliSearch": "https://search.bilibili.com/all?keyword=Fortnite+Scooby+Doo+%E5%8F%B2%E9%85%B7%E6%AF%94+%E7%9A%AE%E8%82%A4&order=pubdate",
        "imageUrl": ""
    })

# CODM S6 P5R - ongoing, add mid-season update note
codm_p5_check = "CODM S6 Persona 5首周"[:30]
if codm_p5_check not in existing_skin_names:
    new_skins_entries.append({
        "game": "CODM (国际版)",
        "skinName": "S6 Persona 5 Royal联动首周运营中：Phantom Thieves Armory四角色（Joker/Panther/Queen/Violet）+Mythic FSS Hurricane Draw",
        "type": "JRPG联动赛季·首周运营",
        "releaseDate": "2026.7.1",
        "brief": "FPS品类×P5R联动正式运营第一周，四位怪盗团角色Operator皮肤通过Series Armory获取，Mythic Draw限时中",
        "sourceUrl": "https://gamemarket.gg/news/call-of-duty-mobile/call-of-duty-mobile-season-6-launch-persona-5-royal-complete-overview",
        "biliSearch": "https://search.bilibili.com/all?keyword=CODM+S6+Persona+5+%E8%81%94%E5%8A%A8+%E9%A6%96%E5%91%A8&order=pubdate",
        "imageUrl": ""
    })

# Delta Force R6 collab D-3
delta_r6_check = "三角洲行动 彩虹六号联动倒计时3天"[:30]
if delta_r6_check not in existing_skin_names:
    new_skins_entries.append({
        "game": "三角洲行动",
        "skinName": "彩虹六号联动倒计时3天（7.10正式开启：金皮Doc+红皮Vigil/Montagne+墨冰武器+免费自选两款传说）",
        "type": "FPS同品类联动·D-3倒计时",
        "releaseDate": "2026.7.10",
        "brief": "FPS撤离品类×R6联动正式服进入最后3天倒计时，社区热度持续攀升，B站相关视频播放量持续上涨",
        "sourceUrl": "https://gl.ali213.net/html/2026-6/1782485.html",
        "biliSearch": "https://search.bilibili.com/all?keyword=%E4%B8%89%E8%A7%92%E6%B4%B2%E8%A1%8C%E5%8A%A8+%E5%BD%A9%E8%99%B9%E5%85%AD%E5%8F%B7+%E8%81%94%E5%8A%A8+%E5%80%92%E8%AE%A1%E6%97%B6&order=pubdate",
        "imageUrl": "http://i2.hdslb.com/bfs/archive/3d749e1d3a6092ef4a5648a7ad1318f970dda1c9.jpg"
    })

# PUBG Mobile Naruto D-2
pubgm_naruto_check = "PUBG Mobile 火影忍者倒计时2天"[:30]
if pubgm_naruto_check not in existing_skin_names:
    new_skins_entries.append({
        "game": "PUBG Mobile",
        "skinName": "火影忍者疾风传联动倒计时2天（7.9上线：5个Mythic级忍者套装+Prize Path系统+查克拉特效）",
        "type": "顶级动漫IP联动·D-2倒计时",
        "releaseDate": "2026.7.9",
        "brief": "射击BR品类4.5版本核心联动进入最后2天倒计时，Mythic级鸣人/佐助/鼬/斑/卡卡西全阵容确认",
        "sourceUrl": "https://www.topuplive.com/news/pubg-mobile-x-naruto-shippuden-collaboration.html",
        "biliSearch": "https://search.bilibili.com/all?keyword=PUBG+Mobile+%E7%81%AB%E5%BD%B1%E5%BF%8D%E8%80%85+%E8%81%94%E5%8A%A8+%E5%80%92%E8%AE%A1%E6%97%B6&order=pubdate",
        "imageUrl": ""
    })

if new_skins_entries:
    new_day = {"date": "2026-07-07", "entries": new_skins_entries}
    skins.insert(0, new_day)

with open('skins.json', 'w', encoding='utf-8') as f:
    json.dump(skins, f, ensure_ascii=False, indent=2)

print(f"Skins updated: {len(skins)} days, latest: {skins[0]['date']}, new entries: {len(new_skins_entries)}")

# === ACTIVITIES ===
with open('activities.json', 'r', encoding='utf-8') as f:
    activities = json.load(f)

new_activities = [
    {
        "id": "2026-07-07-act-01",
        "date": "2026-07-07",
        "game": "CODM × Persona 5 Royal (Activision/TiMi)",
        "title": "【CODM S6 Plunder Treasure Hunt首周运营复盘：PvE Domain+面具Buff+双Armory轮转节奏】",
        "heat": "🔥 7.1上线运营第7天 | Persona 5全球2500万销量IP | 年度最大联动",
        "tag": "🏆 讨论度高",
        "mechanismType": "IP玩法改造+双Armory商店+Mythic Draw限时",
        "mechanism": "- Plunder模式内出现P5R红色Domain，击败Shadow 3波获取Persona面具Buff（强化弹道/速度）\n- 双Series Armory独立商店每周轮转不同怪盗团角色+武器蓝图\n- Mythic FSS Hurricane Draw做最高付费天花板，限时6周窗口",
        "whyHot": "- FPS×JRPG跨品类联动极其罕见，话题性爆棚\n- 面具Buff影响gameplay=不是贴皮而是玩法层联动\n- 双Armory分开收费互不蚕食，ARPU天花板翻倍",
        "insight": "- 【改玩法而非贴皮】是高质量联动的分水岭\n- 双Armory分流=两套独立付费漏斗覆盖不同偏好\n- 对BS启发：联动深度取决于是否改动了核心循环",
        "sourceUrl": "https://gamemarket.gg/news/call-of-duty-mobile/call-of-duty-mobile-season-6-launch-persona-5-royal-complete-overview",
        "imageUrl": ""
    },
    {
        "id": "2026-07-07-act-02",
        "date": "2026-07-07",
        "game": "Riot Games (Valorant/LoL)",
        "title": "【Riot推出Vanguard On-Demand模式：反作弊从常驻变为按需启动】—— 游戏基建层的【用户体验vs安全性】平衡术",
        "heat": "🔥 35%玩家已符合条件 | Win11 25H2+ | 行业首创按需反作弊",
        "tag": "🌟 最新活动",
        "mechanismType": "反作弊体验优化+硬件门槛筛选+信任分层",
        "mechanism": "- Vanguard新增On-Demand模式：内核驱动仅在启动游戏时加载，结束后自动卸载\n- 硬件门槛：Win11 25H2+UEFI Secure Boot+TPM 2.0+VBS+HVCI+IOMMU\n- 约35%玩家已满足条件，新硬件普及后比例持续上升\n- 不强制切换，现有模式可继续使用",
        "whyHot": "- Vanguard常驻争议持续多年，这是Riot首次实质让步\n- 硬件门槛筛选=高端用户优先体验，制造升级动力\n- 竞品（EAC/BattlEye）尚无类似方案",
        "insight": "- 用硬件安全替代软件常驻=技术演进解决用户体验问题\n- 35%符合率说明Win11渗透已到临界点\n- 对BS启发：反作弊体验优化本身可以是营销事件（玩家好感度直接提升）",
        "sourceUrl": "https://www.talkesport.com/news/valorant/riot-vanguard-on-demand-anti-cheat-update/",
        "imageUrl": ""
    }
]

activities = new_activities + activities

with open('activities.json', 'w', encoding='utf-8') as f:
    json.dump(activities, f, ensure_ascii=False, indent=2)

print(f"Activities updated: {len(activities)} entries, latest: {activities[0]['date']}")
print("\nAll 3 JSON files updated successfully!")
