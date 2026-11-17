#!/usr/bin/env python3
"""Tulis ringkasan lengkap setiap laporan ke docs/laporan/*.md dan katalog sumber.

Jalankan setelah build_data.py:
    python3 scripts/build_docs.py
"""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs" / "laporan"
BULAN = ["", "Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus",
         "September", "Oktober", "November", "Desember"]
FILE_TEMA = {
    "Satwa": "satwa.md",
    "Flora & tumbuhan invasif": "flora-dan-tumbuhan-invasif.md",
    "Ekosistem & jasa lingkungan": "ekosistem-dan-jasa-lingkungan.md",
    "Masyarakat & pengelolaan": "masyarakat-dan-pengelolaan.md",
}


def daftar(judul, isi):
    if not isi:
        return ""
    return f"**{judul}**\n\n" + "\n".join(f"- {x}" for x in isi) + "\n\n"


def kartu(k):
    waktu = k["tanggal_pelaksanaan"] or " ".join(
        x for x in [BULAN[k["bulan"]] if k["bulan"] else "", str(k["tahun"] or "")] if x) or "tidak tercantum"
    resort = ", ".join(k["resort"]) or "tidak disebut"
    s = f"### {k['judul']}\n\n"
    s += f"| Waktu | Resort | Sasaran | Surat tugas | Personel |\n|---|---|---|---|---|\n"
    s += f"| {waktu} | {resort} | {k['sasaran']} | {k['nomor_st'] or '-'} | {k['jumlah_personel'] or '-'} |\n\n"
    s += f"{k['ringkasan']}\n\n"
    if k["metode"]:
        s += f"**Metode.** {k['metode']}\n\n"
    if k["lokasi_detail"]:
        s += f"**Lokasi.** {k['lokasi_detail']}\n\n"
    s += daftar("Temuan kunci", k["temuan_kunci"])
    ind = [i for i in k["indikator"] if i.get("nilai") not in (None, "")]
    if ind:
        s += "**Angka yang dilaporkan**\n\n| Indikator | Nilai | Satuan |\n|---|---|---|\n"
        for i in ind:
            s += f"| {i['nama']} | {i['nilai']} | {i.get('satuan') or ''} |\n"
        s += "\n"
    if k["jenis_tercatat"]:
        s += f"**Jenis tercatat ({len(k['jenis_tercatat'])}).** {', '.join(k['jenis_tercatat'])}\n\n"
    s += daftar("Ancaman dan kendala", k["ancaman"])
    s += daftar("Rekomendasi", k["rekomendasi"])
    if k["keterlibatan_masyarakat"]:
        s += f"**Keterlibatan masyarakat.** {k['keterlibatan_masyarakat']}\n\n"
    if k["mitra"]:
        s += f"**Mitra.** {', '.join(k['mitra'])}\n\n"
    src = k["sumber"] or {}
    s += f"**Berkas sumber.** {', '.join(k['berkas'])}"
    if src.get("url"):
        s += f" — [{src['nama']}]({src['url']})"
    if src.get("catatan"):
        s += f" _(catatan: {src['catatan']})_"
    return s + "\n\n---\n\n"


def main():
    kegiatan = json.loads((ROOT / "data" / "kegiatan.json").read_text(encoding="utf-8"))
    per_tema = defaultdict(list)
    for k in kegiatan:
        per_tema[k["tema"]].append(k)
    DOCS.mkdir(parents=True, exist_ok=True)
    indeks = ["# Ringkasan per laporan\n",
              "Setiap berkas di folder ini dibuat otomatis oleh `scripts/build_docs.py` dari `data/kegiatan.json`. "
              "Isinya adalah ringkasan terstruktur tiap LPK/RPK: waktu, lokasi, metode, angka, ancaman, rekomendasi, "
              "keterlibatan masyarakat, dan tautan ke berkas asli di Google Drive.\n"]
    for tema, nama in FILE_TEMA.items():
        isi = sorted(per_tema.get(tema, []), key=lambda k: (k["sasaran"], k["tahun"] or 0, k["bulan"] or 0))
        teks = f"# {tema}\n\n{len(isi)} laporan. Diurutkan menurut sasaran, lalu tahun.\n\n"
        sasaran = None
        for k in isi:
            if k["sasaran"] != sasaran:
                sasaran = k["sasaran"]
                teks += f"## {sasaran}\n\n"
            teks += kartu(k)
        (DOCS / nama).write_text(teks, encoding="utf-8")
        indeks.append(f"- [{tema}]({nama}) — {len(isi)} laporan")
    (DOCS / "README.md").write_text("\n".join(indeks) + "\n", encoding="utf-8")

    katalog = json.loads((ROOT / "data" / "dashboard.json").read_text(encoding="utf-8"))["katalog"]
    t = ["# Katalog berkas sumber di Google Drive\n",
         f"Folder asal: {json.loads((ROOT / 'data' / 'dashboard.json').read_text())['folder_drive']} "
         f"(subfolder `LAP_Teknis`, {len(katalog)} berkas). Berkas asli tidak disalin ke repo karena ukurannya "
         "sekitar 2,3 GB; repo hanya menyimpan hasil kurasinya.\n",
         "| # | Berkas | Ukuran (MB) | Isi | Dipakai | Catatan |", "|---|---|---|---|---|---|"]
    for i, m in enumerate(katalog, 1):
        isi = f"{m['jumlah_berkas_di_dalam']} berkas: {m['contoh_isi']}" if m["jumlah_berkas_di_dalam"] else "-"
        t.append(f"| {i} | [{m['nama']}]({m['url']}) | {m['ukuran_mb']} | {isi} | {m['dipakai_di_dashboard']} | {m['catatan']} |")
    (ROOT / "docs" / "katalog-sumber.md").write_text("\n".join(t) + "\n", encoding="utf-8")
    print("docs/laporan dan docs/katalog-sumber.md ditulis")
    tulis_penyuluhan()


