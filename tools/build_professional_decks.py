#!/usr/bin/env python3
"""Build the professional Day 2 and Day 3 Flutter training decks.

The generated presentations intentionally stay aligned with the written modules:
Day 2 covers Flutter architecture/API/state/storage and Day 3 covers native
integration/testing/performance/release. Custom server implementation and
deployment are intentionally excluded.
"""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path
from typing import Iterable, Sequence

from PIL import Image, ImageOps
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "PPT_Training"
ASSET_DIR = ROOT / "assets" / "cover"
SCREENSHOT_DIR = ROOT / "flutter_projects"

SW = Inches(13.333)
SH = Inches(7.5)

NAVY = "071D3B"
NAVY_2 = "0B2A55"
BLUE = "0E5AA7"
CYAN = "16C6E7"
CYAN_2 = "7BE7F6"
GOLD = "D1A33C"
INK = "10233E"
MUTED = "5D6D82"
PALE = "EEF4F9"
PALE_BLUE = "E4F7FB"
WHITE = "FFFFFF"
GREEN = "19A974"
RED = "D84A4A"
ORANGE = "F59E42"
LINE = "D5E1EC"
CODE = "091827"

FONT = "Aptos"
FONT_DISPLAY = "Aptos Display"
FONT_MONO = "Cascadia Mono"


def rgb(hex_value: str) -> RGBColor:
    return RGBColor.from_string(hex_value)


def set_fill(shape, color: str) -> None:
    shape.fill.solid()
    shape.fill.fore_color.rgb = rgb(color)


def set_line(shape, color: str | None, width: float = 1.0) -> None:
    if color is None:
        shape.line.fill.background()
        return
    shape.line.color.rgb = rgb(color)
    shape.line.width = Pt(width)


def add_box(slide, x, y, w, h, fill=WHITE, line=None, radius=True):
    kind = MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE
    shape = slide.shapes.add_shape(kind, x, y, w, h)
    set_fill(shape, fill)
    set_line(shape, line)
    return shape


def add_text(
    slide,
    text: str,
    x,
    y,
    w,
    h,
    *,
    size=18,
    color=INK,
    bold=False,
    font=FONT,
    align=PP_ALIGN.LEFT,
    valign=MSO_ANCHOR.TOP,
    margin=0.0,
    tracking=None,
):
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame
    tf.clear()
    tf.margin_left = Inches(margin)
    tf.margin_right = Inches(margin)
    tf.margin_top = Inches(margin)
    tf.margin_bottom = Inches(margin)
    tf.vertical_anchor = valign
    p = tf.paragraphs[0]
    p.alignment = align
    p.space_after = Pt(0)
    run = p.add_run()
    run.text = text
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = rgb(color)
    if tracking is not None:
        run.font._element.set("spc", str(tracking))
    return box


def add_rich_text(slide, runs, x, y, w, h, *, size=18, valign=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame
    tf.clear()
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = valign
    p = tf.paragraphs[0]
    for item in runs:
        text, color, bold = item
        run = p.add_run()
        run.text = text
        run.font.name = FONT
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = rgb(color)
    return box


def add_bullets(
    slide,
    items: Sequence[str],
    x,
    y,
    w,
    h,
    *,
    size=17,
    color=INK,
    accent=CYAN,
    gap=8,
):
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"•  {item}"
        p.font.name = FONT
        p.font.size = Pt(size)
        p.font.color.rgb = rgb(color)
        p.space_after = Pt(gap)
        p.level = 0
        if p.runs:
            p.runs[0].font.name = FONT
    return box


def add_header(slide, section: str, title: str, number: int, total: int):
    band = add_box(slide, 0, 0, SW, Inches(0.82), NAVY, None, radius=False)
    add_box(slide, 0, 0, Inches(0.12), Inches(0.82), CYAN, None, radius=False)
    add_text(
        slide,
        section.upper(),
        Inches(0.48),
        Inches(0.19),
        Inches(2.05),
        Inches(0.25),
        size=9,
        color=CYAN_2,
        bold=True,
    )
    add_text(
        slide,
        title,
        Inches(0.48),
        Inches(0.38),
        Inches(10.5),
        Inches(0.35),
        size=23,
        color=WHITE,
        bold=True,
        font=FONT_DISPLAY,
    )
    add_text(
        slide,
        f"{number:02d} / {total:02d}",
        Inches(11.75),
        Inches(0.29),
        Inches(1.05),
        Inches(0.24),
        size=10,
        color=CYAN_2,
        bold=True,
        align=PP_ALIGN.RIGHT,
    )
    return band


def add_footer(slide, day: int):
    add_text(
        slide,
        f"PT. Dok Pantai Lamongan  •  Flutter Professional  •  Hari {day}",
        Inches(0.48),
        Inches(7.12),
        Inches(7.0),
        Inches(0.18),
        size=8,
        color=MUTED,
    )
    add_text(
        slide,
        "Damar Galih Aji Pradana, S.Tr.Kom.",
        Inches(8.5),
        Inches(7.12),
        Inches(4.3),
        Inches(0.18),
        size=8,
        color=MUTED,
        align=PP_ALIGN.RIGHT,
    )


def base_slide(prs, section, title, number, total, day, bg=PALE):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    background = slide.background
    background.fill.solid()
    background.fill.fore_color.rgb = rgb(bg)
    add_header(slide, section, title, number, total)
    add_footer(slide, day)
    return slide


def add_pill(slide, text, x, y, w, *, fill=PALE_BLUE, color=BLUE, size=10):
    add_box(slide, x, y, w, Inches(0.33), fill, None)
    add_text(
        slide,
        text.upper(),
        x,
        y + Inches(0.07),
        w,
        Inches(0.17),
        size=size,
        color=color,
        bold=True,
        align=PP_ALIGN.CENTER,
    )


def add_card(
    slide,
    x,
    y,
    w,
    h,
    title,
    body,
    *,
    icon=None,
    accent=CYAN,
    fill=WHITE,
    title_size=16,
    body_size=13,
):
    add_box(slide, x, y, w, h, fill, LINE)
    add_box(slide, x, y, Inches(0.08), h, accent, None, radius=False)
    dark_card = fill in (NAVY, NAVY_2, CODE)
    card_title_color = WHITE if dark_card else INK
    card_body_color = "D5E7F2" if dark_card else MUTED
    tx = x + Inches(0.28)
    if icon:
        circle = slide.shapes.add_shape(
            MSO_SHAPE.OVAL, tx, y + Inches(0.22), Inches(0.42), Inches(0.42)
        )
        set_fill(circle, accent)
        set_line(circle, None)
        add_text(
            slide,
            icon,
            tx,
            y + Inches(0.30),
            Inches(0.42),
            Inches(0.18),
            size=11,
            color=NAVY,
            bold=True,
            align=PP_ALIGN.CENTER,
        )
        title_x = tx + Inches(0.56)
        title_w = w - Inches(1.0)
    else:
        title_x = tx
        title_w = w - Inches(0.55)
    add_text(
        slide,
        title,
        title_x,
        y + Inches(0.22),
        title_w,
        Inches(0.35),
        size=title_size,
        color=card_title_color,
        bold=True,
    )
    if isinstance(body, (list, tuple)):
        add_bullets(
            slide,
            body,
            tx,
            y + Inches(0.78),
            w - Inches(0.52),
            h - Inches(0.95),
            size=body_size,
            color=card_body_color,
            gap=5,
        )
    else:
        add_text(
            slide,
            body,
            tx,
            y + Inches(0.77),
            w - Inches(0.52),
            h - Inches(0.95),
            size=body_size,
            color=card_body_color,
        )


def add_code(slide, code: str, x, y, w, h, *, label="DART", highlight=None, size=11):
    add_box(slide, x, y, w, h, CODE, NAVY_2)
    label_width = min(2.7, max(0.86, 0.4 + (len(label) * 0.07)))
    add_pill(slide, label, x + Inches(0.18), y + Inches(0.16), Inches(label_width), fill=NAVY_2, color=CYAN_2, size=8)
    add_text(
        slide,
        code,
        x + Inches(0.22),
        y + Inches(0.68),
        w - Inches(0.44),
        h - Inches(0.82),
        size=size,
        color="D9ECF5",
        font=FONT_MONO,
    )
    if highlight:
        add_text(
            slide,
            highlight,
            x + w - Inches(2.05),
            y + Inches(0.17),
            Inches(1.78),
            Inches(0.18),
            size=8,
            color=GOLD,
            bold=True,
            align=PP_ALIGN.RIGHT,
        )


def add_table(slide, headers, rows, x, y, w, h, widths=None, font_size=12):
    shape = slide.shapes.add_table(len(rows) + 1, len(headers), x, y, w, h)
    table = shape.table
    if widths:
        for i, width in enumerate(widths):
            table.columns[i].width = width
    for c, header in enumerate(headers):
        cell = table.cell(0, c)
        cell.text = header
        cell.fill.solid()
        cell.fill.fore_color.rgb = rgb(NAVY_2)
        cell.margin_left = cell.margin_right = Inches(0.1)
        for p in cell.text_frame.paragraphs:
            p.font.name = FONT
            p.font.size = Pt(font_size)
            p.font.bold = True
            p.font.color.rgb = rgb(WHITE)
    for r, row in enumerate(rows, 1):
        for c, value in enumerate(row):
            cell = table.cell(r, c)
            cell.text = str(value)
            cell.fill.solid()
            cell.fill.fore_color.rgb = rgb(WHITE if r % 2 else "F5F8FB")
            cell.margin_left = cell.margin_right = Inches(0.1)
            cell.margin_top = cell.margin_bottom = Inches(0.06)
            for p in cell.text_frame.paragraphs:
                p.font.name = FONT
                p.font.size = Pt(font_size - 1)
                p.font.color.rgb = rgb(INK)
    return table


def add_flow(slide, labels: Sequence[str], x, y, w, *, colors=None, descriptions=None):
    n = len(labels)
    gap = Inches(0.18)
    box_w = (w - gap * (n - 1)) / n
    colors = colors or [BLUE, CYAN, GOLD, GREEN, ORANGE]
    for i, label in enumerate(labels):
        xx = x + i * (box_w + gap)
        fill = colors[i % len(colors)]
        add_box(slide, xx, y, box_w, Inches(0.78), fill, None)
        text_color = WHITE if fill not in (CYAN, GOLD, CYAN_2) else NAVY
        add_text(
            slide,
            label,
            xx + Inches(0.08),
            y + Inches(0.22),
            box_w - Inches(0.16),
            Inches(0.30),
            size=13,
            color=text_color,
            bold=True,
            align=PP_ALIGN.CENTER,
        )
        if i < n - 1:
            chevron = slide.shapes.add_shape(
                MSO_SHAPE.CHEVRON,
                xx + box_w + Inches(0.03),
                y + Inches(0.25),
                Inches(0.12),
                Inches(0.28),
            )
            set_fill(chevron, MUTED)
            set_line(chevron, None)
        if descriptions:
            add_text(
                slide,
                descriptions[i],
                xx,
                y + Inches(0.92),
                box_w,
                Inches(0.72),
                size=10,
                color=MUTED,
                align=PP_ALIGN.CENTER,
            )


def add_connector(slide, x1, y1, x2, y2, color=CYAN, width=2, dashed=False):
    line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x1, y1, x2, y2)
    line.line.color.rgb = rgb(color)
    line.line.width = Pt(width)
    if dashed:
        line.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    return line


def add_notes(slide, session, minutes, objective, delivery, question, reference):
    text = (
        f"SESI: {session}. ALOKASI: {minutes} menit.\n\n"
        f"TUJUAN: {objective}\n\n"
        f"ARAHAN TRAINER: {delivery}\n\n"
        f"PERTANYAAN DISKUSI: {question}\n\n"
        f"RUJUKAN: {reference}"
    )
    slide.notes_slide.notes_text_frame.text = text


def prepare_cover_background(tmp: Path) -> Path:
    source = ASSET_DIR / "cover-background-v2.png"
    target = tmp / "presentation-cover-16x9.png"
    with Image.open(source) as image:
        fitted = ImageOps.fit(image.convert("RGB"), (1920, 1080), centering=(0.52, 0.44))
        fitted.save(target, quality=95)
    return target


def add_cover(prs, day, title, subtitle, tags, background, total):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.shapes.add_picture(str(background), 0, 0, width=SW, height=SH)
    add_box(slide, 0, 0, Inches(7.8), SH, NAVY, None, radius=False)
    add_box(slide, Inches(0.65), Inches(0.65), Inches(5.62), Inches(0.76), WHITE, None)
    slide.shapes.add_picture(str(ASSET_DIR / "image1.png"), Inches(0.88), Inches(0.79), width=Inches(2.28))
    slide.shapes.add_picture(str(ASSET_DIR / "image2.png"), Inches(5.27), Inches(0.73), height=Inches(0.62))
    add_text(slide, f"HARI {day}", Inches(0.72), Inches(1.77), Inches(1.2), Inches(0.25), size=11, color=CYAN_2, bold=True)
    add_text(slide, title, Inches(0.70), Inches(2.10), Inches(6.15), Inches(1.42), size=34, color=WHITE, bold=True, font=FONT_DISPLAY)
    add_text(slide, subtitle, Inches(0.72), Inches(3.62), Inches(5.85), Inches(0.70), size=17, color="BFD7E9")
    cursor = Inches(0.72)
    for tag in tags:
        width = Inches(max(1.15, 0.12 * len(tag) + 0.42))
        add_pill(slide, tag, cursor, Inches(4.65), width, fill=NAVY_2, color=CYAN_2, size=9)
        cursor += width + Inches(0.14)
    add_box(slide, Inches(0.72), Inches(5.55), Inches(5.86), Inches(1.06), NAVY_2, CYAN)
    add_text(slide, "TRAINER & PENULIS", Inches(0.98), Inches(5.80), Inches(2.0), Inches(0.18), size=9, color=CYAN_2, bold=True)
    add_text(slide, "Damar Galih Aji Pradana, S.Tr.Kom.", Inches(0.98), Inches(6.10), Inches(4.9), Inches(0.28), size=16, color=WHITE, bold=True)
    add_text(slide, f"01 / {total:02d}", Inches(11.92), Inches(6.94), Inches(0.85), Inches(0.20), size=9, color=WHITE, bold=True, align=PP_ALIGN.RIGHT)
    return slide


