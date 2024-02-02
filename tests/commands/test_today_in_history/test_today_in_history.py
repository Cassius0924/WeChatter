import json
import unittest
from wechatter.commands._commands import today_in_history


class TestTodayInHistoryCommand(unittest.TestCase):

    def setUp(self):
        with open('tests/commands/test_today_in_history/today_in_history_response.json') as f:
            self.tih_response = json.load(f)
            self.tih_list = self.tih_response['data']

    def test_extract_today_in_history_data_success(self):
        result = today_in_history._extract_today_in_history_data(self.tih_response)
        self.assertListEqual(result, self.tih_list)

    def test_extract_today_in_history_data_failure(self):
        with self.assertRaises(RuntimeError):
            today_in_history._extract_today_in_history_data({})

    def test_generate_today_in_history_message_success(self):
        result = today_in_history._generate_today_in_history_message(self.tih_list)
        true_result = "1. 🗓️ 1421 年\n    🌎 明朝正式迁都北京\n    🌪️ 明朝（1368－1644年）是中国历史上最后一个由汉族建立的中原王朝。历经十二世、十六位皇帝，国祚二百七十六年。1368年明太祖朱元璋在南京应天府称帝，国号大明。\n2. 🗓️ 1895 年\n    🌎 二·二八事件受难者陈澄波出生\n    🌪️ 陈澄波（1895-1947），生于嘉义，一九一三年考进台湾总督府国语学校师范科（今台北师范学校），在校期间获石川钦—郎指导对西洋\n3. 🗓️ 1901 年\n    🌎 立陶宛小提琴家亚莎·海菲兹出生\n    🌪️ 亚莎·海菲兹（Jascha·Heifetz，1901－1987），二十世纪杰出的美籍立陶宛小提琴家；1901年出生于当时属于俄罗斯的立陶宛首都维尔\n4. 🗓️ 1919 年\n    🌎 葡萄牙宣布成立君主国\n    🌪️ 葡萄牙，全称葡萄牙共和国（英语：The Portuguese Republic，葡萄牙语：República Portuguesa），是一个位于欧洲西南部的共和制\n5. 🗓️ 1920 年\n    🌎 北洋政府教育部发布中国第一套法定的新式标点符号\n    🌪️ 1920年4月，胡适、钱玄同、刘复、朱希祖、周作人、马裕藻六位教授首次提出《请颁行新式标点符号方案》，方案次年被批准，成为语言文化发展史上的重要里程碑。\n6. 🗓️ 1925 年\n    🌎 军事理论家米哈伊尔·伏龙芝逝世\n    🌪️ 苏联红军统帅，军事理论家。开创了将革命激情和现代化武装相结合的道路。生于谢米列奇耶州皮什佩克城一医士家庭。1917年十月革\n7. 🗓️ 1937 年\n    🌎 东北军将领王以哲逝世\n    🌪️ 王以哲（1896—1937）字鼎芳，汉族，原名王海山，东北军重要将领之一。国民革命军陆军中将。1896年出生于宾州厅东偏脸子屯（今\n8. 🗓️ 1943 年\n    🌎 斯大林格勒会战结束\n    🌪️ 斯大林格勒战役（俄语：Сталинградская битва，德语：Schlacht von Stalingrad）是第二次世界大战\n9. 🗓️ 1948 年\n    🌎 台湾漫画家蔡志忠出生\n    🌪️ 蔡志忠，生于1948年，台湾彰化人，著名漫画家。15岁起便开始成为职业漫画家，1971年底进入光启社任美术设计，并自学卡通绘制技\n10. 🗓️ 1960 年\n    🌎 香港著名演员惠英红出生\n    🌪️ 惠英红，1960年2月2日生于香港，祖籍山东，满洲正黄旗人，香港著名女演员。香港电影金像奖影后。打女代表人物之一。1977年凭张\n11. 🗓️ 1970 年\n    🌎 英国哲学家伯特兰·罗素逝世\n    🌪️ 伯特兰·罗素（Bertrand Russell，1872—1970）是二十世纪英国哲学家、数学家、逻辑学家、历史学家，无神论或者不可知论者，也是\n12. 🗓️ 1977 年\n    🌎 世界杯主题曲《Wakawaka》演唱者夏奇拉出生\n    🌪️ 夏奇拉（Shakira），1977年2月2日出生于哥伦比亚巴兰基亚，哥伦比亚歌手。1991年，夏奇拉发行了个人首张专辑《Magia》。1998年\n13. 🗓️ 1990 年\n    🌎 南非总统德克勒克宣布废除南非种族隔离制度\n    🌪️ 南非政治家，南非共和国白人总统（1936-），他结束了南非种族隔离制度。并议定了向多数派执政的过渡，因此和纳尔逊·曼德拉 一起"
        self.assertIn(true_result, result)

    def test_generate_today_in_history_message_empty_list(self):
        result = today_in_history._generate_today_in_history_message([])
        self.assertEqual(result, "暂无历史上的今天")
