import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_excel("WEOApr2024.xlsx")
unemp_df = df.loc[df["WEO Subject Code"] == "LUR"]
unemp_df_2022 = unemp_df[["Country", 2022, 2023]]
unemp_df_2022.reset_index(inplace=True, drop=True)
unemp_df_2022 = unemp_df_2022.dropna()
unemp_df_2022[2022] = pd.to_numeric(unemp_df_2022[2022])
unemp_df_2022[2023] = pd.to_numeric(unemp_df_2022[2023])

# 2023 - 2022 차이값
unemp_df_2022["diff"] = unemp_df_2022[2023] - unemp_df_2022[2022]

# 2022년 실업률 오름차순 정렬 후 80개국
sorted_df = unemp_df_2022.sort_values(2022).iloc[:80]

plt.figure(figsize=(15, 8))

# 2022년 실업률 (막대)
plt.bar(sorted_df.iloc[:, 0], sorted_df.iloc[:, 1], label="2022 LUR")
plt.title("Unemployment Rate of Countries (LUR, 2022)")
plt.xticks(rotation=270)

# 관심 국가 표시
korea_df = sorted_df.loc[sorted_df["Country"] == "Korea"]
plt.bar(korea_df["Country"], korea_df[2022], label="Korea")

japan_df = sorted_df.loc[sorted_df["Country"] == "Japan"]
plt.bar(japan_df["Country"], japan_df[2022], label="Japan")

china_df = sorted_df.loc[sorted_df["Country"] == "China"]
plt.bar(china_df["Country"], china_df[2022], label="China")

us_df = sorted_df.loc[sorted_df["Country"] == "United States"]
plt.bar(us_df["Country"], us_df[2022], label="United States")

# 2023 - 2022 차이값 (같은 그래프에 선으로 표시)
plt.plot(sorted_df["Country"], sorted_df["diff"], color="green", marker="o", label="2023 - 2022")

plt.legend()
plt.tight_layout()
plt.show()
