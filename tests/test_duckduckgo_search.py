from duckduckgo_search import ddg
from duckduckgo_search.utils import SESSION


SESSION.proxies = {
    "http": f"socks5h://localhost:7890",
    "https": f"socks5h://localhost:7890"
}
r = ddg("马保国")
print(r[:2])
"""
[{'title': '马保国 - 维基百科，自由的百科全书', 'href': 'https://zh.wikipedia.org/wiki/%E9%A9%AC%E4%BF%9D%E5%9B%BD', 'body': '马保国（1951年 — ） ，男，籍贯 山东 临沂，出生及长大于河南，中国大陆太极拳师，自称"浑元形意太极门掌门人" 。 马保国因2017年约战mma格斗家徐晓冬首次出现
大众视野中。 2020年5月，马保国在对阵民间武术爱好者王庆民的比赛中，30秒内被连续高速击倒三次，此事件成为了持续多日的社交 ...'}, {'title': '馬保國的主页 - 抖音', 'href': 'https://www.douyin.com/user/MS4wLjABAAAAW0E1ziOvxgUh3VVv5FE6xmoo3w5WtZalfphYZKj4mCg', 'body': '6.3万. #马马国教扛打功 最近有几个人模芳我动作，很危险啊，不可以的，朋友们不要受伤了。. 5.3万. #马保国直播带货榜第一 朋友们周末愉快，本周六早上湿点，我本人在此号进行第一次带货直播，活到老，学到老，越活越年轻。. 7.0万. #马保国击破红牛罐 昨天 ...'}]


"""