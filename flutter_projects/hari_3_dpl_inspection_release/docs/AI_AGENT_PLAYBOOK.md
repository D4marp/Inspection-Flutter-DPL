# AI Agent Playbook — Migrasi Kotlin ke Flutter

## Prinsip

Agent mempercepat pekerjaan yang sudah dibatasi oleh PRD; agent tidak menentukan
contract bisnis secara sepihak. Semua perubahan harus dapat ditelusuri dari
perilaku lama, acceptance criterion, patch, dan bukti verifikasi.

## Agent Skill proyek

Skill tersedia di `.agents/skills/migrate-kotlin-slice/SKILL.md`. Folder ini
dapat ditemukan oleh OpenCode. Skill memaksa urutan kerja berikut:

1. Baca PRD, source Kotlin/XML relevan, contract, target Flutter, dan test.
2. Ringkas perilaku teramati serta unknown; jangan mengisi unknown dengan asumsi.
3. Petakan perilaku ke acceptance criteria dan evidence.
4. Buat rencana patch kecil per vertical slice.
5. Implementasikan hanya perubahan yang disetujui PRD.
6. Jalankan format, analyze, dan test yang relevan.
7. Laporkan perubahan, evidence, risiko, dan next slice.

## Context pack minimum

```text
PRD_MIGRASI_KOTLIN.md
legacy/.../InspectionListFragment.kt
legacy/.../fragment_inspection_list.xml
legacy/.../InspectionViewModel.kt
contract/openapi.yaml
lib/src/screens/...
test/...
```

Jangan memasukkan `.env`, API key, token, database dump, keystore, credential,
atau log pengguna ke context/prompt.

## Prompt latihan

```text
Gunakan skill migrate-kotlin-slice.

Goal: migrasikan daftar → detail inspeksi.
Source of truth: PRD dan contract API yang dilampirkan.
Constraints: jangan mengubah endpoint/payload; jangan menambah dependency tanpa
alasan; satu vertical slice; pertahankan error/loading/empty behavior.
Evidence: mapping AC → file/test, flutter analyze, flutter test, dan daftar gap.
```

## Human review gate

- Apakah agent membaca file yang tepat dan menyebut unknown?
- Apakah setiap perubahan punya AC?
- Apakah patch kecil dan dapat di-review?
- Apakah WebView origin/JavaScript/navigation lebih longgar dari PRD?
- Apakah output menyebut command test yang benar-benar dijalankan?
- Apakah secret atau data sensitif masuk diff/log?

Agent output tidak dianggap selesai sebelum reviewer memeriksa diff dan evidence.

## Target file WebView pada slice latihan

```text
lib/src/webview/navigation_policy.dart
lib/src/webview/migration_webview_controller.dart
lib/src/screens/training_webview_screen.dart
```

Agent tidak boleh melonggarkan `TrainingNavigationPolicy` hanya untuk membuat
demo berhasil. Baseline hanya HTTPS ke `presisirencar.com` dan
`www.presisirencar.com`; JavaScript aktif tanpa bridge. Perubahan origin,
scheme, session, bridge, atau upload harus kembali ke PRD dan mendapat review
manusia.
