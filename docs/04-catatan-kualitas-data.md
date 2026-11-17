# Catatan kualitas data dan cara kurasi

## Cara data dikumpulkan

### Folder penyuluhan dan pemberdayaan (274 berkas)

1. Semua berkas diunduh (sekitar 3,5 GB). Setiap berkas berupa zip berisi RPK, LPK, surat tugas, daftar hadir, foto, dan lampiran.
2. Teks diambil dari PDF, DOCX, dan XLSX. Foto dan PDF hasil pindai tanpa lapisan teks tidak terbaca.
3. Setiap arsip diekstrak ke format terstruktur dengan bantuan model bahasa: judul, jenis kegiatan, waktu, resort, desa, peserta, sekolah, kelompok yang dibahas, ringkasan, temuan, kendala, dan rekomendasi. Untuk setiap kelompok yang dibahas, dicatat juga kondisi, anggota, penilaian, kendala, kebutuhan, bantuan, produk, dan pendapatan.
4. Nama kelompok yang ditulis berbeda-beda disatukan, misalnya "KPA Algura", "Algura", dan "Kelompok Pecinta Alam Algura". Hasilnya 43 kelompok. Catatan per kelompok per tahun digabung dari semua laporan tahun itu.
5. Arsip yang isinya kegiatan yang sama (RPK dan LPK terpisah, atau unggahan ganda) digabung menjadi satu kegiatan. Hasilnya 260 kegiatan. Sebanyak 88 dari 274 berkas tidak menjadi kegiatan sendiri karena isinya sudah tergabung atau hanya berisi lampiran. Lihat kolom `dipakai_di_dashboard` di `data/sumber_penyuluhan.csv`.
6. Data ringkas hasil kurasi disimpan di `data/raw/ekstraksi_penyuluhan.json`. `scripts/build_data.py` menormalkan ejaan desa dan nama sekolah, lalu menulis `data/penyuluhan.*`, `data/kelompok.*`, dan `data/kelompok_riwayat.csv`.

Kunci ringkas di `ekstraksi_penyuluhan.json`:

- **kegiatan:** j = judul, jk = jenis kegiatan, g = kelompok jenis (0 pendampingan dan monev, 1 kemitraan, 2 edukasi dan kader, 3 sosialisasi), t/b/tg = tahun/bulan/tanggal, r = resort, d = desa, p = peserta, sk = sekolah, kl = id kelompok, rs = ringkasan, tm = temuan, kd = kendala, rk = rekomendasi, u = id berkas Drive, nf = jumlah berkas di arsip.
- **kelompok.riw[tahun]:** st = status, ang = anggota, prm = anggota perempuan, skor = penilaian, kond = kondisi, kend = kendala, butuh = kebutuhan, ban = bantuan, prod = produk, pend = pendapatan, kt = tema kendala, keg = id kegiatan.

### Folder LAP_Teknis (96 berkas)

1. Seluruh 96 berkas di folder Drive `LAP_Teknis` diunduh (sekitar 2,3 GB).
2. Arsip zip dan rar dibongkar. Tujuh zip tidak standar atau terpotong, jadi isinya dipulihkan per berkas dari header lokal zip. Bagian yang terpotong dibaca sejauh masih utuh.
3. Teks diambil dari PDF, DOCX, dan XLSX (400 baris pertama per lembar). Berkas yang sama-sama milik satu kegiatan (RPK, LPK, lembar analisis) dikelompokkan.
4. Setiap kelompok dibaca dan diekstrak ke format terstruktur (judul, waktu, resort, metode, indikator, temuan, ancaman, rekomendasi, keterlibatan masyarakat) dengan bantuan model bahasa. Hasilnya belum diverifikasi manual satu per satu oleh petugas. Semuanya disimpan di `data/raw/ekstraksi_lpk_rpk.json`.
5. `scripts/build_data.py` menormalkan nama resort, mengelompokkan tema, membuang duplikat, dan membangun semua berkas turunan.

## Keterbatasan yang perlu diketahui