def add_section_slide(prs, day, number, total, marker, title, subtitle, outcomes):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = rgb(NAVY)
    add_box(slide, 0, 0, Inches(0.16), SH, CYAN, None, radius=False)
    add_text(slide, marker, Inches(0.72), Inches(0.92), Inches(1.6), Inches(0.8), size=58, color=CYAN, bold=True, font=FONT_DISPLAY)
    add_text(slide, title, Inches(0.74), Inches(2.05), Inches(7.3), Inches(0.86), size=32, color=WHITE, bold=True, font=FONT_DISPLAY)
    add_text(slide, subtitle, Inches(0.74), Inches(3.04), Inches(6.7), Inches(0.75), size=16, color="BCD4E6")
    add_box(slide, Inches(8.15), Inches(1.05), Inches(4.30), Inches(5.25), NAVY_2, "17406C")
    add_text(slide, "SETELAH BAGIAN INI", Inches(8.55), Inches(1.52), Inches(3.45), Inches(0.22), size=10, color=CYAN_2, bold=True)
    for i, item in enumerate(outcomes, 1):
        yy = Inches(2.03 + (i - 1) * 1.12)
        circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(8.55), yy, Inches(0.46), Inches(0.46))
        set_fill(circle, CYAN if i == 1 else "174F7E")
        set_line(circle, None)
        add_text(slide, str(i), Inches(8.55), yy + Inches(0.11), Inches(0.46), Inches(0.18), size=10, color=NAVY if i == 1 else WHITE, bold=True, align=PP_ALIGN.CENTER)
        add_text(slide, item, Inches(9.22), yy + Inches(0.02), Inches(2.72), Inches(0.58), size=13, color=WHITE, bold=True)
    add_text(slide, f"HARI {day}  •  {number:02d} / {total:02d}", Inches(10.52), Inches(6.95), Inches(1.75), Inches(0.18), size=9, color=CYAN_2, bold=True, align=PP_ALIGN.RIGHT)
    return slide


def add_outcome_slide(prs, day, number, total, title, cards):
    slide = base_slide(prs, "ORIENTASI", title, number, total, day)
    positions = [
        (Inches(0.55), Inches(1.25)),
        (Inches(6.82), Inches(1.25)),
        (Inches(0.55), Inches(4.10)),
        (Inches(6.82), Inches(4.10)),
    ]
    for (x, y), card in zip(positions, cards):
        title, body, icon, accent = card
        add_card(
            slide,
            x,
            y,
            Inches(5.95),
            Inches(2.36),
            title,
            body,
            icon=icon,
            accent=accent,
        )
    return slide


def add_agenda_slide(prs, day, number, total, rows):
    slide = base_slide(prs, "ORIENTASI", "Roadmap pembelajaran", number, total, day)
    add_text(slide, "Satu alur: contract → implementation → evidence", Inches(0.58), Inches(1.08), Inches(8), Inches(0.35), size=17, color=MUTED)
    y = Inches(1.68)
    for i, (time, title, checkpoint) in enumerate(rows, 1):
        accent = [CYAN, BLUE, GOLD, GREEN, ORANGE][(i - 1) % 5]
        add_box(slide, Inches(0.72), y, Inches(1.12), Inches(0.68), accent, None)
        add_text(slide, time, Inches(0.72), y + Inches(0.20), Inches(1.12), Inches(0.24), size=11, color=NAVY if accent in (CYAN, GOLD) else WHITE, bold=True, align=PP_ALIGN.CENTER)
        add_box(slide, Inches(2.02), y, Inches(4.18), Inches(0.68), WHITE, LINE)
        add_text(slide, title, Inches(2.25), y + Inches(0.18), Inches(3.72), Inches(0.28), size=15, color=INK, bold=True)
        add_box(slide, Inches(6.38), y, Inches(5.98), Inches(0.68), "F8FBFD", LINE)
        add_text(slide, checkpoint, Inches(6.64), y + Inches(0.15), Inches(5.42), Inches(0.36), size=13, color=MUTED)
        if i < len(rows):
            add_connector(slide, Inches(1.28), y + Inches(0.68), Inches(1.28), y + Inches(0.93), color=LINE, width=3)
        y += Inches(0.96)
    return slide


