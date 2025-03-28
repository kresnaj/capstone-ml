import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Set style seaborn
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

# Baca dataset
print("Membaca dataset...")
df = pd.read_csv("dataset_pengaduan.csv")

# Tampilkan informasi awal
print("Jumlah data:", len(df))
print("Kolom:", df.columns.tolist())
print("Kategori unik:", df['kategori'].unique())

# Ambil sampel untuk analisis (untuk kecepatan)
sample_size = 1000
df_sample = df.sample(sample_size, random_state=42).copy()
print(f"Menggunakan sampel {sample_size} data untuk analisis")

# Buat fitur numerik dari data teks
print("Membuat fitur numerik dari data teks...")
df_sample['panjang_teks'] = df_sample['pengaduan'].apply(len)
df_sample['jumlah_kata'] = df_sample['pengaduan'].apply(lambda x: len(x.split()))

# 1. Visualisasi jumlah pengaduan per kategori
print("Membuat visualisasi distribusi kategori...")
plt.figure(figsize=(10, 6))
ax = sns.countplot(x='kategori', data=df_sample, hue='kategori', palette='viridis', legend=False)
plt.title('Distribusi Kategori Pengaduan', fontsize=16)
plt.xlabel('Kategori', fontsize=14)
plt.ylabel('Jumlah', fontsize=14)
plt.xticks(rotation=45)

# Tambahkan label jumlah pada setiap bar
for i, p in enumerate(ax.patches):
    ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height() + 5),
                ha='center', fontsize=10)

plt.tight_layout()
plt.savefig('distribusi_kategori.png')
plt.close()
print("Visualisasi 1 selesai!")

# 2. Scatterplot penyebaran data berdasarkan panjang teks dan jumlah pengaduan
print("Membuat scatterplot penyebaran data...")
plt.figure(figsize=(12, 8))
sns.scatterplot(
    x='panjang_teks', 
    y='jumlah_pengaduan',
    hue='kategori',
    style='sentimen',
    s=100,  # Ukuran titik
    alpha=0.7,
    palette='viridis',
    data=df_sample
)
plt.title('Penyebaran Data Pengaduan Berdasarkan Kategori', fontsize=16)
plt.xlabel('Panjang Teks (Jumlah Karakter)', fontsize=14)
plt.ylabel('Jumlah Pengaduan', fontsize=14)
plt.legend(title='Kategori', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('scatter_pengaduan_kategori.png')
plt.close()
print("Visualisasi 2 selesai!")

# 3. Scatterplot penyebaran data berdasarkan jumlah kata dan jumlah pengaduan
print("Membuat scatterplot berdasarkan jumlah kata...")
plt.figure(figsize=(12, 8))
sns.scatterplot(
    x='jumlah_kata', 
    y='jumlah_pengaduan',
    hue='kategori',
    style='sentimen',
    s=100,  # Ukuran titik
    alpha=0.7,
    palette='viridis',
    data=df_sample
)
plt.title('Penyebaran Data Pengaduan Berdasarkan Jumlah Kata', fontsize=16)
plt.xlabel('Jumlah Kata', fontsize=14)
plt.ylabel('Jumlah Pengaduan', fontsize=14)
plt.legend(title='Kategori', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('scatter_jumlah_kata_kategori.png')
plt.close()
print("Visualisasi 3 selesai!")

# 4. Visualisasi penyebaran data dengan FacetGrid berdasarkan kategori
print("Membuat FacetGrid untuk visualisasi berdasarkan kategori...")
g = sns.FacetGrid(df_sample, col='kategori', col_wrap=3, height=4, aspect=1.2)
g.map(sns.scatterplot, 'panjang_teks', 'jumlah_pengaduan', alpha=0.7)
g.fig.suptitle('Penyebaran Data Berdasarkan Kategori', fontsize=16, y=1.02)
plt.tight_layout()
plt.savefig('facet_kategori.png')
plt.close()
print("Visualisasi 4 selesai!")

# 5. Visualisasi distribusi sentimen per kategori
print("Membuat visualisasi distribusi sentimen per kategori...")
plt.figure(figsize=(12, 8))
sentiment_counts = df_sample.groupby(['kategori', 'sentimen']).size().unstack()
sentiment_counts.plot(kind='bar', stacked=True, colormap='viridis')
plt.title('Distribusi Sentimen per Kategori', fontsize=16)
plt.xlabel('Kategori', fontsize=14)
plt.ylabel('Jumlah', fontsize=14)
plt.legend(title='Sentimen')
plt.tight_layout()
plt.savefig('distribusi_sentimen_kategori.png')
plt.close()
print("Visualisasi 5 selesai!")

print("Semua visualisasi selesai! Gambar telah disimpan.") 