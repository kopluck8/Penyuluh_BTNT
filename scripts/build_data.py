#!/usr/bin/env python3
"""Bangun data bersih untuk repo dan dashboard dari hasil ekstraksi mentah.

Masukan : data/raw/ekstraksi_lpk_rpk.json      (folder Drive 1, laporan teknis PEH)
          data/raw/ekstraksi_penyuluhan.json  (folder Drive 2, laporan penyuluhan & pemberdayaan)
Keluaran: data/kegiatan.json|csv, data/indikator.csv, data/sumber_dokumen.csv,
          data/seri/*.csv, data/kehati/*.csv,
          data/penyuluhan.json|csv, data/kelompok.json|csv, data/kelompok_riwayat.csv,
          data/sumber_penyuluhan.csv, data/dashboard.json

Hanya memakai pustaka standar Python 3.9+. Jalankan dari akar repo:
    python3 scripts/build_data.py
"""
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "ekstraksi_lpk_rpk.json"
OUT = ROOT / "data"
DRIVE_FOLDER = "https://drive.google.com/drive/folders/1nvBXpUPzh_nAC3LM6n7UEoqLBEJI3z4z"
RAW_PENYULUHAN = ROOT / "data" / "raw" / "ekstraksi_penyuluhan.json"
DRIVE_FOLDER_PENYULUHAN = "https://drive.google.com/drive/folders/17EdMZt6BFTimHN3LvHvqSq3WOwn_7Uyz"

# Kelompok jenis kegiatan penyuluhan (kode g di data mentah).
GRUP_PENYULUHAN = [
    "Pendampingan & monev kelompok",
    "Kemitraan & kesepakatan konservasi",
    "Edukasi & kader konservasi",
    "Sosialisasi & lainnya",
]
STATUS_URUT = ["aktif", "kurang aktif", "tidak aktif", "baru dibentuk", "tidak disebut"]

# Kelompok laporan yang isinya kembar (berkas sama diunggah dua kali).
DUPLIKAT = {
    "download_2026-11-11_20-34-43",  # = 20-34-17
    "download_2026-11-11_21-35-18",  # = 21-31-52
    "download_2026-11-11_20-47-47",  # = 20-42-59
}

RESORT = [
    ("Doro Ncanga", r"doro ?n?canga|dorocanga"),
    ("Doropeti", r"doropeti|doro peti"),
    ("Pancasila", r"pancasila"),
    ("Oi Katupa", r"oi katupa|katupa"),
    ("Kawinda Toi", r"kawinda"),
    ("Piong", r"piong"),
]
WILAYAH = {
    "Doro Ncanga": "SPTN Wilayah II Pekat",
    "Doropeti": "SPTN Wilayah II Pekat",
    "Pancasila": "SPTN Wilayah II Pekat",
    "Oi Katupa": "SPTN Wilayah I Kore",
    "Kawinda Toi": "SPTN Wilayah I Kore",
    "Piong": "SPTN Wilayah I Kore",
}

TEMA = {
    "Monitoring Satwa Kunci": "Satwa",
    "Inventarisasi & Identifikasi Fauna": "Satwa",
    "Pelepasliaran Satwa": "Satwa",
    "Inventarisasi & Identifikasi Flora": "Flora & tumbuhan invasif",
    "Tumbuhan Asing Invasif": "Flora & tumbuhan invasif",
    "Ground Check Tutupan Lahan & Tipe Ekosistem": "Ekosistem & jasa lingkungan",
    "Stok Karbon": "Ekosistem & jasa lingkungan",
    "Sumber Mata Air & Pemanfaatan Air": "Ekosistem & jasa lingkungan",
    "Sosialisasi & Pemberdayaan Masyarakat": "Masyarakat & pengelolaan",
    "Pendampingan & Penelitian": "Masyarakat & pengelolaan",
    "Perencanaan & Desain Tapak": "Masyarakat & pengelolaan",
}
TEMA_URUT = ["Satwa", "Flora & tumbuhan invasif", "Ekosistem & jasa lingkungan", "Masyarakat & pengelolaan"]

