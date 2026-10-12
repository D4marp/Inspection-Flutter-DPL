# PRD Hari 3 — Flutter WebView dan Migrasi Aplikasi Kotlin

**Trainer dan Pembuat Buku:** Damar Galih Aji Pradana, S.Tr.Kom.

## Problem

Tim memiliki aplikasi Android Kotlin yang perlu dimigrasikan bertahap ke Flutter.
Risiko terbesar bukan syntax, melainkan perilaku yang hilang, contract berubah,
WebView terlalu permisif, dan output AI agent yang tidak dapat ditelusuri.

## Goal

Peserta menyelesaikan satu vertical slice daftar → detail, menulis traceability
PRD, membangun WebView terbatasi, menggunakan Agent Skill yang repeatable, dan
menyerahkan hasil analyze/test/build beserta daftar gap.

## Persona dan outcome

- **Petugas:** alur daftar/detail tetap dapat digunakan dan failure state jelas.
- **Developer:** mapping Kotlin → Flutter dapat direview per slice.
- **Reviewer/PIC:** setiap acceptance criterion mempunyai evidence dan owner.

## Source of truth

Urutan otoritas adalah contract bisnis/API yang disetujui, perilaku legacy yang
teramati, PRD slice, test/evidence, lalu implementasi. Nama class, screenshot,
atau saran agent tidak boleh sendiri dianggap sebagai contract.

## Requirements migrasi

| ID | Kebutuhan |
|---|---|
| D3-01 | Inventory Activity/Fragment, XML, ViewModel, Retrofit, storage, navigation |
| D3-02 | Behavior map mencatat input, output, state, error, side effect, dan unknown |
| D3-03 | Slice mempunyai goal, out-of-scope, AC, evidence, dan owner |
| D3-04 | Activity/Fragment dipetakan ke route/screen Flutter |
| D3-05 | XML dipetakan ke widget tree yang responsive |
| D3-06 | ViewModel/LiveData dipetakan ke state/controller dengan lifecycle jelas |
| D3-07 | Retrofit/data layer dipetakan tanpa mengubah endpoint/payload |
| D3-08 | Format, analyze, tests, dan smoke test dicatat |

## Requirements WebView

| ID | Kebutuhan |
|---|---|
| WV-01 | Controller dibuat terpisah dari `WebViewWidget` |
| WV-02 | Loading, error, reload, dan back behavior terlihat |
| WV-03 | Konten latihan membuka `https://www.presisirencar.com/` |
| WV-04 | JavaScript aktif untuk interaksi situs, tanpa JavaScript bridge |
| WV-05 | Hanya HTTPS ke `presisirencar.com` dan `www.presisirencar.com` yang diizinkan |
| WV-06 | Tidak ada API key/token di HTML, JS, URL query, asset, atau log |
| WV-07 | WebView bukan alasan untuk menghindari migrasi native Flutter tanpa keputusan produk |
| WV-08 | Navigation policy dipisah sebagai pure function dan mempunyai unit test |

## Agent Skill

Skill proyek berada di:

```text
flutter_projects/hari_3_dpl_inspection_release/
  .agents/skills/migrate-kotlin-slice/SKILL.md
```

Skill mengharuskan agent membaca PRD/source/test, menyebut unknown, membuat patch
kecil, menjalankan quality gate, dan melaporkan gap. Agent dilarang mengarang
contract, memperluas origin/bridge WebView, membocorkan secret, atau mengaku
telah menjalankan test tanpa evidence.

## Acceptance criteria

| ID | Evidence lulus |
|---|---|
| AC1 | Behavior map legacy tersedia dan unknown tidak disamarkan |
| AC2 | PRD slice daftar-detail mempunyai AC dan out-of-scope |
| AC3 | Daftar/detail Flutter memakai ID yang sama dan navigation parity |
| AC4 | Loading/empty/error/retry dapat dibedakan |
| AC5 | WebView berhasil membuka `https://www.presisirencar.com/` |
| AC6 | Exact-host allowlist lulus dan external link ditolak |
| AC7 | Skill valid dan path dapat ditemukan tool |
| AC8 | Prompt/context bebas credential dan data sensitif |
| AC9 | `flutter analyze` bersih dan seluruh test hijau |
| AC10 | APK debug dapat dibangun untuk smoke test |
| AC11 | Gap parity, risiko, owner, dan next slice dicatat |

## Definition of done

PRD, behavior map, app Migration Lab, WebView boundary, Agent Skill, hasil
analyze/test/build, dan handover gap tersedia. Rewrite seluruh aplikasi,
JavaScript bridge produksi, perubahan kontrak API, deployment store, dan fitur AI di
runtime aplikasi berada di luar scope Hari 3.
