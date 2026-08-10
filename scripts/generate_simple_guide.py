"""Generate a plain-language PDF guide for Anti-cheat Detective."""

# ruff: noqa: E501

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Flowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "anti-cheat-detective-simple-guide.pdf"

NAVY = colors.HexColor("#173E56")
BLUE = colors.HexColor("#285B78")
TEAL = colors.HexColor("#2B7772")
AMBER = colors.HexColor("#D99A2B")
AMBER_PALE = colors.HexColor("#FFF2D7")
INK = colors.HexColor("#17212B")
MUTED = colors.HexColor("#64727E")
LINE = colors.HexColor("#D9E0E4")
PAPER = colors.HexColor("#F7F9FA")
SOFT_BLUE = colors.HexColor("#EEF4F6")
WHITE = colors.white


def register_fonts() -> None:
    base = Path("/System/Library/Fonts/Supplemental")
    pdfmetrics.registerFont(TTFont("GuideBody", str(base / "Arial.ttf")))
    pdfmetrics.registerFont(TTFont("GuideBodyBold", str(base / "Arial Bold.ttf")))
    pdfmetrics.registerFont(TTFont("GuideDisplay", str(base / "Georgia.ttf")))
    pdfmetrics.registerFont(TTFont("GuideDisplayBold", str(base / "Georgia Bold.ttf")))
    pdfmetrics.registerFont(TTFont("GuideMono", str(base / "Courier New.ttf")))
    pdfmetrics.registerFont(TTFont("GuideMonoBold", str(base / "Courier New Bold.ttf")))


register_fonts()
TITLE = ParagraphStyle(
    "Title",
    fontName="GuideDisplayBold",
    fontSize=31,
    leading=34,
    textColor=INK,
    spaceAfter=8,
)
SUBTITLE = ParagraphStyle(
    "Subtitle",
    fontName="GuideBody",
    fontSize=12.5,
    leading=18,
    textColor=MUTED,
    spaceAfter=14,
)
SECTION = ParagraphStyle(
    "Section",
    fontName="GuideDisplayBold",
    fontSize=23,
    leading=27,
    textColor=INK,
    spaceAfter=10,
)
H2 = ParagraphStyle(
    "H2",
    fontName="GuideBodyBold",
    fontSize=12.5,
    leading=16,
    textColor=NAVY,
    spaceBefore=9,
    spaceAfter=5,
)
BODY = ParagraphStyle(
    "Body",
    fontName="GuideBody",
    fontSize=10.2,
    leading=14.6,
    textColor=INK,
    spaceAfter=7,
)
SMALL = ParagraphStyle(
    "Small",
    fontName="GuideBody",
    fontSize=8.3,
    leading=11.5,
    textColor=MUTED,
)
LABEL = ParagraphStyle(
    "Label",
    fontName="GuideMonoBold",
    fontSize=7.4,
    leading=9,
    textColor=BLUE,
    tracking=1,
    spaceAfter=7,
)
MONO = ParagraphStyle(
    "Mono",
    fontName="GuideMono",
    fontSize=8.5,
    leading=12,
    textColor=INK,
)
BOX_TITLE = ParagraphStyle(
    "BoxTitle",
    fontName="GuideBodyBold",
    fontSize=10,
    leading=13,
    textColor=NAVY,
    spaceAfter=3,
)
BOX_BODY = ParagraphStyle(
    "BoxBody",
    fontName="GuideBody",
    fontSize=8.8,
    leading=12.2,
    textColor=INK,
)
CENTER = ParagraphStyle(
    "Center",
    parent=BODY,
    alignment=TA_CENTER,
)


def p(text: str, style: ParagraphStyle = BODY) -> Paragraph:
    return Paragraph(text, style)


def label(text: str) -> Paragraph:
    return p(text.upper(), LABEL)


def section(number: str, title: str, intro: str | None = None) -> list[Flowable]:
    items: list[Flowable] = [label(f"Section {number}"), p(title, SECTION)]
    if intro:
        items.append(p(intro, SUBTITLE))
    return items


