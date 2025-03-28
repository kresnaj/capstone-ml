import pandas as pd
import numpy as np
import random

# Tentukan jumlah data dan rentang tanggal
start_date = "1980-01-01"
periods = 20000
date_range = pd.date_range(start=start_date, periods=periods, freq='D')

# Definisikan kategori dan template pengaduan per kategori
categories = {
    "PDAM": [
        "Air tidak mengalir selama {} jam di wilayah {}.",
        "Tagihan PDAM naik {} persen bulan ini di {}.",
        "Kualitas air buruk sejak {} terjadi gangguan di {}."
    ],
    "Pendidikan": [
        "Fasilitas sekolah di {} sangat minim, terutama ruang {}.",
        "Biaya pendidikan meningkat {} persen tanpa adanya perbaikan sarana di {}.",
        "Kualitas pengajaran menurun di {} karena {} guru yang tidak profesional."
    ],
    "Transportasi": [
        "Jadwal bus di {} sering terlambat, membuat penumpang {}.",
        "Kondisi angkutan umum di {} sangat kotor dan tidak terawat.",
        "Kemacetan parah di {} terutama di sekitar {}."
    ],
    "Kesehatan": [
        "Pelayanan di rumah sakit {} lambat, terutama bagian {}.",
        "Ketersediaan obat di {} tidak mencukupi untuk {} pasien.",
        "Antrian di klinik {} terlalu panjang, mengganggu {} waktu pasien."
    ],
    "Infrastruktur": [
        "Jalan rusak parah di {} sehingga mengganggu aktivitas {}.",
        "Pembangunan {} di {} terkesan terburu-buru dan tidak berkualitas.",
        "Penerangan jalan di {} sangat minim, membahayakan keselamatan {}."
    ]
}

# Data tambahan untuk mengganti placeholder
wilayah = ["Jakarta", "Bandung", "Surabaya", "Medan", "Semarang", "Yogyakarta", "Denpasar", "Makassar", "Palembang", "Balikpapan"]
waktu = ["pagi", "siang", "sore", "malam"]
ruang = ["kelas", "laboratorium", "perpustakaan", "kantin"]
alasan = ["kurangnya dana", "manajemen yang buruk", "kendala teknis", "kekurangan tenaga ahli"]
tempat = ["terminal", "stasiun", "pintu masuk", "area parkir"]

# Fungsi untuk menghasilkan pengaduan berdasarkan kategori
def generate_complaint(category):
    template = random.choice(categories[category])
    count_placeholders = template.count("{}")
    values = []

    for _ in range(count_placeholders):
        if category == "PDAM":
            value = random.choice([str(random.randint(2, 8)), str(random.randint(5, 20)), random.choice(wilayah)])
        elif category == "Pendidikan":
            value = random.choice([str(random.randint(10, 50)), random.choice(waktu), random.choice(ruang), random.choice(alasan)])
        elif category == "Transportasi":
            value = random.choice([str(random.randint(5, 30)) + " menit", random.choice(waktu), random.choice(tempat)])
        elif category == "Kesehatan":
            value = random.choice([str(random.randint(10, 60)) + " menit", random.choice(["darurat", "non-darurat"]), random.choice(wilayah)])
        elif category == "Infrastruktur":
            value = random.choice([random.choice(wilayah), random.choice(waktu), random.choice(["kendaraan", "pejalan kaki"])])
        else:
            value = "info"
        values.append(value)

    complaint = template.format(*values)
    return complaint

# Buat tren linear + noise untuk analisis time series
np.random.seed(42)
trend = np.linspace(0, 100, periods)
noise = np.random.normal(loc=0, scale=10, size=periods)
target_time_series = trend + noise  # Misalnya sebagai jumlah pengaduan rata-rata per hari

# Buat dataset dummy
data = []
for i in range(periods):
    cat = random.choice(list(categories.keys()))
    complaint = generate_complaint(cat)
    sentiment = random.choices(["positif", "negatif", "netral"], weights=[0.3, 0.5, 0.2])[0]
    
    data.append({
        "ID": i + 1,
        "date": date_range[i],
        "kategori": cat,
        "pengaduan": complaint,
        "sentimen": sentiment,
        "jumlah_pengaduan": round(target_time_series[i], 2)  # Simulasi jumlah pengaduan per hari
    })

# Buat DataFrame dan simpan ke CSV
df = pd.DataFrame(data)
df.to_csv("dataset_pengaduan.csv", index=False, encoding='utf-8-sig')

print("SUCCESS!")