SASARAN = [
    ("Elang flores", r"elang flores|nisaetus|eflo"),
    ("Rusa timor", r"rusa"),
    ("Raptor", r"raptor|pemangsa"),
    ("Burung", r"burung|aves"),
    ("Anggrek", r"anggrek|orchid"),
    ("Tumbuhan asing invasif", r"invasi|\bias\b|\basing\b"),
    ("Tumbuhan penting", r"tumbuhan|flora|hhbk|vegetasi"),
    ("Tutupan lahan", r"tutupan|lahan|open area"),
    ("Mata air", r"mata air|\bair\b"),
    ("Stok karbon", r"karbon"),
    ("Masyarakat", r"masyarakat"),
    ("Pemulihan ekosistem", r"pemulihan"),
    ("Wisata & desain tapak", r"odtwa|tapak|wisata"),
]

# Bentuk keterlibatan masyarakat yang tercatat di laporan.
PERAN = [
    ("Tenaga lapangan dari desa", r"buruh|pembantu (lapangan|teknis)|tenaga kerja|pemandu"),
    ("Sumber informasi lokasi/satwa", r"informasi|wawancara|keterangan|menginformasikan"),
    ("Komunitas & kelompok mitra", r"sindikat|kelompok tani|k-pata|komunitas|bumdes|\bmitra\b|\bmpa\b"),
    ("Pemanfaatan sumber daya oleh warga", r"memanfaatkan|pemanfaatan|madu|ladang|jambu mete|pipa"),
    ("Sosialisasi & edukasi", r"sosialisasi|penyuluhan|edukasi|peserta|penyadaran"),
]

ANCAMAN = [
    ("Kebakaran", r"kebakar|terbakar|\bapi\b"),
    ("Perambahan & ladang", r"perambah|ladang|garapan|jagung|pembukaan lahan"),
    ("Penebangan liar", r"penebangan|illegal logging|logging|tebang"),
    ("Perburuan", r"perburuan|berburu|pemburu|\bburu\b|jerat"),
    ("Ternak di kawasan", r"ternak|\bsapi\b|kerbau|\bkuda\b"),
    ("Tumbuhan invasif", r"invasi|kerinyuh|chromolaena|lantana|\basing\b"),
    ("Pengambilan madu & HHBK", r"madu|pengasapan"),
]

KATA_INDIVIDU = re.compile(r"individu|ekor")


def norm_resort(raw, judul):
    teks = f"{raw or ''}".lower()
    hasil = [n for n, pola in RESORT if re.search(pola, teks)]
    if not hasil:
        hasil = [n for n, pola in RESORT if re.search(pola, (judul or "").lower())]
    return hasil


SASARAN_KATEGORI = {
    "Inventarisasi & Identifikasi Flora": None,  # anggrek / tumbuhan penting, lihat di bawah
    "Tumbuhan Asing Invasif": "Tumbuhan asing invasif",
    "Ground Check Tutupan Lahan & Tipe Ekosistem": "Tutupan lahan & ekosistem",
    "Stok Karbon": "Stok karbon",
    "Sumber Mata Air & Pemanfaatan Air": "Mata air",
    "Sosialisasi & Pemberdayaan Masyarakat": "Sosialisasi TSL",
    "Pendampingan & Penelitian": "Pemulihan ekosistem",
    "Perencanaan & Desain Tapak": "Wisata & desain tapak",
}


def norm_sasaran(k):
    judul = (k["judul"] or "").lower()
    teks = f"{k['target'] or ''} {judul}".lower()
    if "kemitraan" in judul:
        return "Kemitraan konservasi"
    if "madu" in judul:
        return "Lebah madu hutan"
    kat = k["kategori"]
    if kat in SASARAN_KATEGORI:
        if SASARAN_KATEGORI[kat]:
            return SASARAN_KATEGORI[kat]
        return "Anggrek" if re.search(r"anggrek|orchid", teks) else "Tumbuhan penting"
    for nama, pola in SASARAN[:4]:  # satwa: elang flores, rusa, raptor, burung
        if re.search(pola, teks):
            return nama
    return "Kehati lainnya"