GRUP_FILE = {
    "Pendampingan & monev kelompok": "penyuluhan-pendampingan-dan-monev.md",
    "Kemitraan & kesepakatan konservasi": "penyuluhan-kemitraan-konservasi.md",
    "Edukasi & kader konservasi": "penyuluhan-edukasi-dan-kader.md",
    "Sosialisasi & lainnya": "penyuluhan-sosialisasi.md",
}
STATUS_IKON = {"aktif": "🟢 aktif", "kurang aktif": "🟡 kurang aktif", "tidak aktif": "🔴 tidak aktif",
               "baru dibentuk": "🔵 baru dibentuk", "tidak disebut": "⚪ tidak disebut"}


def waktu_teks(k):
    return k.get("tanggal") or " ".join(
        x for x in [BULAN[k["bulan"]] if k.get("bulan") else "", str(k["tahun"] or "")] if x) or "tidak tercantum"


def kartu_penyuluhan(k):
    s = f"### {k['judul']}\n\n"
    s += "| Waktu | Jenis | Resort | Desa | Peserta |\n|---|---|---|---|---|\n"
    s += (f"| {waktu_teks(k)} | {k['jenis_kegiatan']} | {', '.join(k['resort']) or '-'} | "
          f"{', '.join(k['desa']) or '-'} | {k['peserta'] or '-'} |\n\n")
    s += f"{k['ringkasan']}\n\n"
    if k["kelompok"]:
        s += f"**Kelompok yang dibahas.** {', '.join(k['kelompok'])}\n\n"
    if k["sekolah"]:
        s += "**Sekolah.** " + ", ".join(
            x["nama"] + (f" ({x['peserta']} siswa)" if x.get("peserta") else "") for x in k["sekolah"]) + "\n\n"
    s += daftar("Temuan", k["temuan"])
    s += daftar("Kendala", k["kendala"])
    s += daftar("Rekomendasi", k["rekomendasi"])
    if k["url"]:
        s += f"**Berkas sumber.** [buka di Google Drive]({k['url']}) ({k['jumlah_berkas'] or '?'} berkas di dalam arsip)"
    return s + "\n\n---\n\n"