def bullet(text: str) -> Paragraph:
    style = ParagraphStyle(
        "Bullet",
        parent=BODY,
        leftIndent=13,
        firstLineIndent=-9,
        bulletIndent=0,
        spaceAfter=5,
    )
    return Paragraph(f"- {text}", style)


def numbered(number: int, title: str, text: str) -> Table:
    number_cell = p(str(number), ParagraphStyle(
        f"Number{number}",
        fontName="GuideDisplayBold",
        fontSize=18,
        leading=20,
        textColor=WHITE,
        alignment=TA_CENTER,
    ))
    content = [p(title, BOX_TITLE), p(text, BOX_BODY)]
    table = Table([[number_cell, content]], colWidths=[12 * mm, 151 * mm], hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), BLUE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOX", (0, 0), (-1, -1), 0.6, LINE),
        ("LEFTPADDING", (0, 0), (0, 0), 4),
        ("RIGHTPADDING", (0, 0), (0, 0), 4),
        ("TOPPADDING", (0, 0), (0, 0), 8),
        ("BOTTOMPADDING", (0, 0), (0, 0), 8),
        ("LEFTPADDING", (1, 0), (1, 0), 10),
        ("RIGHTPADDING", (1, 0), (1, 0), 10),
        ("TOPPADDING", (1, 0), (1, 0), 7),
        ("BOTTOMPADDING", (1, 0), (1, 0), 7),
    ]))
    return table


def callout(title: str, text: str, tone: str = "blue") -> Table:
    bg = SOFT_BLUE if tone == "blue" else AMBER_PALE
    edge = BLUE if tone == "blue" else AMBER
    box = Table([[p(title, BOX_TITLE), p(text, BOX_BODY)]], colWidths=[38 * mm, 125 * mm])
    box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), 3, edge),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    return box


