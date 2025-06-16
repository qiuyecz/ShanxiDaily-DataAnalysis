import pandas as pd
from pyecharts.charts import Bar
from pyecharts import options as opts
import glob
import os


# 统计不同长度区间的新闻数量
def count_news_by_length(directory):
    length_ranges = ['0 - 100字', '101 - 200字', '201 - 300字', '301 - 400字', '400字以上']
    counts = [0, 0, 0, 0, 0]

    # 遍历所有符合条件的CSV文件
    for file_path in glob.glob(os.path.join(directory, '山西日报*.csv')):
        df = pd.read_csv(file_path, encoding='utf-8')
        if 'info' in df.columns:
            for title in df['info'].dropna():  # 去除空值
                title_length = len(title)
                if title_length <= 100:
                    counts[0] += 1
                elif title_length <= 200:
                    counts[1] += 1
                elif title_length <= 300:
                    counts[2] += 1
                elif title_length <= 400:
                    counts[3] += 1
                else:
                    counts[4] += 1

    return length_ranges, counts


# 生成柱状图
def generate_bar_chart(length_ranges, counts):
    bar = (
        Bar()
        .add_xaxis(length_ranges)
        .add_yaxis("新闻数量", counts)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="山西日报新闻信息长度分布"),
            xaxis_opts=opts.AxisOpts(name="长度区间"),
            yaxis_opts=opts.AxisOpts(name="新闻数量")
        )
    )
    bar.render("news_length_distribution.html")


# 主函数
def main():
    directory = r'..\数据存储'
    length_ranges, counts = count_news_by_length(directory)
    generate_bar_chart(length_ranges, counts)


if __name__ == "__main__":
    main()