def build_day2(background: Path):
    total = 39
    prs = Presentation()
    prs.slide_width = SW
    prs.slide_height = SH
    n = 1

    s = add_cover(
        prs,
        2,
        "Flutter Data, API\n& Clean Architecture",
        "Clean architecture, REST API client, state, session, cache, dan failure handling di Flutter.",
        ["CLEAN CODE", "REST API", "STATE", "CACHE"],
        background,
        total,
    )
    add_notes(s, "Pembukaan", 3, "Menyepakati target teknis Hari 2.", "Tegaskan bahwa JSONPlaceholder siap dipakai. Waktu kelas dipakai untuk implementasi Flutter dan pembuktian perilakunya.", "Apa risiko terbesar ketika UI langsung bergantung pada detail HTTP?", "Modul Hari 2 dan PRD Hari 2.")
    n += 1

    s = add_outcome_slide(
        prs,
        2,
        n,
        total,
        "Hasil belajar yang dapat dibuktikan",
        [
            ("Arsitektur teruji", ["UI tidak mengetahui HTTP", "Dependency dapat diganti dengan fake"], "A", CYAN),
            ("API client bertipe", ["Model sesuai kontrak", "Status dan schema tervalidasi"], "C", BLUE),
            ("State dapat diprediksi", ["Loading, data, empty, error, cached", "Submit ganda dicegah"], "S", GOLD),
            ("Operasional aman", ["Token tidak masuk log", "Environment dan cache punya kebijakan"], "O", GREEN),
        ],
    )
    add_notes(s, "08.30–08.40", 10, "Menjelaskan standar kelulusan.", "Minta peserta menyebut bukti untuk tiap kartu, bukan hanya fitur yang terlihat.", "Bukti apa yang membedakan 'berfungsi' dari 'siap dilanjutkan tim'?", "PRD Hari 2 AC1–AC11.")
    n += 1

    s = add_agenda_slide(
        prs,
        2,
        n,
        total,
        [
            ("08.30", "Architecture & clean boundaries", "Refactor tanpa mengubah perilaku UI"),
            ("10.15", "API client, auth, GET & POST", "Data API tampil dan create berhasil"),
            ("13.00", "State, session & cache", "Restart/offline/logout dapat dijelaskan"),
            ("14.45", "Failure engineering", "401/422/500/timeout memberi UX tepat"),
            ("16.00", "Review & checkpoint", "Test, bukti request, tag day-2"),
        ],
    )
    add_notes(s, "08.40–08.45", 5, "Menghubungkan agenda dengan checkpoint.", "Tekankan bahwa teori selalu diikuti praktik dan bukti.", "Bagian mana yang paling berisiko menghabiskan waktu?", "Silabus 3 Hari, jadwal Hari 2.")
    n += 1

    s = base_slide(prs, "ORIENTASI", "Baseline day-1 sebelum refactor", n, total, 2)
    add_card(s, Inches(0.60), Inches(1.25), Inches(5.85), Inches(4.95), "Harus tetap bekerja", ["List, detail, dan form valid", "Navigation tidak menduplikasi data", "Empty/error state sudah terlihat", "Controller dan TextEditingController di-dispose"], icon="✓", accent=GREEN, body_size=15)
    add_card(s, Inches(6.80), Inches(1.25), Inches(5.90), Inches(4.95), "Yang berubah hari ini", ["Sumber data lokal → remote API", "Data flow diberi boundary", "State menjadi eksplisit", "Session dan cache memiliki policy", "Test memanfaatkan dependency seam"], icon="→", accent=CYAN, body_size=15)
    add_pill(s, "RULE", Inches(5.55), Inches(6.38), Inches(1.35), fill=NAVY, color=CYAN_2)
    add_text(s, "Refactor yang baik menjaga perilaku pengguna sambil memperbaiki struktur internal.", Inches(2.55), Inches(6.73), Inches(8.2), Inches(0.28), size=13, color=MUTED, bold=True, align=PP_ALIGN.CENTER)
    add_notes(s, "08.45–09.00", 15, "Menentukan input yang sehat untuk Hari 2.", "Jangan lanjut jika flow dasar day-1 masih rusak. Gunakan starter sebagai recovery.", "Apa yang harus tetap sama setelah data lokal diganti API?", "Materi Hari 1 dan checkpoint day-1.")
    n += 1

    s = add_section_slide(prs, 2, n, total, "01", "Clean boundaries", "Pisahkan alasan perubahan—UI, orchestration, data policy, dan transport.", ["Menggambar aliran dependency", "Menempatkan tanggung jawab", "Membuat seam untuk test"])
    add_notes(s, "09.00–09.02", 2, "Membuka bagian arsitektur.", "Hubungkan konsep dengan kode proyek yang sudah ada.", "Layer mana paling sering menjadi tempat campur-aduk?", "Flutter app architecture recommendations.")
    n += 1

    s = base_slide(prs, "ARCHITECTURE", "Aliran data dan arah dependency", n, total, 2)
    add_flow(s, ["View", "Controller", "Repository", "Remote / Local"], Inches(0.75), Inches(1.72), Inches(11.85), descriptions=["Render + user intent", "State + orchestration", "Source policy", "HTTP / cache / secure store"])
    add_box(s, Inches(0.75), Inches(4.22), Inches(11.85), Inches(1.45), WHITE, LINE)
    add_rich_text(s, [("Dependency mengarah ke dalam. ", INK, True), ("Data mengalir dua arah sebagai request dan result, tetapi UI tidak mengimpor package HTTP atau storage.", MUTED, False)], Inches(1.06), Inches(4.65), Inches(11.25), Inches(0.56), size=16)
    add_pill(s, "CLEAN CODE TEST", Inches(4.95), Inches(6.02), Inches(3.1), fill=PALE_BLUE, color=BLUE)
    add_text(s, "Jika host atau implementasi API berubah, View tidak ikut berubah.", Inches(2.05), Inches(6.48), Inches(9.2), Inches(0.28), size=14, color=BLUE, bold=True, align=PP_ALIGN.CENTER)
    add_notes(s, "09.02–09.15", 13, "Menjelaskan boundary dan arah dependency.", "Trace aksi refresh dari View hingga API lalu kembali sebagai state.", "Apa import yang tidak boleh muncul pada file screen?", "Modul Hari 2: aliran tanggung jawab.")
    n += 1

    s = base_slide(prs, "ARCHITECTURE", "Tanggung jawab: satu alasan untuk berubah", n, total, 2)
    add_table(s, ["Layer", "Mengetahui", "Tidak mengetahui", "Bukti"], [
        ["View", "UI state + user intent", "URL, JSON, token", "Widget test"],
        ["Controller", "Use flow + state", "HTTP status detail", "State test"],
        ["Repository", "Remote/cache policy", "Widget", "Repository test"],
        ["ApiClient", "Endpoint + schema", "UI", "Contract test"],
        ["Store", "Persist/read/delete", "Navigation", "Storage test"],
    ], Inches(0.60), Inches(1.35), Inches(12.10), Inches(4.55), widths=[Inches(1.65), Inches(3.1), Inches(3.15), Inches(2.25)], font_size=13)
    add_box(s, Inches(0.60), Inches(6.15), Inches(12.10), Inches(0.58), PALE_BLUE, None)
    add_text(s, "Heuristik: nama layer harus menjelaskan keputusan yang menjadi tanggung jawabnya.", Inches(0.88), Inches(6.34), Inches(11.55), Inches(0.23), size=13, color=BLUE, bold=True, align=PP_ALIGN.CENTER)
    add_notes(s, "09.15–09.28", 13, "Memetakan tanggung jawab ke file.", "Gunakan tabel sebagai rubric review. Minta peserta menunjukkan satu pelanggaran di starter.", "Siapa yang memutuskan kapan cache boleh dipakai?", "Modul Hari 2: service/repository/controller.")
    n += 1

    s = base_slide(prs, "ARCHITECTURE", "Feature slice yang tetap sederhana", n, total, 2)
    add_code(s, "lib/\n  core/\n    config/app_config.dart\n    failure/app_failure.dart\n  features/inspection/\n    data/api_client.dart\n    data/inspection_repository.dart\n    domain/inspection.dart\n    presentation/inspection_controller.dart\n    presentation/screens/\n  features/session/\n    session_controller.dart\n    token_store.dart", Inches(0.62), Inches(1.25), Inches(5.58), Inches(5.58), label="PROJECT TREE", size=12)
    add_card(s, Inches(6.55), Inches(1.25), Inches(6.15), Inches(2.42), "Kapan dipakai?", ["Tim/fitur mulai bertambah", "Ownership per fitur lebih jelas", "Shared core benar-benar kecil"], icon="?", accent=CYAN, body_size=14)
    add_card(s, Inches(6.55), Inches(3.92), Inches(6.15), Inches(2.91), "Jangan over-engineer", ["Hari 2 boleh mempertahankan folder layer dari buku", "Interface dibuat pada dependency yang perlu diganti", "Use case ditambah saat rule bisnis benar-benar tumbuh"], icon="!", accent=GOLD, body_size=14)
    add_notes(s, "09.28–09.40", 12, "Menunjukkan evolusi struktur tanpa memaksa clean architecture penuh.", "Bandingkan dengan struktur modul; jelaskan bahwa ini opsi saat proyek bertumbuh.", "Kapan interface hanya menambah boilerplate?", "Modul Hari 2; prinsip YAGNI.")
    n += 1

    s = base_slide(prs, "ARCHITECTURE", "Dependency injection = test seam", n, total, 2)
    code = "abstract interface class InspectionGateway {\n  Future<List<Inspection>> list();\n  Future<Inspection> create(CreateInspection input);\n}\n\nclass InspectionController extends ChangeNotifier {\n  InspectionController(this.gateway);\n  final InspectionGateway gateway;\n}\n\n// production → HttpInspectionRepository\n// test       → FakeInspectionGateway"
    add_code(s, code, Inches(0.60), Inches(1.30), Inches(7.15), Inches(5.45), highlight="DEPEND ON ABSTRACTION", size=12)
    add_card(s, Inches(8.06), Inches(1.30), Inches(4.63), Inches(2.40), "Nilai praktis", ["Test tanpa network/plugin", "Failure dapat dipicu sengaja", "Implementasi dapat diganti"], icon="DI", accent=CYAN, body_size=13)
    add_card(s, Inches(8.06), Inches(3.98), Inches(4.63), Inches(2.77), "Batas kelas", ["Tidak semua class butuh interface", "Constructor injection sudah cukup", "Hindari service locator global"], icon="≠", accent=GOLD, body_size=13)
    add_notes(s, "09.40–09.55", 15, "Mengaitkan constructor injection dengan testability.", "Demo ganti implementation production menjadi fake tanpa mengubah controller.", "Dependency mana yang paling perlu dibuat fake?", "Modul Hari 2: dependency melalui constructor.")
    n += 1

    s = base_slide(prs, "ARCHITECTURE", "DTO, domain model, dan input command", n, total, 2)
    add_flow(s, ["JSON", "InspectionDto", "Inspection", "View model"], Inches(0.70), Inches(1.52), Inches(11.90), descriptions=["Bentuk kontrak server", "Parsing + validation", "Tipe bisnis stabil", "Format untuk UI"])
    add_card(s, Inches(0.70), Inches(3.55), Inches(3.74), Inches(2.66), "Pisahkan bila…", ["Nama field server berubah", "Domain punya enum/value object", "Satu model dipakai banyak endpoint"], icon="+", accent=CYAN, body_size=13)
    add_card(s, Inches(4.79), Inches(3.55), Inches(3.74), Inches(2.66), "Gabungkan bila…", ["Proyek kecil dan schema stabil", "Mapping hanya duplikasi", "Tidak ada rule domain tambahan"], icon="=", accent=GREEN, body_size=13)
    add_card(s, Inches(8.88), Inches(3.55), Inches(3.72), Inches(2.66), "Tetap wajib", ["Enum memvalidasi kondisi", "Tanggal dinormalisasi UTC", "Missing field gagal di boundary"], icon="✓", accent=GOLD, body_size=13)
    add_notes(s, "09.55–10.00", 5, "Memperkenalkan mapping sesuai kompleksitas.", "Tunjukkan Inspection.fromJson yang sudah ada dan jelaskan kapan DTO terpisah berguna.", "Apa dampak cast error jika dibiarkan lolos ke UI?", "Modul Hari 2: model JSON.")
    n += 1

    s = add_section_slide(prs, 2, n, total, "02", "REST API di Flutter", "Flutter membaca kontrak, memetakan JSON, dan mengubah response menjadi state yang dapat diuji.", ["Membuat API client", "Memilih environment", "Memetakan failure"])
    add_notes(s, "10.15–10.17", 2, "Membuka sesi API Flutter.", "Endpoint publik sudah siap. Mulai dari response contract lalu implementasikan ApiClient.", "Bagaimana mencegah detail HTTP bocor ke widget?", "PRD Hari 2: kontrak API.")
    n += 1

    s = base_slide(prs, "API CLIENT", "Aliran integrasi API dari sisi Flutter", n, total, 2)
    # topology boxes
    nodes = [
        ("View", "render state\nuser intent", Inches(0.65), CYAN),
        ("Controller", "orchestrate\nnotify UI", Inches(3.20), BLUE),
        ("Repository", "remote/cache\npolicy", Inches(5.75), GOLD),
        ("ApiClient", "Bearer + JSON\ntimeout", Inches(8.30), GREEN),
        ("HTTPS API", "contract ready\ntraining data", Inches(10.85), ORANGE),
    ]
    for title, body, x, color in nodes:
        add_box(s, x, Inches(1.72), Inches(1.85), Inches(1.48), WHITE, color)
        add_text(s, title, x, Inches(1.98), Inches(1.85), Inches(0.28), size=15, color=INK, bold=True, align=PP_ALIGN.CENTER)
        add_text(s, body, x + Inches(0.08), Inches(2.38), Inches(1.69), Inches(0.48), size=11, color=MUTED, align=PP_ALIGN.CENTER)
        if x < Inches(10.5):
            add_connector(s, x + Inches(1.86), Inches(2.46), x + Inches(2.45), Inches(2.46), color=CYAN, width=2)
    add_card(s, Inches(0.66), Inches(4.10), Inches(5.78), Inches(2.26), "Fokus peserta Flutter", ["Mapping JSON ke model", "State dan recovery UI", "Lifecycle serta testability"], icon="1", accent=CYAN, body_size=14)
    add_card(s, Inches(6.78), Inches(4.10), Inches(5.78), Inches(2.26), "Sudah siap dipakai", ["Base URL publik", "Kontrak/status response", "Tanpa akun/deployment"], icon="2", accent=GOLD, body_size=14)
    add_notes(s, "10.17–10.30", 13, "Menjelaskan aliran integrasi Flutter.", "Trace aksi user sampai ApiClient dan kembali sebagai UI state. Tekankan batas simulated write.", "Layer mana yang memutuskan cache fallback?", "Modul Hari 2: data flow.")
    n += 1

    s = base_slide(prs, "API CLIENT", "Membaca kontrak sebagai Flutter developer", n, total, 2)
    add_card(s, Inches(0.62), Inches(1.30), Inches(3.78), Inches(4.95), "Request", ["Method + path", "Auth scheme", "Headers", "Query/path params", "Body schema + example"], icon="RQ", accent=CYAN, body_size=14)
    add_card(s, Inches(4.78), Inches(1.30), Inches(3.78), Inches(4.95), "Response", ["Success status", "Error status", "Schema per status", "Pagination metadata", "Timestamp + timezone"], icon="RS", accent=BLUE, body_size=14)
    add_card(s, Inches(8.94), Inches(1.30), Inches(3.78), Inches(4.95), "Flutter mapping", ["DTO/model bertipe", "Enum tervalidasi", "422 ke field errors", "401 ke session flow", "DateTime ke UTC"], icon="FM", accent=GOLD, body_size=14)
    add_text(s, "Rule: aplikasi tidak menebak nama field, status code, atau bentuk error.", Inches(1.45), Inches(6.55), Inches(10.45), Inches(0.30), size=15, color=BLUE, bold=True, align=PP_ALIGN.CENTER)
    add_notes(s, "10.30–10.43", 13, "Mengajarkan cara menerjemahkan kontrak ke Dart.", "Cocokkan login, list, dan create dengan model, enum, validator, serta failure mapper.", "Apa yang terjadi bila field wajib hilang?", "Kontrak API training dan model Dart.")
    n += 1

    s = base_slide(prs, "API CONTRACT", "Contract minimum untuk DPL Inspection", n, total, 2)
    add_table(s, ["Operation", "Input", "Success", "Failure penting"], [
        ["POST /auth/login", "username, password", "200 token + user", "401 invalid credential"],
        ["GET /inspections", "page, per_page", "200 items + total", "401, 500"],
        ["POST /inspections", "assetCode, location, condition, note", "201 Inspection", "401, 409, 422"],
        ["GET /health", "—", "200 status + version", "503 dependency down"],
    ], Inches(0.58), Inches(1.28), Inches(12.16), Inches(4.62), widths=[Inches(2.55), Inches(3.62), Inches(2.76), Inches(3.23)], font_size=12)
    add_box(s, Inches(0.58), Inches(6.10), Inches(12.16), Inches(0.64), PALE_BLUE, CYAN)
    add_rich_text(s, [("COMPATIBILITY  •  ", BLUE, True), ("Field wajib dan status yang dipakai app tidak berubah tanpa versioning atau migration.", INK, False)], Inches(0.90), Inches(6.29), Inches(11.52), Inches(0.25), size=12)
    add_notes(s, "10.43–10.53", 10, "Memetakan endpoint ke method Flutter.", "Jalankan satu request contoh, lalu implementasikan method dan model yang sesuai.", "Status mana yang mengakhiri session?", "PRD Hari 2 dan mock_api.py.")
    n += 1

    s = base_slide(prs, "API CONTRACT", "Environment tanpa hard-coded URL", n, total, 2)
    add_code(s, "class AppConfig {\n  const AppConfig({required this.apiBaseUrl});\n\n  factory AppConfig.fromEnvironment() {\n    const raw = String.fromEnvironment('API_BASE_URL');\n    final uri = Uri.tryParse(raw);\n    if (uri == null || !uri.hasAuthority) {\n      throw StateError('API_BASE_URL tidak valid');\n    }\n    return AppConfig(apiBaseUrl: uri);\n  }\n}", Inches(0.60), Inches(1.25), Inches(6.35), Inches(5.55), label="CONFIG", highlight="FAIL FAST", size=11)
    add_table(s, ["Target", "Base URL", "Aturan"], [
        ["iOS Simulator", "http://localhost:8000", "debug fallback"],
        ["Android Emulator", "http://10.0.2.2:8000", "debug fallback"],
        ["Device", "https://api-training…", "hosted HTTPS"],
        ["Release", "https://api-staging…", "no localhost"],
    ], Inches(7.25), Inches(1.25), Inches(5.47), Inches(3.65), widths=[Inches(1.55), Inches(2.4), Inches(1.52)], font_size=11)
    add_card(s, Inches(7.25), Inches(5.15), Inches(5.47), Inches(1.65), "Command", "flutter run --dart-define=API_BASE_URL=https://api-training.example", icon="$", accent=GOLD, body_size=12)
    add_notes(s, "10.53–11.03", 10, "Mencegah environment leak dan URL tersebar.", "Tunjukkan satu command run dan fail-fast ketika define kosong.", "Mengapa default localhost berbahaya untuk release?", "Modul Hari 2: alamat API.")
    n += 1

    s = base_slide(prs, "API CONTRACT", "ApiClient: kecil, deterministik, dapat diuji", n, total, 2)
    code = "Future<Inspection> create(CreateInspection input) async {\n  final response = await _http.post(\n    baseUrl.resolve('/inspections'),\n    headers: await _authorizedJsonHeaders(),\n    body: jsonEncode(input.toJson()),\n  ).timeout(timeout);\n\n  return switch (response.statusCode) {\n    201 => InspectionDto.decode(response.body).toDomain(),\n    _ => throw ApiFailure.fromResponse(response),\n  };\n}"
    add_code(s, code, Inches(0.60), Inches(1.28), Inches(7.25), Inches(5.46), highlight="TRANSPORT ONLY", size=11)
    add_card(s, Inches(8.15), Inches(1.28), Inches(4.56), Inches(2.47), "ApiClient boleh", ["Membentuk URI/header/body", "Timeout + decode", "Map response ke failure"], icon="✓", accent=GREEN, body_size=13)
    add_card(s, Inches(8.15), Inches(4.02), Inches(4.56), Inches(2.72), "ApiClient tidak boleh", ["Menampilkan SnackBar", "Memilih cache fallback", "Mengubah navigation", "Menyimpan widget state"], icon="×", accent=RED, body_size=13)
    add_notes(s, "11.03–11.18", 15, "Menjaga ApiClient fokus pada transport.", "Bandingkan dengan source hari 2. Tunjukkan http.Client injection.", "Keputusan cache berada di layer mana?", "Materi Hari 2: GET/POST.")
    n += 1

    s = base_slide(prs, "API CONTRACT", "HTTP status → typed failure → UX", n, total, 2)
    add_table(s, ["Signal", "Typed failure", "Policy", "UX"], [
        ["401", "unauthorized", "hapus session", "kembali login"],
        ["409", "conflict", "jangan retry buta", "jelaskan duplikasi"],
        ["422", "validation", "map field errors", "tetap di form"],
        ["429", "rateLimited", "hormati Retry-After", "coba nanti"],
        ["5xx", "server", "retry terkontrol", "error + retry"],
        ["timeout/offline", "network", "GET boleh cache", "cached/read-only"],
        ["invalid JSON", "contract", "no silent fallback", "format tidak valid"],
    ], Inches(0.60), Inches(1.23), Inches(12.12), Inches(5.43), widths=[Inches(1.55), Inches(2.35), Inches(3.65), Inches(4.57)], font_size=12)
    add_notes(s, "11.18–11.32", 14, "Memisahkan technical error dari keputusan UX.", "Minta peserta menelusuri satu status dari HTTP sampai UI.", "Mengapa 401 tidak boleh menampilkan cache lama?", "Modul Hari 2: HTTP error.")
    n += 1

    s = base_slide(prs, "API CONTRACT", "Session flow yang aman", n, total, 2)
    add_flow(s, ["Login", "Validate", "Store token", "Authorize", "Expire / logout"], Inches(0.62), Inches(1.42), Inches(12.08), descriptions=["credential → HTTPS", "200 + schema", "secure storage", "Bearer per request", "clear token + cache"])
    add_card(s, Inches(0.62), Inches(3.50), Inches(5.84), Inches(2.70), "Security baseline", ["Tidak mencetak token/password", "TLS untuk hosted API", "Token disimpan via secure storage", "401 mengakhiri session"], icon="S", accent=CYAN, body_size=13)
    add_card(s, Inches(6.82), Inches(3.50), Inches(5.88), Inches(2.70), "Bukan scope training", ["Refresh token rotation", "SSO/OAuth production", "Certificate pinning", "Audit layanan production"], icon="→", accent=GOLD, body_size=13)
    add_notes(s, "11.32–11.43", 11, "Menjelaskan lifecycle session.", "Tunjukkan token sebagai detail platform, bukan state yang disebar ke widget.", "Data apa saja yang harus dibersihkan saat logout?", "Modul Hari 2: secure storage/logout.")
    n += 1

    s = base_slide(prs, "API CONTRACT", "POST, timeout, dan idempotency", n, total, 2)
    add_card(s, Inches(0.65), Inches(1.30), Inches(3.62), Inches(4.90), "Fakta", ["Timeout hanya berarti client berhenti menunggu", "Server mungkin sudah membuat record", "Retry dapat menggandakan data"], icon="1", accent=RED, body_size=14)
    add_card(s, Inches(4.52), Inches(1.30), Inches(3.62), Inches(4.90), "Client", ["Disable submit saat request", "Buat request ID stabil", "Jangan auto-retry POST tanpa policy"], icon="2", accent=CYAN, body_size=14)
    add_card(s, Inches(8.39), Inches(1.30), Inches(3.62), Inches(4.90), "API contract", ["Terima Idempotency-Key", "Kembalikan hasil request yang sama", "409 bila aturan bisnis konflik"], icon="3", accent=GOLD, body_size=14)
    add_box(s, Inches(1.65), Inches(6.38), Inches(10.05), Inches(0.42), NAVY, None)
    add_text(s, "Kelas inti: submit guard. Pengayaan profesional: idempotency end-to-end.", Inches(1.75), Inches(6.51), Inches(9.85), Inches(0.18), size=12, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
    add_notes(s, "11.43–11.55", 12, "Membahas ketidakpastian POST timeout.", "Simulasikan delay dan minta peserta menjelaskan kemungkinan state server.", "Kapan retry POST aman?", "Modul Hari 2: timeout dan duplikasi POST.")
    n += 1

    s = base_slide(prs, "PRAKTIK", "Lab 1 — contract sebelum wiring UI", n, total, 2)
    add_card(s, Inches(0.62), Inches(1.25), Inches(7.42), Inches(5.42), "Langkah", ["Buka /docs dan catat server/version", "Login benar dan salah", "GET tanpa token → 401", "POST invalid → 422 + field error", "POST valid → 201 + server ID", "Simpan request/response tanpa secret"], icon="LAB", accent=CYAN, body_size=15)
    add_card(s, Inches(8.35), Inches(1.25), Inches(4.36), Inches(2.28), "Definition of Done", ["Schema cocok dengan model", "Status code cocok PRD", "Base URL tercatat"], icon="✓", accent=GREEN, body_size=12)
    add_card(s, Inches(8.35), Inches(3.79), Inches(4.36), Inches(2.88), "Fallback", ["Jika hosted API down, jalankan mock Python", "Gunakan kontrak identik", "Catat blocker hosting terpisah"], icon="B", accent=GOLD, body_size=13)
    add_notes(s, "11.55–12.00", 5, "Memberi briefing praktik sebelum istirahat/kelanjutan.", "Peserta bekerja berpasangan. Reviewer memeriksa ApiClient, mapping, status dan UI state.", "Bukti apa yang aman dibagikan?", "requests.http dan kontrak API training.")
    n += 1

    s = add_section_slide(prs, 2, n, total, "03", "State & data policy", "State eksplisit membuat UI deterministik; repository membuat keputusan sumber data.", ["Memodelkan state", "Mengatur cache", "Menjaga lifecycle async"])
    add_notes(s, "13.00–13.02", 2, "Membuka sesi state/storage.", "Kaitkan response API dengan kondisi UI yang dapat dilihat pengguna.", "Apakah loading adalah bool atau bagian dari model state?", "Modul Hari 2: ChangeNotifier.")
    n += 1

    s = base_slide(prs, "STATE", "State eksplisit, bukan kumpulan bool", n, total, 2)
    add_code(s, "sealed class InspectionState { const InspectionState(); }\nclass Initial extends InspectionState {}\nclass Loading extends InspectionState {\n  const Loading(this.previous);\n  final List<Inspection> previous;\n}\nclass Data extends InspectionState {\n  const Data(this.items, {required this.source, required this.at});\n}\nclass Failure extends InspectionState {\n  const Failure(this.error, this.previous);\n}", Inches(0.60), Inches(1.25), Inches(6.55), Inches(5.55), label="STATE MODEL", size=11)
    add_card(s, Inches(7.46), Inches(1.25), Inches(5.25), Inches(2.52), "Masalah banyak bool", ["loading + error bisa aktif bersamaan", "empty tidak jelas", "cached terselip sebagai flag"], icon="?", accent=RED, body_size=13)
    add_card(s, Inches(7.46), Inches(4.06), Inches(5.25), Inches(2.74), "Pilihan kelas", ["Source saat ini boleh tetap bool sederhana", "Gunakan invariant yang jelas", "Sealed state adalah jalur evolusi"], icon="→", accent=CYAN, body_size=13)
    add_notes(s, "13.02–13.17", 15, "Menunjukkan state model yang menghilangkan kombinasi ilegal.", "Bandingkan dengan controller source; minta peserta menuliskan invariant tiap bool.", "Bisakah error tampil sambil data lama tetap terlihat?", "Modul Hari 2: ChangeNotifier.")
    n += 1

    s = base_slide(prs, "STATE", "Repository mengorkestrasi remote dan cache", n, total, 2)
    add_flow(s, ["load()", "remote GET", "write cache", "Data(remote)"], Inches(0.72), Inches(1.42), Inches(11.88), descriptions=["user intent", "authoritative", "best effort", "fresh timestamp"])
    add_text(s, "failure network / timeout", Inches(3.12), Inches(3.38), Inches(2.4), Inches(0.24), size=12, color=RED, bold=True, align=PP_ALIGN.CENTER)
    add_connector(s, Inches(4.31), Inches(3.18), Inches(4.31), Inches(4.03), color=RED, width=2, dashed=True)
    add_flow(s, ["read cache", "validate schema", "Data(cache)", "read-only UI"], Inches(0.72), Inches(4.10), Inches(11.88), colors=[GOLD, ORANGE, GOLD, NAVY_2], descriptions=["optional", "drop corrupt", "with fetchedAt", "create disabled"])
    add_text(s, "401 / validation / server contract error tidak otomatis memakai cache.", Inches(1.70), Inches(6.45), Inches(9.92), Inches(0.28), size=14, color=BLUE, bold=True, align=PP_ALIGN.CENTER)
    add_notes(s, "13.17–13.32", 15, "Menjelaskan source policy di repository.", "Trace success dan offline. Bedakan failure jaringan dari auth/contract.", "Mengapa cache read-only?", "Modul Hari 2: cache fallback.")
    n += 1

    s = base_slide(prs, "STATE", "Cache policy harus tertulis", n, total, 2)
    add_table(s, ["Kondisi", "Remote", "Cache", "Aksi UI"], [
        ["GET 200", "authoritative", "tulis + timestamp", "fresh data"],
        ["offline/timeout", "unavailable", "baca jika valid", "banner cached"],
        ["401", "session invalid", "hapus", "login"],
        ["422", "request invalid", "jangan pakai", "field errors"],
        ["5xx", "server failure", "sesuai policy", "retry/cached jelas"],
        ["cache corrupt", "—", "hapus", "error bila remote gagal"],
        ["logout", "—", "hapus", "signed out"],
    ], Inches(0.58), Inches(1.22), Inches(12.16), Inches(5.42), widths=[Inches(2.25), Inches(2.45), Inches(3.05), Inches(4.41)], font_size=12)
    add_notes(s, "13.32–13.44", 12, "Membuat cache policy dapat direview.", "Tekankan fetchedAt dan mode read-only. Jangan menyamarkan stale data sebagai fresh.", "Kapan 5xx boleh fallback?", "Modul dan PRD Hari 2.")
    n += 1

    s = base_slide(prs, "STATE", "Async lifecycle: hasil lama tidak boleh menang", n, total, 2)
    add_card(s, Inches(0.60), Inches(1.28), Inches(3.78), Inches(4.96), "Risiko", ["Double tap mengirim dua request", "Search lama selesai setelah query baru", "Controller disposed saat request selesai", "Refresh menimpa create"], icon="!", accent=RED, body_size=14)
    add_card(s, Inches(4.78), Inches(1.28), Inches(3.78), Inches(4.96), "Guard", ["isLoading/isSubmitting", "request generation ID", "disposed/mounted check", "cancel/debounce jika relevan"], icon="G", accent=CYAN, body_size=14)
    add_card(s, Inches(8.96), Inches(1.28), Inches(3.78), Inches(4.96), "Ownership", ["Controller dibuat sekali", "Listener dilepas pemilik", "http.Client ditutup", "Context tidak disimpan"], icon="O", accent=GREEN, body_size=14)
    add_text(s, "Correctness dulu; cancellation dan concurrency ditambah saat use case menuntut.", Inches(1.40), Inches(6.52), Inches(10.55), Inches(0.28), size=14, color=BLUE, bold=True, align=PP_ALIGN.CENTER)
    add_notes(s, "13.44–13.58", 14, "Mencegah race condition dan update setelah dispose.", "Demo double refresh atau delayed response.", "Bagaimana membuktikan response lama tidak menimpa response baru?", "Modul Hari 2: lifecycle controller.")
    n += 1

    s = base_slide(prs, "STATE", "UI merender state—bukan mengarang state", n, total, 2)
    items = [
        ("Initial", "trigger load once", CYAN),
        ("Loading", "skeleton/progress; previous optional", BLUE),
        ("Data", "list + timestamp + source", GREEN),
        ("Empty", "explain + create CTA", GOLD),
        ("Failure", "message + recovery", RED),
        ("Cached", "visible banner + read-only", ORANGE),
    ]
    for i, (name, desc, color) in enumerate(items):
        col, row = i % 3, i // 3
        x = Inches(0.62 + col * 4.18)
        y = Inches(1.33 + row * 2.55)
        add_card(s, x, y, Inches(3.84), Inches(2.18), name, desc, icon=str(i + 1), accent=color, body_size=13)
    add_text(s, "Setiap state menjawab: apa yang terjadi, data apa tersedia, dan aksi apa aman.", Inches(1.18), Inches(6.56), Inches(10.95), Inches(0.25), size=14, color=BLUE, bold=True, align=PP_ALIGN.CENTER)
    add_notes(s, "13.58–14.10", 12, "Mengaitkan state ke komponen UI.", "Minta peserta menunjuk layar untuk tiap state. Pastikan retry tidak tersembunyi.", "Apa perbedaan Empty dan Failure?", "PRD Hari 2: loading/success/empty/error.")
    n += 1

    s = base_slide(prs, "STATE", "Search, filter, dan pagination punya semantics", n, total, 2)
    add_card(s, Inches(0.62), Inches(1.26), Inches(3.82), Inches(4.98), "Local filter", ["Hanya data yang sudah dimuat", "Cepat dan offline", "Label jangan menyiratkan global search"], icon="L", accent=CYAN, body_size=14)
    add_card(s, Inches(4.76), Inches(1.26), Inches(3.82), Inches(4.98), "Server search", ["Query menjadi kontrak", "Debounce + cancellation", "Error/loading per query"], icon="S", accent=BLUE, body_size=14)
    add_card(s, Inches(8.90), Inches(1.26), Inches(3.82), Inches(4.98), "Pagination", ["Cursor/page konsisten", "Deduplicate by ID", "Prevent request ganda", "Refresh reset page"], icon="P", accent=GOLD, body_size=14)
    add_box(s, Inches(2.05), Inches(6.42), Inches(9.25), Inches(0.40), NAVY, None)
    add_text(s, "Semantics lebih penting daripada sekadar field search terlihat.", Inches(2.10), Inches(6.54), Inches(9.15), Inches(0.18), size=12, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
    add_notes(s, "14.10–14.25", 15, "Mencegah search/pagination yang menyesatkan.", "Bandingkan local filter dengan server query. Pagination tetap demo/pengayaan.", "Apakah pencarian lokal menemukan data di halaman yang belum dimuat?", "Modul Hari 2: search/pagination.")
    n += 1

    s = base_slide(prs, "PRAKTIK", "Lab 2 — state, restart, offline, logout", n, total, 2)
    add_card(s, Inches(0.60), Inches(1.26), Inches(7.34), Inches(5.42), "Skenario berurutan", ["Login → fresh list + timestamp", "Restart → session dipulihkan", "Stop API → refresh → cached/read-only", "Start API → retry → fresh", "Logout → token dan cache hilang", "Login ulang → tidak memakai cache user lama"], icon="LAB", accent=CYAN, body_size=15)
    add_card(s, Inches(8.26), Inches(1.26), Inches(4.46), Inches(2.46), "Bukti minimum", ["Screen recording / screenshot", "Log tanpa secret", "State transition dicatat"], icon="E", accent=GREEN, body_size=13)
    add_card(s, Inches(8.26), Inches(4.02), Inches(4.46), Inches(2.66), "Code review", ["Tidak request dari build", "Repository memilih source", "UI tidak akses storage"], icon="R", accent=GOLD, body_size=13)
    add_notes(s, "14.25–14.30", 5, "Memberi briefing lab sebelum istirahat.", "Pasangan bertukar driver/reviewer setelah skenario offline.", "Apa bukti cache benar-benar dibersihkan saat logout?", "PRD Hari 2 acceptance.")
    n += 1

    s = add_section_slide(prs, 2, n, total, "04", "Failure engineering", "Sistem profesional dirancang untuk gagal dengan jelas, aman, dan dapat dipulihkan.", ["Menguji failure", "Membuat observability", "Melakukan clean-code review"])
    add_notes(s, "14.45–14.47", 2, "Membuka sesi failure handling.", "Gunakan fault simulation pada mock/hosted API.", "Failure mana yang paling berbahaya bila disamarkan?", "Modul Hari 2: troubleshooting.")
    n += 1

    s = base_slide(prs, "FAILURE", "Matriks fault injection", n, total, 2)
    add_table(s, ["Skenario", "Cara simulasi", "Expected result", "Evidence"], [
        ["401", "token invalid/expired", "clear session → login", "transition"],
        ["422", "note terlalu pendek", "field error; form tetap", "response + UI"],
        ["500", "--fail-list/create", "message + retry", "state"],
        ["timeout", "--delay 11", "GET cache / POST uncertain", "timing"],
        ["offline", "stop container/server", "cache atau error", "banner"],
        ["invalid JSON", "contract fault", "contract failure", "no crash"],
    ], Inches(0.58), Inches(1.25), Inches(12.16), Inches(5.18), widths=[Inches(1.75), Inches(3.05), Inches(4.05), Inches(3.31)], font_size=12)
    add_text(s, "Uji satu fault pada satu waktu agar diagnosis tidak ambigu.", Inches(2.05), Inches(6.58), Inches(9.25), Inches(0.25), size=14, color=BLUE, bold=True, align=PP_ALIGN.CENTER)
    add_notes(s, "14.47–15.02", 15, "Membuat kegagalan dapat direproduksi.", "Jalankan fault terarah; catat expected sebelum melihat hasil.", "Mengapa mencampur beberapa fault membuat diagnosis lemah?", "mock_api.py fault flags.")
    n += 1

    s = base_slide(prs, "FAILURE", "Observability tanpa membocorkan secret", n, total, 2)
    add_card(s, Inches(0.62), Inches(1.28), Inches(3.78), Inches(4.98), "Log", ["method + path", "status + duration", "request ID", "failure type", "environment/version"], icon="L", accent=CYAN, body_size=14)
    add_card(s, Inches(4.78), Inches(1.28), Inches(3.78), Inches(4.98), "Redact", ["Authorization", "password", "token", "PII/body sensitif", "keystore path/password"], icon="×", accent=RED, body_size=14)
    add_card(s, Inches(8.94), Inches(1.28), Inches(3.78), Inches(4.98), "Correlate", ["X-Request-Id", "request → response", "app version", "timestamp UTC", "user-safe error ID"], icon="ID", accent=GOLD, body_size=14)
    add_text(s, "Debugging mengikuti request–response, bukan tebak-tebakan screenshot.", Inches(1.23), Inches(6.56), Inches(10.85), Inches(0.25), size=14, color=BLUE, bold=True, align=PP_ALIGN.CENTER)
    add_notes(s, "15.02–15.15", 13, "Menetapkan logging Flutter yang aman dan berguna.", "Tunjukkan method, path, status, duration, dan request ID tanpa Authorization/body sensitif.", "Data apa yang tidak boleh masuk log?", "Security baseline materi Hari 2.")
    n += 1

    s = base_slide(prs, "CLEAN CODE", "Anti-pattern → refactor", n, total, 2)
    add_table(s, ["Smell", "Risiko", "Refactor minimum"], [
        ["HTTP di widget", "lifecycle + test sulit", "pindah ApiClient/repository"],
        ["String error acak", "UX tidak konsisten", "typed failure + mapper"],
        ["Global mutable state", "ownership kabur", "constructor + owner jelas"],
        ["Catch Object lalu diam", "bug tersembunyi", "handle known; report unknown"],
        ["URL/token tersebar", "env/security leak", "AppConfig + TokenStore"],
        ["Bool saling konflik", "state ilegal", "invariant/sealed state"],
        ["Retry semua request", "duplikasi/rate limit", "retry policy per operation"],
    ], Inches(0.58), Inches(1.22), Inches(12.16), Inches(5.50), widths=[Inches(3.05), Inches(3.80), Inches(5.31)], font_size=12)
    add_notes(s, "15.15–15.30", 15, "Melatih code review berbasis smell.", "Setiap pasangan memilih satu smell nyata dan melakukan refactor minimum.", "Refactor mana memberi dampak terbesar dengan perubahan terkecil?", "Modul Hari 2: clean code.")
    n += 1

    s = base_slide(prs, "CLEAN CODE", "Test portfolio untuk Hari 2", n, total, 2)
    add_card(s, Inches(0.62), Inches(1.30), Inches(3.76), Inches(4.84), "Unit", ["JSON parse", "validation", "failure mapping", "cache policy"], icon="U", accent=CYAN, body_size=14)
    add_card(s, Inches(4.78), Inches(1.30), Inches(3.76), Inches(4.84), "State", ["load success", "error + retry", "401 expire", "submit guard"], icon="S", accent=BLUE, body_size=14)
    add_card(s, Inches(8.94), Inches(1.30), Inches(3.76), Inches(4.84), "API client", ["JSON fixture", "status/schema", "auth header", "timeout/failure mapping"], icon="C", accent=GOLD, body_size=14)
    add_box(s, Inches(1.33), Inches(6.34), Inches(10.65), Inches(0.48), NAVY, None)
    add_text(s, "Test boundary yang bernilai—bukan mengejar jumlah test.", Inches(1.50), Inches(6.48), Inches(10.30), Inches(0.20), size=13, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
    add_notes(s, "15.30–15.45", 15, "Menetapkan test sesuai risiko.", "Tuliskan satu test per kartu yang akan ditambahkan Hari 3.", "Test mana paling cepat mendeteksi contract drift?", "Modul Hari 2 dan Hari 3 testing.")
    n += 1

    s = base_slide(prs, "PRAKTIK", "Lab 3 — failure drill & code review", n, total, 2)
    add_card(s, Inches(0.60), Inches(1.25), Inches(7.34), Inches(5.44), "Tugas pasangan", ["Pilih dua fault dari matriks", "Prediksi state dan UX", "Jalankan fault", "Perbaiki satu clean-code smell", "Tambahkan satu test regression", "Review dengan pasangan lain"], icon="LAB", accent=CYAN, body_size=15)
    add_card(s, Inches(8.26), Inches(1.25), Inches(4.46), Inches(2.47), "Reviewer checks", ["Boundary bersih", "Error actionable", "Secret tidak terlihat"], icon="R", accent=GOLD, body_size=13)
    add_card(s, Inches(8.26), Inches(4.02), Inches(4.46), Inches(2.67), "Stop condition", ["Expected = actual", "Test lulus", "Tidak mengubah scope fitur"], icon="✓", accent=GREEN, body_size=13)
    add_notes(s, "15.45–16.00", 15, "Menjalankan failure drill singkat.", "Trainer fokus pada evidence dan reasoning, bukan membantu menambah fitur.", "Apakah perbaikan mencegah regresi yang sama?", "PRD Hari 2.")
    n += 1

    s = base_slide(prs, "CHECKPOINT", "Definition of Done — day 2", n, total, 2)
    add_table(s, ["Area", "Wajib", "Bukti"], [
        ["API client", "login, GET, POST, 401, 422", "test + REST capture"],
        ["Architecture", "UI → controller → repository → data", "source review"],
        ["State", "loading/data/empty/error/cached", "demo states"],
        ["Session", "secure token + logout clear", "restart/logout"],
        ["Resilience", "timeout/offline/retry", "fault drill"],
        ["Quality", "format/analyze/test", "clean output"],
        ["Git", "README + lockfile + no secret", "tag day-2"],
    ], Inches(0.58), Inches(1.22), Inches(12.16), Inches(5.48), widths=[Inches(2.05), Inches(5.85), Inches(4.26)], font_size=12)
    add_notes(s, "16.00–16.10", 10, "Menilai hasil dengan evidence.", "Gunakan status Lulus/Perlu perbaikan/Terhalang prasyarat.", "Area mana belum punya bukti?", "PRD Hari 2 AC1–AC11.")
    n += 1

    s = base_slide(prs, "CHECKPOINT", "Flutter integration checklist", n, total, 2)
    add_card(s, Inches(0.62), Inches(1.28), Inches(3.78), Inches(5.06), "Configuration", ["Base URL via dart-define", "HTTPS untuk release", "Timeout terpusat", "No hard-coded secret", "Debug cleartext terbatas", "Environment terlihat"], icon="CF", accent=GOLD, body_size=13)
    add_card(s, Inches(4.78), Inches(1.28), Inches(3.78), Inches(5.06), "Implementation", ["Model/DTO bertipe", "ApiClient fokus transport", "Repository memilih source", "Controller memiliki state", "UI hanya render/intent", "Lifecycle ditutup"], icon="FL", accent=CYAN, body_size=13)
    add_card(s, Inches(8.94), Inches(1.28), Inches(3.78), Inches(5.06), "Evidence", ["Test parser/state", "GET/POST berhasil", "401/422 dipetakan", "Offline/cache jelas", "Request ID tanpa token", "README dapat diikuti"], icon="✓", accent=GREEN, body_size=13)
    add_text(s, "Review berpusat pada kualitas implementasi Flutter.", Inches(2.10), Inches(6.58), Inches(9.10), Inches(0.25), size=14, color=BLUE, bold=True, align=PP_ALIGN.CENTER)
    add_notes(s, "16.10–16.20", 10, "Melakukan review integrasi Flutter.", "Gunakan checklist untuk source review dan demo. Deployment layanan tidak dibahas.", "Boundary mana masih bocor?", "Modul dan PRD Hari 2.")
    n += 1

    s = base_slide(prs, "CHECKPOINT", "Evaluasi: jelaskan keputusan, bukan hafalan", n, total, 2)
    questions = [
        "Mengapa UI tidak boleh mengetahui HTTP status?",
        "Kapan GET boleh memakai cache?",
        "Mengapa POST timeout tidak otomatis aman untuk retry?",
        "Apa bukti model Dart sesuai response API?",
        "Dependency apa yang dibuat fake untuk state test?",
        "Apa yang harus dibersihkan saat 401/logout?",
    ]
    for i, q in enumerate(questions):
        col, row = i % 2, i // 2
        x = Inches(0.62 + col * 6.18)
        y = Inches(1.30 + row * 1.72)
        add_card(s, x, y, Inches(5.87), Inches(1.43), f"{i + 1:02d}", q, accent=CYAN if col == 0 else GOLD, title_size=13, body_size=12)
    add_notes(s, "16.20–16.27", 7, "Mengukur reasoning peserta.", "Gunakan pertanyaan bergilir; minta contoh dari source mereka.", "Keputusan mana yang masih belum bisa dibuktikan?", "Materi dan PRD Hari 2.")
    n += 1

    s = base_slide(prs, "CLOSING", "Checkpoint Git dan kelanjutan Hari 3", n, total, 2, bg=NAVY)
    add_text(s, "day-2", Inches(0.72), Inches(1.22), Inches(4.2), Inches(0.85), size=54, color=CYAN, bold=True, font=FONT_DISPLAY)
    add_text(s, "Commit yang dapat dijalankan ulang", Inches(0.75), Inches(2.14), Inches(5.5), Inches(0.42), size=22, color=WHITE, bold=True)
    add_code(s, "dart format lib test\nflutter analyze\nflutter test\n\ngit add .\ngit commit -m \"Complete day-2 API checkpoint\"\ngit tag day-2", Inches(0.75), Inches(2.86), Inches(5.90), Inches(3.22), label="QUALITY GATE", size=12)
    add_card(s, Inches(7.05), Inches(1.22), Inches(5.55), Inches(4.86), "Input Hari 3", ["Contract API stabil", "Failure dapat disimulasikan", "Controller/repository dapat di-fake", "Tidak ada secret di repo", "Known blocker punya PIC"], icon="→", accent=CYAN, fill=NAVY_2, body_size=14)
    add_text(s, f"{n:02d} / {total:02d}", Inches(11.62), Inches(6.88), Inches(0.95), Inches(0.22), size=10, color=CYAN_2, bold=True, align=PP_ALIGN.RIGHT)
    add_notes(s, "16.27–16.30", 3, "Menutup Hari 2 dengan checkpoint reproducible.", "Pastikan README mencatat base URL placeholder dan fallback mock.", "Apa satu blocker yang perlu selesai sebelum Hari 3?", "README proyek Hari 2.")
    n += 1

    s = base_slide(prs, "REFERENCE", "Referensi dan scope pengayaan", n, total, 2)
    add_card(s, Inches(0.62), Inches(1.22), Inches(5.86), Inches(5.52), "Rujukan inti", ["docs.flutter.dev/app-architecture", "docs.flutter.dev/cookbook/networking", "Dart JSON serialization", "flutter_secure_storage", "shared_preferences", "Modul + PRD Hari 2"], icon="R", accent=CYAN, body_size=13)
    add_card(s, Inches(6.82), Inches(1.22), Inches(5.90), Inches(5.52), "Pengayaan setelah kelas", ["Code generation model/DTO", "Refresh-token rotation", "Offline write queue + conflict resolution", "Observability Flutter", "Integration test di CI", "Pagination/cursor penuh"], icon="+", accent=GOLD, body_size=13)
    add_notes(s, "Cadangan", 1, "Menutup dengan rujukan yang dapat dilanjutkan.", "Jangan mengerjakan pengayaan sebelum acceptance inti lulus.", "Pengayaan mana memberi nilai terbesar untuk roadmap tim?", "Dokumentasi resmi dan modul Hari 2.")

    assert len(prs.slides) == total, (len(prs.slides), total)
    out = ROOT / "Hari_2_Flutter_Professional.pptx"
    prs.save(out)
    shutil.copy2(out, OUT_DIR / "Hari_2_Architecture_API_State_Storage.pptx")
    return out


def build_day3(background: Path):
    total = 39
    prs = Presentation()
    prs.slide_width = SW
    prs.slide_height = SH
    n = 1

    s = add_cover(prs, 3, "Flutter Quality, Native\n& Release Engineering", "Foto native, test strategy, performance evidence, signing, dan release yang dapat diaudit.", ["NATIVE", "TESTING", "DEVTOOLS", "RELEASE"], background, total)
    add_notes(s, "Pembukaan", 3, "Menyepakati target Hari 3.", "Hari 3 membawa keputusan Hari 2 menuju bukti kualitas dan artefak release.", "Apa yang membuat build layak disebut release candidate?", "Modul dan PRD Hari 3.")
    n += 1

    s = add_outcome_slide(prs, 3, n, total, "Hasil belajar yang dapat dibuktikan", [
        ("Native boundary", ["Plugin dibungkus adapter", "Lifecycle/cancel/error jelas"], "N", CYAN),
        ("Test portfolio", ["Unit, state, widget, contract", "Fake mengganti dependency"], "T", BLUE),
        ("Performance evidence", ["Skenario repeatable", "Before/after tanpa klaim palsu"], "P", GOLD),
        ("Release confidence", ["Signer diverifikasi", "Smoke test + release notes"], "R", GREEN),
    ])
    add_notes(s, "08.30–08.40", 10, "Menjelaskan Definition of Done Hari 3.", "Minta peserta menentukan evidence untuk tiap outcome.", "Apa beda test lulus dengan release siap?", "PRD Hari 3.")
    n += 1

    s = add_agenda_slide(prs, 3, n, total, [
        ("08.30", "Native photo boundary", "Preview, cancel, lost-data, ownership"),
        ("10.15", "Test strategy & quality gate", "Unit/state/widget/contract lulus"),
        ("13.00", "Profiling & clean-up", "Satu perbaikan terukur"),
        ("14.45", "Android release engineering", "Signed APK/AAB + verification"),
        ("16.00", "Demo & handover", "Smoke test, notes, tag day-3"),
    ])
    add_notes(s, "08.40–08.45", 5, "Menjelaskan roadmap Hari 3.", "Tunjukkan kapan sesi praktik dan kapan bukti diperiksa.", "Bagian mana memerlukan physical device?", "Silabus Hari 3.")
    n += 1

    s = base_slide(prs, "ORIENTASI", "Input dari day-2: quality starts upstream", n, total, 3)
    add_card(s, Inches(0.62), Inches(1.26), Inches(3.78), Inches(4.98), "API integration", ["Model/schema stabil", "Failure mapping jelas", "ApiClient dapat diuji"], icon="C", accent=CYAN, body_size=14)
    add_card(s, Inches(4.78), Inches(1.26), Inches(3.78), Inches(4.98), "Architecture", ["Boundary dapat di-fake", "Ownership lifecycle jelas", "State deterministik"], icon="A", accent=BLUE, body_size=14)
    add_card(s, Inches(8.94), Inches(1.26), Inches(3.78), Inches(4.98), "Security", ["No secret in repo/log", "Session clear", "Release memakai HTTPS"], icon="S", accent=GOLD, body_size=14)
    add_text(s, "Jika day-2 belum stabil, Hari 3 menjadi debugging marathon—bukan quality engineering.", Inches(1.0), Inches(6.53), Inches(11.3), Inches(0.28), size=14, color=RED, bold=True, align=PP_ALIGN.CENTER)
    add_notes(s, "08.45–08.55", 10, "Memastikan baseline Hari 2 siap.", "Jalankan smoke login/list/create singkat sebelum plugin dipasang.", "Apa blocker yang harus dihentikan sebelum menambah native feature?", "Checkpoint day-2.")
    n += 1

    s = add_section_slide(prs, 3, n, total, "01", "Native feature boundary", "Gunakan plugin untuk capability platform; bungkus agar UI dan test tetap bersih.", ["Mendesain adapter", "Menangani lifecycle", "Menjaga ownership file"])
    add_notes(s, "08.55–08.57", 2, "Membuka sesi native feature.", "Scope tetap satu fitur foto lokal sesuai buku.", "Apa yang membuat plugin berbeda dari widget biasa?", "Modul Hari 3: image_picker.")
    n += 1

    s = base_slide(prs, "NATIVE", "Plugin adalah infrastructure dependency", n, total, 3)
    add_flow(s, ["PhotoPanel", "PhotoController", "PhotoPicker", "image_picker", "Android / iOS"], Inches(0.62), Inches(1.45), Inches(12.08), descriptions=["render + intent", "state machine", "app abstraction", "plugin API", "platform capability"])
    add_card(s, Inches(0.62), Inches(3.62), Inches(5.82), Inches(2.56), "Mengapa adapter?", ["Plugin dapat di-fake", "Exception diterjemahkan", "UI tidak bergantung XFile langsung"], icon="A", accent=CYAN, body_size=13)
    add_card(s, Inches(6.82), Inches(3.62), Inches(5.88), Inches(2.56), "Kapan MethodChannel?", ["Capability tidak tersedia", "Perlu API native khusus", "Tim siap memelihara dua platform"], icon="M", accent=GOLD, body_size=13)
    add_notes(s, "08.57–09.10", 13, "Menempatkan plugin pada boundary infrastructure.", "Jelaskan jalur UI ke native tanpa masuk terlalu dalam ke MethodChannel.", "Bagaimana widget test berjalan tanpa membuka kamera?", "Modul Hari 3: plugin vs MethodChannel.")
    n += 1

    s = base_slide(prs, "NATIVE", "Photo picker sebagai state machine", n, total, 3)
    states = [
        ("idle", CYAN), ("picking", BLUE), ("selected", GREEN), ("cancelled", GOLD), ("failure", RED), ("recovering", ORANGE)
    ]
    positions = [(0.8, 1.45), (3.1, 1.45), (5.4, 1.45), (3.1, 4.25), (7.7, 4.25), (7.7, 1.45)]
    for (label, color), (x, y) in zip(states, positions):
        add_box(s, Inches(x), Inches(y), Inches(1.75), Inches(0.78), color, None)
        add_text(s, label, Inches(x), Inches(y + 0.23), Inches(1.75), Inches(0.25), size=14, color=NAVY if color in (CYAN, GOLD) else WHITE, bold=True, align=PP_ALIGN.CENTER)
    arrows = [((2.55, 1.84), (3.05, 1.84)), ((4.85, 1.84), (5.35, 1.84)), ((7.15, 1.84), (7.65, 1.84)), ((3.98, 2.25), (3.98, 4.2)), ((8.58, 2.25), (8.58, 4.2)), ((9.45, 1.84), (11.85, 1.84))]
    for (a, b) in arrows:
        add_connector(s, Inches(a[0]), Inches(a[1]), Inches(b[0]), Inches(b[1]), color=MUTED, width=2)
    add_card(s, Inches(10.02), Inches(1.22), Inches(2.65), Inches(4.45), "Invariant", ["Satu pick aktif", "Cancel bukan error", "Selected terikat ID", "Recovery tidak lintas record"], icon="✓", accent=CYAN, body_size=12)
    add_text(s, "State machine mengurangi kombinasi _busy, _photo, _message yang ambigu.", Inches(0.95), Inches(6.38), Inches(9.05), Inches(0.28), size=14, color=BLUE, bold=True)
    add_notes(s, "09.10–09.25", 15, "Memodelkan alur foto secara eksplisit.", "Trace success, cancel, permission error, dan lost-data recovery.", "Apakah cancel harus ditampilkan sebagai error?", "PhotoPanel dan modul Hari 3.")
    n += 1

    s = base_slide(prs, "NATIVE", "Lifecycle, lost data, dan record identity", n, total, 3)
    add_code(s, "Future<void> pick(PhotoSource source) async {\n  if (state.isBusy) return;\n  await pendingStore.save(inspectionId);\n  emit(const Picking());\n  try {\n    final photo = await picker.pick(source);\n    if (!_isCurrentInspection()) return;\n    emit(photo == null ? const Cancelled() : Selected(photo));\n  } on PhotoPermissionFailure {\n    emit(const Failure('Periksa izin perangkat'));\n  } finally {\n    await pendingStore.clear();\n  }\n}", Inches(0.60), Inches(1.25), Inches(6.62), Inches(5.55), label="LIFECYCLE", highlight="IDENTITY FIRST", size=10.7)
    add_card(s, Inches(7.53), Inches(1.25), Inches(5.18), Inches(2.42), "Recovery rule", ["Simpan inspectionId sebelum picker", "retrieveLostData saat init", "Map hanya ke ID yang sama"], icon="R", accent=ORANGE, body_size=13)
    add_card(s, Inches(7.53), Inches(3.94), Inches(5.18), Inches(2.86), "Widget ownership", ["ValueKey(item.id)", "No context after dispose", "Busy disables action", "Previous preview survives cancel"], icon="O", accent=CYAN, body_size=13)
    add_notes(s, "09.25–09.42", 17, "Menjaga foto tidak menempel ke record salah.", "Gunakan source PhotoPanel sebagai demo. Tekankan recovery Android.", "Mengapa inspectionId harus disimpan sebelum membuka picker?", "image_picker lost data guidance.")
    n += 1

    s = base_slide(prs, "NATIVE", "File sementara bukan attachment server", n, total, 3)
    add_card(s, Inches(0.62), Inches(1.28), Inches(3.78), Inches(5.02), "Preview lokal", ["Path dapat sementara", "Belum tersinkron", "Tidak lintas device", "Boleh hilang setelah lifecycle"], icon="L", accent=CYAN, body_size=14)
    add_card(s, Inches(4.78), Inches(1.28), Inches(3.78), Inches(5.02), "Persist lokal", ["Copy ke app storage", "Metadata per inspection", "Cleanup policy", "Permission/privacy"], icon="P", accent=BLUE, body_size=14)
    add_card(s, Inches(8.94), Inches(1.28), Inches(3.78), Inches(5.02), "Upload server", ["Multipart/presigned URL", "Progress + retry", "Idempotency", "Retention/security"], icon="U", accent=GOLD, body_size=14)
    add_text(s, "Scope kelas berhenti di preview lokal; batas ini wajib terlihat di UI dan release notes.", Inches(1.0), Inches(6.54), Inches(11.3), Inches(0.28), size=14, color=RED, bold=True, align=PP_ALIGN.CENTER)
    add_notes(s, "09.42–09.55", 13, "Membedakan preview, persistence, dan upload.", "Jangan menjanjikan persistence dari sekadar Image.file.", "Apa konsekuensi privacy saat foto di-upload?", "Modul Hari 3: batas fitur foto.")
    n += 1

    s = base_slide(prs, "PRAKTIK", "Lab 1 — photo boundary", n, total, 3)
    add_card(s, Inches(0.60), Inches(1.25), Inches(7.34), Inches(5.44), "Skenario wajib", ["Pilih dari galeri → preview", "Cancel → preview lama tetap", "Permission/error → pesan actionable", "Double tap → satu picker", "Buka record lain → foto tidak berpindah", "Android process recovery → ID sama"], icon="LAB", accent=CYAN, body_size=15)
    add_card(s, Inches(8.26), Inches(1.25), Inches(4.46), Inches(2.47), "Device matrix", ["Simulator: gallery", "Physical: camera", "Widget test: fake picker"], icon="D", accent=GOLD, body_size=13)
    add_card(s, Inches(8.26), Inches(4.02), Inches(4.46), Inches(2.67), "Definition of Done", ["No crash", "No cross-record state", "Scope preview jelas"], icon="✓", accent=GREEN, body_size=13)
    add_notes(s, "09.55–10.00", 5, "Briefing praktik photo boundary.", "Gunakan perangkat fisik untuk acceptance kamera jika tersedia.", "Skenario mana tidak dapat dibuktikan oleh simulator?", "PRD Hari 3 AC foto.")
    n += 1

    s = add_section_slide(prs, 3, n, total, "02", "Test strategy", "Uji boundary berdasarkan risiko; gunakan fake untuk determinisme dan device untuk integrasi nyata.", ["Menyusun portfolio", "Menguji contract/state", "Menjalankan quality gate"])
    add_notes(s, "10.15–10.17", 2, "Membuka sesi testing.", "Tegaskan tiap test menjawab pertanyaan berbeda.", "Apa yang tidak bisa dibuktikan unit test?", "Flutter testing overview.")
    n += 1

    s = base_slide(prs, "TESTING", "Portfolio test berdasarkan confidence", n, total, 3)
    levels = [
        ("Unit", "cepat • banyak", Inches(0.90), Inches(4.88), Inches(11.55), CYAN),
        ("State / repository", "boundary • fake", Inches(2.00), Inches(3.72), Inches(9.35), BLUE),
        ("Widget", "interaction • UI states", Inches(3.05), Inches(2.56), Inches(7.25), GOLD),
        ("Integration / smoke", "plugin • network • release", Inches(4.10), Inches(1.40), Inches(5.15), GREEN),
    ]
    for title, desc, x, y, w, color in levels:
        add_box(s, x, y, w, Inches(0.92), color, None)
        add_text(s, title, x + Inches(0.15), y + Inches(0.18), w - Inches(0.3), Inches(0.25), size=16, color=NAVY if color in (CYAN, GOLD) else WHITE, bold=True, align=PP_ALIGN.CENTER)
        add_text(s, desc, x + Inches(0.15), y + Inches(0.51), w - Inches(0.3), Inches(0.18), size=10, color=NAVY if color in (CYAN, GOLD) else WHITE, align=PP_ALIGN.CENTER)
    add_text(s, "Semakin tinggi, semakin mahal—tetapi semakin dekat ke real environment.", Inches(1.40), Inches(6.35), Inches(10.55), Inches(0.28), size=14, color=BLUE, bold=True, align=PP_ALIGN.CENTER)
    add_notes(s, "10.17–10.30", 13, "Memilih level test sesuai risiko.", "Jangan menjadikan pyramid sebagai target persentase; gunakan confidence.", "Di level mana permission kamera dibuktikan?", "Flutter testing overview.")
    n += 1

    s = base_slide(prs, "TESTING", "Unit test: contract model dan rule bisnis", n, total, 3)
    add_code(s, "group('Inspection.fromJson', () {\n  test('normalizes timestamp to UTC', () {\n    final item = Inspection.fromJson(validPayload);\n    expect(item.createdAt.isUtc, isTrue);\n  });\n\n  test('rejects unknown condition', () {\n    expect(\n      () => Inspection.fromJson({...validPayload, 'condition': 'x'}),\n      throwsFormatException,\n    );\n  });\n});", Inches(0.60), Inches(1.28), Inches(7.08), Inches(5.44), label="UNIT TEST", size=11)
    add_card(s, Inches(7.98), Inches(1.28), Inches(4.73), Inches(2.42), "Good test", ["Nama menjelaskan perilaku", "Input mewakili risk", "Assert outcome, bukan implementation"], icon="✓", accent=GREEN, body_size=13)
    add_card(s, Inches(7.98), Inches(4.00), Inches(4.73), Inches(2.72), "Prioritas", ["Required field missing", "enum unknown", "UTC normalization", "validation boundaries"], icon="P", accent=CYAN, body_size=13)
    add_notes(s, "10.30–10.43", 13, "Menulis test pada boundary JSON/domain.", "Sengaja rusak parser lalu lihat test gagal; pulihkan.", "Bug apa yang tidak tertangkap oleh round-trip test saja?", "Model Inspection dan module testing.")
    n += 1

    s = base_slide(prs, "TESTING", "State test dengan fake dependency", n, total, 3)
    add_code(s, "test('401 expires session and exposes safe failure', () async {\n  final gateway = FakeGateway()\n    ..listError = const UnauthorizedFailure();\n  var expired = false;\n  final controller = InspectionController(\n    gateway, onSessionExpired: () => expired = true,\n  );\n\n  await controller.load();\n\n  expect(expired, isTrue);\n  expect(controller.state, isA<Failure>());\n});", Inches(0.60), Inches(1.28), Inches(7.05), Inches(5.46), label="STATE TEST", highlight="NO NETWORK", size=10.8)
    add_card(s, Inches(7.96), Inches(1.28), Inches(4.75), Inches(2.42), "Fake controls", ["success data", "specific failure", "delay/completion order"], icon="F", accent=CYAN, body_size=13)
    add_card(s, Inches(7.96), Inches(4.00), Inches(4.75), Inches(2.74), "Assert", ["state transition", "side effect callback", "submit guard", "previous data policy"], icon="A", accent=GOLD, body_size=13)
    add_notes(s, "10.43–10.58", 15, "Menguji controller tanpa HTTP/plugin.", "Tunjukkan dependency seam Hari 2 menjadi payoff Hari 3.", "Mengapa mock framework tidak wajib?", "Modul Hari 3: fake repository.")
    n += 1

    s = base_slide(prs, "TESTING", "API client test menjaga mapping Flutter", n, total, 3)
    add_flow(s, ["JSON fixture", "MockClient", "DTO decode", "Domain assertions"], Inches(0.72), Inches(1.40), Inches(11.90), descriptions=["known payload", "status/headers", "strict boundary", "business meaning"])
    add_card(s, Inches(0.72), Inches(3.62), Inches(5.75), Inches(2.63), "Minimum contract test", ["Status sesuai operation", "Required fields ada", "Enum/date valid", "Error body dapat dipetakan"], icon="C", accent=CYAN, body_size=13)
    add_card(s, Inches(6.84), Inches(3.62), Inches(5.78), Inches(2.63), "Test cases", ["200 parse success", "401 typed failure", "422 field mapping", "invalid JSON rejected"], icon="T", accent=GOLD, body_size=13)
    add_notes(s, "10.58–11.10", 12, "Mencegah regression pada ApiClient.", "Gunakan JSON fixture dan MockClient agar test cepat serta deterministik.", "Breaking response apa yang harus membuat test gagal?", "Modul Hari 2/3 dan package:http testing.")
    n += 1

    s = base_slide(prs, "TESTING", "Widget test: render state + user intent", n, total, 3)
    add_card(s, Inches(0.62), Inches(1.28), Inches(3.78), Inches(4.98), "Arrange", ["Fake controller/gateway", "Known state", "MaterialApp wrapper", "Stable keys"], icon="A", accent=CYAN, body_size=14)
    add_card(s, Inches(4.78), Inches(1.28), Inches(3.78), Inches(4.98), "Act", ["Tap retry/save", "Enter invalid input", "Pump transition", "Scroll/ensureVisible"], icon="A", accent=BLUE, body_size=14)
    add_card(s, Inches(8.94), Inches(1.28), Inches(3.78), Inches(4.98), "Assert", ["Correct state UI", "Action invoked once", "Navigation policy", "No hidden error"], icon="A", accent=GOLD, body_size=14)
    add_text(s, "Widget test tidak membuktikan permission, TLS, plugin registration, atau signer.", Inches(1.30), Inches(6.54), Inches(10.70), Inches(0.28), size=14, color=RED, bold=True, align=PP_ALIGN.CENTER)
    add_notes(s, "11.10–11.25", 15, "Menguji UI state dan interaksi.", "Gunakan key untuk save/retry. Jelaskan batas widget test.", "Apa yang masih memerlukan device test?", "Modul Hari 3: widget test.")
    n += 1

    s = base_slide(prs, "TESTING", "Integration & smoke test: environment nyata", n, total, 3)
    add_table(s, ["Scenario", "Debug", "Profile", "Release APK"], [
        ["Login/API HTTPS", "✓", "✓", "wajib"],
        ["Create + timeout policy", "✓", "opsional", "wajib"],
        ["Gallery/camera", "✓", "✓", "wajib device"],
        ["Permission denied", "✓", "—", "wajib"],
        ["Offline/cache", "✓", "—", "wajib"],
        ["Restart/logout", "✓", "—", "wajib"],
        ["Performance scenario", "—", "wajib", "sampling"],
    ], Inches(0.58), Inches(1.25), Inches(12.16), Inches(5.34), widths=[Inches(4.15), Inches(2.15), Inches(2.45), Inches(3.41)], font_size=12)
    add_text(s, "Release configuration adalah dependency—maka smoke test release tidak boleh dilewati.", Inches(1.0), Inches(6.62), Inches(11.3), Inches(0.25), size=13, color=BLUE, bold=True, align=PP_ALIGN.CENTER)
    add_notes(s, "11.25–11.38", 13, "Memisahkan tujuan mode test.", "Tunjukkan matrix device/mode dan pilih subset realistis.", "Mengapa debug success tidak menjamin release success?", "PRD Hari 3 release acceptance.")
    n += 1

    s = base_slide(prs, "TESTING", "Quality gate yang dapat dijalankan ulang", n, total, 3)
    add_code(s, "dart format --output=none --set-exit-if-changed lib test\nflutter analyze\nflutter test\n\n# Setelah profile + smoke test:\nflutter build apk --release \\\n  --dart-define=API_BASE_URL=https://api-staging.example\nflutter build appbundle --release \\\n  --dart-define=API_BASE_URL=https://api-staging.example", Inches(0.60), Inches(1.28), Inches(7.18), Inches(5.40), label="QUALITY GATE", size=11.5)
    add_card(s, Inches(8.08), Inches(1.28), Inches(4.63), Inches(2.42), "Gate gagal bila", ["format berubah", "analyzer issue", "test gagal", "build gagal"], icon="×", accent=RED, body_size=13)
    add_card(s, Inches(8.08), Inches(4.00), Inches(4.63), Inches(2.68), "Evidence terpisah", ["DevTools trace", "signer fingerprint", "device smoke result"], icon="E", accent=CYAN, body_size=13)
    add_notes(s, "11.38–11.50", 12, "Menyusun gate otomatis dan evidence manual.", "Jalankan format/analyze/test sebelum profiling.", "Evidence apa yang tidak dihasilkan command ini?", "Modul Hari 3 quality checks.")
    n += 1

    s = base_slide(prs, "PRAKTIK", "Lab 2 — regression safety net", n, total, 3)
    add_card(s, Inches(0.60), Inches(1.25), Inches(7.34), Inches(5.44), "Tugas", ["Tambahkan parser boundary test", "Tambahkan state success + failure test", "Tambahkan widget test invalid form/retry", "Jalankan dengan sengaja satu regression", "Pulihkan dan jalankan quality gate", "Catat test yang masih membutuhkan device"], icon="LAB", accent=CYAN, body_size=15)
    add_card(s, Inches(8.26), Inches(1.25), Inches(4.46), Inches(2.47), "Review", ["Deterministic", "Behavior-focused", "No real secret/network"], icon="R", accent=GOLD, body_size=13)
    add_card(s, Inches(8.26), Inches(4.02), Inches(4.46), Inches(2.67), "Done", ["Test gagal saat bug", "Test lulus setelah fix", "Output bersih"], icon="✓", accent=GREEN, body_size=13)
    add_notes(s, "11.50–12.00", 10, "Menjalankan regression exercise.", "Peserta menunjukkan test merah lalu hijau, bukan hanya final output.", "Apakah test benar-benar menangkap bug yang dimaksud?", "Modul Hari 3 latihan testing.")
    n += 1

    s = add_section_slide(prs, 3, n, total, "03", "Performance evidence", "Optimasi dimulai dari skenario yang dapat diulang—bukan dari tebakan atau slogan const.", ["Mendefinisikan scenario", "Membaca DevTools", "Membuktikan perubahan"])
    add_notes(s, "13.00–13.02", 2, "Membuka sesi performance.", "Gunakan physical device dan profile mode.", "Apa baseline yang perlu dicatat?", "Flutter DevTools Performance.")
    n += 1

    s = base_slide(prs, "PERFORMANCE", "Measure → diagnose → change → re-measure", n, total, 3)
    add_flow(s, ["Scenario", "Baseline", "Hypothesis", "One change", "Compare"], Inches(0.60), Inches(1.48), Inches(12.12), descriptions=["device + mode", "trace + symptom", "likely cause", "small + reviewable", "same conditions"])
    add_card(s, Inches(0.60), Inches(3.68), Inches(5.85), Inches(2.48), "Skenario training", ["Scroll list panjang", "Search saat list tampil", "Buka foto resolusi besar"], icon="S", accent=CYAN, body_size=13)
    add_card(s, Inches(6.82), Inches(3.68), Inches(5.90), Inches(2.48), "Evidence", ["Device + mode", "Trace/screenshot", "Before/after", "Batas kesimpulan"], icon="E", accent=GOLD, body_size=13)
    add_text(s, "Jika kondisi berubah, perbandingan tidak valid.", Inches(3.05), Inches(6.44), Inches(7.25), Inches(0.28), size=15, color=RED, bold=True, align=PP_ALIGN.CENTER)
    add_notes(s, "13.02–13.15", 13, "Menetapkan eksperimen performance.", "Pilih satu scenario yang realistis dan singkat.", "Apa yang membuat before/after tidak dapat dibandingkan?", "Modul Hari 3: profiling.")
    n += 1

    s = base_slide(prs, "PERFORMANCE", "Diagnosis berdasarkan symptom", n, total, 3)
    add_table(s, ["Symptom", "Periksa", "Perubahan kandidat"], [
        ["Frame lambat saat scroll", "build/layout/paint", "lazy list, split widget"],
        ["Typing search tersendat", "filter tiap build", "memoize/debounce"],
        ["Memory naik setelah foto", "decode + retained image", "resize, release reference"],
        ["Refresh terasa lambat", "network vs render", "timing + loading UX"],
        ["Seluruh layar rebuild", "listener scope", "narrow observer"],
        ["Jank pertama buka", "shader/image decode", "warmup/size evidence"],
    ], Inches(0.58), Inches(1.24), Inches(12.16), Inches(5.28), widths=[Inches(3.35), Inches(3.88), Inches(4.93)], font_size=12)
    add_text(s, "Pisahkan latency jaringan dari work pada UI thread.", Inches(2.50), Inches(6.60), Inches(8.30), Inches(0.25), size=14, color=BLUE, bold=True, align=PP_ALIGN.CENTER)
    add_notes(s, "13.15–13.28", 13, "Menghubungkan symptom ke tool dan perbaikan.", "Buka DevTools view yang relevan, jangan semua sekaligus.", "Bagaimana membedakan server lambat dari render lambat?", "DevTools docs.")
    n += 1

    s = base_slide(prs, "PERFORMANCE", "Rebuild scope dan derived data", n, total, 3)
    add_code(s, "class InspectionListView extends StatelessWidget {\n  const InspectionListView({required this.items, super.key});\n\n  @override\n  Widget build(BuildContext context) => ListView.builder(\n    itemCount: items.length,\n    itemBuilder: (_, index) {\n      final item = items[index];\n      return InspectionTile(\n        key: ValueKey(item.id),\n        item: item,\n      );\n    },\n  );\n}\n\n// Hitung visibleItems saat input/state berubah, bukan di tiap build besar.", Inches(0.60), Inches(1.25), Inches(7.12), Inches(5.55), label="UI", size=10.8)
    add_card(s, Inches(8.03), Inches(1.25), Inches(4.68), Inches(2.47), "Checklist", ["ListView.builder", "stable key by ID", "listener scope", "const where useful"], icon="✓", accent=GREEN, body_size=13)
    add_card(s, Inches(8.03), Inches(4.00), Inches(4.68), Inches(2.80), "Anti-myth", ["const bukan universal fix", "pecah widget harus ada alasan", "ukur impact pada scenario"], icon="!", accent=GOLD, body_size=13)
    add_notes(s, "13.28–13.43", 15, "Mengurangi work yang tidak perlu.", "Gunakan Inspector/rebuild stats untuk menunjuk scope.", "Apakah banyak widget kecil selalu lebih cepat?", "Modul Hari 3 performance checklist.")
    n += 1

    s = base_slide(prs, "PERFORMANCE", "Image memory dan resource ownership", n, total, 3)
    add_card(s, Inches(0.62), Inches(1.28), Inches(3.78), Inches(4.98), "Decode", ["maxWidth/imageQuality", "thumbnail untuk list", "hindari full-res preview", "ukur memory peak"], icon="I", accent=CYAN, body_size=14)
    add_card(s, Inches(4.78), Inches(1.28), Inches(3.78), Inches(4.98), "Retain", ["state punya owner", "hapus reference lama", "no cache tanpa policy", "cleanup temporary file"], icon="M", accent=BLUE, body_size=14)
    add_card(s, Inches(8.94), Inches(1.28), Inches(3.78), Inches(4.98), "Dispose", ["controller/listener", "http client", "stream/timer", "plugin operation guard"], icon="D", accent=GOLD, body_size=14)
    add_text(s, "Memory leak dan memory spike adalah masalah berbeda—buktikan dengan timeline.", Inches(1.05), Inches(6.54), Inches(11.2), Inches(0.28), size=14, color=BLUE, bold=True, align=PP_ALIGN.CENTER)
    add_notes(s, "13.43–13.56", 13, "Menjaga image dan resource lifecycle.", "Pilih foto besar lalu amati memory. Jangan membuat klaim leak dari satu spike.", "Apa perbedaan resource leak dan temporary allocation?", "Modul Hari 3: gambar/memory.")
    n += 1

    s = base_slide(prs, "PRAKTIK", "Lab 3 — satu perbaikan, satu bukti", n, total, 3)
    add_card(s, Inches(0.60), Inches(1.25), Inches(7.34), Inches(5.44), "Template eksperimen", ["Device/mode/commit", "Skenario dan dataset", "Symptom + baseline trace", "Hipotesis", "Satu perubahan", "Re-run kondisi sama", "Kesimpulan + limitasi"], icon="LAB", accent=CYAN, body_size=14)
    add_card(s, Inches(8.26), Inches(1.25), Inches(4.46), Inches(2.47), "Diterima", ["Reproducible", "Evidence tersimpan", "No inflated % claim"], icon="✓", accent=GREEN, body_size=13)
    add_card(s, Inches(8.26), Inches(4.02), Inches(4.46), Inches(2.67), "Tidak diterima", ["'Terasa lebih cepat'", "Mode/device berubah", "Banyak change sekaligus"], icon="×", accent=RED, body_size=13)
    add_notes(s, "13.56–14.10", 14, "Melakukan micro-experiment performance.", "Trainer membantu memilih satu perubahan kecil.", "Apakah hasil dapat diulang oleh reviewer?", "Modul Hari 3: pengukuran.")
    n += 1

    s = base_slide(prs, "QUALITY", "Polishing end-to-end sebelum release", n, total, 3)
    add_table(s, ["Flow", "Happy path", "Failure path", "UX evidence"], [
        ["Session", "login/restart", "wrong/expired", "actionable"],
        ["List", "fresh data", "empty/offline/500", "state distinct"],
        ["Create", "201 once", "422/timeout", "guard + recovery"],
        ["Photo", "select/replace", "cancel/denied", "record-bound"],
        ["Logout", "clear", "during async", "safe transition"],
        ["Responsive", "normal content", "keyboard/long text", "no overflow"],
    ], Inches(0.58), Inches(1.24), Inches(12.16), Inches(5.26), widths=[Inches(2.05), Inches(3.22), Inches(3.35), Inches(3.54)], font_size=12)
    add_text(s, "Tambahkan fitur hanya setelah jalur inti stabil.", Inches(3.15), Inches(6.60), Inches(7.0), Inches(0.25), size=14, color=BLUE, bold=True, align=PP_ALIGN.CENTER)
    add_notes(s, "14.10–14.25", 15, "Menutup gap end-to-end.", "Gunakan tabel sebagai regression checklist sebelum build.", "Flow mana masih berbeda antara debug dan release?", "Modul Hari 3: polishing.")
    n += 1

    s = base_slide(prs, "PLATFORM", "iOS overview — 20 menit, scope terkontrol", n, total, 3)
    add_flow(s, ["Bundle ID", "Team", "Certificate", "Provisioning", "Archive / TestFlight"], Inches(0.62), Inches(1.45), Inches(12.08), descriptions=["identity", "account", "signing trust", "device/app rights", "distribution"])
    add_card(s, Inches(0.62), Inches(3.62), Inches(5.84), Inches(2.58), "Dibahas", ["Mac + Xcode requirement", "Simulator vs physical device", "Permission string plugin"], icon="iOS", accent=CYAN, body_size=13)
    add_card(s, Inches(6.82), Inches(3.62), Inches(5.88), Inches(2.58), "Ditunda", ["Archive production", "App Store Connect upload", "Review App Store"], icon="→", accent=GOLD, body_size=13)
    add_notes(s, "14.10–14.30", 20, "Memberi gambaran iOS tanpa menggeser fokus Android.", "Gunakan overview, tidak perlu instalasi/console walkthrough.", "Fitur apa yang masih butuh physical iPhone?", "Modul Hari 3: iOS overview.")
    n += 1

    s = add_section_slide(prs, 3, n, total, "04", "Release engineering", "Artefak release harus reproducible, signed, verified, smoke-tested, dan dapat di-roll back.", ["Memisahkan environment", "Memverifikasi signer", "Menyusun handover"])
    add_notes(s, "14.45–14.47", 2, "Membuka sesi Android release.", "Gunakan key/app ID latihan, bukan production.", "Apa yang perlu dibuktikan selain build sukses?", "Android app signing docs.")
    n += 1

    s = base_slide(prs, "RELEASE", "Build identity: environment, version, signer", n, total, 3)
    add_card(s, Inches(0.62), Inches(1.28), Inches(3.78), Inches(4.98), "Environment", ["API staging HTTPS", "No debug cleartext", "No localhost", "Feature flags known"], icon="E", accent=CYAN, body_size=14)
    add_card(s, Inches(4.78), Inches(1.28), Inches(3.78), Inches(4.98), "Version", ["versionName semantic", "versionCode increases", "commit/tag trace", "release notes match"], icon="V", accent=BLUE, body_size=14)
    add_card(s, Inches(8.94), Inches(1.28), Inches(3.78), Inches(4.98), "Signer", ["training upload key", "fingerprint known", "key not in Git", "verify artifact"], icon="S", accent=GOLD, body_size=14)
    add_text(s, "Nama file bukan bukti environment, version, atau signer.", Inches(2.18), Inches(6.53), Inches(8.98), Inches(0.28), size=14, color=RED, bold=True, align=PP_ALIGN.CENTER)
    add_notes(s, "14.47–15.00", 13, "Menentukan identitas release candidate.", "Catat nilai sebelum build. Pastikan key.properties dan *.jks ignored.", "Bagaimana menghubungkan APK dengan commit source?", "Modul Hari 3: Android config.")
    n += 1

    s = base_slide(prs, "RELEASE", "Signing chain dan custody", n, total, 3)
    add_flow(s, ["Source", "Build", "Upload key", "Play signing", "Installed APK"], Inches(0.62), Inches(1.42), Inches(12.08), descriptions=["trusted commit", "controlled env", "team custody", "store custody", "verified cert"])
    add_card(s, Inches(0.62), Inches(3.58), Inches(5.84), Inches(2.72), "Training key", ["Khusus app latihan", "Password tidak dicetak", "Tidak mengganti key app operasional", "Fingerprint boleh dicatat"], icon="K", accent=GOLD, body_size=13)
    add_card(s, Inches(6.82), Inches(3.58), Inches(5.88), Inches(2.72), "Repository hygiene", ["key.properties ignored", "*.jks ignored", "No absolute secret path in docs", "Check staged files"], icon="G", accent=CYAN, body_size=13)
    add_notes(s, "15.00–15.15", 15, "Menjelaskan upload key vs app signing key.", "Jalankan keytool dengan key latihan; jangan tampilkan password.", "Siapa pemegang key production dan bagaimana recovery-nya?", "Android app signing docs.")
    n += 1

    s = base_slide(prs, "RELEASE", "Pipeline release candidate", n, total, 3)
    add_flow(s, ["Quality gate", "Build APK/AAB", "Verify", "Install", "Smoke", "Tag + notes"], Inches(0.52), Inches(1.40), Inches(12.28), descriptions=["format/analyze/test", "staging env", "signer + hash", "physical device", "core flows", "handover"])
    add_card(s, Inches(0.62), Inches(3.65), Inches(3.78), Inches(2.54), "Fail fast", ["Stop on first gate failure", "Fix root cause", "Rebuild from clean state"], icon="1", accent=RED, body_size=13)
    add_card(s, Inches(4.78), Inches(3.65), Inches(3.78), Inches(2.54), "Trace", ["Commit/tag", "toolchain versions", "artifact checksum"], icon="2", accent=CYAN, body_size=13)
    add_card(s, Inches(8.94), Inches(3.65), Inches(3.78), Inches(2.54), "Approve", ["Named reviewer", "Evidence complete", "Known limits accepted"], icon="3", accent=GREEN, body_size=13)
    add_notes(s, "15.15–15.28", 13, "Menyusun pipeline manual yang repeatable.", "Jangan menganggap CI/CD wajib dalam kelas; flow ini dapat diotomasi nanti.", "Pada tahap mana artefak yang salah harus ditolak?", "Modul Hari 3 build/handover.")
    n += 1

    s = base_slide(prs, "RELEASE", "Build dan verifikasi artefak", n, total, 3)
    add_code(s, "flutter build apk --release \\\n+  --dart-define=API_BASE_URL=https://api-staging.example\n\nflutter build appbundle --release \\\n+  --dart-define=API_BASE_URL=https://api-staging.example\n\napksigner verify --verbose --print-certs \\\n+  build/app/outputs/flutter-apk/app-release.apk\n\njarsigner -verify -verbose -certs \\\n+  build/app/outputs/bundle/release/app.aab", Inches(0.60), Inches(1.22), Inches(7.38), Inches(5.60), label="RELEASE", highlight="VERIFY, DON'T ASSUME", size=10.5)
    add_card(s, Inches(8.28), Inches(1.22), Inches(4.43), Inches(2.46), "APK", ["Install ke device", "Smoke test langsung", "Verify signer"], icon="APK", accent=CYAN, body_size=13)
    add_card(s, Inches(8.28), Inches(3.96), Inches(4.43), Inches(2.86), "AAB", ["Untuk store distribution", "Tidak di-adb install langsung", "Verify archive signature", "Track processing separately"], icon="AAB", accent=GOLD, body_size=13)
    add_notes(s, "15.28–15.43", 15, "Membangun dan memverifikasi APK/AAB.", "Ganti placeholder URL. Bandingkan fingerprint dengan keytool.", "Mengapa release label tidak cukup membuktikan signer?", "Flutter Android deployment.")
    n += 1

    s = base_slide(prs, "RELEASE", "Smoke test release: risk-based", n, total, 3)
    add_table(s, ["Risk", "Scenario", "Expected", "Evidence"], [
        ["Config", "launch + API HTTPS", "no debug-only dependency", "device/log"],
        ["Auth", "login + 401", "session correct", "screen"],
        ["Data", "list/create/offline", "policy correct", "record + banner"],
        ["Native", "gallery/camera/denied", "no crash", "photo/device"],
        ["Lifecycle", "background/restart", "state safe", "steps"],
        ["Security", "inspect logs/repo", "no secrets", "review"],
        ["Identity", "version + cert", "matches plan", "fingerprint"],
    ], Inches(0.58), Inches(1.22), Inches(12.16), Inches(5.50), widths=[Inches(1.55), Inches(3.55), Inches(3.65), Inches(3.41)], font_size=12)
    add_notes(s, "15.43–15.55", 12, "Menjalankan smoke test berbasis risiko.", "Gunakan APK release pada physical Android. Catat pass/fail/blocker.", "Flow apa yang paling mungkin berbeda dari debug?", "PRD Hari 3 acceptance.")
    n += 1

    s = base_slide(prs, "RELEASE", "Release notes, rollback, dan known limits", n, total, 3)
    add_card(s, Inches(0.62), Inches(1.28), Inches(3.78), Inches(5.05), "Release notes", ["Version + commit", "Perubahan user-visible", "Environment/API", "Migration/permission", "Known limitations"], icon="N", accent=CYAN, body_size=14)
    add_card(s, Inches(4.78), Inches(1.28), Inches(3.78), Inches(5.05), "Rollback", ["Previous artifact/version", "Data compatibility", "Owner + trigger", "Store/internal path", "Communication"], icon="R", accent=RED, body_size=14)
    add_card(s, Inches(8.94), Inches(1.28), Inches(3.78), Inches(5.05), "Batas wajib", ["Cache read-only", "Foto lokal sementara", "Camera physical device", "Hosted API dependency", "No production audit"], icon="!", accent=GOLD, body_size=14)
    add_text(s, "Known limit yang jelas lebih profesional daripada janji yang tidak diuji.", Inches(1.2), Inches(6.55), Inches(10.9), Inches(0.27), size=14, color=BLUE, bold=True, align=PP_ALIGN.CENTER)
    add_notes(s, "15.55–16.00", 5, "Mendokumentasikan release secara jujur.", "Pastikan cache/foto limitation masuk notes.", "Apa trigger rollback yang dapat diamati?", "Modul Hari 3 handover.")
    n += 1

    s = base_slide(prs, "CHECKPOINT", "Definition of Done — day 3", n, total, 3)
    add_table(s, ["Area", "Wajib", "Bukti"], [
        ["Native", "foto benar + lifecycle", "device matrix"],
        ["Tests", "unit/state/widget", "green output"],
        ["API client", "schema/status mapping", "test evidence"],
        ["Performance", "1 experiment", "before/after"],
        ["Release", "signed APK/AAB", "cert + paths"],
        ["Smoke", "core flows release", "pass/fail record"],
        ["Handover", "notes + blocker + tag", "day-3 package"],
    ], Inches(0.58), Inches(1.22), Inches(12.16), Inches(5.48), widths=[Inches(2.05), Inches(5.85), Inches(4.26)], font_size=12)
    add_notes(s, "16.00–16.10", 10, "Menilai acceptance akhir.", "Gunakan status Lulus/Perlu perbaikan/Terhalang prasyarat.", "Bukti mana masih bergantung akun/perangkat eksternal?", "PRD Hari 3.")
    n += 1

    s = base_slide(prs, "CHECKPOINT", "Demo akhir: satu cerita, bukan daftar fitur", n, total, 3)
    add_flow(s, ["Login", "List", "Create", "Offline", "Photo", "Release proof"], Inches(0.52), Inches(1.45), Inches(12.28), descriptions=["wrong + right", "fresh + retry", "invalid + valid", "cache banner", "select + cancel", "version + signer"])
    add_card(s, Inches(0.62), Inches(3.72), Inches(5.84), Inches(2.52), "Presenter", ["Sebut expected result sebelum aksi", "Tunjukkan evidence", "Jelaskan known limit"], icon="P", accent=CYAN, body_size=13)
    add_card(s, Inches(6.82), Inches(3.72), Inches(5.88), Inches(2.52), "Reviewer", ["Catat mismatch", "Minta repro steps", "Pisahkan blocker eksternal"], icon="R", accent=GOLD, body_size=13)
    add_notes(s, "16.10–16.20", 10, "Menjalankan demo end-to-end.", "Batasi demo pada jalur inti. Jangan improvisasi fitur belum diuji.", "Apakah demo membuktikan release artifact atau hanya debug app?", "Review akhir silabus.")
    n += 1

    s = base_slide(prs, "CHECKPOINT", "Handover package", n, total, 3)
    add_card(s, Inches(0.62), Inches(1.24), Inches(3.78), Inches(5.12), "Source", ["day-3 tag", "pubspec.lock", "README run/test/build", "No secret/build cache"], icon="S", accent=CYAN, body_size=14)
    add_card(s, Inches(4.78), Inches(1.24), Inches(3.78), Inches(5.12), "Evidence", ["test output", "DevTools trace", "APK/AAB path", "signer fingerprint", "smoke result"], icon="E", accent=BLUE, body_size=14)
    add_card(s, Inches(8.94), Inches(1.24), Inches(3.78), Inches(5.12), "Operational", ["API URL/version", "release notes", "known limits", "blocker + PIC", "next action/date"], icon="O", accent=GOLD, body_size=14)
    add_text(s, "Handover selesai ketika orang lain dapat menjalankan, menilai, dan melanjutkan.", Inches(0.9), Inches(6.60), Inches(11.5), Inches(0.25), size=13, color=BLUE, bold=True, align=PP_ALIGN.CENTER)
    add_notes(s, "16.20–16.27", 7, "Menyusun paket handover.", "Minta satu pasangan mencoba README pasangan lain.", "Apakah orang lain dapat reproduce hasil tanpa bantuan author?", "Modul Hari 3 handover.")
    n += 1

    s = base_slide(prs, "CLOSING", "Checkpoint Git — release candidate", n, total, 3, bg=NAVY)
    add_text(s, "day-3", Inches(0.72), Inches(1.22), Inches(4.2), Inches(0.85), size=54, color=CYAN, bold=True, font=FONT_DISPLAY)
    add_text(s, "Quality is evidence, not confidence", Inches(0.75), Inches(2.14), Inches(6.2), Inches(0.42), size=22, color=WHITE, bold=True)
    add_code(s, "dart format --output=none --set-exit-if-changed lib test\nflutter analyze\nflutter test\n\ngit add .\ngit commit -m \"Complete day-3 release checkpoint\"\ngit tag day-3", Inches(0.75), Inches(2.86), Inches(6.10), Inches(3.22), label="FINAL GATE", size=11.4)
    add_card(s, Inches(7.22), Inches(1.22), Inches(5.38), Inches(4.86), "Sebelum push", ["No token/password/key", "No build/ or .dart_tool", "PPTX dapat dibuka", "README menunjuk hosted API", "Known blocker tercatat"], icon="✓", accent=CYAN, fill=NAVY_2, body_size=14)
    add_text(s, f"{n:02d} / {total:02d}", Inches(11.62), Inches(6.88), Inches(0.95), Inches(0.22), size=10, color=CYAN_2, bold=True, align=PP_ALIGN.RIGHT)
    add_notes(s, "16.27–16.30", 3, "Menutup training dengan checkpoint aman.", "Periksa staged files sebelum push.", "Apakah repository dapat diklon dan dijalankan ulang?", "README paket training.")
    n += 1

    s = base_slide(prs, "REFERENCE", "Referensi dan roadmap lanjutan", n, total, 3)
    add_card(s, Inches(0.62), Inches(1.22), Inches(5.86), Inches(5.52), "Rujukan inti", ["docs.flutter.dev/testing", "docs.flutter.dev/tools/devtools", "pub.dev/packages/image_picker", "docs.flutter.dev/deployment/android", "developer.android.com app signing", "Modul + PRD Hari 3"], icon="R", accent=CYAN, body_size=13)
    add_card(s, Inches(6.82), Inches(1.22), Inches(5.90), Inches(5.52), "Roadmap setelah kelas", ["Upload attachment", "Offline write queue", "Integration test automation", "Contract test CI", "Flavor + secrets management", "Play Internal Testing"], icon="+", accent=GOLD, body_size=13)
    add_notes(s, "Cadangan", 1, "Memberi arah kelanjutan realistis.", "Pisahkan roadmap dari target training yang sudah dinilai.", "Langkah berikut mana paling mengurangi risiko proyek?", "Dokumentasi resmi dan modul Hari 3.")

    assert len(prs.slides) == total, (len(prs.slides), total)
    out = ROOT / "Hari_3_Flutter_Professional.pptx"
    prs.save(out)
    shutil.copy2(out, OUT_DIR / "Hari_3_Testing_Performance_Release_Android.pptx")
    return out


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="dpl-decks-") as tmp_name:
        background = prepare_cover_background(Path(tmp_name))
        day2 = build_day2(background)
        day3 = build_day3(background)
    print(f"Built {day2.relative_to(ROOT)}")
    print(f"Built {day3.relative_to(ROOT)}")
    print("Updated PPT_Training delivery copies")


if __name__ == "__main__":
    main()
