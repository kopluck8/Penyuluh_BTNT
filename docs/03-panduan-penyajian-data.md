# Panduan menyajikan data penyuluhan dan pemberdayaan di dashboard

Panduan ini merangkum praktik yang dipakai di dashboard dan bisa dipakai untuk laporan berikutnya. Rujukannya adalah prinsip desain dashboard yang umum dipakai: Stephen Few (*Information Dashboard Design*), Cole Nussbaumer Knaflic (*Storytelling with Data*), Edward Tufte (rasio data-tinta), serta panduan aksesibilitas warna untuk pembaca buta warna.

## 1. Mulai dari pertanyaan, bukan dari grafik

Setiap bagian dashboard menjawab satu pertanyaan yang biasa ditanyakan pimpinan atau mitra:

| Pertanyaan | Bentuk sajian yang tepat |
|---|---|
| Berapa banyak kegiatan, kelompok, anggota tahun ini? | **Angka besar (stat tile)** dengan pembanding tahun lalu |
| Bagaimana perubahannya dari tahun ke tahun? | **Grafik garis** (angka berkelanjutan) atau **batang per tahun** (hitungan) |
| Di mana kegiatan terkonsentrasi? | **Peta panas resort × tahun** atau batang berperingkat |
| Kelompok mana yang naik kelas, mana yang stagnan? | **Tabel dengan panah perubahan**, atau grafik "slope" dua titik waktu |
| Apa isi dan rekomendasi laporan? | **Kartu kegiatan** yang bisa dibuka, dengan tautan ke dokumen asli |

Jika jawabannya satu angka, tampilkan angkanya. Grafik batang dengan satu batang atau diagram lingkaran dua irisan tidak menambah informasi.

## 2. Susunan halaman

1. **Ringkasan di atas**: 4–6 angka kunci. Pembaca yang hanya punya 10 detik tetap mendapat intinya.
2. **Tren tahunan** di bawahnya, karena permintaan utamanya adalah perubahan dari tahun ke tahun.
3. **Rincian dan penjelajahan** (filter, tabel, kartu) paling bawah.
4. **Filter dalam satu baris** di atas bagian yang difilter (tahun, resort, tema). Filter mengubah semua grafik di bawahnya sekaligus.

## 3. Pilih grafik sesuai tugas data

- **Hitungan per tahun** (jumlah kegiatan, jumlah kelompok): batang vertikal, sumbu mulai dari nol.
- **Komposisi per tahun** (tema kegiatan, kelas kelompok): batang bertumpuk dengan **paling banyak 4–5 kategori**. Kategori lain digabung menjadi "Lainnya".
- **Nilai yang berubah halus** (pendapatan rata-rata anggota, debit air): grafik garis dengan titik penanda.
- **Dua ukuran berbeda satuan** (misalnya jumlah anggota dan pendapatan): **dua grafik terpisah**, jangan satu grafik dengan dua sumbu Y. Dua sumbu membuat korelasi palsu.
- **Matriks resort × tahun**: peta panas satu warna (terang = sedikit, gelap = banyak), dengan angka di dalam sel.
- **Perbandingan antar resort**: batang horizontal yang diurutkan dari terbesar.
- Hindari diagram lingkaran untuk membandingkan nilai yang mirip, grafik 3D, dan gradasi pelangi.

## 4. Warna

- Warna dipakai untuk **identitas** (tema, resort) atau **besaran** (gelap-terang satu warna), tidak untuk hiasan.
- Satu kategori selalu memakai warna yang sama di semua grafik. Filter tidak boleh mengubah warna kategori yang tersisa.
- Maksimal delapan warna kategori. Urutannya sudah diuji agar tetap terbedakan oleh pembaca buta warna.
- Warna status (merah, kuning, hijau) hanya untuk status (misalnya kelompok "tidak aktif"), dan selalu ditemani label teks atau ikon.
- Mode gelap dan terang memakai warna yang dipilih khusus untuk masing-masing latar, bukan sekadar dibalik.

## 5. Jujur terhadap data

Laporan teknis TN Tambora memakai metode yang berbeda dari tahun ke tahun. Dashboard menerapkan aturan berikut:

- **Jangan menjumlahkan angka dari metode berbeda.** Jumlah rusa dari perjumpaan langsung tidak dijumlahkan dengan taksiran dari jejak. Dashboard menampilkan keduanya terpisah dan selalu menyebut nama indikator aslinya.
- **Tandai data yang kosong sebagai kosong**, bukan nol. "Tidak dimonitor" berbeda dengan "nol individu".
- **Sebutkan sumbernya.** Setiap kartu kegiatan bertaut ke berkas asli di Google Drive.
- **Beri catatan jika data tidak lengkap**, misalnya arsip yang terpotong atau RPK tanpa LPK.

## 6. Data kelompok binaan yang layak disajikan

Supaya kondisi kelompok binaan bisa dilihat dari tahun ke tahun, kumpulkan data yang sama setiap tahun untuk kelompok yang sama (data panel). Indikator yang disarankan:

| Aspek | Indikator | Sajian |
|---|---|---|
| Kelembagaan | Jumlah kelompok aktif, jumlah anggota, anggota perempuan, kelas kelompok | Stat tile + batang bertumpuk kelas per tahun |
| Kapasitas | Jumlah pelatihan, pendampingan oleh penyuluh | Batang per tahun |
| Ekonomi | Produksi, pendapatan kelompok, pendapatan rata-rata anggota | Garis per tahun, median antar kelompok |
| Dukungan | Jenis dan nilai bantuan | Batang per tahun, tabel per kelompok |
| Konservasi | Luas areal kelola, kontribusi pada patroli, pemulihan, atau pengurangan perambahan | Garis atau tabel |

Untuk pendapatan, gunakan **median** antar kelompok, bukan rata-rata, karena satu kelompok besar bisa menarik rata-rata jauh ke atas.

## 7. Aksesibilitas dan perangkat

- Teks minimal 14 px, kontras cukup di mode gelap dan terang.
- Setiap grafik punya tooltip saat disentuh atau diarahkan, dan **tabel data** sebagai alternatif.
- Tata letak menyesuaikan layar ponsel, karena banyak petugas lapangan membuka dashboard dari ponsel.
- Semua berkas data disediakan dalam CSV agar bisa dibuka di Excel atau Google Sheets.

## 8. Pemeliharaan

- Data mentah hanya diubah di satu tempat (`data/raw/` atau `data/kelompok_binaan/`), lalu skrip membangun ulang semua turunan.
- Setiap pembaruan lewat *pull request* supaya ada jejak siapa mengubah apa dan kapan.
- GitHub Pages menerbitkan ulang dashboard otomatis setelah perubahan digabung ke cabang `main`.
