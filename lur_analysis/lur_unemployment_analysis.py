import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_excel('WEOApr2024.xlsx')
unemp_df = df.loc[df['WEO Subject Code'] == 'LUR']
unemp_df = unemp_df[['Country', 2022, 2023]]
unemp_df.reset_index(inplace=True, drop=True)
unemp_df = unemp_df.dropna()
unemp_df[2022] = pd.to_numeric(unemp_df[2022])
unemp_df[2023] = pd.to_numeric(unemp_df[2023])

# 2023 - 2022 차이값
unemp_df['Diff'] = unemp_df[2023] - unemp_df[2022]

# 조건: 2022년 실업률 오름차순 80개국
sorted_df = unemp_df.sort_values(2022).iloc[:80]

plt.figure(figsize=(15, 8))

# 사진 기준: 파란 Diff, 주황 2023
plt.bar(sorted_df['Country'], sorted_df['Diff'], label='Diff')
plt.bar(sorted_df['Country'], sorted_df[2023], label='2023')

plt.title('Unemployment Rate Difference of 2022 and 2023 year')
plt.xticks(rotation=270)

# 조건: 관심 국가 3~4개 표시
korea_df = sorted_df.loc[sorted_df['Country'] == 'Korea']
plt.plot(korea_df['Country'], korea_df[2023], 'o', label='Korea')

japan_df = sorted_df.loc[sorted_df['Country'] == 'Japan']
plt.plot(japan_df['Country'], japan_df[2023], 'o', label='Japan')

china_df = sorted_df.loc[sorted_df['Country'] == 'China']
plt.plot(china_df['Country'], china_df[2023], 'o', label='China')

us_df = sorted_df.loc[sorted_df['Country'] == 'United States']
plt.plot(us_df['Country'], us_df[2023], 'o', label='United States')

plt.legend()
plt.show()
