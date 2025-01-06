import pandas as pd
import numpy as np
from statsmodels.tsa.filters.hp_filter import hpfilter
from scipy.stats import zscore
from sklearn.decomposition import PCA

class DataPreprocessor:
    def __init__(self, data:pd.DataFrame, start_year=2004, start_month=1):
        self.data = data
        self.start_year = start_year
        self.start_month = start_month
    def adjust_breakpoints(self, h=12):
        """Adjust for historical breakpoints in Google Trends data"""
        breakpoints = {
            '2011': (2011 - self.start_year) * h - self.start_month + 1,
            '2016': (2016 - self.start_year) * h - self.start_month + 1,
            '2022': (2022 - self.start_year) * h - self.start_month + 1
        }
        
        for col in self.data.columns[1:]:
            for year, point in breakpoints.items():
                pre_mean = self.data.iloc[point-h:point, :][col].mean()
                post_mean = self.data.iloc[point:point+h, :][col].mean()
                ratio = pre_mean / post_mean
                self.data.iloc[point:, :][col] *= ratio
                
        return self
    
    def log_transform(self):
        # 定义一个函数
        def func(x):
            if not type(x) is str:
                return np.log(x) if x > 0 else np.log(1)
            else:
                return x
        """Apply log transformation to data"""
        self.data = self.data.applymap(func)
        return self
    
    def hp_filter(self, lambda_=1600):
        """Apply Hodrick-Prescott filter"""
        for col in self.data.columns[1:]:
            cycle, trend = hpfilter(self.data[col], lamb=lambda_)
            self.data[col] = trend
        return self
    
    def extract_common_trend(self):
        """Extract common trend using PCA"""
        pca = PCA(n_components=1)
        common_trend = pca.fit_transform(self.data.iloc[...,1:])
        self.data.iloc[...,1:] = self.data.iloc[...,1:].sub(common_trend, axis=0)
        return self
    
    def calculate_differences(self, h=12):
        """Calculate monthly differences"""
        self.data.iloc[...,1:] = self.data.iloc[...,1:].diff(h)
        self.data.iloc[:h, 1:] = np.nan
        return self
    
    def save_data(self, output_path):
        """Save processed data to CSV"""
        self.data.to_csv(output_path, index=False)
        
if __name__ == "__main__":
    # Example usage
    df = pd.read_csv('data\over_time\original_data\Italy\\all\\all.csv')
    preprocessor = DataPreprocessor(df)
    (preprocessor.adjust_breakpoints()
                 .log_transform()
                 .hp_filter()
                 .extract_common_trend()
                 .calculate_differences()
                 .save_data('data/processed_data.csv'))
