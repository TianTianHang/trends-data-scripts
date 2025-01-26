import csv
import os
import random
from time import sleep
import pandas as pd
from trendspy import Trends

def get_trends_data(keyword, start_date, end_date):
    try:
        data = tr.interest_by_region(
            f'"{keyword}"', 
            timeframe=f'{start_date} {end_date}',
            inc_low_vol=True
        )
        return data
    
    except Exception as e:
        print(f"获取趋势数据时出错 - 短语: {keyword}, 时间范围: {start_date} 到 {end_date}, 错误: {e}")
        return None
def get_trends_data_over_time(keyword, start_date, end_date,geo):
    try:
        data = tr.interest_over_time(
            f'"{keyword}"', 
            timeframe=f'{start_date} {end_date}',
            geo=geo
        )
        return data
    
    except Exception as e:
        print(f"获取趋势数据时出错 - 短语: {keyword}, 时间范围: {start_date} 到 {end_date}, 错误: {e}")
        return None

def process_phrases(save_path):
    # 读取拉丁短语文件
    with open('data/latin_phrases.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file,delimiter=" ")
        phrases = [row[0] for row in reader]

    # 处理每个短语
    for phrase in phrases:
        # 创建目录
        dir_path = f'data/{save_path}/{phrase}'
        os.makedirs(dir_path, exist_ok=True)

        # 按年获取Google Trends数据
        for year in range(2004, 2024):
            start_date = f'{year}-01-01'
            end_date = f'{year+1}-01-01'
            file_path = f'{dir_path}/{phrase}-{start_date}-{end_date}.csv'
            if os.path.exists(file_path):
                continue
            # 获取数据
            data = get_trends_data(phrase, start_date, end_date)
            sleep(random.randrange(1,5))
            # 保存数据到CSV
            data.to_csv(file_path, index=False)


def process_phrases_with_country(save_path):
    # 读取拉丁短语文件
    with open('data/latin_phrases.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file,delimiter=" ")
        phrases = [row[0] for row in reader]
    # 读取国家文件
    with open('data/countries.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file,delimiter=",")
        countries = [[row[0],row[3],row[15]] for row in reader]
    
    countries=[c for c in countries if c[2]=='Europe']
    for country in countries:
        # 处理每个短语
        
        for phrase in phrases:
            # 创建目录
            dir_path = f'data/{save_path}/{country[0]}'
            os.makedirs(dir_path, exist_ok=True)
            start_date = f'2004-01-01'
            end_date = f'2025-01-01'
            file_path = f'{dir_path}/{phrase}-{start_date}-{end_date}.csv'
            if os.path.exists(file_path):
                continue
            # 获取数据
            data = get_trends_data_over_time(phrase, start_date, end_date,country[1])
            while not type(data)==pd.DataFrame or data.empty:
                t=random.randrange(20,20*2)
                print(f"等待{t}s")
                sleep(t)
                data = get_trends_data_over_time(phrase, start_date, end_date,country[1])
                continue
            # 保存数据到CSV
            data.to_csv(file_path, index=True)
            sleep(random.randrange(20,20*2))
        process_all_data(dir_path)
        
def process_all_data(input_dir):
     # 用于存储所有CSV文件数据的列表
    all_data = []

    # 遍历目录中的所有文件
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.csv'):
                # 构造文件路径
                file_path = os.path.join(root, file)
                
                # 提取文件名中的keyword、start_date、end_date
                file_name = os.path.splitext(file)[0]  # 去掉文件扩展名
                parts = file_name.split('-')
                if len(parts) >= 3:
                    keyword = parts[0]  # 关键词部分
                    start_date = '-'.join(parts[1:4]) # 开始日期
                    end_date ='-'.join(parts[4:7]) # 结束日期
                    timeframe = f'{start_date} {end_date}'  # 时间范围
                    
                    # 读取CSV文件到DataFrame
                    df = pd.read_csv(file_path)
                    if not all_data:
                        all_data.append(df["time [UTC]"])
                    all_data.append(df[keyword])

    # 合并所有DataFrame
    if all_data:
        output_dir=f'{input_dir}/all'
        os.makedirs(output_dir, exist_ok=True)
        output_file=f'{output_dir}/all.csv'
        combined_df = pd.concat(all_data, axis=1)

        # 保存合并后的DataFrame为CSV
        combined_df.to_csv(output_file, index=False,na_rep='NA')
        print(f"Data merged and saved to {output_file}")
    else:
        print("No valid data found to merge.")
from env import proxies
tr = Trends(request_delay=10.0, proxy=proxies)

process_phrases('over_time/original_data')
