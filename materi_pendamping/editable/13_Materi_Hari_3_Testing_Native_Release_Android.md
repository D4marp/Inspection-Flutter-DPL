# Materi Hari 3 — Flutter WebView, Agent Skill, dan Migrasi Kotlin

**Trainer dan Pembuat Buku:** Damar Galih Aji Pradana, S.Tr.Kom.

> Proyek praktik: `flutter_projects/hari_3_dpl_inspection_release`

## Outcome

Peserta tidak diminta rewrite seluruh aplikasi. Targetnya satu vertical slice
yang kecil, dapat diuji, dan dapat ditelusuri dari legacy Kotlin ke Flutter.
WebView dipelajari sebagai bounded surface. AI agent dipakai melalui skill dan
human review gate.

## Rundown 6,5 jam

| Waktu | Topik | Evidence |
|---|---|---|
| 08.30–09.15 | Inventory legacy | Behavior map + unknown |
| 09.15–10.00 | PRD slice | AC → evidence matrix |
| 10.15–11.15 | Kotlin → Flutter mapping | Architecture map |
| 11.15–12.00 | Agent Skill | Skill + context pack + prompt |
| 13.00–14.00 | WebView implementation | Situs latihan + states |
| 14.00–14.45 | Security boundary | HTTPS allowlist + external block |
| 14.45–15.45 | Migration lab | Slice + tests |
| 15.45–16.30 | Build, parity review, handover | Evidence + gap |

## 1. Inventory sebelum coding

Untuk slice daftar → detail, baca hanya file yang relevan: Activity/Fragment,
XML, ViewModel/LiveData, Retrofit/DTO/repository, navigation graph, storage, dan
test. Catat:

- trigger pengguna;
- input dan output;
- state loading/data/empty/error;
- navigation/back;
- network/storage side effect;
- behavior yang belum dapat dipastikan.

Unknown adalah temuan penting. Jangan meminta agent menebak.

## 2. PRD vertical slice

PRD minimum berisi problem, user outcome, source of truth, in/out of scope,
acceptance criteria, evidence, dependency, risk, dan next slice.

```text
Legacy behavior → PRD AC → Flutter file → Test/smoke evidence → Gap
```

Challenge: pilih satu Fragment. Tulis tiga AC positif, dua failure AC, dan satu
out-of-scope. Reviewer harus dapat mengatakan “lulus/gagal” tanpa menebak.

## 3. Mapping Kotlin ke Flutter

| Android Kotlin | Flutter | Review question |
|---|---|---|
| Activity/Fragment | Screen + route | Siapa pemilik navigation? |
| XML/RecyclerView | Widget tree/ListView | Apakah constraints aman? |
| ViewModel/LiveData | Controller/state | Kapan load/dispose? |
| Retrofit | ApiClient | Method/status/payload sama? |
| Repository | Repository | Remote/cache policy sama? |
| SharedPreferences | explicit storage | Data/session kapan dihapus? |
| Intent/deep link | route/deep link | Input tervalidasi? |

Migrasi dilakukan per vertical slice. Architecture target boleh berbeda selama
observable behavior dan contract yang disetujui tetap dipenuhi.

## 4. Agent Skill

Skill berada di `.agents/skills/migrate-kotlin-slice/SKILL.md`. Tool dapat
menemukan skill dari folder `.agents/skills` dan memuat instruksi ketika relevan.

```text
Gunakan skill migrate-kotlin-slice.
Goal: migrasikan daftar → detail.
Source of truth: PRD + source Kotlin/XML + OpenAPI.
Constraints: jangan ubah contract; satu slice; no secret.
Evidence: AC mapping, patch kecil, analyze/test, gap.
```

Context pack tidak boleh memuat `.env`, key/token, keystore, credential, dump,
atau log sensitif. Reviewer memeriksa diff dan command output; kata “done” dari
agent bukan quality gate.

## 5. WebView Flutter

Package modern memisahkan `WebViewController` dan `WebViewWidget`. Project
latihan menambahkan boundary yang lebih mudah dibedah:

```text
webview/navigation_policy.dart
webview/migration_webview_controller.dart
screens/training_webview_screen.dart
```

Policy adalah pure function yang dapat diuji tanpa platform view. Controller
memegang konfigurasi WebView, sedangkan screen hanya merender state.

```dart
static bool allows(String rawUrl) {
  if (rawUrl == 'about:blank') return true;
  final uri = Uri.tryParse(rawUrl);
  return uri != null &&
      uri.scheme == 'https' &&
      {'presisirencar.com', 'www.presisirencar.com'}.contains(uri.host);
}
```

Controller membuka `https://www.presisirencar.com/`. JavaScript aktif karena
situs memakai interaksi Next.js, tetapi aplikasi tidak membuat JavaScript
bridge. Implementasikan progress, error, reload, dan browser back. Allowlist
harus membandingkan scheme dan host secara exact; jangan memakai `contains` pada
string URL. Untuk produksi, tambah kebijakan session/logout, deep link, upload/
download, observability, dan threat review.

Challenge: klik tautan WhatsApp/Google Maps dan buktikan
`NavigationDelegate` menolak. Ubah satu aturan secara sengaja, tulis test/manual
evidence yang menangkap regresi, lalu pulihkan. Setelah policy lulus, uji
controller dan `WebViewWidget` pada emulator/device.

## 6. Migration lab

1. Buka tab PRD dalam aplikasi.
2. Petakan satu behavior Kotlin ke target Flutter.
3. Gunakan Agent Skill dengan context minimum.
4. Review plan sebelum patch.
5. Implementasikan perubahan kecil.
6. Jalankan format/analyze/test.
7. Smoke test PRD, WebView, target daftar/detail, dan skill screen.
8. Catat parity, gap, risiko, owner, dan next slice.

## 7. Quality gate dan build

```sh
cd flutter_projects/hari_3_dpl_inspection_release
fvm dart format --output=none --set-exit-if-changed lib test
fvm flutter analyze
fvm flutter test
fvm flutter build apk --debug
```

Device/emulator test tetap dibutuhkan untuk WebView platform implementation,
back behavior, dan plugin foto. Widget test tidak membuktikan semua integrasi
native.

## Handover

- PRD slice dan behavior map.
- Agent Skill serta contoh prompt yang telah disanitasi.
- Mapping AC → file/test/evidence.
- Hasil analyze/test/build.
- Daftar gap, risiko, owner, dan next slice.
- Catatan WebView origin/JavaScript/session.

Selesai berarti dapat direview dan direproduksi, bukan sekadar berhasil tampil
pada satu device trainer.