SASARAN_MASYARAKAT = {"Kemitraan konservasi", "Sosialisasi TSL", "Pemulihan ekosistem", "Wisata & desain tapak"}


def tema_kegiatan(k):
    """Kegiatan yang langsung bersentuhan dengan warga masuk tema masyarakat."""
    if norm_sasaran(k) in SASARAN_MASYARAKAT or re.search(r"fasilitasi|zona khusus", (k["judul"] or "").lower()):
        return "Masyarakat & pengelolaan"
    return TEMA.get(k["kategori"], "Masyarakat & pengelolaan")


def cocok(daftar, teks):
    teks = (teks or "").lower()
    return [n for n, pola in daftar if re.search(pola, teks)]


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def sumber_kelompok(group, manifest_by_name):
    """Kembalikan berkas Drive asal sebuah kelompok laporan."""
    if group.startswith("_loose/"):
        nama = group[len("_loose/"):].removesuffix(".txt")
    elif group.startswith("_rar/"):
        nama = "LapTeknis.rar"
    else:
        nama = group.split("/")[0] + ".zip"
    m = manifest_by_name.get(nama)
    if not m:
        return None
    return {
        "nama": m["nama"],
        "url": f"https://drive.google.com/file/d/{m['id']}/view",
        "catatan": m.get("catatan"),
    }


def angka(v):
    if isinstance(v, (int, float)):
        return v
    try:
        return float(str(v).replace(",", "."))
    except ValueError:
        return None


def pilih_indikator(k, pola_wajib, pola_tolak=r"lain|vegetasi|jenis|kontak|tambora|20\d\d"):
    """Ambil satu angka 'individu teramati/diduga' dari indikator laporan."""
    kandidat = []
    for ind in k["indikator"]:
        nama = (ind.get("nama") or "").lower()
        sat = (ind.get("satuan") or "").lower()
        nilai = angka(ind.get("nilai"))
        if nilai is None or re.search(pola_tolak, nama):
            continue
        if not re.search(pola_wajib, nama + " " + sat):
            continue
        if not KATA_INDIVIDU.search(sat + " " + nama):
            continue
        if "kepadatan" in nama or "densitas" in nama or "/" in sat:
            continue
        kandidat.append((nama, nilai, ind))
    return kandidat