def tulis_penyuluhan():
    dash = json.loads((ROOT / "data" / "dashboard.json").read_text(encoding="utf-8"))
    keg, kel = dash["penyuluhan"], dash["kelompok"]

    per_grup = defaultdict(list)
    for k in keg:
        per_grup[k["kelompok_kegiatan"]].append(k)
    baris = []
    for grup, nama in GRUP_FILE.items():
        isi = sorted(per_grup.get(grup, []), key=lambda k: (k["tahun"] or 9999, k["bulan"] or 13))
        teks = f"# {grup}\n\n{len(isi)} laporan dari folder penyuluhan dan pemberdayaan. Diurutkan menurut tahun.\n\n"
        tahun = "awal"
        for k in isi:
            if k["tahun"] != tahun:
                tahun = k["tahun"]
                teks += f"## {tahun or 'Tahun tidak tercantum'}\n\n"
            teks += kartu_penyuluhan(k)
        (DOCS / nama).write_text(teks, encoding="utf-8")
        baris.append(f"- [{grup}]({nama}) — {len(isi)} laporan")
    readme = DOCS / "README.md"
    readme.write_text(readme.read_text(encoding="utf-8").rstrip() + "\n\n## Penyuluhan dan pemberdayaan\n\n"
                      "Dibuat dari `data/penyuluhan.json` (folder Drive kedua).\n\n" + "\n".join(baris) + "\n",
                      encoding="utf-8")

    # Profil kelompok binaan, satu bagian per kelompok, riwayat per tahun.
    ref = {k["id"]: k for k in keg}
    tahun_semua = sorted({t for g in kel for t in g["riwayat"]})
    out = ["# Profil kelompok binaan\n",
           f"{len(kel)} kelompok yang muncul di laporan pendampingan, monev, dan pembentukan kelompok. "
           "Dibuat otomatis oleh `scripts/build_docs.py` dari `data/kelompok.json`. "
           "Kotak kosong pada tabel berarti kelompok tidak dibahas di laporan tahun itu, bukan berarti tidak aktif.\n",
           "Keterangan: " + " · ".join(STATUS_IKON.values()) + "\n",
           "| Kelompok | Desa | Resort | " + " | ".join(tahun_semua) + " |",
           "|---|---|---|" + "---|" * len(tahun_semua)]
    urut = sorted(kel, key=lambda g: (g["resort"], g["nama"]))
    for g in urut:
        sel = [STATUS_IKON[g["riwayat"][t]["status"]].split()[0] if t in g["riwayat"] else "" for t in tahun_semua]
        jangkar = g["id"]
        out.append(f"| [{g['nama']}](#{jangkar}) | {g['desa'] or '-'} | {g['resort']} | " + " | ".join(sel) + " |")
    out.append("")
    resort = None
    for g in urut:
        if g["resort"] != resort:
            resort = g["resort"]
            out.append(f"## Resort {resort}\n")
        out.append(f'<a id="{g["id"]}"></a>\n### {g["nama"]}\n')
        out.append(f"| Desa | Jenis | Usaha | Dibentuk | Dasar |\n|---|---|---|---|---|\n"
                   f"| {g['desa'] or '-'} | {g['jenis']} | {g['usaha']} | {g['dibentuk'] or '-'} | {g['dasar_pembentukan'] or '-'} |\n")
        for t, r in g["riwayat"].items():
            kepala = f"**{t} · {STATUS_IKON[r['status']]}**"
            if r["anggota"]:
                kepala += f" · {r['anggota']} anggota" + (f" ({r['anggota_perempuan']} perempuan)" if r["anggota_perempuan"] else "")
            out.append(kepala + "\n")
            if r["kondisi"]:
                out.append(r["kondisi"] + "\n")
            for judul, isi in (("Penilaian", r["penilaian"]), ("Kendala", r["kendala"]), ("Kebutuhan", r["kebutuhan"]),
                               ("Bantuan yang tercatat", r["bantuan"]), ("Produk/usaha", r["produk"])):
                if isi:
                    out.append(f"- *{judul}:* " + "; ".join(isi))
            if r["kegiatan"]:
                out.append("- *Laporan:* " + ", ".join(
                    f"[{ref[i]['judul'][:60]}]({ref[i]['url']})" if ref.get(i, {}).get("url") else i
                    for i in r["kegiatan"] if i in ref))
            out.append("")
    (ROOT / "docs" / "kelompok-binaan.md").write_text("\n".join(out) + "\n", encoding="utf-8")

    kat = dash["katalog_penyuluhan"]
    t = ["# Katalog berkas penyuluhan dan pemberdayaan\n",
         f"Folder asal: {dash['folder_drive_penyuluhan']} ({len(kat)} berkas, sekitar "
         f"{sum(m['ukuran_mb'] for m in kat) / 1000:.1f} GB). Berkas asli tidak disalin ke repo.\n",
         "| # | Berkas | Ukuran (MB) | Kegiatan di data | Dipakai |", "|---|---|---|---|---|"]
    for i, m in enumerate(kat, 1):
        t.append(f"| {i} | [{m['nama']}]({m['url']}) | {m['ukuran_mb']} | {m['kegiatan'] or '-'} | {m['dipakai_di_dashboard']} |")
    (ROOT / "docs" / "katalog-sumber-penyuluhan.md").write_text("\n".join(t) + "\n", encoding="utf-8")
    print("docs/laporan/penyuluhan-*.md, docs/kelompok-binaan.md, docs/katalog-sumber-penyuluhan.md ditulis")


if __name__ == "__main__":
    main()
