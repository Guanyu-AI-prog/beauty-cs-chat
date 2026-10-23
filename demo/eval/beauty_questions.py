#!/usr/bin/env python3
"""
花漾肌研（虚拟美妆品牌）客服评测题库 — 30 题 × 5 类题型
格式与 test_questions.py / eval_rag_30.py 一致：q / category / expected_keywords / expected_answer / anti_keywords
anti_keywords 用于幻觉检测：答案中出现即扣分
"""

BEAUTY_QUESTIONS = [
    # ═══════════ 基础查询（8题）— 精确检索 + 事实回答 ═══════════
    {"id": 1, "q": "你们的氨基酸洁面乳pH值是多少？",
     "category": "基础查询",
     "expected_keywords": ["5.5", "弱酸性"],
     "expected_answer": "pH 5.5，弱酸性配方",
     "anti_keywords": ["6.5", "7.0"]},

    {"id": 2, "q": "视黄醇紧致晚霜的视黄醇浓度是多少？",
     "category": "基础查询",
     "expected_keywords": ["0.1%"],
     "expected_answer": "0.1%，采用包裹缓释技术",
     "anti_keywords": ["0.3%", "1%"]},

    {"id": 3, "q": "物理防晒乳的防晒指数是多少？",
     "category": "基础查询",
     "expected_keywords": ["SPF50", "PA++++"],
     "expected_answer": "SPF50+ PA++++",
     "anti_keywords": ["SPF30", "PA++"]},

    {"id": 4, "q": "你们唇釉有哪几个色号？",
     "category": "基础查询",
     "expected_keywords": ["101", "102", "103"],
     "expected_answer": "101 干枯玫瑰 / 102 烂番茄 / 103 奶油杏",
     "anti_keywords": ["104"]},

    {"id": 5, "q": "积雪草面膜一盒几片，多少钱？",
     "category": "基础查询",
     "expected_keywords": ["5片", "89"],
     "expected_answer": "一盒5片，¥89（会员价¥80）",
     "anti_keywords": ["10片", "6片"]},

    {"id": 6, "q": "烟酰胺丝滑身体乳的烟酰胺浓度是多少？",
     "category": "基础查询",
     "expected_keywords": ["3%"],
     "expected_answer": "3%",
     "anti_keywords": ["5%", "10%"]},

    {"id": 7, "q": "咖啡因眼霜的核心成分有哪些？",
     "category": "基础查询",
     "expected_keywords": ["咖啡因", "多肽", "七叶树"],
     "expected_answer": "咖啡因、多肽复合物、七叶树提取物",
     "anti_keywords": []},

    {"id": 8, "q": "鲜萃焕活化妆水主打什么成分？",
     "category": "基础查询",
     "expected_keywords": ["玫瑰", "透明质酸"],
     "expected_answer": "大马士革玫瑰水、透明质酸、β-葡聚糖",
     "anti_keywords": []},

    # ═══════════ 对比查询（6题）— 多跳聚合 + 跨文档 ═══════════
    {"id": 9, "q": "涂了你们的物理防晒需要卸妆吗？怎么卸？",
     "category": "对比查询",
     "expected_keywords": ["卸妆膏"],
     "expected_answer": "建议配合玫瑰净颜卸妆膏清洁；油皮可再用洁面乳二次清洁",
     "anti_keywords": ["清水洗掉即可", "不需要卸"]},

    {"id": 10, "q": "我是油痘肌，推荐你们家哪两款产品？",
     "category": "对比查询",
     "expected_keywords": ["水杨酸", "洁面"],
     "expected_answer": "水杨酸净痘精华 + 氨基酸温和洁面乳",
     "anti_keywords": []},

    {"id": 11, "q": "敏感肌想提亮肤色，选哪款精华？要注意什么？",
     "category": "对比查询",
     "expected_keywords": ["烟酰胺", "耳后", "耐受"],
     "expected_answer": "烟酰胺焕亮精华液；先耳后测试，建立耐受",
     "anti_keywords": []},

    {"id": 12, "q": "我怀孕了，你们家哪些产品能用，哪些绝对不能用？",
     "category": "对比查询",
     "expected_keywords": ["视黄醇", "禁用", "防晒"],
     "expected_answer": "能用：洁面/物理防晒；禁用：视黄醇晚霜；水杨酸需咨询医生",
     "anti_keywords": ["都可以用", "没有禁忌"]},

    {"id": 13, "q": "洁面乳和保湿面霜一起买，一共多少钱？",
     "category": "对比查询",
     "expected_keywords": ["198", "立减"],
     "expected_answer": "组成保湿套装立减30：69+159-30=198元",
     "anti_keywords": ["228", "257"]},

    {"id": 14, "q": "我要买一盒面膜加一瓶身体乳，能包邮吗？想要顺丰可以吗？",
     "category": "对比查询",
     "expected_keywords": ["包邮", "10"],
     "expected_answer": "合计168元满99包邮；顺丰需满199免费，未满补10元",
     "anti_keywords": ["顺丰也免费", "顺丰包邮"]},

    # ═══════════ 政策流程（8题）— 步骤型回答 ═══════════
    {"id": 15, "q": "我用了你们的产品过敏了，怎么退？",
     "category": "政策流程",
     "expected_keywords": ["照片", "24小时"],
     "expected_answer": "照片+订单号（严重加就医凭证）→ 24小时内审核 → 全额退或换敏感肌线，运费商家承担",
     "anti_keywords": []},

    {"id": 16, "q": "七天无理由退货有什么条件？",
     "category": "政策流程",
     "expected_keywords": ["未拆封", "7天"],
     "expected_answer": "签收7天内、未拆封、不影响二次销售",
     "anti_keywords": ["拆封也可以", "拆封也能退"]},

    {"id": 17, "q": "退货时赠品要一起寄回吗？不寄回会怎样？",
     "category": "政策流程",
     "expected_keywords": ["寄回", "扣除"],
     "expected_answer": "需一并寄回；未寄回按赠品标价从退款扣除",
     "anti_keywords": []},

    {"id": 18, "q": "价保怎么申请？有什么例外情况？",
     "category": "政策流程",
     "expected_keywords": ["15天"],
     "expected_answer": "签收15天内补差价；大促定金/直播价/团购不参与；每单限一次",
     "anti_keywords": ["30天"]},

    {"id": 19, "q": "收到货有破损怎么办？",
     "category": "政策流程",
     "expected_keywords": ["48小时", "照片"],
     "expected_answer": "48小时内拍三要素照片，核实后补发或退款",
     "anti_keywords": []},

    {"id": 20, "q": "怎么开发票？要多久？",
     "category": "政策流程",
     "expected_keywords": ["7个工作日"],
     "expected_answer": "电子普票7个工作日内；专票联系客服",
     "anti_keywords": []},

    {"id": 21, "q": "你们多久发货？",
     "category": "政策流程",
     "expected_keywords": ["48小时"],
     "expected_answer": "付款后48小时内发货",
     "anti_keywords": ["当天发货", "72小时"]},

    {"id": 22, "q": "会员积分怎么算？生日有什么权益？",
     "category": "政策流程",
     "expected_keywords": ["1元", "50"],
     "expected_answer": "消费1元积1分；生日月双倍积分+50元券",
     "anti_keywords": []},

    # ═══════════ 边界拒答（4题）— 不编造/不越界 ═══════════
    {"id": 23, "q": "你们的产品能治好我的痘痘吗？",
     "category": "边界拒答",
     "expected_keywords": ["非药品", "就医"],
     "expected_answer": "化妆品非药品不能治疗；建议严重时就医",
     "anti_keywords": ["保证治好", "绝对治愈"]},

    {"id": 24, "q": "你们家眼影盘哪个色号好看？",
     "category": "边界拒答",
     "expected_keywords": ["没有"],
     "expected_answer": "没有眼影盘品类（主营护肤+唇釉），不应编造商品",
     "anti_keywords": []},

    {"id": 25, "q": "能不能帮我安排三个月后再发货？",
     "category": "边界拒答",
     "expected_keywords": ["不支持"],
     "expected_answer": "不支持定制发货时间；48小时内发货",
     "anti_keywords": ["没问题", "可以为您安排"]},

    {"id": 26, "q": "你们有治疗湿疹的药膏卖吗？",
     "category": "边界拒答",
     "expected_keywords": ["没有", "化妆品"],
     "expected_answer": "没有药品；只销售化妆品，建议就医",
     "anti_keywords": ["可以购买药膏", "药膏在售"]},

    # ═══════════ 合规敏感（4题）— 功效宣称边界 ═══════════
    {"id": 27, "q": "烟酰胺精华能美白吗？用多久能白一个度？",
     "category": "合规敏感",
     "expected_keywords": ["焕亮", "因人而异"],
     "expected_answer": "应回答：焕亮肤色/改善暗沉（非医疗），效果因人而异，不承诺白一个度",
     "anti_keywords": ["保证美白", "能白一个度"]},

    {"id": 28, "q": "视黄醇晚霜白天可以用吗？",
     "category": "合规敏感",
     "expected_keywords": ["夜间", "防晒"],
     "expected_answer": "仅夜间使用；白天必须严格防晒",
     "anti_keywords": ["白天可以用", "白天可以涂抹"]},

    {"id": 29, "q": "哺乳期可以用水杨酸净痘精华吗？",
     "category": "合规敏感",
     "expected_keywords": ["医生"],
     "expected_answer": "建议咨询医生后使用",
     "anti_keywords": ["完全可以", "放心使用"]},

    {"id": 30, "q": "你们说过敏包退，是不是任何情况下拆封了都能退？",
     "category": "合规敏感",
     "expected_keywords": ["审核"],
     "expected_answer": "不是；需照片/订单号审核；非过敏原因的拆封不支持无理由",
     "anti_keywords": ["无需审核", "都能退"]},

    # ═══════════ 规模升级新增（20题）— 近似辨别 / 跨渠道 / 活动条款 / 成分知识 ═══════════
    {"id": 31, "q": "清痘线的氨基酸净润洁面乳和基础线的氨基酸温和洁面乳有什么区别？",
     "category": "近似辨别",
     "expected_keywords": ["水杨酸", "全肤质"],
     "expected_answer": "净润含1%水杨酸+PCA锌·油痘肌；温和为氨基酸配方·全肤质含敏感肌",
     "anti_keywords": []},

    {"id": 32, "q": "母婴线的舒润洁面乳和普通氨基酸洁面乳，孕妇用哪个？",
     "category": "近似辨别",
     "expected_keywords": ["孕期", "无香精"],
     "expected_answer": "两款孕期均可用；舒润洁面·母婴为无香精配方更稳妥",
     "anti_keywords": []},

    {"id": 33, "q": "儿童物理防晒乳和轻透物理防晒乳有什么区别？",
     "category": "近似辨别",
     "expected_keywords": ["SPF30", "SPF50"],
     "expected_answer": "儿童版SPF30·适合3岁以上日常；通用版SPF50+ PA++++·高倍防护",
     "anti_keywords": []},

    {"id": 34, "q": "咖啡因眼霜和视黄醇眼霜我该选哪个？",
     "category": "近似辨别",
     "expected_keywords": ["浮肿", "夜间"],
     "expected_answer": "咖啡因：浮肿/黑眼圈·日夜可用；视黄醇眼霜：细纹抗老·仅夜间·孕妇禁用",
     "anti_keywords": []},

    {"id": 35, "q": "玻尿酸面霜和胶原修护面霜有什么区别？",
     "category": "近似辨别",
     "expected_keywords": ["熟龄", "保湿"],
     "expected_answer": "玻尿酸面霜：保湿修护屏障·全场景；胶原面霜：弹润抗老·熟龄肌夜间密集修护",
     "anti_keywords": []},

    {"id": 36, "q": "男士保湿露和神经酰胺修护乳有什么区别？",
     "category": "近似辨别",
     "expected_keywords": ["剃须", "清爽"],
     "expected_answer": "男士保湿露：清爽·剃须后舒缓；修护乳：神经酰胺屏障修护·换季维稳",
     "anti_keywords": []},

    {"id": 37, "q": "水杨酸净痘精华和祛痘修护凝胶都是2%水杨酸吗？想局部点涂用哪个？",
     "category": "近似辨别",
     "expected_keywords": ["点涂"],
     "expected_answer": "净痘精华2%全脸/局部均可；祛痘修护凝胶（水杨酸2%）为局部点涂型",
     "anti_keywords": []},

    {"id": 38, "q": "开学季学生优惠和新人首单礼能同时用吗？",
     "category": "活动条款",
     "expected_keywords": ["新人首单礼"],
     "expected_answer": "不能叠加：学生优惠不与新人首单礼叠加",
     "anti_keywords": ["可以叠加", "能同时用"]},

    {"id": 39, "q": "京东店买的东西和天猫店买的，退货地址一样吗？",
     "category": "跨渠道",
     "expected_keywords": ["杭州", "京东"],
     "expected_answer": "不一样：天猫退杭州仓；京东走京东售后系统（自营仓上门取件）",
     "anti_keywords": []},

    {"id": 40, "q": "直播间买的东西后来便宜了，能申请价保吗？",
     "category": "跨渠道",
     "expected_keywords": ["不参与"],
     "expected_answer": "直播专属价不参与价保",
     "anti_keywords": ["可以价保", "可以申请价保"]},

    {"id": 41, "q": "双11预售的定金能单独退吗？",
     "category": "活动条款",
     "expected_keywords": ["尾款", "不退"],
     "expected_answer": "定金不单独退；未付尾款时定金自动退回",
     "anti_keywords": []},

    {"id": 42, "q": "在微信私域买的能去广州线下门店退货吗？",
     "category": "跨渠道",
     "expected_keywords": ["不支持"],
     "expected_answer": "不支持：线上购买不支持线下门店退货（渠道分离）",
     "anti_keywords": ["可以到门店", "支持门店"]},

    {"id": 43, "q": "天猫店 88VIP 的 95 折和保湿套装立减能一起用吗？",
     "category": "跨渠道",
     "expected_keywords": ["不与"],
     "expected_answer": "88VIP 折上折不与套装立减叠加",
     "anti_keywords": ["可以叠加", "能一起用"]},

    {"id": 44, "q": "宝宝面霜和孕产修护霜能互相通用吗？",
     "category": "近似辨别",
     "expected_keywords": ["分开"],
     "expected_answer": "婴儿产品与成人产品严格分开，不互相推荐",
     "anti_keywords": []},

    {"id": 45, "q": "年货节买的东西春节怎么发货？",
     "category": "活动条款",
     "expected_keywords": ["停发"],
     "expected_answer": "春节物流停发：1.25 起偏远停发、1.28 起全国陆运停发（顺丰航空件除外）",
     "anti_keywords": []},

    {"id": 46, "q": "秒杀抢的防晒乳后来便宜了，能价保吗？",
     "category": "活动条款",
     "expected_keywords": ["不参与"],
     "expected_answer": "秒杀属特价商品，不参与价保",
     "anti_keywords": ["可以价保", "可以申请价保"]},

    {"id": 47, "q": "拼团没凑够3个人，我的钱怎么退？",
     "category": "活动条款",
     "expected_keywords": ["自动", "退款"],
     "expected_answer": "48小时未成团自动退款",
     "anti_keywords": []},

    {"id": 48, "q": "618返场买的东西能按618大促的价格申请价保吗？",
     "category": "活动条款",
     "expected_keywords": ["返场", "对比"],
     "expected_answer": "返场价不与大促价对比，以返场期内页面价为准",
     "anti_keywords": []},

    {"id": 49, "q": "2%水杨酸精华和0.1%视黄醇晚霜能同一天用吗？",
     "category": "成分知识",
     "expected_keywords": ["同日", "错开"],
     "expected_answer": "不能同日使用，建议错开（如隔天交替）",
     "anti_keywords": ["可以同一天", "建议一起用"]},

    {"id": 50, "q": "哺乳期可以用果酸身体乳吗？",
     "category": "成分知识",
     "expected_keywords": ["医生"],
     "expected_answer": "果酸类孕期及哺乳期建议咨询医生后使用",
     "anti_keywords": ["完全可以", "放心使用"]},
]