def simple_table(rows: list[list[str]], widths: list[float], header: bool = True) -> Table:
    converted = []
    for row_index, row in enumerate(rows):
        row_style = BOX_TITLE if header and row_index == 0 else BOX_BODY
        converted.append([p(cell, row_style) for cell in row])
    table = Table(converted, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("GRID", (0, 0), (-1, -1), 0.5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]
    if header:
        commands.extend([
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ])
    for row_index in range(1 if header else 0, len(rows)):
        if row_index % 2 == 0:
            commands.append(("BACKGROUND", (0, row_index), (-1, row_index), PAPER))
    table.setStyle(TableStyle(commands))
    return table


class AnalysisFlow(Flowable):
    """A six-step vertical flow diagram."""

    def __init__(self, width: float) -> None:
        super().__init__()
        self.width = width
        self.height = 300

    def draw(self) -> None:
        canvas = self.canv
        steps = [
            ("1", "PGN arrives", "A game is uploaded or pasted."),
            ("2", "PGN is checked", "Empty, broken, or multiple games are rejected."),
            ("3", "Stockfish searches", "Each position is searched at the chosen depth."),
            ("4", "Moves are compared", "Best move score is compared with played move score."),
            ("5", "Metrics are built", "ACPL and first-choice match rate are calculated."),
            ("6", "Results are shown", "The page polls the job and displays both players."),
        ]
        box_h = 38
        gap = 11
        left = 9
        box_w = self.width - 18
        top = self.height - box_h
        for index, (number, title, detail) in enumerate(steps):
            y = top - index * (box_h + gap)
            canvas.setFillColor(WHITE)
            canvas.setStrokeColor(LINE)
            canvas.roundRect(left, y, box_w, box_h, 3, fill=1, stroke=1)
            canvas.setFillColor(BLUE if index < 5 else TEAL)
            canvas.circle(left + 18, y + box_h / 2, 10, fill=1, stroke=0)
            canvas.setFillColor(WHITE)
            canvas.setFont("GuideBodyBold", 9)
            canvas.drawCentredString(left + 18, y + 15, number)
            canvas.setFillColor(NAVY)
            canvas.setFont("GuideBodyBold", 9.5)
            canvas.drawString(left + 38, y + 23, title)
            canvas.setFillColor(MUTED)
            canvas.setFont("GuideBody", 8.2)
            canvas.drawString(left + 38, y + 10, detail)
            if index < len(steps) - 1:
                canvas.setStrokeColor(AMBER)
                canvas.setLineWidth(1.2)
                x = left + 18
                canvas.line(x, y - 1, x, y - gap + 2)
                canvas.line(x - 2.5, y - gap + 5, x, y - gap + 2)
                canvas.line(x + 2.5, y - gap + 5, x, y - gap + 2)


class ArchitectureFlow(Flowable):
    """A left-to-right software architecture diagram."""

    def __init__(self, width: float) -> None:
        super().__init__()
        self.width = width
        self.height = 108

    def draw(self) -> None:
        canvas = self.canv
        labels = ["Web page", "FastAPI", "PGN parser", "Stockfish", "Features", "Result"]
        gap = 7
        box_w = (self.width - gap * 5) / 6
        box_h = 47
        y = 36
        for index, text in enumerate(labels):
            x = index * (box_w + gap)
            canvas.setFillColor(SOFT_BLUE if index not in (3, 5) else AMBER_PALE)
            canvas.setStrokeColor(BLUE if index not in (3, 5) else AMBER)
            canvas.roundRect(x, y, box_w, box_h, 3, fill=1, stroke=1)
            canvas.setFillColor(NAVY)
            canvas.setFont("GuideBodyBold", 7.8)
            words = text.split(" ")
            if len(words) == 1:
                canvas.drawCentredString(x + box_w / 2, y + 19, text)
            else:
                canvas.drawCentredString(x + box_w / 2, y + 25, words[0])
                canvas.drawCentredString(x + box_w / 2, y + 14, " ".join(words[1:]))
            if index < len(labels) - 1:
                x1 = x + box_w + 1
                x2 = x + box_w + gap - 1
                mid = y + box_h / 2
                canvas.setStrokeColor(MUTED)
                canvas.line(x1, mid, x2, mid)
                canvas.line(x2 - 3, mid + 2, x2, mid)
                canvas.line(x2 - 3, mid - 2, x2, mid)
        canvas.setFillColor(MUTED)
        canvas.setFont("GuideBody", 7.5)
        canvas.drawString(0, 14, "Input and output stay on the local machine when the app runs locally.")


def page_chrome(canvas, doc) -> None:  # noqa: ANN001
    canvas.saveState()
    width, height = A4
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(18 * mm, height - 14 * mm, width - 18 * mm, height - 14 * mm)
    canvas.setFont("GuideMonoBold", 6.8)
    canvas.setFillColor(BLUE)
    canvas.drawString(18 * mm, height - 10.5 * mm, "ANTI-CHEAT DETECTIVE")
    canvas.setFont("GuideBody", 7.2)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(width - 18 * mm, 10 * mm, f"Simple project guide  |  {doc.page}")
    canvas.restoreState()


def cover_page(canvas, doc) -> None:  # noqa: ANN001
    canvas.saveState()
    width, height = A4
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, width, height, fill=1, stroke=0)
    canvas.setStrokeColor(colors.Color(1, 1, 1, alpha=0.09))
    for x in range(0, int(width), 30):
        canvas.line(x, 0, x, height)
    for y in range(0, int(height), 30):
        canvas.line(0, y, width, y)
    canvas.setFillColor(AMBER)
    canvas.rect(24 * mm, height - 43 * mm, 18 * mm, 2.4 * mm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("GuideMonoBold", 8)
    canvas.drawString(24 * mm, height - 35 * mm, "PROJECT HANDBOOK  /  19 JULY 2026")
    canvas.setFont("GuideDisplayBold", 34)
    canvas.drawString(24 * mm, height - 76 * mm, "Anti-cheat")
    canvas.drawString(24 * mm, height - 91 * mm, "Detective")
    canvas.setFont("GuideBody", 14)
    canvas.setFillColor(colors.HexColor("#DCE8EE"))
    canvas.drawString(24 * mm, height - 108 * mm, "A simple explanation of what was built,")
    canvas.drawString(24 * mm, height - 116 * mm, "how it works, and what it cannot prove")

    board_x = width - 93 * mm
    board_y = 33 * mm
    square = 8 * mm
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 0:
                canvas.setFillColor(colors.Color(1, 1, 1, alpha=0.11))
            else:
                canvas.setFillColor(colors.Color(0.85, 0.60, 0.17, alpha=0.42))
            canvas.rect(board_x + col * square, board_y + row * square, square, square, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("GuideDisplayBold", 42)
    canvas.drawCentredString(board_x + 32 * mm, board_y + 21 * mm, "N")
    canvas.setFont("GuideBody", 8.5)
    canvas.setFillColor(colors.HexColor("#DCE8EE"))
    canvas.drawString(24 * mm, 28 * mm, "Working local prototype  |  Python  |  Stockfish  |  FastAPI  |  Docker")
    canvas.restoreState()


def build_story() -> list[Flowable]:
    story: list[Flowable] = []

    story.extend([
        Spacer(1, 180 * mm),
        PageBreak(),
    ])

    story.extend(section("01", "The whole project in one minute", "This page is the shortest possible explanation of the work."))
    story.append(callout(
        "What it is",
        "A local research app that reads one chess game, asks Stockfish to evaluate every move, and shows simple measurements for White and Black.",
    ))
    story.append(Spacer(1, 7 * mm))
    story.append(simple_table([
        ["Question", "Plain answer"],
        ["What goes in?", "A PGN file or pasted PGN text. PGN is the normal text format used to store a chess game."],
        ["What happens?", "The app compares each played move with Stockfish's preferred move."],
        ["What comes out?", "ACPL, median move loss, engine first-choice match rate, and the number of moves measured."],
        ["Does it say who cheated?", "No. The current version intentionally does not give a cheating verdict or probability."],
        ["Where does it run?", "Locally in Docker at http://localhost:8000."],
    ], [42 * mm, 121 * mm]))
    story.append(Spacer(1, 7 * mm))
    story.append(callout(
        "Most important rule",
        "A person can play moves similar to an engine for many innocent reasons. Strong statistics can support an investigation, but they are not proof by themselves.",
        tone="amber",
    ))
    story.append(PageBreak())

    story.extend(section("02", "Why the project exists", "The goal is careful detection research, not an automatic accusation machine."))
    story.append(p("Chess engines can find extremely strong moves. A player who secretly receives engine help may make choices that look unusually engine-like. The research question is whether we can measure that pattern in a transparent and honest way."))
    story.append(p("The project started with five non-negotiable rules:"))
    for text in [
        "Explain every number. The user should know where a measurement came from.",
        "Never let a language model invent or calculate raw statistics. It may receive only validated structured data in a later stage.",
        "Do not treat a controversial case as proof that the detector is correct.",
        "Use independently confirmed cases for future validation, and record the source of both the game and the outside evidence.",
        "Never advertise precision or recall as trustworthy when the sample is too small.",
    ]:
        story.append(bullet(text))
    story.append(Spacer(1, 5 * mm))
    story.append(callout(
        "Research inspiration",
        "The long-term method is inspired by Kenneth Regan's statistical chess research. The current code implements only a transparent baseline, not the full Regan method.",
    ))
    story.append(Spacer(1, 6 * mm))
    story.append(p("The original plan has six stages: background research, data pipeline, advanced features, structured report writing, validation, and a final demo. The working prototype has completed the initial repository, the basic analysis engine, and the local user interface."))
    story.append(PageBreak())

    story.extend(section("03", "What happens when you click Analyze", "The browser hides the technical steps, but the process remains easy to audit."))
    story.append(AnalysisFlow(163 * mm))
    story.append(Spacer(1, 5 * mm))
    story.append(callout(
        "Why two engine searches?",
        "For each position, the app first lets Stockfish choose freely. Then it searches again while forcing the move that was actually played. This makes the comparison explicit.",
        tone="amber",
    ))
    story.append(PageBreak())

    story.extend(section("04", "How one move is measured", "A small made-up example shows the basic calculation."))
    story.append(p("Imagine it is White's turn. Stockfish says its best move gives White a score of +0.60 pawns. The move actually played gives White only +0.25 pawns."))
    formula = Table([
        [p("Best move", BOX_TITLE), p("+0.60 pawns = +60 centipawns", MONO)],
        [p("Played move", BOX_TITLE), p("+0.25 pawns = +25 centipawns", MONO)],
        [p("Move loss", BOX_TITLE), p("60 - 25 = 35 centipawns", MONO)],
    ], colWidths=[45 * mm, 118 * mm])
    formula.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.7, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, LINE),
        ("BACKGROUND", (0, 2), (-1, 2), AMBER_PALE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(formula)
    story.append(Spacer(1, 7 * mm))
    story.append(p("All scores are converted to the point of view of the player who is moving. This matters because a positive score for White is a negative score for Black. Checkmate scores are converted to a large centipawn value so the calculations remain numeric."))
    story.append(callout(
        "Safety in the calculation",
        "The code never records a negative loss. If two searches produce tiny ordering differences, the loss is limited to zero instead of suggesting the played move was better than the engine's own best move.",
    ))
    story.append(PageBreak())

    story.extend(section("05", "The measurements in plain language", "These are descriptions of move quality, not labels for human behavior."))
    story.append(simple_table([
        ["Measurement", "Meaning", "How to read it"],
        ["ACPL", "Average centipawn loss across a player's moves.", "Lower usually means stronger or more accurate play."],
        ["Median loss", "The middle move loss after losses are sorted.", "Less affected by one very large mistake than the average."],
        ["Top-1 match rate", "Share of moves equal to Stockfish's first choice.", "Higher means more direct agreement with this engine at this depth."],
        ["Move count", "Number of half-moves measured for that player.", "A result based on 5 moves is much weaker than one based on many games."],
    ], [31 * mm, 68 * mm, 64 * mm]))
    story.append(Spacer(1, 7 * mm))
    story.append(p("The sample game used during testing had ten moves per player. White produced 2.9 ACPL and 90% first-choice matching; Black produced 3.7 ACPL and 60% matching. These numbers look very accurate because the sample is short and mostly opening theory. They do not suggest cheating."))
    story.append(Spacer(1, 5 * mm))
    story.append(callout(
        "Do not compare blindly",
        "ACPL depends on rating, time control, opening preparation, position difficulty, game phase, hardware, engine version, and search depth.",
        tone="amber",
    ))
    story.append(PageBreak())

    story.extend(section("06", "The theory for future detection", "Real statistical detection asks whether the full pattern is unexpectedly strong for the situation."))
    story.append(p("The planned approach starts with a normal-behavior model. It asks: for a player of this rating, in this kind of position and time control, how likely was each available move?"))
    for number, title, text in [
        (1, "Build an expected baseline", "Use many ordinary games grouped by rating and time control."),
        (2, "Measure position difficulty", "A forced move should count less than a surprising engine-only move."),
        (3, "Look across many decisions", "A long repeated pattern matters more than one brilliant move."),
        (4, "Standardize the surprise", "Compare observed performance with the expected range and calculate uncertainty."),
        (5, "Test false positives", "Check strong clean players and controversial cases to learn when the method overreacts."),
    ]:
        story.append(numbered(number, title, text))
        story.append(Spacer(1, 2.5 * mm))
    story.append(Spacer(1, 3 * mm))
    story.append(callout(
        "Current boundary",
        "None of this future model is presented as finished. The current app stops at basic engine measurements and does not output a cheating score.",
        tone="amber",
    ))
    story.append(PageBreak())

    story.extend(section("07", "How the software is organized", "Each part has one clear responsibility."))
    story.append(ArchitectureFlow(163 * mm))
    story.append(simple_table([
        ["Part", "Job"],
        ["web/index.html", "The page for file upload, pasted PGN, progress, errors, and results."],
        ["api/app.py", "Creates background jobs and exposes the health, create, and result endpoints."],
        ["engine/pgn.py", "Reads exactly one valid non-empty chess game."],
        ["engine/stockfish.py", "Starts Stockfish and compares every played move with the best move."],
        ["features/baseline.py", "Calculates ACPL, median loss, match rate, and move count."],
        ["agent/schemas.py", "Defines the validated numeric boundary for a future writing agent."],
        ["tests/", "Checks parsing, metrics, engine behavior, API behavior, and the web page."],
    ], [48 * mm, 115 * mm]))
    story.append(Spacer(1, 5 * mm))
    story.append(p("The API uses an in-memory job dictionary protected by a lock. This is enough for a local proof of concept. It is not yet designed for many users, multiple servers, or jobs that must survive a restart."))
    story.append(PageBreak())

    story.extend(section("08", "How to use the finished app", "The normal workflow no longer requires Swagger or command-line knowledge."))
    for number, title, text in [
        (1, "Start the app", "From the project folder, run: docker compose up -d"),
        (2, "Open the page", "Visit http://localhost:8000 in a browser."),
        (3, "Add a game", "Choose a .pgn file, paste PGN text, or press Load sample."),
        (4, "Analyze", "Press Analyze game. The page submits the job and checks progress automatically."),
        (5, "Read the evidence sheet", "Compare White and Black, but pay attention to move count and the limitations note."),
        (6, "Stop when finished", "Run: docker compose down"),
    ]:
        story.append(numbered(number, title, text))
        story.append(Spacer(1, 3 * mm))
    story.append(Spacer(1, 4 * mm))
    story.append(callout(
        "Privacy",
        "When used at localhost, the PGN is sent only from the browser to the local Docker app on the same computer. The current code does not upload it to an outside service.",
    ))
    story.append(PageBreak())

    story.extend(section("09", "What was done to make it trustworthy", "Small engineering choices prevent silent errors and make the prototype reproducible."))
    story.append(simple_table([
        ["Protection", "Why it matters"],
        ["One game per request", "The app cannot silently analyze only the first game in a large pasted block."],
        ["Invalid PGN rejection", "Broken or empty input fails before engine work begins."],
        ["Player point of view", "White and Black scores are interpreted correctly for the person moving."],
        ["Recorded engine depth", "A result shows the setting that influenced it."],
        ["Structured result schema", "Unexpected or invented fields are rejected."],
        ["No accusation endpoint", "The software cannot turn two baseline metrics into an unsupported verdict."],
        ["Docker image", "Python, the application, and Stockfish run in a repeatable environment."],
    ], [55 * mm, 108 * mm]))
    story.append(Spacer(1, 6 * mm))
    story.append(p("Verification completed on 19 July 2026:"))
    for text in [
        "15 automated tests passed.",
        "Total measured test coverage was 87%.",
        "The Stockfish wrapper reached 94% coverage using a fake engine for repeatable tests.",
        "The Ruff code-quality check passed.",
        "The Python wheel built successfully and included the web interface.",
        "Docker Compose rebuilt and started successfully.",
        "The complete browser flow was tested: load sample, analyze, poll, and show results.",
    ]:
        story.append(bullet(text))
    story.append(PageBreak())

    story.extend(section("10", "What the system cannot know", "This is the most important page for responsible use."))
    story.append(p("The app sees chess moves. It does not see the person's thoughts, preparation, physical environment, communications, or intent. Therefore it cannot directly know whether assistance occurred."))
    story.append(simple_table([
        ["Possible innocent reason", "How it can affect the numbers"],
        ["Opening preparation", "Known moves can match the engine for a long sequence."],
        ["Forced position", "Only one or two sensible moves may exist."],
        ["Strong player", "Elite players naturally choose engine-like moves more often."],
        ["Short game", "A tiny sample can look extreme by chance."],
        ["Simple position", "Accurate moves may be easy for many players."],
        ["Different engine settings", "Depth, version, and hardware can change the preferred move."],
    ], [55 * mm, 108 * mm]))
    story.append(Spacer(1, 6 * mm))
    story.append(callout(
        "What would support a real conclusion?",
        "A careful statistical pattern across enough games, a well-calibrated comparison group, transparent uncertainty, and evidence outside the move statistics such as devices, communications, observation, or admission.",
        tone="amber",
    ))
    story.append(PageBreak())

    story.extend(section("11", "What should be built next", "The prototype is usable, but it is not yet a validated detector."))
    story.append(simple_table([
        ["Priority", "Next work", "Reason"],
        ["1", "Create a licensed baseline-data manifest and download scripts.", "Every game must have a known source and reproducible path."],
        ["2", "Add a command-line analysis tool that writes JSON.", "Batch research needs repeatable machine-readable outputs."],
        ["3", "Add rating, time control, phase, complexity, and clock features.", "Raw ACPL and match rate ignore major context."],
        ["4", "Build clean controls and independently confirmed case sets.", "Evaluation needs both false-positive and true-positive evidence."],
        ["5", "Calibrate a simple statistical model before a complex model.", "A transparent baseline is easier to audit."],
        ["6", "Add validated report generation.", "A writing agent should explain verified numbers, never create them."],
    ], [18 * mm, 73 * mm, 72 * mm]))
    story.append(Spacer(1, 7 * mm))
    story.append(p("Only after those steps should the project report precision, recall, or a suspiciousness score. Even then, the output should be treated as investigative support rather than a verdict."))
    story.append(PageBreak())

    story.extend(section("12", "Glossary and references", "A final quick reference for the main terms used in the project."))
    story.append(simple_table([
        ["Term", "Simple meaning"],
        ["PGN", "Portable Game Notation, a text format that stores chess moves and game details."],
        ["Stockfish", "A very strong open-source chess engine."],
        ["Centipawn", "One hundredth of a pawn, used as a small unit for chess evaluation."],
        ["ACPL", "Average amount of evaluation lost per move."],
        ["Top-1 match", "The played move is the engine's first choice."],
        ["UCI", "A standard way for chess software to communicate with an engine."],
        ["API", "A set of addresses that software uses to send requests and receive results."],
        ["Background job", "Work that continues after the initial request returns."],
        ["False positive", "A clean player or game is incorrectly treated as suspicious."],
    ], [39 * mm, 124 * mm]))
    story.append(Spacer(1, 7 * mm))
    story.append(p("<b>Methodology references planned for the final academic report</b>", H2))
    for reference in [
        "Regan and Haworth - Intrinsic Chess Ratings (AAAI, 2011).",
        "Barnes and Hernandez-Castro - On the Limits of Engine Analysis for Cheating Detection (2015).",
        "Biswas and Regan - work on quantifying depth and complexity of chess thinking and knowledge.",
        "Lichess Irwin - architecture reference only; the project does not copy it directly.",
    ]:
        story.append(bullet(reference))
    story.append(Spacer(1, 8 * mm))
    story.append(callout(
        "Final takeaway",
        "The project now has a working and understandable measurement tool. The honest next step is better data and calibration, not a stronger-looking accusation screen.",
    ))

    return story


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=24 * mm,
        leftMargin=24 * mm,
        topMargin=22 * mm,
        bottomMargin=19 * mm,
        title="Anti-cheat Detective - Simple Project Guide",
        author="Codex",
        subject="Plain-language explanation of the Anti-cheat Detective project",
    )
    doc.build(build_story(), onFirstPage=cover_page, onLaterPages=page_chrome)
    print(OUTPUT)


if __name__ == "__main__":
    main()
