import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

def get_total_count_by_hour_df(hour_df):
    hour_count_df = hour_df.groupby(by="hours").agg({"count_cr": ["sum"]})
    return hour_count_df

def count_by_day_df(day_df):
    day_df['category_days'] = day_df['one_of_week'].apply(lambda x: 'Weekend' if x in ['Saturday', 'Sunday'] else 'Weekday')
    day_df_count = day_df.groupby('category_days').agg({'count_cr': 'sum'}).reset_index()
    return day_df_count

# Membaca DataFrame dari file CSV
day_df = pd.read_csv("day_clean.csv")
hour_df = pd.read_csv("hour_clean.csv")

# Mengkonversi kolom tanggal menjadi datetime
day_df["dteday"] = pd.to_datetime(day_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

# Menghitung total penyewaan berdasarkan jam
hour_count_df = get_total_count_by_hour_df(hour_df)
# Menghitung total penyewaan berdasarkan jenis hari
day_df_count = count_by_day_df(day_df)

# Melengkapi Dashboard dengan Visualisasi Data
st.header('Bike Sharing :sparkles:')

# Pertanyaan 1: Penyewaan berdasarkan jam
st.subheader("Pada jam berapa yang paling banyak dan paling sedikit disewa?")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

# Barplot untuk jam penyewa terbanyak
sns.barplot(x="hours", y=("count_cr", "sum"), data=hour_count_df.sort_values(by=("count_cr", "sum"), ascending=False).head(5), palette=["#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3"], ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Hours (PM)", fontsize=30)
ax[0].set_title("Jam dengan banyak penyewa sepeda", loc="center", fontsize=30)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

# Barplot untuk jam penyewa paling sedikit
sns.barplot(x="hours", y=("count_cr", "sum"), data=hour_count_df.sort_values(by=("count_cr", "sum")).head(5), palette=["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3","#90CAF9"], ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Hours (AM)",  fontsize=30)
ax[1].set_title("Jam dengan sedikit penyewa sepeda", loc="center", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

# Pertanyaan 2: Perbandingan penyewaan berdasarkan jenis hari
st.subheader("Perbandingan Penyewaan: Hari Kerja vs Akhir Pekan")
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(x="category_days", y="count_cr", data=day_df_count, palette=['#1E90FF', '#FF6347'], ax=ax2)

# Mengatur label dan judul
ax2.set_title("Perbandingan Penyewaan: Hari Kerja vs Akhir Pekan", fontsize=16)
ax2.set_xlabel("Jenis Hari", fontsize=12)
ax2.set_ylabel("Jumlah Penyewaan Sepeda", fontsize=12)

st.pyplot(fig2)