def main():
    raw = json.loads(RAW.read_text(encoding="utf-8"))
    manifest = raw["manifest"]
    manifest_by_name = {m["nama"]: m for m in manifest}

    kegiatan = []
    dipakai = set()
    for k in raw["kegiatan"]:
        g = k["_group"].split("/")[0]
        if g in DUPLIKAT:
            continue
        resort = norm_resort(k["resort"], k["judul"])
        wilayah = sorted({WILAYAH[r] for r in resort}) or (
            [w for w in ["SPTN Wilayah I Kore", "SPTN Wilayah II Pekat"]
             if k["wilayah"] and w.split()[-1].lower() in k["wilayah"].lower()]
        )
        sumber = sumber_kelompok(k["_group"], manifest_by_name)
        if sumber:
            dipakai.add(sumber["nama"])
        teks_ancaman = " ".join(k["ancaman"] + k["temuan_kunci"])
        base = f"{k['tahun'] or 'na'}-{slug(k['judul'])[:48]}"
        uid, n = base, 2
        while any(x["id"] == uid for x in kegiatan):
            uid, n = f"{base}-{n}", n + 1
        kegiatan.append({
            "id": uid,
            "judul": k["judul"],
            "tahun": k["tahun"],
            "bulan": k["bulan"],
            "tanggal_pelaksanaan": k["tanggal_pelaksanaan"],
            "kategori": k["kategori"],
            "tema": tema_kegiatan(k),
            "sasaran": norm_sasaran(k),
            "target": k["target"],
            "resort": resort,
            "wilayah": wilayah,
            "nomor_st": k["nomor_st"],
            "jumlah_personel": k["jumlah_personel"],
            "mitra": k["mitra"],
            "metode": k["metode"],
            "lokasi_detail": k["lokasi_detail"],
            "ringkasan": k["ringkasan"],
            "temuan_kunci": k["temuan_kunci"],
            "ancaman": k["ancaman"],
            "rekomendasi": k["rekomendasi"],
            "keterlibatan_masyarakat": k["keterlibatan_masyarakat"],
            "peran_masyarakat": cocok(PERAN, k["keterlibatan_masyarakat"]),
            "tema_ancaman": cocok(ANCAMAN, teks_ancaman),
            "jenis_tercatat": k["jenis_tercatat"],
            "indikator": k["indikator"],
            "berkas": k["_files"],
            "sumber": sumber,
        })

    kegiatan.sort(key=lambda x: (x["tahun"] or 0, x["bulan"] or 0, x["judul"]))
    (OUT / "kegiatan.json").write_text(json.dumps(kegiatan, ensure_ascii=False, indent=1), encoding="utf-8")

    flat = []
    for k in kegiatan:
        r = dict(k)
        for c in ("resort", "wilayah", "mitra", "peran_masyarakat", "tema_ancaman", "jenis_tercatat", "berkas"):
            r[c] = "; ".join(k[c] or [])
        for c in ("temuan_kunci", "ancaman", "rekomendasi"):
            r[c] = " | ".join(k[c] or [])
        r["sumber_drive"] = (k["sumber"] or {}).get("url")
        flat.append(r)
    tulis_csv(OUT / "kegiatan.csv",
              ["id", "tahun", "bulan", "tanggal_pelaksanaan", "judul", "kategori", "tema", "sasaran",
               "resort", "wilayah", "nomor_st", "jumlah_personel", "mitra", "metode", "lokasi_detail",
               "ringkasan", "temuan_kunci", "ancaman", "rekomendasi", "keterlibatan_masyarakat",
               "peran_masyarakat", "tema_ancaman", "jenis_tercatat", "berkas", "sumber_drive"], flat)

    ind_rows = []
    for k in kegiatan:
        for ind in k["indikator"]:
            ind_rows.append({"kegiatan_id": k["id"], "tahun": k["tahun"], "resort": "; ".join(k["resort"]),
                             "sasaran": k["sasaran"], **ind})
    tulis_csv(OUT / "indikator.csv", ["kegiatan_id", "tahun", "resort", "sasaran", "nama", "nilai", "satuan", "keterangan"], ind_rows)

    # Katalog semua berkas di folder Drive.
    kembar = {"download_2026-11-11_20-34-43.zip": "download_2026-11-11_20-34-17.zip",
              "download_2026-11-11_21-35-18.zip": "download_2026-11-11_21-31-52.zip",
              "download_2026-11-11_20-47-47.zip": "download_2026-11-11_20-42-59.zip"}
    katalog = []
    for m in manifest:
        isi = m.get("isi") or []
        catatan = [m.get("catatan")] if m.get("catatan") else []
        if m["nama"] in kembar:
            catatan.append(f"isi sama dengan {kembar[m['nama']]}, tidak dihitung dua kali")
        if m["nama"].startswith("00. Daftar KEHATI"):
            dipakai.add(m["nama"])
            catatan.append("daftar jenis KEHATI (xlsx) dipakai untuk data/kehati; sisanya buku panduan identifikasi")
        if m["ukuran"] < 10000:
            catatan.append(f"hanya {m['ukuran'] // 1000} KB berisi zip lain; kemungkinan unggahan gagal, mohon diunggah ulang")
        if isi and all(p.rsplit(".", 1)[-1].lower() in {"shp", "shx", "dbf", "prj", "cpg", "qmd", "sbn", "sbx", "xml", "lock"} for p, _ in isi):
            catatan.append("hanya data spasial (shapefile), belum divisualkan")
        katalog.append({
            "nama": m["nama"],
            "ukuran_mb": round(m["ukuran"] / 1e6, 2),
            "jumlah_berkas_di_dalam": len(isi),
            "contoh_isi": "; ".join(p.split("/")[-1] for p, _ in isi[:6]),
            "dipakai_di_dashboard": "ya" if m["nama"] in dipakai else "tidak",
            "catatan": "; ".join(catatan),
            "url": f"https://drive.google.com/file/d/{m['id']}/view",
        })
    tulis_csv(OUT / "sumber_dokumen.csv", list(katalog[0].keys()), katalog)

    # Seri satwa kunci: satu angka per laporan, dengan label indikator aslinya.
    def seri(sasaran, pola):
        out = []
        for k in kegiatan:
            if k["sasaran"] != sasaran or not k["tahun"]:
                continue
            kand = pilih_indikator(k, pola)
            if not kand:
                continue
            langsung = [c for c in kand if re.search(r"langsung|teramati|dijumpai|terpantau|jumlah individu", c[0] + " " + (c[2].get("satuan") or "").lower())]
            nama, nilai, ind = (langsung or kand)[0]
            out.append({
                "kegiatan_id": k["id"], "tahun": k["tahun"], "bulan": k["bulan"],
                "resort": k["resort"][0] if k["resort"] else "Tidak disebut",
                "nilai": nilai, "indikator": ind["nama"], "satuan": ind.get("satuan"),
                "jenis_angka": "teramati langsung" if langsung else "dugaan/estimasi",
            })
        return out

    seri_elang = seri("Elang flores", r"elang|individu|populasi|ekor")
    seri_rusa = seri("Rusa timor", r"rusa|individu|perjumpaan|populasi|ekor")
    kol = ["kegiatan_id", "tahun", "bulan", "resort", "nilai", "indikator", "satuan", "jenis_angka"]
    tulis_csv(OUT / "seri" / "elang_flores.csv", kol, seri_elang)
    tulis_csv(OUT / "seri" / "rusa_timor.csv", kol, seri_rusa)

    rusa_dc = [
        {"periode": "2020", "perjumpaan_langsung": 26, "jejak_min": None, "jejak_maks": None},
        {"periode": "2021", "perjumpaan_langsung": 21, "jejak_min": 8, "jejak_maks": 26},
        {"periode": "Mei 2022", "perjumpaan_langsung": 0, "jejak_min": 6, "jejak_maks": 46},
        {"periode": "Nov 2022", "perjumpaan_langsung": 3, "jejak_min": 6, "jejak_maks": 46},
    ]
    tulis_csv(OUT / "seri" / "rusa_doro_ncanga_2020_2022.csv", list(rusa_dc[0].keys()), rusa_dc)

    kehati = {s: [r for r in rows if any(str(v).strip() for v in r.values())]
              for s, rows in raw["kehati"].items()}
    nama_file = {"Aves": "burung", "Flora": "flora", "Mamal": "mamalia", "Orchid": "anggrek",
                 "Flora_May be Found": "flora_kemungkinan_ada"}
    for sheet, rows in kehati.items():
        kolom = list(dict.fromkeys(c for r in rows for c in r))
        tulis_csv(OUT / "kehati" / f"{nama_file[sheet]}.csv", kolom, rows)

    # Data kelompok binaan (diisi petugas memakai templat). Baris contoh diabaikan.
    kb_path = OUT / "kelompok_binaan" / "kelompok_binaan.csv"
    kelompok_binaan = []
    if kb_path.exists():
        with kb_path.open(encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                if not r.get("nama_kelompok") or r["nama_kelompok"].startswith("CONTOH"):
                    continue
                for c in ("tahun", "tahun_dibentuk", "jumlah_anggota", "anggota_perempuan", "pelatihan_jumlah"):
                    r[c] = int(float(r[c])) if r.get(c) else None
                for c in ("bantuan_nilai_rp", "produksi", "pendapatan_kelompok_rp", "pendapatan_rata_anggota_rp", "luas_areal_ha"):
                    r[c] = float(r[c]) if r.get(c) else None
                kelompok_binaan.append(r)

    # Ringkasan untuk dashboard.
    aves = kehati["Aves"]
    dash = {
        "dibangun_dari": "data/raw/ekstraksi_lpk_rpk.json",
        "folder_drive": DRIVE_FOLDER,
        "tema_urut": TEMA_URUT,
        "peran_urut": [p for p, _ in PERAN],
        "ancaman_urut": [a for a, _ in ANCAMAN],
        "resort_urut": [r for r, _ in RESORT],
        "wilayah": WILAYAH,
        "kegiatan": [{c: k[c] for c in (
            "id", "judul", "tahun", "bulan", "tanggal_pelaksanaan", "kategori", "tema", "sasaran", "resort",
            "wilayah", "nomor_st", "jumlah_personel", "mitra", "metode", "lokasi_detail", "ringkasan",
            "temuan_kunci", "ancaman", "rekomendasi", "keterlibatan_masyarakat", "peran_masyarakat",
            "tema_ancaman", "jenis_tercatat", "indikator", "berkas", "sumber")} for k in kegiatan],
        "seri": {"elang_flores": seri_elang, "rusa_timor": seri_rusa, "rusa_doro_ncanga": rusa_dc},
        "kehati": {
            "jumlah": {nama_file[s]: len(v) for s, v in kehati.items()},
            "burung_iucn": Counter(r.get("IUCN") or "Tidak ada data" for r in aves),
            "burung_lindung": Counter(r.get("P.106/2018") or "Tidak ada data" for r in aves),
            "burung_tipe": Counter(r.get("Tipe") or "Lainnya" for r in aves),
            "flora_invasif": sum(1 for r in kehati["Flora"] if str(r.get("Invasive")).lower() == "true"),
            "burung": aves,
            "anggrek": kehati["Orchid"],
        },
        "katalog": katalog,
        "kelompok_binaan": kelompok_binaan,
    }
    dash.update(bangun_penyuluhan())
    dash["dibangun_dari"] = ["data/raw/ekstraksi_lpk_rpk.json", "data/raw/ekstraksi_penyuluhan.json"]
    (OUT / "dashboard.json").write_text(json.dumps(dash, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    c = Counter(k["tahun"] for k in kegiatan)
    print(f"{len(kegiatan)} kegiatan; per tahun {sorted(c.items(), key=lambda x: x[0] or 0)}")
    print(f"seri elang {len(seri_elang)}, rusa {len(seri_rusa)}; katalog {len(katalog)} berkas")


def tulis_csv(path, kolom, baris):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=kolom)
        w.writeheader()
        for b in baris:
            w.writerow({c: b.get(c) for c in kolom})


# Ejaan desa dibakukan; dusun yang desanya jelas dari laporan digabung ke desanya.
DESA_EJAAN = {
    "soritatanga": "Sori Tatanga", "sori tatanga": "Sori Tatanga", "tolo kalo": "Tolokalo",
    "oibura": "Oi Bura", "kawinda to’i": "Kawinda Toi", "kawinda na’e": "Kawinda Nae",
}
DUSUN_KE_DESA = {
    "karyasari": "Sori Tatanga", "karya sari": "Sori Tatanga",
    "tompo jaya": "Tolokalo", "so tompo": "Tolokalo", "so tompo jaya": "Tolokalo",
    "pancasila": "Tambora", "bukit bunga": "Doropeti",
}


def norm_desa(nilai):
    hasil = []
    for v in nilai:
        t = v.strip()
        m = re.search(r"desa ([^,]+)", t, re.I)
        if m:
            t = m.group(1)
        else:
            t = re.sub(r"^dusun\s+", "", t, flags=re.I)
            t = DUSUN_KE_DESA.get(t.lower(), t)
        t = DESA_EJAAN.get(t.lower().strip(), t.strip())
        if t not in hasil:
            hasil.append(t)
    return hasil


def norm_sekolah(nama):
    t = re.sub(r"\b(SD|SMP|SMA|SMK)\s*(Negeri|N)\b", r"\1N", nama.strip())
    return re.sub(r"\b0+(\d)", r"\1", t)


def drive_url(fid):
    return f"https://drive.google.com/file/d/{fid}/view" if fid else None


def bangun_penyuluhan():
    """Folder Drive 2: laporan penyuluhan, pendampingan, dan monev kelompok binaan.

    Data mentah memakai kunci ringkas (lihat docs/04-catatan-kualitas-data.md).
    Fungsi ini menulis CSV/JSON yang mudah dibaca dan mengembalikan bagian dashboard.
    """
    raw = json.loads(RAW_PENYULUHAN.read_text(encoding="utf-8"))
    nama_kel = {k["id"]: k["nama"] for k in raw["kelompok"]}

    resort_kel = {k["id"]: k.get("resort") for k in raw["kelompok"]}
    keg = []
    for k in raw["kegiatan"]:
        # Laporan tanpa resort (biasanya tingkat SPTN) mewarisi resort kelompok yang dibahas.
        resort = k.get("r") or sorted({resort_kel[i] for i in k.get("kl", []) if resort_kel.get(i)},
                                      key=lambda r: [n for n, _ in RESORT].index(r))
        sekolah = [{"nama": norm_sekolah(s[0]), "jenjang": s[1] if len(s) > 1 else None,
                    "peserta": s[2] if len(s) > 2 else None} for s in k.get("sk", [])]
        keg.append({
            "id": k["id"],
            "judul": k["j"],
            "jenis_kegiatan": k["jk"],
            "kelompok_kegiatan": GRUP_PENYULUHAN[k["g"]],
            "tahun": k.get("t"),
            "bulan": k.get("b"),
            "tanggal": k.get("tg"),
            "resort": resort,
            "resort_dari_kelompok": not k.get("r") and bool(resort),
            "wilayah": sorted({WILAYAH[r] for r in resort if r in WILAYAH}),
            "desa": norm_desa(k.get("d", [])),
            "peserta": k.get("p"),
            "sekolah": sekolah,
            "kelompok_id": k.get("kl", []),
            "kelompok": [nama_kel[i] for i in k.get("kl", []) if i in nama_kel],
            "ringkasan": k["rs"],
            "temuan": k.get("tm", []),
            "kendala": k.get("kd", []),
            "rekomendasi": k.get("rk", []),
            "jumlah_berkas": k.get("nf"),
            "url": drive_url(k.get("u")),
        })
    keg.sort(key=lambda x: (x["tahun"] or 9999, x["bulan"] or 13, x["id"]))

    kel = []
    for g in raw["kelompok"]:
        riw = {}
        for th, r in sorted(g["riw"].items()):
            riw[th] = {
                "status": r.get("st") or "tidak disebut",
                # 0 di data mentah berarti jumlah tidak disebut, bukan kelompok tanpa anggota.
                "anggota": r.get("ang") or None,
                "anggota_perempuan": r.get("prm") if r.get("ang") else None,
                "penilaian": r.get("skor", []),
                "kondisi": r.get("kond"),
                "kendala": r.get("kend", []),
                "tema_kendala": r.get("kt", []),
                "kebutuhan": r.get("butuh", []),
                "bantuan": r.get("ban", []),
                "produk": r.get("prod", []),
                "pendapatan": r.get("pend"),
                "kegiatan": r.get("keg", []),
            }
        akhir = max(riw) if riw else None
        kel.append({
            "id": g["id"], "nama": g["nama"], "desa": (norm_desa([g["desa"]]) or [None])[0] if g.get("desa") else None,
            "resort": g.get("resort") or "Tidak disebut",
            "wilayah": WILAYAH.get(g.get("resort"), "Tidak disebut"),
            "jenis": g["jenis"], "usaha": g["usaha"], "ketua": g.get("ketua"),
            "dibentuk": g.get("dibentuk"), "dasar_pembentukan": g.get("dasar"),
            "tahun_terakhir": int(akhir) if akhir else None,
            "status_terakhir": riw[akhir]["status"] if akhir else None,
            "riwayat": riw,
        })

    # CSV untuk dibuka di spreadsheet.
    gabung = lambda xs: "; ".join(str(x) for x in xs if x)
    tulis_csv(OUT / "penyuluhan.csv",
              ["id", "tahun", "bulan", "judul", "jenis_kegiatan", "kelompok_kegiatan", "resort", "desa",
               "peserta", "kelompok", "sekolah", "ringkasan", "url"],
              [{**k, "resort": gabung(k["resort"]), "desa": gabung(k["desa"]), "kelompok": gabung(k["kelompok"]),
                "sekolah": gabung(s["nama"] for s in k["sekolah"])} for k in keg])
    tulis_csv(OUT / "kelompok.csv",
              ["id", "nama", "desa", "resort", "wilayah", "jenis", "usaha", "dibentuk", "dasar_pembentukan",
               "tahun_terakhir", "status_terakhir", "tahun_dilaporkan"],
              [{**g, "tahun_dilaporkan": gabung(g["riwayat"])} for g in kel])
    tulis_csv(OUT / "kelompok_riwayat.csv",
              ["kelompok_id", "nama", "tahun", "status", "anggota", "anggota_perempuan", "penilaian", "kondisi",
               "tema_kendala", "kendala", "kebutuhan", "bantuan", "produk", "jumlah_laporan"],
              [{"kelompok_id": g["id"], "nama": g["nama"], "tahun": th, **{c: r[c] for c in (
                  "status", "anggota", "anggota_perempuan", "kondisi")},
                "penilaian": gabung(r["penilaian"]), "tema_kendala": gabung(r["tema_kendala"]),
                "kendala": gabung(r["kendala"]), "kebutuhan": gabung(r["kebutuhan"]),
                "bantuan": gabung(r["bantuan"]), "produk": gabung(r["produk"]),
                "jumlah_laporan": len(r["kegiatan"])}
               for g in kel for th, r in g["riwayat"].items()])
    (OUT / "penyuluhan.json").write_text(json.dumps(keg, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT / "kelompok.json").write_text(json.dumps(kel, ensure_ascii=False, indent=1), encoding="utf-8")

    # Katalog folder 2: berkas mana yang dipakai oleh kegiatan mana.
    dipakai = defaultdict(list)
    for k in raw["kegiatan"]:
        if k.get("u"):
            dipakai[k["u"]].append(k["id"])
    katalog = [{"nama": nama, "ukuran_mb": mb, "kegiatan": gabung(dipakai.get(fid, [])),
                "dipakai_di_dashboard": "ya" if fid in dipakai else "tidak", "url": drive_url(fid)}
               for fid, nama, mb in raw["manifest"]]
    tulis_csv(OUT / "sumber_penyuluhan.csv", list(katalog[0].keys()), katalog)

    print(f"penyuluhan: {len(keg)} kegiatan, {len(kel)} kelompok, "
          f"{sum(len(g['riwayat']) for g in kel)} catatan kelompok-tahun, katalog {len(katalog)} berkas")
    return {
        "folder_drive_penyuluhan": DRIVE_FOLDER_PENYULUHAN,
        "grup_penyuluhan": GRUP_PENYULUHAN,
        "status_urut": STATUS_URUT,
        "kendala_urut": raw["kendala_urut"],
        "penyuluhan": keg,
        "kelompok": kel,
        "katalog_penyuluhan": katalog,
    }


if __name__ == "__main__":
    main()
