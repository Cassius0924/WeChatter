import json
import unittest

from wechatter.commands._commands import zhihu_hot


class TestZhihuHotCommand(unittest.TestCase):
    def setUp(self):
        with open("tests/commands/test_zhihu_hot/zhihu_hot_response.json") as f:
            self.r_json = json.load(f)
            self.zhihu_hot_list = self.r_json["data"]

    def test_extract_zhihu_hot_data_success(self):
        result = zhihu_hot._extract_zhihu_hot_data(self.r_json)
        self.assertEqual(result, self.zhihu_hot_list)

    def test_extract_zhihu_hot_data_failure(self):
        with self.assertRaises(Exception):
            zhihu_hot._extract_zhihu_hot_data({})

    def test_generate_zhihu_hot_message_success(self):
        result = zhihu_hot._generate_zhihu_hot_message(self.zhihu_hot_list)
        true_result = "1. 得州州长警告拜登称，若「联邦化」得州国民警卫队将是政治错误，如何解读？该事件将会如何演变？\n2. 贵州一村民办酒席被挂工作证人员往食物撒盐，当地通报「已致歉」，如何评价此事？\n3. 美国联合包裹运送服务公司宣布将裁员 1.2 万人，将节省约 10 亿美元成本，哪些信息值得关注？\n4. 汞比金多一个质子，理论上汞比金更难形成，为什么汞比金便宜？\n5. 沙特伊朗等五国已正式成为金砖成员国，34 个国家提出书面申请，对金砖扩容做何展望？哪些信息值得关注？\n6. 23-24 赛季 NBA快船 125:109 奇才，如何评价这场比赛？\n7. 戴尔服务中国公司拟注销，哪些信息值得关注？\n8. 如何看待 2 月 1 日 A 股市场行情？\n9. 如何评价“祸不及家人的前提是惠不及家人”这个观点？\n10. 明明知道熬夜对身体不好，可就是戒不掉，我该怎么办？\n11. 「复旦研究员刺杀书记案」一审宣判被告死缓，犯故意杀人罪，哪些信息值得关注？如何看待此案？\n12. 白所成等10名缅北重大犯罪嫌疑人被押解回国，缅北四大家族尽数覆灭，哪些信息值得关注？\n13. 韩国瑜当选台新任立法机构负责人，释放了哪些信息？这对台湾当局执政有何影响？\n14. 财政部表示基本养老保险基金已累计结余近 6 万亿元，养老金按时足额发放有保证，哪些信息值得关注？\n15. 河南暴雪来临，洛阳等地已开始下雪，目前情况如何？会对春运出行带来哪些影响？\n16. 同事听到我用“免贵姓…”回答“您贵姓？”这个问题的时候全都笑了，是哪里出了问题？\n17. 如何评价《崩坏：星穹铁道》千星纪游PV：「旧梦重温」？\n18. 23-24 赛季英超利物浦 4:1 切尔西，如何评价这场比赛？\n19. 孩子应该做家务、做饭吗？\n20. 你在跑步路上遇到的最大的阻碍是什么？"
        self.assertIn(true_result, result)

    def test_generate_zhihu_hot_message_empty_list(self):
        result = zhihu_hot._generate_zhihu_hot_message([])
        self.assertEqual(result, "暂无知乎热搜")

    def test_generate_zhihu_hot_quoted_response_success(self):
        result = zhihu_hot._generate_zhihu_hot_quoted_response(self.zhihu_hot_list)
        true_result = '{"1": "https://www.zhihu.com/question/642169181", "2": "https://www.zhihu.com/question/642297518", "3": "https://www.zhihu.com/question/642108938", "4": "https://www.zhihu.com/question/641995117", "5": "https://www.zhihu.com/question/642299758", "6": "https://www.zhihu.com/question/642287890", "7": "https://www.zhihu.com/question/642154023", "8": "https://www.zhihu.com/question/642290406", "9": "https://www.zhihu.com/question/641648705", "10": "https://www.zhihu.com/question/640060689", "11": "https://www.zhihu.com/question/642299465", "12": "https://www.zhihu.com/question/642125769", "13": "https://www.zhihu.com/question/642330312", "14": "https://www.zhihu.com/question/642307679", "15": "https://www.zhihu.com/question/642184584", "16": "https://www.zhihu.com/question/521484226", "17": "https://www.zhihu.com/question/642314136", "18": "https://www.zhihu.com/question/642267038", "19": "https://www.zhihu.com/question/641865103", "20": "https://www.zhihu.com/question/640626886"}'
        self.assertEqual(result, true_result)
