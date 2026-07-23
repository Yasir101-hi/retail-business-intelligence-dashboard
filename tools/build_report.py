"""Build the portfolio-ready Saudi retail BI PDF report."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "Saudi_Retail_BI_Dashboard_Report.pdf"
IMAGES = ROOT / "images"

NAVY = colors.HexColor("#111C3A")
BLUE = colors.HexColor("#2F5597")
ORANGE = colors.HexColor("#F4A300")
TEAL = colors.HexColor("#00A98F")
LIGHT_BLUE = colors.HexColor("#EAF0FA")
LIGHT_GRAY = colors.HexColor("#F5F7FA")
MID_GRAY = colors.HexColor("#67728A")
GRID = colors.HexColor("#D5DDEA")
WHITE = colors.white

pdfmetrics.registerFont(
    TTFont("DejaVuSans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
)
pdfmetrics.registerFont(
    TTFont(
        "DejaVuSans-Bold",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    )
)


def image_for_page(filename: str, width: float) -> Image:
    path = IMAGES / filename
    source = ImageReader(path)
    pixel_width, pixel_height = source.getSize()
    height = width * pixel_height / pixel_width
    return Image(str(path), width=width, height=height)


def bullet(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(f"- {text}", style)


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="ReportTitle",
        parent=styles["Title"],
        fontName="DejaVuSans-Bold",
        fontSize=28,
        leading=33,
        textColor=NAVY,
        alignment=TA_LEFT,
        spaceAfter=10,
    )
)
styles.add(
    ParagraphStyle(
        name="Subtitle",
        parent=styles["Normal"],
        fontName="DejaVuSans",
        fontSize=11,
        leading=17,
        textColor=MID_GRAY,
        spaceAfter=16,
    )
)
styles.add(
    ParagraphStyle(
        name="SectionTitle",
        parent=styles["Heading1"],
        fontName="DejaVuSans-Bold",
        fontSize=15,
        leading=19,
        textColor=WHITE,
        backColor=NAVY,
        borderPadding=(7, 8, 7, 8),
        spaceBefore=4,
        spaceAfter=10,
    )
)
styles.add(
    ParagraphStyle(
        name="Subheading",
        parent=styles["Heading2"],
        fontName="DejaVuSans-Bold",
        fontSize=11.5,
        leading=15,
        textColor=BLUE,
        spaceBefore=5,
        spaceAfter=5,
    )
)
styles.add(
    ParagraphStyle(
        name="Body",
        parent=styles["BodyText"],
        fontName="DejaVuSans",
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor("#27324A"),
        spaceAfter=5,
    )
)
styles.add(
    ParagraphStyle(
        name="ReportBullet",
        parent=styles["Body"],
        leftIndent=9,
        firstLineIndent=-7,
        spaceAfter=3,
    )
)
styles.add(
    ParagraphStyle(
        name="Caption",
        parent=styles["Body"],
        fontSize=7.5,
        leading=10,
        textColor=MID_GRAY,
        alignment=TA_CENTER,
        spaceBefore=4,
        spaceAfter=7,
    )
)
styles.add(
    ParagraphStyle(
        name="Small",
        parent=styles["Body"],
        fontSize=7.5,
        leading=10.5,
        textColor=MID_GRAY,
    )
)
styles.add(
    ParagraphStyle(
        name="TableText",
        parent=styles["Body"],
        fontName="DejaVuSans",
        fontSize=7.5,
        leading=10,
        spaceAfter=0,
    )
)
styles.add(
    ParagraphStyle(
        name="TableLabel",
        parent=styles["TableText"],
        fontName="DejaVuSans-Bold",
    )
)
styles.add(
    ParagraphStyle(
        name="KpiValue",
        parent=styles["Body"],
        fontName="DejaVuSans-Bold",
        fontSize=15,
        leading=18,
        textColor=NAVY,
        alignment=TA_CENTER,
        spaceAfter=2,
    )
)
styles.add(
    ParagraphStyle(
        name="KpiLabel",
        parent=styles["Small"],
        alignment=TA_CENTER,
    )
)


def header_footer(canvas, doc) -> None:
    width, height = A4
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, height - 17 * mm, width, 17 * mm, fill=1, stroke=0)
    canvas.setFillColor(TEAL)
    canvas.rect(0, height - 18 * mm, width, 1.2 * mm, fill=1, stroke=0)
    canvas.setFillColor(ORANGE)
    canvas.rect(0, height - 18 * mm, 70 * mm, 1.2 * mm, fill=1, stroke=0)
    canvas.setFont("DejaVuSans-Bold", 7)
    canvas.setFillColor(WHITE)
    canvas.drawString(16 * mm, height - 10.5 * mm, "SAUDI RETAIL BI DASHBOARD REPORT")
    canvas.setFont("DejaVuSans", 7)
    canvas.drawRightString(
        width - 16 * mm, height - 10.5 * mm, "Prepared by Yasir Awad"
    )

    canvas.setStrokeColor(GRID)
    canvas.line(16 * mm, 13 * mm, width - 16 * mm, 13 * mm)
    canvas.setFillColor(MID_GRAY)
    canvas.setFont("DejaVuSans", 7)
    canvas.drawString(16 * mm, 8.5 * mm, "Business Intelligence | Power BI")
    canvas.drawRightString(
        width - 16 * mm, 8.5 * mm, f"Page {canvas.getPageNumber()}"
    )
    canvas.restoreState()


doc = SimpleDocTemplate(
    str(OUTPUT),
    pagesize=A4,
    rightMargin=16 * mm,
    leftMargin=16 * mm,
    topMargin=25 * mm,
    bottomMargin=19 * mm,
    title="Saudi Retail Business Intelligence Dashboard Report",
    author="Yasir Awad",
)

story = []

# Page 1 - Cover
story.extend(
    [
        Spacer(1, 19 * mm),
        Paragraph("Saudi Retail Business Intelligence Dashboard Report", styles["ReportTitle"]),
        Paragraph(
            "Power BI reporting for retail sales performance, customer behavior, "
            "inventory risk, profitability, and branch operations in Saudi Arabia.",
            styles["Subtitle"],
        ),
    ]
)

project_details_raw = [
    ("Prepared by", "Yasir Awad - Data Analyst"),
    ("Project type", "Freelance retail BI / Power BI dashboard"),
    ("Domain", "Retail | Sales | Customer analytics | Inventory operations"),
    ("Tools", "Power BI | DAX | Power Query | Data modeling"),
    ("Purpose", "Document dashboard objectives, verified findings, and recommendations"),
]
project_details = [
    [
        Paragraph(label, styles["TableLabel"]),
        Paragraph(value, styles["TableText"]),
    ]
    for label, value in project_details_raw
]
details_table = Table(project_details, colWidths=[38 * mm, 132 * mm])
details_table.setStyle(
    TableStyle(
        [
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#27324A")),
            ("BACKGROUND", (0, 0), (0, -1), LIGHT_BLUE),
            ("GRID", (0, 0), (-1, -1), 0.5, GRID),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]
    )
)
story.extend([details_table, Spacer(1, 8 * mm)])

kpis = [
    [Paragraph("965.79K", styles["KpiValue"]), Paragraph("12K", styles["KpiValue"]),
     Paragraph("375.35K", styles["KpiValue"]), Paragraph("38.86%", styles["KpiValue"])],
    [Paragraph("Total revenue", styles["KpiLabel"]), Paragraph("Total orders", styles["KpiLabel"]),
     Paragraph("Total profit", styles["KpiLabel"]), Paragraph("Profit margin", styles["KpiLabel"])],
]
kpi_table = Table(kpis, colWidths=[42.5 * mm] * 4, rowHeights=[12 * mm, 9 * mm])
kpi_table.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GRAY),
            ("BOX", (0, 0), (-1, -1), 0.7, GRID),
            ("INNERGRID", (0, 0), (-1, -1), 0.7, GRID),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]
    )
)
story.extend(
    [
        kpi_table,
        Spacer(1, 7 * mm),
        Paragraph(
            "<b>Confidentiality note:</b> Client and store identities are anonymized. "
            "Product names are generic where necessary.",
            styles["Small"],
        ),
        PageBreak(),
    ]
)

# Page 2 - Executive summary
story.extend(
    [
        Paragraph("1. Executive Summary", styles["SectionTitle"]),
        Paragraph(
            "This report documents a four-page Power BI solution designed to give "
            "retail managers one reliable view of sales, profitability, customer value, "
            "inventory exposure, and branch performance.",
            styles["Body"],
        ),
        Paragraph("Business problem", styles["Subheading"]),
        Paragraph(
            "Operational and commercial metrics were distributed across sales, "
            "customer, product, branch, and inventory records. Management needed a "
            "clear way to identify revenue drivers, compare branch performance, monitor "
            "customer retention, and prioritize stock replenishment.",
            styles["Body"],
        ),
        Paragraph("Project objectives", styles["Subheading"]),
        bullet("Provide an executive view of revenue, orders, profit, and margin.", styles["ReportBullet"]),
        bullet("Explain product, category, and branch contribution.", styles["ReportBullet"]),
        bullet("Measure new and returning customer behavior.", styles["ReportBullet"]),
        bullet("Identify products and branches exposed to stockout risk.", styles["ReportBullet"]),
        bullet("Turn findings into practical management recommendations.", styles["ReportBullet"]),
        Spacer(1, 5 * mm),
        Paragraph("Dashboard structure", styles["Subheading"]),
    ]
)

structure = [
    ["Page", "Decision supported"],
    ["Executive Overview", "High-level KPI monitoring and revenue mix"],
    ["Sales Performance", "Product, category, branch, margin, and growth analysis"],
    ["Customer Behavior", "Customer value, retention, and segment analysis"],
    ["Inventory & Operations", "Stock coverage, reorder signals, and branch exposure"],
]
structure_table = Table(structure, colWidths=[48 * mm, 122 * mm], repeatRows=1)
structure_table.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("FONTNAME", (0, 0), (-1, 0), "DejaVuSans-Bold"),
            ("FONTNAME", (0, 1), (-1, -1), "DejaVuSans"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 0.5, GRID),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]
    )
)
story.extend([structure_table, PageBreak()])

# Page 3 - Questions and method
story.extend(
    [
        Paragraph("2. Business Questions and Method", styles["SectionTitle"]),
        Paragraph("Questions addressed", styles["Subheading"]),
    ]
)
questions = [
    ["Area", "Question"],
    ["Sales", "Which products, categories, and branches generate the strongest results?"],
    ["Customers", "How much value comes from returning customers and priority segments?"],
    ["Inventory", "Which fast-moving products are at or below their reorder threshold?"],
    ["Management", "Where should replenishment and retention actions be prioritized?"],
]
questions_table = Table(questions, colWidths=[34 * mm, 136 * mm], repeatRows=1)
questions_table.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("FONTNAME", (0, 0), (-1, 0), "DejaVuSans-Bold"),
            ("FONTNAME", (0, 1), (0, -1), "DejaVuSans-Bold"),
            ("FONTNAME", (1, 1), (1, -1), "DejaVuSans"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 0.5, GRID),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]
    )
)
story.extend(
    [
        questions_table,
        Spacer(1, 6 * mm),
        Paragraph("Implementation approach", styles["Subheading"]),
        bullet("Structured sales, customer, product, branch, calendar, and inventory tables.", styles["ReportBullet"]),
        bullet("Used dedicated DAX measure tables for each reporting page.", styles["ReportBullet"]),
        bullet("Applied consistent filters and reusable dimensions across report visuals.", styles["ReportBullet"]),
        bullet("Validated dashboard statements against displayed totals before documentation.", styles["ReportBullet"]),
        bullet("Used a linear scale for branch comparisons to avoid visual distortion.", styles["ReportBullet"]),
        Paragraph("Validation decisions", styles["Subheading"]),
        Paragraph(
            "The unsupported claim that the top three products generated more than "
            "30% of revenue was removed. The verified top-five contribution is 249.89K, "
            "or approximately 25.9%. The comparison card is labeled Prior Period Revenue "
            "because its 870.01K value is a report-context baseline rather than a "
            "standalone monthly total.",
            styles["Body"],
        ),
        PageBreak(),
    ]
)


def dashboard_page(
    number: int,
    title: str,
    filename: str,
    caption: str,
    findings: list[str],
    interpretation: str,
) -> None:
    story.append(Paragraph(f"{number}. Dashboard Page - {title}", styles["SectionTitle"]))
    story.append(image_for_page(filename, doc.width))
    story.append(Paragraph(caption, styles["Caption"]))
    story.append(Paragraph("Key findings", styles["Subheading"]))
    for finding in findings:
        story.append(bullet(finding, styles["ReportBullet"]))
    story.append(Paragraph("Business interpretation", styles["Subheading"]))
    story.append(Paragraph(interpretation, styles["Body"]))
    story.append(PageBreak())


dashboard_page(
    3,
    "Executive Overview",
    "executive-overview.png",
    "Executive view of revenue, orders, profit, margin, monthly movement, "
    "category contribution, leading products, and branch performance.",
    [
        "Revenue reached 965.79K, with 375.35K profit and a 38.86% margin.",
        "Vape generated 418.55K, representing 43.34% of revenue.",
        "Tabuk led branch revenue at approximately 252.82K.",
        "November and December produced the strongest monthly results.",
    ],
    "The overview gives management one concise performance checkpoint while preserving "
    "drill-down paths into product, customer, and inventory decisions.",
)

dashboard_page(
    4,
    "Sales Performance Analysis",
    "sales-performance.png",
    "Product contribution, branch comparison, category margins, prior-period "
    "revenue, and growth analysis.",
    [
        "The top five products generated 249.89K, or approximately 25.9% of revenue.",
        "The current-context revenue is 11% above the 870.01K prior-period baseline.",
        "Vape delivered the strongest category margin at 43.5%.",
        "Branch revenue was relatively balanced, with Tabuk narrowly leading.",
    ],
    "Management can protect availability for high-contribution products while using "
    "category margins and branch demand together for commercial planning.",
)

dashboard_page(
    5,
    "Customer Behavior Analysis",
    "customer-behavior.png",
    "Customer count, revenue per customer, ordering frequency, retention contribution, "
    "and value segmentation.",
    [
        "The report tracks 500 customers and approximately 1.93K revenue per customer.",
        "Returning customers contributed 501.23K, or 51.9% of revenue.",
        "The base includes 261 new customers and 239 returning customers.",
        "Only 11 customers are classified as high value, indicating retention opportunity.",
    ],
    "Retention campaigns should focus on medium- and high-value customers while "
    "tracking returning-customer revenue as a primary loyalty KPI.",
)

dashboard_page(
    6,
    "Inventory & Operations Analysis",
    "inventory-operations.png",
    "Stock level, average stock, reorder exposure, fast-moving products at risk, "
    "and low-stock products by branch.",
    [
        "Total stock is approximately 18K, with an average of 110 units per product.",
        "Seventeen products reached the reorder threshold.",
        "Jeddah has the highest exposure, with seven low-stock products.",
        "Inventory coverage remains 89.38%, but fast-moving items still require action.",
    ],
    "Demand and stock exposure should be reviewed together so replenishment protects "
    "future sales rather than responding only after a stockout occurs.",
)

# Page 8 - Recommendations and project outcome
story.extend(
    [
        Paragraph("7. Recommendations and Project Outcome", styles["SectionTitle"]),
        Paragraph("Business recommendations", styles["Subheading"]),
        bullet("Review the 17 reorder-required products every week.", styles["ReportBullet"]),
        bullet("Prioritize high-revenue, fast-moving products during replenishment.", styles["ReportBullet"]),
        bullet("Investigate Jeddah allocation and replenishment lead times.", styles["ReportBullet"]),
        bullet("Protect availability in the Vape category while monitoring concentration risk.", styles["ReportBullet"]),
        bullet("Target medium- and high-value customers with retention campaigns.", styles["ReportBullet"]),
        bullet("Use branch demand and inventory exposure together for stock allocation.", styles["ReportBullet"]),
        bullet("Prepare inventory earlier for the stronger November and December demand.", styles["ReportBullet"]),
        Spacer(1, 5 * mm),
        Paragraph("Project outcome", styles["Subheading"]),
        Paragraph(
            "The project delivers a reusable management reporting layer that connects "
            "sales performance, profitability, customer behavior, and inventory risk. "
            "It demonstrates practical capability in Power BI, DAX, Power Query, data "
            "modeling, KPI design, validation, and business communication.",
            styles["Body"],
        ),
        Paragraph("Files included", styles["Subheading"]),
    ]
)

files = [
    ["File", "Purpose"],
    ["Saudi_Retail_BI_Dashboard.pbix", "Interactive four-page Power BI report"],
    ["Saudi_Retail_BI_Dashboard_Report.pdf", "Management-facing project report"],
    ["README.md", "Portfolio summary, findings, and review instructions"],
    ["docs/", "Data model and verified KPI documentation"],
    ["tools/", "Repeatable layout repair and report generation scripts"],
]
files_table = Table(files, colWidths=[68 * mm, 102 * mm], repeatRows=1)
files_table.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("FONTNAME", (0, 0), (-1, 0), "DejaVuSans-Bold"),
            ("FONTNAME", (0, 1), (-1, -1), "DejaVuSans"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 0.5, GRID),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]
    )
)
story.extend(
    [
        files_table,
        Spacer(1, 6 * mm),
        Paragraph("Author", styles["Subheading"]),
        Paragraph(
            "<b>Yasir Awad</b><br/>"
            "Data Analyst | Business Intelligence | Energy & Operations Analytics<br/>"
            "GitHub: github.com/Yasir101-hi<br/>"
            "LinkedIn: linkedin.com/in/yasirawad",
            styles["Body"],
        ),
    ]
)

doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(OUTPUT)
