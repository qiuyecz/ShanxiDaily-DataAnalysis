import pandas as pd
import jieba
from pyecharts.charts import WordCloud
from pyecharts import options as opts
import glob

# 1. 读取多个CSV文件并合并
csv_pattern = "..\\数据存储\\山西日报*.csv"  # 使用通配符匹配多个文件
csv_files = glob.glob(csv_pattern)
all_data = []

for file in csv_files:
    df = pd.read_csv(file)
    data = df.to_dict("records")  # 转换为字典列表
    all_data.extend(data)  # 将当前文件的数据添加到总数据列表中

# 2. 提取所有新闻内容并合并
all_text = " ".join([item["info"] + " " + item["title"] for item in all_data])

# 3. 使用jieba进行中文分词
words = jieba.lcut(all_text)

# 4. 过滤停用词
stopwords = set(["的", "了", "在", "是", "我"
                , "有", "和", "就", "日前", "两个"
                ,"有限公司", "设立","记者","工作"
                ,"学习","本报讯","推进","第一"
                ,"晚报","我省","启动","活动"
                ,"根据"])  # 自定义停用词
filtered_words = [word for word in words if len(word) > 1 and word not in stopwords]

# 5. 统计词频
word_counts = {}
for word in filtered_words:
    word_counts[word] = word_counts.get(word, 0) + 1

# 6. 生成词云图
wordcloud = (
    WordCloud()
    .add(series_name="新闻热词", data_pair=list(word_counts.items()), word_size_range=[20, 100])
    .set_global_opts(
        title_opts=opts.TitleOpts(title="新闻热词词云图"),
        tooltip_opts=opts.TooltipOpts(is_show=True),
    )
)

# 7. 保存为HTML文件
wordcloud.render("news_wordcloud.html")