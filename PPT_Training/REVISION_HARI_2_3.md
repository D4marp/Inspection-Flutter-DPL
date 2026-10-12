# Revisi Profesional PPT Hari 2 dan Hari 3

Deck Hari 2 dan Hari 3 dibangun ulang agar lebih visual, lebih advanced, dan
lebih mudah dipakai saat mengajar. Keduanya tetap mengikuti urutan dan batas
scope buku pendamping.

## Perubahan Hari 2

- Scaffold, AppBar, Row, Column, Form, responsive constraints, dan validation.
- JSONPlaceholder public open-source API dengan GET, POST, PUT, DELETE simulasi.
- Mapper Post → Inspection serta tutorial implementasi per file.
- Flutter CRUD melalui controller/repository/ApiClient facade dan empat file
  operasi Read/Create/Update/Delete yang dapat dibedah satu per satu.
- `image_picker` dan `file_picker` dengan selected/previewed/uploaded boundary.
- Instalasi OpenCode, `/connect`, `/models`, dan API key security boundary.
- Empat lab/challenge dengan Definition of Done dan evidence.

## Perubahan Hari 3

- Inventory legacy Kotlin/XML dan behavior map sebelum coding.
- PRD vertical slice dan traceability acceptance → file/test/evidence.
- Mapping Activity/Fragment/XML/ViewModel/Retrofit ke Flutter.
- WebView local asset dengan policy, controller, dan screen terpisah;
  loading/error/reload, JavaScript off, dan navigation block.
- Agent Skill `migrate-kotlin-slice`, context hygiene, human review gate.
- Analyze/test/build, parity review, gap register, dan handover.

## Format

- 16:9, 41 slide per deck.
- Tema navy–cyan–gold mengikuti cover buku.
- Layout, header, footer, card, dan code panel memakai komponen desain deck lama.
- Snippet dipangkas menjadi satu konsep per slide dengan label nama file.
- Diagram, flow, decision matrix, code panel, dan section divider native PPT.
- Presenter notes tersedia di setiap slide.
- File root `Hari_2_Flutter_Professional.pptx` dan
  `Hari_3_Flutter_Professional.pptx` identik dengan delivery copy di folder ini.

Deck Hari 2 dapat dibuat ulang dengan:

```sh
python3 tools/build_day2_crud_ai_picker_deck.py
```

Deck Hari 3 dapat dibuat ulang dengan:

```sh
python3 tools/build_day3_ai_webview_deck.py
```

