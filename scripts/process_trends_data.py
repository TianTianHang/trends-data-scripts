import csv
import os
import pandas as pd
import numpy as np

def process_missing_data(input_file, output_file, keyword):
    # 读取CSV文件，处理空文件情况
    try:
        df = pd.read_csv(input_file)
        if df.empty:
            df = pd.DataFrame(columns=['geoName', 'geoCode', keyword])
    except pd.errors.EmptyDataError:
        df = pd.DataFrame(columns=['geoName', 'geoCode', keyword])
    
    # 读取国家名称和代码映射
    geo_mapping = pd.read_csv("data/geo_country_with_location.csv")
    geo_dict = dict(zip(geo_mapping['geoCode'], geo_mapping['geoName']))
    
    
    # 创建包含所有国家的DataFrame
    all_countries = pd.DataFrame({
        'geoName': list(geo_dict.values()),
        'geoCode': list(geo_dict.keys())
    })
    
    # 合并原始数据和所有国家数据
    merged_df = pd.merge(all_countries, df, on=['geoName', 'geoCode'], how='left')
    
    # 使用映射数据填充缺失值
    merged_df[keyword] = merged_df[keyword].fillna(-1)
    
    # 保存处理后的数据
    merged_df.to_csv(output_file, index=False)

def process_phrases(input_path,save_path):
    # 读取拉丁短语文件
    with open('data/latin_phrases.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file,delimiter=" ")
        phrases = [row[0] for row in reader]

    # 处理每个短语
    for phrase in phrases:
        # 创建目录
        dir_path = f'data/{save_path}/{phrase}'
        in_dir_path= f'data/{input_path}/{phrase}'
        os.makedirs(dir_path, exist_ok=True)

        # 按年获取Google Trends数据
        for year in range(2004, 2024):
            start_date = f'{year}-01-01'
            end_date = f'{year+1}-01-01'
            input_file = f'{in_dir_path}/{phrase}-{start_date}-{end_date}.csv'
            output_file = f'{dir_path}/{phrase}-{start_date}-{end_date}.csv'
            if os.path.exists(output_file):
                continue
            process_missing_data(input_file, output_file, phrase)

process_phrases('yearly/original data', 'yearly/process data')
