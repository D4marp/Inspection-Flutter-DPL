# Materi Hari 2 — Flutter CRUD Public API, Picker, dan OpenCode

**Trainer dan Pembuat Buku:** Damar Galih Aji Pradana, S.Tr.Kom.

> Proyek: `flutter_projects/hari_2_dpl_inspection_api`
> API: `https://jsonplaceholder.typicode.com`

## Outcome dan rundown

| Waktu | Topik | Evidence |
|---|---|---|
| 08.30–09.00 | Review Hari 1 | Baseline list/detail/form |
| 09.00–10.00 | Scaffold/AppBar/Row/Column/Form | UI responsive + validation |
| 10.15–10.45 | JSONPlaceholder dan batas simulasi | curl GET/POST/PUT/DELETE |
| 10.45–12.00 | Model, mapper, ApiClient | Mapping + mock tests |
| 13.00–14.15 | Repository, controller, CRUD UI | Full simulated CRUD |
| 14.15–15.00 | Image/file picker | Preview, metadata, cancel |
| 15.00–15.40 | OpenCode dan API key | `/connect`, `/models`, safe setup |
| 15.40–16.30 | Challenge dan quality gate | Tests, APK, explanation |

## 1. UI foundation

`Scaffold` adalah shell page. `AppBar` memberi konteks. `Row` dan `Column`
bekerja di dalam constraints sehingga text dinamis perlu `Expanded`, `Flexible`,
atau `Wrap`. `Form` memvalidasi sebelum mengirim intent ke controller.

Challenge UI: buat tiga summary card responsive, form dengan disabled submitting
state, dan validation yang tetap dapat dijangkau ketika keyboard terbuka.

## 2. Kenali JSONPlaceholder

Verifikasi endpoint publik:

```sh
curl 'https://jsonplaceholder.typicode.com/posts?_limit=2'

curl -X POST 'https://jsonplaceholder.typicode.com/posts' \
  -H 'Content-Type: application/json' \
  -d '{"title":"PMP-900","body":"Simulasi","userId":1}'
```

POST mengembalikan 201 dan ID baru, tetapi record itu tidak dapat dibaca kembali.
PUT/DELETE juga mengembalikan response sukses tanpa mengubah data server. Ini
ideal untuk latihan HTTP/UI state, bukan untuk persistence production.

## 3. Pembuatan per file

### `models/inspection.dart`

Mendefinisikan model domain dan enum kondisi. JSON cache internal memakai
`fromJson/toJson`. Model tidak mengenal `/posts`.

### `data/json_placeholder_mapper.dart`

Memetakan `{userId,id,title,body}` menjadi `Inspection`. Saat write, mapper
menghasilkan `title/body/userId` dan field domain agar simulated response dapat
dipetakan kembali.

### `data/crud/` — satu file per operasi

Empat operasi dipisah agar trainer dapat membuka dan menguji satu intent pada
satu waktu:

```text
read_inspections.dart    → GET    /posts?_limit=20 → 200
create_inspection.dart   → POST   /posts           → 201
update_inspection.dart   → PUT    /posts/{id}      → 200
delete_inspection.dart   → DELETE /posts/{id}      → 200/204
```

Semua operasi memakai `JsonResponseDecoder` dan `ApiException` yang sama.
Masing-masing class memiliki method `call()` sehingga dapat dipanggil dan
dites secara mandiri.

### `data/api_client.dart`

Menjadi facade tipis yang mendelegasikan `fetch/create/update/delete` ke empat
operation object. Repository tetap memiliki satu dependency sederhana tanpa
mengubah file CRUD menjadi satu god object.

### `data/inspection_repository.dart`

Menentukan remote/cache policy. GET sukses ditulis ke cache. Timeout/network
dapat memakai cache read-only. Write selalu menuju public API dan tidak masuk
offline queue.

### `controllers/inspection_controller.dart`

Mengelola loading, submitting, cached, error, dan list mutation. Create/update/
delete mengubah state lokal menggunakan response API. Refresh mengganti state
dengan data publik lagi.

### `app.dart`

Composition root yang membuat `ApiClient` dan `InspectionRepository` satu kali.
Base URL default adalah HTTPS JSONPlaceholder. Tidak ada login karena endpoint
publik tidak membutuhkan auth.

### `screens/home_screen.dart`

Merender loading/data/empty/error/cache serta aksi CRUD. Banner simulasi selalu
terlihat. Tombol reset memanggil GET ulang.

### `screens/inspection_form_screen.dart`

Satu form untuk Create/Update. Image/file picker hanya state lokal; tidak masuk
request JSON.

### `test/json_placeholder_api_test.dart`

Memakai `MockClient` untuk menguji URL, method, mapping, payload, dan status
tanpa internet. Tutorial rinci dan snippet lengkap tersedia di
`flutter_projects/hari_2_dpl_inspection_api/docs/JSONPLACEHOLDER_PER_FILE.md`.

## 4. Arsitektur

```text
Screen → Controller → Repository → ApiClient facade
                                      ↓
             Read / Create / Update / Delete operation
                                      ↓
             JsonPlaceholderMapper → Inspection
```

Widget tidak melakukan `http`, `jsonDecode`, atau membaca status code.

## 5. Image/file picker

```dart
final image = await ImagePicker().pickImage(
  source: ImageSource.gallery,
  maxWidth: 1600,
  imageQuality: 82,
);

final file = await FilePicker.pickFile();
```

Selected/previewed bukan uploaded. Tangani cancel, permission/error, ukuran file,
dan lifecycle. Scope Hari 2 berhenti pada preview/metadata.

## 6. OpenCode dan API key

```sh
brew install anomalyco/tap/opencode
opencode
```

Di TUI gunakan `/connect` dan `/models`. API key adalah credential developer
tool, bukan secret yang ditaruh di Flutter. Fitur AI produksi harus memakai
layanan tepercaya organisasi untuk policy, quota, redaction, audit, dan rotasi key.

## Challenge kelas

1. Parameterkan `_limit` dan validasi range.
2. Tambahkan search/filter lokal.
3. Tambahkan badge `SIMULATED` untuk hasil write.
4. Fake response 500 dan buktikan cache/retry.
5. Ganti mapper `/posts` menjadi `/todos` tanpa mengubah UI.
6. Tulis PRD migrasi dari simulasi ke layanan persistent.

## Quality gate

```sh
cd flutter_projects/hari_2_dpl_inspection_api
fvm dart format --output=none --set-exit-if-changed lib test
fvm flutter analyze
fvm flutter test
fvm flutter build apk --debug
```

Peserta menyerahkan demo empat HTTP method, penjelasan per file, hasil test/build,
serta bukti bahwa perubahan write hilang setelah reset.