- **Status kelompok adalah tafsiran dari kata-kata laporan.** "Kurang aktif" bisa berarti kehadiran rapat rendah atau usaha belum berjalan. Baca kondisi lengkapnya di profil kelompok sebelum menyimpulkan.
- **Kotak kosong bukan berarti kelompok bubar.** Artinya tidak ada laporan tahun itu yang membahas kelompok tersebut. Pada 2025 hampir semua kelompok hanya disebut tanpa penilaian.
- **Jumlah anggota sering berupa jumlah yang hadir**, bukan anggota terdaftar. Angka 0 di sumber dianggap tidak disebut.
- **Jumlah peserta** hanya ada di 120 dari 260 laporan penyuluhan.
- **Jenis dan bidang usaha kelompok** ditentukan dari isi laporan dan bisa kurang tepat untuk kelompok yang usahanya berganti. Contohnya Kelompok Tani Karyasari, yang beralih dari HHBK porang ke minuman jahe merah.
- **Hasil ekstraksi otomatis bisa keliru di detail kecil.** Untuk angka yang dipakai dalam keputusan, buka berkas aslinya lewat tautan di kartu kegiatan atau di [katalog sumber](katalog-sumber.md).
- **Laporan sering tidak konsisten di dalam dirinya sendiri**, misalnya tanggal berbeda antara RPK dan LPK, atau jumlah jenis berbeda antara narasi dan tabel. Ringkasan per laporan mencatat perbedaan ini bila ditemukan.
- **Metode berbeda antar tahun dan antar resort.** Angka populasi satwa adalah hasil satu kali pengamatan dengan metode tertentu, bukan sensus. Jangan dibaca sebagai tren populasi tanpa melihat metodenya.
- **Beberapa kegiatan hanya punya RPK** (rencana), misalnya stok karbon Doro Ncanga 2025. Kegiatan ini dihitung sebagai terdokumentasi, tetapi tidak ada hasilnya.
- **Satu laporan tanpa tahun**: "Analisis data Doropeti" (lembar Excel raptor), isinya sama dengan inventarisasi raptor Doropeti Juli 2021.

## Berkas yang bermasalah

| Berkas | Masalah |
|---|---|
| `2022031418_Monitoring_Elflo_Katupa_Pt.zip` | Hanya 3 KB, berisi zip lain. Kemungkinan unggahan gagal. Mohon diunggah ulang. |
| `download_2026-11-11_18-31-17.zip`, `18-59-44`, `20-19-46`, `20-25-03`, `20-43-36`, `22-04-52`, `22-49-22` | Zip tidak standar atau terpotong. Isi dipulihkan sebagian. |
| `download_2026-11-11_20-34-43.zip`, `21-35-18`, `20-47-47` | Isinya sama dengan zip lain, jadi tidak dihitung dua kali. |
| `download_2026-11-11_20-39-34.zip` | Hanya shapefile transek rusa Doro Ncanga Mei 2022, belum divisualkan. |
| `1 - LPK Ident Burung Oi Katupa.pdf` (di dalam zip) | Gagal dibuka. Data burung Oi Katupa 2023 diambil dari tally sheet. |
| Sejumlah PDF hasil pindai (tally sheet, hasil uji lab karbon) | Tidak ada teks yang bisa dibaca mesin. Isinya belum masuk data. |

## Normalisasi yang diterapkan

- Nama resort: "Dorocanga", "Doro Ncanga", "DC" menjadi **Doro Ncanga**; "Kawinda To'i" menjadi **Kawinda Toi**; site Karyasari masuk **Doropeti**.
- Wilayah: SPTN Wilayah I Kore (Piong, Kawinda Toi, Oi Katupa) dan SPTN Wilayah II Pekat (Doro Ncanga, Doropeti, Pancasila). Penulisan "Pekat/Kempo" disatukan.
- Tema: 11 kategori kegiatan diringkas menjadi 4 tema (satwa; flora dan tumbuhan invasif; ekosistem dan jasa lingkungan; masyarakat dan pengelolaan) agar grafik tidak memakai terlalu banyak warna.
- Bentuk keterlibatan masyarakat dan tema ancaman diturunkan dengan kata kunci dari teks laporan. Daftar kata kuncinya ada di `scripts/build_data.py` (`PERAN` dan `ANCAMAN`) dan bisa disesuaikan.
