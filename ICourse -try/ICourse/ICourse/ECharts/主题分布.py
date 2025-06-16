import pandas as pd
from collections import defaultdict
from pyecharts import options as opts
from pyecharts.charts import Pie
import glob
import os


# 读取CSV文件并统计新闻主题分布
def read_csv_and_count_themes(directory):
    theme_counts = defaultdict(int)

    # 使用glob模块查找所有符合条件的CSV文件
    for file_path in glob.glob(os.path.join(directory, '山西日报*.csv')):
        df = pd.read_csv(file_path, encoding='utf-8')
        if 'title' in df.columns:
            for _, row in df.iterrows():
                title = row['title']
                theme = classify_theme(title)
                if theme:
                    theme_counts[theme] += 1

    return theme_counts


# 分类函数，根据标题判断主题
def classify_theme(title):
    # 分类逻辑
    keywords = {
        '政治': ['省政府', '政策', '表彰', '会议', '省委', '书记', '常委', '巡视', '动员会', '部署会', '纪委', '监委',
                 '通报', '立法', '中央指示', '人大'],
        '经济': ['发展', '企业', '经济', '质量奖', '投资', '融资', '民营经济', '进出口', '消费', '市场', '商务厅',
                 '产值', '增长', '项目', '招商', '就业', '产值', '经济形势', '经济指标'],
        '文化': ['音乐会', '节日', '文化', '活动', '展览', '艺术', '剧院', '非遗', '文物', '博物馆', '文化节', '文艺',
                 '书画展', '文化传承', '文化交流', '文化创新', '文化创意'],
        '社会': ['未成年人', '安全', '高考', '托育', '汛期', '民生', '教育', '医疗', '社保', '就业', '住房', '环保',
                 '污染', '生态', '抗旱救灾', '社区', '养老', '信访', '维权', '公益', '救助', '灾害', '扶贫',
                 '乡村振兴'],
        '体育': ['体育赛事', '运动会', '马拉松', '足球赛', '篮球赛', '体育健身', '青少年体育', '体育消费季', '体育公园',
                 '体育场馆'],
        '科技': ['创新', '科技', '院士工作站', '科研', '技术', '研发', '智能', '信息化', '数字化', '科技创新',
                 '科技成果', '科技活动', '科技论坛'],
        '旅游': ['旅游', '景区', '文旅', '游客', '旅行', '端午主题旅游线路', '文旅活动', '文旅融合', '旅游公路',
                 '乡村游', '红色旅游', '旅游线路', '旅游节'],
        '生态': ['生态环境保护', '生态', '环保督察', '绿色', '自然保护区', '生态修复', '绿化', '治沙', '环保行动',
                 '生态建设', '生物多样性'],
        '法律': ['法律', '法规', '司法', '检察院', '法院', '律师', '普法', '法治', '合规', '维权', '法律援助',
                 '法律宣传'],
        '交通': ['交通', '公路', '铁路', '机场', '运输', '物流', '高速公路', '交通管制', '交通项目', '交通建设',
                 '公共交通', '交通规划'],
        '农业': ['农业', '农村', '农民', '农产品', '乡村振兴', '农田', '农业科技', '农业机械', '农业项目', '农村改革',
                 '三农'],
        '教育': ['学校', '学生', '教师', '教育', '教学', '招生', '考试', '校园', '教育政策', '教育改革', '教育项目',
                 '课外活动'],
        '健康': ['医院', '医生', '健康', '医疗', '防疫', '疫苗', '中药', '体检', '健康管理', '养生', '疾病预防'],
        '金融': ['银行', '金融', '贷款', '融资', '投资', '股市', '债券', '基金', '保险', '理财', '金融科技',
                 '金融服务'],
        '能源': ['煤炭', '电力', '新能源', '能源', '风电', '光伏', '电网', '能源项目', '能源转型', '节能减排',
                 '绿色能源'],
        '建筑': ['建筑', '房地产', '城市规划', '基础设施建设', '桥梁', '道路', '公共设施', '建筑项目', '建筑设计',
                 '施工']
    }

    for theme, word_list in keywords.items():
        for word in word_list:
            if word in title:
                return theme
    return '其他'  # 无法分类的主题归为“其他”


# 生成饼图
def generate_pie_chart(theme_counts):
    themes = list(theme_counts.keys())
    counts = list(theme_counts.values())

    pie = (
        Pie()
        .add("", [list(z) for z in zip(themes, counts)])
        .set_global_opts(title_opts=opts.TitleOpts(title="山西日报新闻主题分布"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)"))
    )
    pie.render("news_themes_pie.html")


# 主函数
def main():
    directory = r'..\数据存储'
    theme_counts = read_csv_and_count_themes(directory)
    generate_pie_chart(theme_counts)


if __name__ == "__main__":
    main()