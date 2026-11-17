"""Ringkasan naratif per jenis kegiatan penyuluhan dan pemberdayaan.

Disusun dari isi seluruh laporan di folder Drive penyuluhan (lihat data/penyuluhan.json).
Angka (jumlah laporan, tahun, desa, peserta) dihitung otomatis oleh build_data.py;
teks di sini hanya merangkum apa yang dikerjakan dan apa yang ditemukan.
Urutan kunci = urutan tampil di dashboard dan dokumen.
"""

PROGRAM = {
    "Pendampingan kelompok binaan": {
        "tujuan": "Kunjungan rutin penyuluh ke kelompok binaan untuk membina kelembagaan, usaha, dan pemanfaatan bantuan.",
        "poin": [
            "Kegiatan terbanyak di folder ini. Hampir setiap kunjungan mencatat kehadiran anggota, kondisi alat bantuan, dan kendala usaha.",
            "Masalah yang paling sering dicatat adalah anggota tidak aktif, pertemuan tidak rutin, dan alat bantuan yang rusak atau tersebar di rumah anggota.",
            "Rincian per kelompok ada di bagian Kelompok binaan dan di docs/kelompok-binaan.md.",
        ],
    },
    "Monitoring & evaluasi kelompok": {
        "tujuan": "Penilaian berkala keaktifan kelompok dan pemanfaatan bantuan, kadang dengan skor kriteria dan indikator (K&I).",
        "poin": [
            "Monev rutin berjalan sejak 2021, paling banyak pada 2022–2024.",
            "Hasil monev menjadi sumber utama status aktif, kurang aktif, atau tidak aktif di matriks kelompok.",
            "Skor K&I hanya tercatat pada sebagian kecil kelompok, misalnya Citra Madu Lestari (2,08 pada 2023, kategori berhasil), sehingga belum bisa dibuat tren.",
        ],
    },
    "Pembentukan kelompok": {
        "tujuan": "Membentuk kelompok baru lewat musyawarah dan penggalian potensi desa.",
        "poin": [
            "2020: kelompok binaan Desa Sorinomo (kerajinan, Kali Wangi Sorinomo).",
            "2022: kelompok baru di Desa Piong, yang sudah punya Oi Jara, Moti La Halo, dan Madu Putih. Warga menanyakan pengelolaan mobil 4x4 yang direncanakan, dan Sanggar Offroad tercatat baru dibentuk pada tahun yang sama. Di Dusun Tompo Jaya, Tolokalo, dibentuk Kelompok Tani So Tompo Jaya (33 anggota) untuk kemitraan konservasi.",
            "2023: Doro Ncanga Offroad di Sori Tatanga, dan rencana kelompok kemitraan di Oi Katupa (Bintang Sembilan, baru tahap RPK).",
            "Pertanyaan warga yang muncul berulang: kejelasan batas kawasan dan pengelolaan aset bantuan seperti mobil 4x4.",
        ],
    },
    "Penyusunan RPP/RKT/RPM": {
        "tujuan": "Menyusun Rencana Pengelolaan Program (RPP), Rencana Kerja Tahunan (RKT), dan Rencana Pemberdayaan Masyarakat (RPM) bersama kelompok.",
        "poin": [
            "2020: FGD RPP untuk KPA Algura, River Tubing, dan Citra Madu Lestari (Kawinda Toi), Oi Saro Kreatif, ALPATAR (Oi Bura), dan Fokus Tambora PD (Doropeti).",
            "2021: RPP dan RKT kelompok wisata berkuda Nente Jara. Dicatat bahwa kuda pacuan milik anggota belum jinak untuk wisata.",
            "2022: RPM Desa Sori Tatanga. 2023: RPP dan RKT Kelompok Tani Karyasari, saat permintaan porang turun.",
            "Rekomendasi yang berulang: rencana perlu disusun lebih matang sesuai juknis lalu benar-benar dijalankan.",
        ],
    },
    "Bantuan ekonomi produktif": {
        "tujuan": "Penyerahan bantuan peralatan atau dana usaha kepada kelompok.",
        "poin": [
            "2020: bibit durian dan kelengkeng untuk Sorinomo Berkarya. Laporan mencatat persyaratan penerima belum lengkap saat penyerahan.",
            "2022: penyerahan bantuan di Resort Piong, termasuk Rp125 juta untuk Sanggar Offroad membeli mobil offroad.",
            "Riwayat kelompok penerima menunjukkan banyak bantuan yang kemudian rusak atau tidak dipakai. Lihat bagian Kelompok binaan.",
        ],
    },
    "Kemitraan konservasi": {
        "tujuan": "Memberi akses pemanfaatan tradisional di zona tradisional lewat perjanjian kerja sama (PKS) dengan kelompok masyarakat.",
        "poin": [
            "Karyasari, Sori Tatanga: FGD kelayakan PKS (2020) lalu penguatan kelembagaan Kelompok Tani Karyasari (2021, 30 dari 50 anggota hadir). HHBK yang direncanakan, yaitu porang, dinilai belum cukup menguntungkan.",
            "So Tompo, Tolokalo (2022): sosialisasi rencana, FGD kelayakan dengan narasumber dari direktorat pusat, dan pra-penandatanganan PKS dengan 27 anggota. Pada pendampingan 2023 hanya 3 anggota hadir karena sibuk menanam jagung.",
            "2023: identifikasi lokasi potensi kemitraan di Kawinda Toi dan Oi Katupa.",
            "2026: Citra Madu Lestari (15 anggota) dinilai memenuhi syarat untuk melanjutkan akses pemanfaatan tradisional, dan PKS-nya diusulkan diperpanjang.",
        ],
    },
    "Kesepakatan konservasi desa": {
        "tujuan": "Kesepakatan Konservasi Desa (KKD) antara Balai dan pemerintah desa penyangga.",
        "poin": [
            "Ditandatangani dengan Sori Tatanga (November 2021), lalu Oi Saro, Sorinomo, dan Tolokalo (April 2022), Kawinda Nae (Agustus 2022), dan Oi Panihi (September 2022).",
            "Masalah yang diangkat warga: batas kawasan, penanaman yang melewati pal batas, dan tingginya aktivitas warga di dalam kawasan.",
            "Setiap laporan merekomendasikan KKD dijadikan dasar program desa dan dimonev berkala. Belum ada laporan monev KKD di folder ini.",
        ],
    },
    "Pemulihan ekosistem": {
        "tujuan": "Pendampingan dan pengawasan penanaman di areal terdegradasi bersama kelompok masyarakat.",
        "poin": [
            "So Lia/So Tompo, Doro Ncanga (November 2022): 45 ha, dikerjakan 40 anggota Kelompok Tani So Tompo Jaya. Jalan berlumpur menghambat pengangkutan bibit.",
            "Labu Bili, Piong (Januari 2023): 45 ha. Tanah keras dan cuaca panas menyulitkan pembuatan lubang tanam.",
            "Patroli November 2023 di So Lia menemukan areal pemulihan terbakar dan banyak tanaman mati. Rekomendasinya pengamanan yang lebih intensif.",
        ],
    },
    "Tambora Goes To School": {
        "tujuan": "Pendidikan konservasi di sekolah sekitar kawasan: pengenalan TN Tambora, fungsi hutan, flora dan satwa dilindungi.",
        "poin": [
            "Dua gelombang besar: 2020 (9 kegiatan, sebagian terganggu pandemi) dan 2023 (12 kegiatan), lalu berlanjut pada 2024 dan 2026 dengan nama Kampanye/Promosi Goes To School.",
            "Sasaran dari SD sampai SMA/SMK dan pondok pesantren. Metodenya paparan, video, permainan, kuis, dan simulasi Pohon Harapan.",
            "Kendala yang berulang: jadwal bentrok dengan ujian sehingga siswa sedikit, dan sekolah yang sulit dijangkau.",
            "Rekomendasi yang berulang: belajar langsung di kawasan, lebih banyak praktik, dan menjadikannya agenda tahunan.",
        ],
    },
    "Kader konservasi": {
        "tujuan": "Membentuk dan membina kader konservasi atau Bina Cinta Alam dari pelajar, pramuka, dan pemuda.",
        "poin": [
            "2022: pembentukan kader di SPTN I Kore (28 peserta, Kecamatan Sanggar) dan SPTN II Pekat/Kempo (30 peserta).",
            "2023: pembinaan PEPA, pecinta alam SMAN 1 Sanggar, dan Sakawanabakti, pramuka Pekat (dua kali, masing-masing 20 orang). Materinya antara lain drone dan keanekaragaman hayati.",
            "2024: peningkatan kapasitas 20 kader SPTN I Kore. Evaluasinya: sebagian besar kader belum aktif dan belum melaporkan kegiatan.",
            "Desember 2025: Kemah Bakti Kader Bina Cinta Alam di Sanctuary Rusa Doro Ncanga (40 peserta dari 8 sekolah), dengan penanaman dan pengamatan rusa.",
        ],
    },
    "Sosialisasi karhutla": {
        "tujuan": "Pencegahan kebakaran hutan dan lahan lewat sosialisasi, anjangsana, dan patroli bersama MPA/MMP.",
        "poin": [
            "2021–2024: satu sosialisasi per resort di kantor desa atau resort, biasanya dengan 20 peserta (aparat desa, MPA, MMP, kelompok madu, petani jagung).",
            "2025: berubah menjadi anjangsana dua desa per kegiatan bersama Muspika dan Satpol PP kecamatan. Jangkauannya meluas ke desa di luar resort (Beringin Jaya, Konte, Dorokobo, Kore, Boro).",
            "2026: ditambah smart patrol bersama MPA (5 petugas dan 5 anggota MPA) serta sosialisasi kepada pendaki di Oi Marai, Tambora, dan Oi Bura.",
            "Temuan dari lapangan: membakar untuk membuka lahan masih dianggap murah dan praktis; mobil tangki tidak bisa masuk ke jalan sempit; kantor desa Oi Katupa belum berlistrik; ternak digembalakan di dalam kawasan; ada konflik lahan warga dengan PT AWB di Kadindi dan Tambora.",
        ],
    },
    "Penanganan sampah": {
        "tujuan": "Membersihkan sampah pengunjung di objek wisata dan jalur pendakian sebagai bagian dari pencegahan kebakaran.",
        "poin": [
            "2022 dan 2023 di Oi Marai dan jalur pendakian Kawinda Toi, serta 2022 di jalur Doro Ncanga dan Sanctuary Rusa (termasuk sisa Festival Tambora).",
            "Setiap kegiatan melibatkan 5 petugas dan 5 warga atau anggota kelompok mitra.",
            "Rekomendasinya kegiatan tahunan dan pemasangan kembali papan larangan buang sampah dan peringatan kebakaran.",
        ],
    },
    "Sosialisasi zonasi": {
        "tujuan": "Menjelaskan zonasi baru dan batas kawasan TN Tambora kepada warga dan pemangku kepentingan.",
        "poin": [
            "2022: di Sori Tatanga, Tambora, Kawinda Toi, Oi Katupa, dan Piong (sekitar 30 peserta per desa), serta di BAPPEDA Kabupaten Bima bersama dinas, pegiat wisata, dan media.",
            "2024: sosialisasi batas Zona Tradisional Kawinda Toi (35 peserta).",
            "Yang paling sering ditanyakan warga adalah batas TN dengan hutan produksi dan lahan perusahaan. PT AWB disebut tidak hadir saat diundang.",
            "Rekomendasinya leaflet, peta, dan papan informasi batas zonasi.",
        ],
    },
    "Penyadartahuan & sosialisasi lain": {
        "tujuan": "Penyadartahuan perlindungan dan pengamanan kawasan, kampanye konservasi, dan pameran.",
        "poin": [
            "2025: rangkaian Sosialisasi dan Anjangsana Penyadartahuan Perlindungan dan Pengamanan di desa penyangga SPTN II, yaitu Kempo, Ta'a, Sorinomo, Nangakara, Soro Barat, Tolokalo, Pekat, Calabai, Kadindi, Nangamiro, Tambora, Oi Bura, Doropeti, dan Sori Tatanga.",
            "2023: sosialisasi pemberdayaan dan penyusunan rencana usaha kelompok di Sori Tatanga. Laporannya menyebut sebagian anggota Sama Weki adalah mantan pelaku illegal logging.",
            "2026: kampanye konservasi di Pantai Lakey, Hu'u, dan booth di FTN-TWA Expo, Ragunan, Jakarta.",
            "Pesan yang berulang: batas kawasan perlu disosialisasikan rutin oleh aparat desa bersama penyuluh.",
        ],
    },
    "Lainnya": {
        "tujuan": "Kegiatan lapangan pendukung wisata dan sarana.",
        "poin": [
            "2022: pengecekan sumber air di Pos 2 jalur Doro Ncanga dan progres jembatan akses Oi Marai.",
            "2026: penjagaan pintu masuk Wisata Alam Oi Marai saat musim ramai. Tercatat 186 pengunjung dalam tiga hari (138 wisatawan dan 48 pendaki), dengan puncak 109 orang pada 16 Agustus.",
        ],
    },
}

# Penyatuan nama jenis kegiatan yang sebenarnya sama.
JENIS_SINONIM = {"Penyusunan RPP/RKT": "Penyusunan RPP/RKT/RPM"}
