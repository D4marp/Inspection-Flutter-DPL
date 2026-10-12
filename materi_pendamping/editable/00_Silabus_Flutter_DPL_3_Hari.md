# Silabus Profesional Flutter DPL — 3 Hari

**Trainer dan Pembuat Buku:** Damar Galih Aji Pradana, S.Tr.Kom.

## Tujuan program

Program tiga hari ini memindahkan peserta dari fondasi Dart/Flutter ke aplikasi
CRUD, lalu ke migrasi Android Kotlin berbasis PRD dengan WebView dan AI coding
agent. Setiap hari berdurasi 6–7 jam dan memiliki challenge, evidence, review,
serta quality gate agar kelas tidak selesai hanya karena live coding selesai.

## Outcome akhir

- Hari 1: peserta mampu membangun UI Flutter dan form tervalidasi.
- Hari 2: peserta mampu menghubungkan UI ke open CRUD API, picker, dan OpenCode.
- Hari 3: peserta mampu merencanakan/membuktikan satu slice migrasi Kotlin,
  membatasi WebView, dan memakai Agent Skill secara aman.

## Peta tiga hari

| Hari | Fokus | Output utama |
|---|---|---|
| 1 | Dart, widget, layout, navigation, form | App list/detail/form lokal |
| 2 | UI composition, full CRUD, picker, OpenCode/API key | App CRUD + evidence API/picker/AI setup |
| 3 | PRD migrasi Kotlin, WebView, Agent Skill, quality gate | Migration Lab + PRD + skill + build |

## Metode pembelajaran

Setiap blok mengikuti pola singkat: konsep → live trace → guided lab → challenge
mandiri/pair → review evidence. Trainer tidak memberi solusi lengkap di awal.
Peserta harus mengembangkan source: variasi UI, failure scenario, test, dan
perbaikan berdasar review.

## Hari 1 — Fondasi Flutter profesional

| Waktu | Materi | Challenge |
|---|---|---|
| 08.30–09.15 | Toolchain, project anatomy, Dart essentials | Trace entry point dan widget tree |
| 09.15–10.00 | Stateless/Stateful, state lokal | Ubah state tanpa global mutable data |
| 10.15–11.30 | Scaffold, AppBar, layout constraints | Rebuild screen dari wireframe |
| 11.30–12.00 | List, Card, navigation | Tambah empty state |
| 13.00–14.15 | Form dan validation | Dynamic rule berdasarkan kondisi |
| 14.15–15.15 | Detail, routing, responsive UI | Narrow screen + long text |
| 15.15–16.00 | Debug dan widget test awal | Buat test gagal lalu perbaiki |
| 16.00–16.30 | Demo dan checkpoint | Tag day-1 + evidence |

## Hari 2 — UI, CRUD, picker, dan OpenCode

| Waktu | Materi | Challenge/evidence |
|---|---|---|
| 08.30–09.00 | Review baseline | Jelaskan ownership tiap widget/layer |
| 09.00–10.00 | Scaffold/AppBar/Row/Column/Form | UI responsive + validation |
| 10.15–12.00 | JSONPlaceholder, mapper, GET/POST | Public API + simulated write |
| 13.00–14.15 | PUT/DELETE dan controller state | Full CRUD end-to-end |
| 14.15–15.00 | Image/file picker | Preview, metadata, cancel/error |
| 15.00–15.40 | OpenCode install, `/connect`, `/models` | Setup tanpa expose key |
| 15.40–16.15 | Agent-assisted challenge | Patch kecil + review diff/test |
| 16.15–16.30 | Quality gate | Flutter/API tests + no-secret audit |

## Hari 3 — WebView dan migrasi Kotlin berbasis PRD

| Waktu | Materi | Challenge/evidence |
|---|---|---|
| 08.30–09.15 | Inventory legacy Kotlin/XML | Behavior map dan unknown list |
| 09.15–10.00 | PRD vertical slice dan traceability | AC → evidence matrix |
| 10.15–11.15 | Mapping Activity/XML/ViewModel/Retrofit | Kotlin → Flutter architecture map |
| 11.15–12.00 | Agent Skill `migrate-kotlin-slice` | Context pack + safe prompt |
| 13.00–14.00 | WebView controller/widget | presisirencar.com + loading/error/back |
| 14.00–14.45 | WebView security | HTTPS exact-host allowlist + external block |
| 14.45–15.45 | Migration lab | Implement satu slice + tests |
| 15.45–16.15 | Analyze/test/build dan parity review | Evidence, gap, next slice |
| 16.15–16.30 | Handover | PRD, skill, release notes |

## Challenge bank

- Ubah layout untuk text scale 200% tanpa overflow.
- Tambahkan search/filter tanpa memindahkan HTTP ke widget.
- Simulasikan 500, timeout, invalid JSON, dan cache fallback dengan evidence.
- Jelaskan beda selected, previewed, persisted, dan uploaded.
- Review output agent dan temukan asumsi contract yang tidak didukung source.
- Buat allowlist WebView dan buktikan external navigation ditolak.
- Petakan satu Fragment Kotlin menjadi route/screen Flutter dan tulis gap.

## Evaluasi

| Aspek | Bobot |
|---|---:|
| Perilaku aplikasi dan acceptance | 35% |
| Arsitektur/boundary | 20% |
| Failure handling dan security | 20% |
| Test/build evidence | 15% |
| Penjelasan dan handover | 10% |

Peserta lulus bila acceptance inti terpenuhi dan tidak ada pelanggaran secret atau
security boundary. Stretch challenge meningkatkan kedalaman, bukan menutup
kegagalan requirement inti.

## Prasyarat trainer

- Flutter/FVM, Android SDK/Xcode sesuai target tersedia sebelum kelas.
- Akses HTTPS ke JSONPlaceholder telah diuji sebelum kelas.
- OpenCode 1 stable telah diuji; akun/provider disiapkan masing-masing peserta.
- API key tidak dimasukkan ke slide, source, atau chat kelompok.
- Source Kotlin contoh dan contract API telah disanitasi.
- Device/emulator untuk smoke test WebView dan picker tersedia.

## Artefak paket

- Tiga PPT profesional dengan speaker notes.
- Tiga PRD dan tiga modul harian dalam Markdown/PDF.
- Proyek Flutter Hari 1–3.
- JSONPlaceholder public API dan tutorial implementasi per file.
- Agent Skill `.agents/skills/migrate-kotlin-slice/SKILL.md` pada proyek Hari 3.
