# PRD Hari 2 — Flutter CRUD dengan JSONPlaceholder

**Trainer dan Pembuat Buku:** Damar Galih Aji Pradana, S.Tr.Kom.

## Tujuan

Peserta mengembangkan checkpoint Hari 1 menjadi aplikasi Flutter yang mempunyai
page shell/form yang rapi, terhubung ke API publik open-source JSONPlaceholder,
dapat memilih gambar/file, serta memakai OpenCode tanpa membocorkan API key.

## API utama

```text
https://jsonplaceholder.typicode.com
```

JSONPlaceholder tidak membutuhkan akun atau API key dan mendukung HTTP method
GET, POST, PUT, PATCH, dan DELETE. Resource yang dipakai adalah `/posts`.

Write bersifat simulasi: response POST/PUT/DELETE dapat dipakai untuk latihan
state UI, tetapi perubahan tidak disimpan permanen. Refresh mengembalikan data
public API. Batas ini harus terlihat pada aplikasi dan dijelaskan oleh peserta.

## Output wajib

- UI dengan `Scaffold`, `AppBar`, `Row`, `Column`, `Form`, dan validation.
- GET `/posts?_limit=20` dipetakan menjadi daftar inspection.
- POST `/posts`, PUT `/posts/{id}`, dan DELETE `/posts/{id}` berjalan.
- Mapper terpisah antara schema Post dan model domain Inspection.
- Read, Create, Update, dan Delete berada dalam empat operation file terpisah.
- Banner simulasi selalu terlihat pada tab CRUD.
- Image preview dan file metadata dengan label belum di-upload.
- OpenCode terpasang; API key tidak berada di Flutter.
- Format, analyze, tests, dan APK debug lulus.

## Contract latihan

| Intent | Method | Path | Status | Persistence |
|---|---|---|---:|---|
| Read | GET | `/posts?_limit=20` | 200 | data publik |
| Create | POST | `/posts` | 201 | simulasi |
| Update | PUT | `/posts/{id}` | 200 | simulasi |
| Delete | DELETE | `/posts/{id}` | 200 | simulasi |

## Mapping schema

| JSONPlaceholder | Inspection |
|---|---|
| `id` | `id` dan kode fallback `POST-001` |
| `userId` | lokasi fallback `User 1` |
| `body` | catatan fallback |
| `title` | field standar saat write |
| field tambahan `assetCode/location/condition/note` | nilai domain simulated response |

Mapping berada di `json_placeholder_mapper.dart`, bukan di widget atau model.

## Functional requirements

| ID | Kebutuhan |
|---|---|
| D2-01 | Aplikasi langsung membuka Home tanpa login palsu |
| D2-02 | GET menampilkan loading, data/empty, error, retry, dan cache |
| D2-03 | POST valid menambah simulated response ke state lokal |
| D2-04 | PUT mengganti item berdasarkan ID |
| D2-05 | DELETE meminta konfirmasi dan menghapus item lokal setelah status 200 |
| D2-06 | Refresh/reset mengembalikan daftar public API |
| D2-07 | UI menjelaskan bahwa write tidak persisten |
| D2-08 | Network/timeout/invalid JSON dipetakan ke pesan yang dapat ditindaklanjuti |
| D2-09 | Image/file picker menangani sukses dan cancel tanpa crash |
| D2-10 | API key AI tidak masuk source, asset, build, log, atau screenshot |

## Acceptance criteria

| ID | Evidence lulus |
|---|---|
| AC1 | GET public API menghasilkan daftar inspection |
| AC2 | Unit test membuktikan Post → Inspection mapping |
| AC3 | Create memberi ID 101 dan item tampil lokal |
| AC4 | Update memakai `/posts/{id}` dan response mengganti item |
| AC5 | Delete dapat dibatalkan; status 200 menghapus item lokal |
| AC6 | Reset membuktikan perubahan write tidak persisten |
| AC7 | Banner simulasi terlihat sebelum peserta menjalankan write |
| AC8 | Empat operasi CRUD berada pada empat file; `ApiClient` hanya menjadi facade |
| AC9 | Picker tidak dikirim ke JSONPlaceholder |
| AC10 | `flutter analyze` bersih dan seluruh test hijau |
| AC11 | APK debug berhasil dibangun |
| AC12 | Git diff bebas API key/token/credential nyata |

## Definition of done

Empat method CRUD dapat didemokan, batas simulasi dapat dijelaskan, tutorial
pembuatan per file tersedia, picker mempunyai scope yang benar, dan quality gate
lulus. Persistence nyata, auth, upload multipart, database, dan layanan
production berada di luar scope inti Hari 2.
