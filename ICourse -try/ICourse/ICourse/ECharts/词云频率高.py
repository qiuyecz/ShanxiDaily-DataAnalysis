import pandas as pd
import jieba
from pyecharts.charts import WordCloud
from pyecharts import options as opts
import glob

# 读取多个CSV文件并合并
csv_pattern = "..\\数据存储\\山西日报*.csv"
csv_files = glob.glob(csv_pattern)
all_data = []

for file in csv_files:
    df = pd.read_csv(file)
    data = df.to_dict("records")
    all_data.extend(data)

# 提取所有新闻内容并合并
all_text = " ".join([item["info"] + " " + item["title"] for item in all_data])

# 使用jieba进行中文分词
words = jieba.lcut(all_text)

# 过滤停用词
stopwords = set(["的", "了", "在", "是", "我"
                , "有", "和", "就", "日前", "两个"
                ,"有限公司", "设立","记者","工作"
                ,"学习","本报讯","推进","第一"
                ,"晚报","我省","启动","活动"
                ,"根据"])
filtered_words = [word for word in words if len(word) > 1 and word not in stopwords]

# 统计词频
word_counts = {}
for word in filtered_words:
    word_counts[word] = word_counts.get(word, 0) + 1

# 过滤低频词
min_frequency = 5  # 设置最小频率阈值
filtered_word_counts = {k: v for k, v in word_counts.items() if v >= min_frequency}

# 按词频排序并取前N个词
top_n = 100  # 设置最多显示多少词语
sorted_words = sorted(filtered_word_counts.items(), key=lambda x: x[1], reverse=True)
final_word_counts = dict(sorted_words[:top_n])

# 生成词云图
wordcloud = (
    WordCloud()
    .add(series_name="新闻热词",
         data_pair=list(final_word_counts.items()),
         word_size_range=[20, 100])
    .set_global_opts(
        title_opts=opts.TitleOpts(title=f"新闻热词词云图（出现频率≥{min_frequency}次）"),
        tooltip_opts=opts.TooltipOpts(is_show=True),
    )
)

# 保存为HTML文件
wordcloud.render("news_wordcloud.html")

print(f"原始词语数量: {len(word_counts)}")
print(f"过滤后词语数量: {len(final_word_counts)}")