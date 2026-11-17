# Penyuluh BTNT

Kurasi laporan penyuluhan, pemberdayaan masyarakat, dan kegiatan teknis **Balai Taman Nasional Tambora** 2020–2026. Repo ini juga berisi dashboard statis untuk GitHub Pages yang menampilkan kondisi kelompok binaan dari tahun ke tahun.

**Dashboard:** https://kopluck8.github.io/Penyuluh_BTNT/ (aktif setelah GitHub Pages dinyalakan, lihat di bawah)

## Isi singkat

- **260 laporan penyuluhan dan pemberdayaan** (pendampingan dan monev kelompok, kemitraan konservasi, kader konservasi, Tambora Goes To School, sosialisasi zonasi dan karhutla).
- **96 laporan teknis PEH** (satwa, flora, tumbuhan invasif, ekosistem).
- **43 kelompok binaan** dengan riwayat kondisi per tahun: aktif, kurang aktif, tidak aktif, atau baru dibentuk. Untuk tiap kelompok tercatat juga kendala, kebutuhan, bantuan, dan produknya.

## Mulai membaca dari sini

| Dokumen | Isi |
|---|---|
| [docs/02-masyarakat-dan-kelompok-binaan.md](docs/02-masyarakat-dan-kelompok-binaan.md) | Temuan utama tentang kelompok binaan dan penyuluhan |
| [docs/kelompok-binaan.md](docs/kelompok-binaan.md) | Profil dan riwayat per tahun untuk 43 kelompok |
| [docs/01-gambaran-umum.md](docs/01-gambaran-umum.md) | Gambaran dua folder dan hasil teknis (satwa, flora, ekosistem) |
| [docs/03-panduan-penyajian-data.md](docs/03-panduan-penyajian-data.md) | Cara menyajikan data ini supaya jelas |
| [docs/04-catatan-kualitas-data.md](docs/04-catatan-kualitas-data.md) | Cara kurasi dan keterbatasan data |
| [docs/laporan/](docs/laporan/README.md) | Ringkasan per laporan, dengan tautan ke berkas asli |
| [docs/katalog-sumber-penyuluhan.md](docs/katalog-sumber-penyuluhan.md), [docs/katalog-sumber.md](docs/katalog-sumber.md) | Daftar semua berkas di Google Drive |

## Struktur repo

```
data/
  raw/                      hasil ekstraksi dari laporan (sumber semua berkas turunan)
  penyuluhan.csv|json       260 kegiatan penyuluhan dan pemberdayaan
  kelompok.csv|json         43 kelompok binaan
  kelompok_riwayat.csv      satu baris per kelompok per tahun
  kegiatan.csv|json         96 kegiatan teknis PEH
  indikator.csv, seri/, kehati/   angka teknis dan daftar jenis
  sumber_*.csv              katalog berkas Drive
  kelompok_binaan/          templat isian monev untuk tahun berikutnya
  dashboard.json            data gabungan untuk dashboard
docs/                       penjelasan dan ringkasan laporan
scripts/
  build_data.py             data/raw -> semua CSV/JSON
  build_docs.py             data -> docs/laporan, docs/kelompok-binaan.md, katalog
site/                       dashboard (HTML, CSS, JS tanpa pustaka luar)
.github/workflows/pages.yml deploy otomatis ke GitHub Pages
```

## Memperbarui data

```bash
python3 scripts/build_data.py
python3 scripts/build_docs.py
```

Hanya butuh Python 3.9 atau lebih baru, tanpa paket tambahan.

Untuk melihat dashboard di komputer sendiri:

```bash
mkdir -p site/data && cp data/dashboard.json site/data/
cd site && python3 -m http.server 8000
```

Lalu buka http://localhost:8000.

## Menyalakan GitHub Pages

Cukup sekali: buka **Settings → Pages → Build and deployment**, lalu pilih **Source: GitHub Actions**. Setiap push ke `main` akan membangun ulang data dan menerbitkan dashboard.

## Catatan

Ringkasan laporan dibuat dengan bantuan model bahasa dan belum diverifikasi satu per satu. Untuk angka yang dipakai dalam keputusan, buka berkas aslinya lewat tautan di dashboard atau di katalog. Berkas asli (sekitar 5,8 GB) tetap di Google Drive dan tidak disalin ke repo.
