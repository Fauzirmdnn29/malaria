import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Fungsi untuk membersihkan data
def clean_malaria_data(df, years):
    # Menyusun header dan membersihkan data
    df_cleaned = df.iloc[2:, :4]
    df_cleaned.columns = ["Province", str(years[0]), str(years[1]), str(years[2])]
    df_cleaned = df_cleaned.reset_index(drop=True)
    return df_cleaned

# Membaca data
file_2016_2018 = "malaria_2016_2018.xlsx"
file_2019_2021 = "malaria_2019-2021.xlsx"

data_2016_2018 = pd.ExcelFile(file_2016_2018)
data_2019_2021 = pd.ExcelFile(file_2019_2021)

df_2016_2018 = data_2016_2018.parse("Sheet1")
df_2019_2021 = data_2019_2021.parse("Sheet1")

# Membersihkan data
df_2016_2018_cleaned = clean_malaria_data(df_2016_2018, [2016, 2017, 2018])
df_2019_2021_cleaned = clean_malaria_data(df_2019_2021, [2019, 2020, 2021])

# Menggabungkan data
malaria_data = pd.merge(
    df_2016_2018_cleaned, df_2019_2021_cleaned, on="Province", how="outer"
)
year_columns = malaria_data.columns[1:]
malaria_data[year_columns] = malaria_data[year_columns].apply(pd.to_numeric, errors="coerce")

# Streamlit Dashboard
st.title("Malaria Dashboard (2016-2021)")

# Total kejadian malaria per tahun
st.subheader("Total Malaria Cases per Year")
total_cases = malaria_data[year_columns].sum()
st.write(total_cases)

# Visualisasi tren malaria
st.subheader("Malaria Trend Over the Years")
fig, ax = plt.subplots(figsize=(10, 6))
for index, row in malaria_data.iterrows():
    ax.plot(year_columns, row[year_columns], label=row["Province"], alpha=0.5)
ax.set_xlabel("Year")
ax.set_ylabel("Malaria Cases (per 1000 people)")
ax.set_title("Trends of Malaria by Province")
ax.legend(loc="upper right", fontsize="small", bbox_to_anchor=(1.3, 1))
st.pyplot(fig)

# Distribusi malaria per provinsi
st.subheader("Malaria Cases by Province (2016-2021)")
malaria_data["Total"] = malaria_data[year_columns].sum(axis=1)
sorted_data = malaria_data.sort_values(by="Total", ascending=False)

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(sorted_data["Province"], sorted_data["Total"], color="skyblue")
ax.set_xlabel("Total Malaria Cases (per 1000 people)")
ax.set_title("Malaria Distribution by Province")
st.pyplot(fig)


# Section: Kenaikan Kasus Malaria Per Tahun
st.header("Kenaikan Kasus Malaria Per Tahun")

# Menghitung kenaikan kasus per tahun
malaria_data["Change_2017"] = malaria_data["2017"] - malaria_data["2016"]
malaria_data["Change_2018"] = malaria_data["2018"] - malaria_data["2017"]
malaria_data["Change_2019"] = malaria_data["2019"] - malaria_data["2018"]
malaria_data["Change_2020"] = malaria_data["2020"] - malaria_data["2019"]
malaria_data["Change_2021"] = malaria_data["2021"] - malaria_data["2020"]

# Menyusun data kenaikan per tahun
change_data = malaria_data[["Province", "Change_2017", "Change_2018", "Change_2019", "Change_2020", "Change_2021"]]
change_data = change_data.set_index("Province")

# Membuat heatmap untuk visualisasi kenaikan per tahun
st.subheader("Visualisasi Kenaikan Kasus Malaria Per Tahun")
fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(
    change_data.transpose(),
    annot=True,
    fmt=".0f",
    cmap="YlGnBu",
    cbar_kws={"label": "Kenaikan Kasus"},
    linewidths=0.5,
    ax=ax,
)
ax.set_title("Kenaikan Kasus Malaria Per Tahun Berdasarkan Provinsi")
ax.set_xlabel("Provinsi")
ax.set_ylabel("Tahun")
st.pyplot(fig)

# Menampilkan provinsi dengan kenaikan kasus tertinggi
st.subheader("Provinsi dengan Kenaikan Kasus Tertinggi")
total_changes = change_data.sum(axis=1).sort_values(ascending=False)
st.write(total_changes.head(10))


