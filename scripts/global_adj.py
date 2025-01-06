import geopandas as gpd
from matplotlib import pyplot as plt
import networkx as nx
import pandas as pd
# 加载自然地球数据集中的国家边界数据
world = gpd.read_file("data/geo/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp")
loc=pd.read_csv("./data/geo_country_with_location.csv")
# 过滤掉 ISO_A2 为 -99 的国家
world = world[world.ISO_A2 != '-99'].reset_index(drop=True)

# 创建图对象
G = nx.Graph()
pos={}
# 计算邻接关系
for i, country1 in world.iterrows():
    c=loc[loc.geoCode==country1.ISO_A2]
    if not c.empty:
        pos[i]=(c.lon.values[0],c.lat.values[0])
    else:
        pos[i]=(0,0)
    G.add_node(i)
    for j, country2 in world.iterrows():
        if i != j and country1.geometry.touches(country2.geometry):
            G.add_edge(i,j)
            G.add_edge(j,i)

# 绘制图形
plt.figure(figsize=(100, 100))
nx.draw_networkx(G,pos=pos)
plt.title('Graph Visualization using NetworkX')
plt.show()