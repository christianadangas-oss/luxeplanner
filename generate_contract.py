from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

OUTPUT = "maison_leroux_catering_contract.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=letter,
    rightMargin=0.9*inch,
    leftMargin=0.9*inch,
    topMargin=0.9*inch,
    bottomMargin=0.9*inch,
)

styles = getSampleStyleSheet()

# Custom styles
firm = ParagraphStyle("firm", fontSize=22, fontName="Times-Bold",
    alignment=TA_CENTER, spaceAfter=2, letterSpacing=2)
firm_sub = ParagraphStyle("firm_sub", fontSize=9, fontName="Times-Roman",
    alignment=TA_CENTER, spaceAfter=14, textColor=colors.HexColor("#666666"))
doc_title = ParagraphStyle("doc_title", fontSize=14, fontName="Times-Bold",
    alignment=TA_CENTER, spaceAfter=4)
doc_ref = ParagraphStyle("doc_ref", fontSize=9, fontName="Times-Roman",
    alignment=TA_CENTER, textColor=colors.HexColor("#666666"), spaceAfter=14)
party_name = ParagraphStyle("party_name", fontSize=12, fontName="Times-Bold",
    alignment=TA_CENTER, spaceAfter=2)
party_detail = ParagraphStyle("party_detail", fontSize=9, fontName="Times-Roman",
    alignment=TA_CENTER, textColor=colors.HexColor("#555555"), spaceAfter=4)
and_style = ParagraphStyle("and_style", fontSize=10, fontName="Times-Italic",
    alignment=TA_CENTER, textColor=colors.HexColor("#888888"), spaceAfter=8)
article_head = ParagraphStyle("article_head", fontSize=10, fontName="Helvetica-Bold",
    spaceBefore=16, spaceAfter=4, textColor=colors.HexColor("#111111"))
clause = ParagraphStyle("clause", fontSize=10.5, fontName="Times-Roman",
    leftIndent=18, spaceAfter=5, alignment=TA_JUSTIFY, leading=15)
clause_bold = ParagraphStyle("clause_bold", fontSize=10.5, fontName="Times-Bold",
    leftIndent=18, spaceAfter=3)
bullet = ParagraphStyle("bullet", fontSize=10.5, fontName="Times-Roman",
    leftIndent=36, spaceAfter=3, bulletIndent=24)
normal = ParagraphStyle("normal", fontSize=10.5, fontName="Times-Roman",
    spaceAfter=5, alignment=TA_JUSTIFY, leading=15)
risk_note = ParagraphStyle("risk_note", fontSize=9.5, fontName="Helvetica",
    leftIndent=10, spaceAfter=6, textColor=colors.HexColor("#993333"),
    borderPadding=(6,8,6,8))

def rule(thick=1.5):
    return HRFlowable(width="100%", thickness=thick,
                      color=colors.HexColor("#111111"), spaceAfter=10, spaceBefore=4)

def thin_rule():
    return HRFlowable(width="100%", thickness=0.5,
                      color=colors.HexColor("#aaaaaa"), spaceAfter=10, spaceBefore=4)

def art(title):
    return Paragraph(title, article_head)

def cl(num, text):
    return Paragraph(f"{num}  {text}", clause)

def bul(text):
    return Paragraph(f"• {text}", bullet)

def spacer(h=0.1):
    return Spacer(1, h*inch)

# Payment table data
pay_data = [
    ["Payment", "Amount", "Due Date", "Notes"],
    ["Deposit (non-refundable)", "$18,900.00", "March 15, 2025",
     "20% of total. Secures date. Non-refundable under any circumstances."],
    ["2nd Payment", "$28,350.00", "June 1, 2025",
     "Required before menu tasting is scheduled."],
    ["3rd Payment", "$28,350.00", "August 1, 2025",
     "Non-refundable after August 1."],
    ["Final Balance", "Remaining\nbalance", "Sept 12, 2025",
     "Based on confirmed count. Wire or certified check only."],
    ["Overtime", "$1,200/hr", "Post-event\ninvoice",
     "If event extends past 11:00 PM. Written auth required by 10:30 PM."],
]

cancel_data = [
    ["Cancellation Notice", "Amount Forfeited"],
    ["More than 180 days prior\n(before March 24, 2025)", "Deposit only — $18,900"],
    ["90–180 days prior\n(March 24 – June 22, 2025)", "50% of total — $47,250"],
    ["60–89 days prior\n(June 23 – July 22, 2025)", "75% of total — $70,875"],
    ["Fewer than 60 days prior\n(after July 22, 2025)", "100% of total — $94,500"],
]

tbl_style = TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#f0f0f0")),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 8.5),
    ("FONTNAME", (0,1), (-1,-1), "Times-Roman"),
    ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#bbbbbb")),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("LEFTPADDING", (0,0), (-1,-1), 7),
    ("RIGHTPADDING", (0,0), (-1,-1), 7),
])

# Summary box
summary_data = [
    ["Event", "Whitfield–Fontaine Wedding Reception"],
    ["Event Date", "Saturday, September 20, 2025"],
    ["Venue", "The Pierre Hotel — Grand Ballroom, New York, NY"],
    ["Guest Count", "220 seated + 40 cocktail-only (260 total maximum)"],
    ["Service Hours", "Cocktail 5:30–7:00 PM  |  Dinner 7:00–11:00 PM"],
    ["Total Value", "$94,500.00  (220 × $380 + cocktail supplement + 22% service charge)"],
]
summary_style = TableStyle([
    ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"),
    ("FONTNAME", (1,0), (1,-1), "Times-Roman"),
    ("FONTSIZE", (0,0), (-1,-1), 9.5),
    ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#fafafa")),
    ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#bbbbbb")),
    ("INNERGRID", (0,0), (-1,-1), 0.25, colors.HexColor("#dddddd")),
    ("TOPPADDING", (0,0), (-1,-1), 4),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ("LEFTPADDING", (0,0), (-1,-1), 8),
    ("RIGHTPADDING", (0,0), (-1,-1), 8),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("COLWIDTH", (0,0), (0,-1), 1.2*inch),
])

story = []

# Cover
story += [
    spacer(0.1),
    Paragraph("Maison LeRoux", firm),
    Paragraph("CATERING & PRIVATE EVENTS", firm_sub),
    rule(2),
    Paragraph("Exclusive Catering Services Agreement", doc_title),
    Paragraph("Contract No. MLR-2025-0847  ·  Prepared: March 12, 2025", doc_ref),
    rule(2),
    spacer(0.15),
    Paragraph("Agreement Between", ParagraphStyle("tiny", fontSize=8,
        fontName="Helvetica", alignment=TA_CENTER,
        textColor=colors.HexColor("#999999"), spaceAfter=8)),
    Paragraph("Maison LeRoux Catering & Events, LLC", party_name),
    Paragraph(
        "142 West 57th Street, Suite 900, New York, NY 10019"
        "Tel: (212) 555-0183  ·  events@maisonleroux.com  ·  License No. NYC-CAT-2019-4421",
        party_detail),
    Paragraph("— and —", and_style),
    Paragraph("Mr. James Whitfield & Ms. Camille Fontaine", party_name),
    Paragraph(
        "88 Park Avenue, Apt 14C, New York, NY 10016"
        "Tel: (917) 555-0294  ·  camillewhitfield2025@gmail.com",
        party_detail),
    spacer(0.15),
    thin_rule(),
]

# Event summary table
story.append(Paragraph("Event Summary", ParagraphStyle("sh", fontSize=9,
    fontName="Helvetica-Bold", spaceAfter=5)))
story.append(Table(summary_data,
    colWidths=[1.3*inch, 4.9*inch], style=summary_style))
story.append(spacer(0.1))

# Article 1
story += [
    art("Article 1 — Nature of Agreement"),
    cl("1.1", 'Maison LeRoux Catering & Events, LLC ("Caterer") shall be engaged as an independent contractor to provide exclusive full-service catering. Caterer is not an agent or employee of Client.'),
    cl("1.2", "Caterer holds NYC DOHMH food service permits and all licenses required by New York State, "
       "current through December 31, 2025. License No. NYC-CAT-2019-4421."),
    cl("1.3", "Exclusivity. Caterer is the sole provider of all food and non-alcoholic beverages at "
       "the Event. No outside food permitted. Exception: Client's wedding cake from an NYC-licensed bakery."),
    cl("1.4", "Caterer shall not subcontract food preparation or service staff without Client's prior written consent."),
]

# Article 2
story += [
    art("Article 2 — Scope of Services"),
    cl("2.1", "Cocktail Hour (5:30–7:00 PM): Passed hors d'oeuvres for 260 guests, two butler "
       "stations, one staffed raw bar, sparkling wine welcome toast."),
    cl("2.2", "Seated Dinner (7:00–11:00 PM): Four-course plated dinner for 220 guests, choice "
       "of two entrées, full French service."),
    cl("2.3", "Staffing included:"),
    bul("1 Executive Chef (on-site from 10:00 AM) and 2 Sous Chefs"),
    bul("1 Event Director / Captain"),
    bul("22 Servers (guaranteed 1:10 ratio), 4 Bussers, 2 Bartenders (non-alcoholic), 2 Kitchen Porters"),
    cl("2.4", "Equipment included: All china, flatware, glassware, serving platters, chafers, "
       "staff linen napkins. Guest table linens are Client's responsibility."),
    cl("2.5", "Setup & Breakdown: Kitchen access required by 10:00 AM. Ballroom "
       "setup access required by 2:00 PM. Full breakdown by 1:00 AM on September 21, 2025. "
       "Client must secure these venue access windows."),
    cl("2.6", "Dietary accommodations: Up to 30 special dietary requests accommodated if "
       "submitted by September 5, 2025. Requests after this date cannot be guaranteed."),
]

# Article 3
story += [
    art("Article 3 — Guest Count & Pricing"),
    cl("3.1", "Final menu confirmed by July 15, 2025. Tasting for 4 guests scheduled by July 1, 2025."),
    cl("3.2", "Final guaranteed guest count due in writing by September 5, 2025. "
       "This is the minimum billing count regardless of actual attendance. "
       "Count increases up to 10% accepted until September 12, 2025."),
    cl("3.3", "Pricing: $380.00 per seated dinner guest  ·  $65.00 per cocktail-only guest "
       "above seated count. Inclusive of food, non-alcoholic beverages, staffing, and equipment. "
       "Excludes alcohol, venue fees, and gratuity."),
    cl("3.4", "A 22% service charge applies to all food and labor. This is retained by Caterer "
       "for operational costs and is not a gratuity to service staff."),
]

# Article 4 — Payment table
story += [
    art("Article 4 — Compensation & Payment Schedule"),
    spacer(0.05),
    Table(pay_data,
          colWidths=[1.4*inch, 0.9*inch, 1.0*inch, 2.9*inch],
          style=tbl_style),
    spacer(0.05),
    cl("4.1", "All payments by wire transfer or certified bank check only. Late payments incur "
       "1.5% per month interest. Delinquency over 15 days allows Caterer to suspend planning services."),
]

# Article 5 — Cancellation
story += [
    art("Article 5 — Cancellation & Termination"),
    Paragraph(
        "⚠  Risk flag: tiered non-refundable provisions apply. Full contract value ($94,500) "
        "forfeited if cancelled within 60 days of event.",
        risk_note),
    spacer(0.05),
    Table(cancel_data,
          colWidths=[3.0*inch, 3.2*inch],
          style=tbl_style),
    spacer(0.05),
    cl("5.3", "Date Change. One postponement allowed (90+ days notice) for a $2,500 fee, "
       "subject to Caterer availability. Second changes treated as cancellation and rebooking."),
    cl("5.4", "Force Majeure covers: declared government emergency, mandatory venue closure by "
       "government order, pandemic-related gathering prohibition, fire, flood, or act of God. "
       "Does NOT cover personal illness, change of mind, or financial hardship. "
       "No cash refunds — payments applied to rebook within 18 months of original date."),
    cl("5.5", "Cancellation by Caterer. Full refund (less direct costs incurred) if Caterer "
       "permanently closes or loses required permits. Minimum 60 days written notice required."),
]

# Article 6
story += [
    art("Article 6 — Liability & Insurance"),
    cl("6.1", "Caterer maintains: CGL insurance minimum $2,000,000 per occurrence / $5,000,000 aggregate. "
       "Certificate of insurance naming Client and The Pierre Hotel as additional insureds due by "
       "August 15, 2025."),
    cl("6.2", "Caterer not liable for other vendors' actions, indirect damages, or guest property "
       "damage not caused by Caterer's negligence."),
]

# Article 7
story += [
    art("Article 7 — Venue Coordination"),
    cl("7.1", "Client warrants Caterer is an approved vendor at The Pierre Hotel and that the "
       "venue contract permits access per Article 2.5."),
    cl("7.2", "Minimum two (2) loading dock parking spaces from 9:00 AM to be arranged "
       "by Client through the venue at no charge to Caterer."),
]

# Article 8
story += [
    art("Article 8 — Governing Law & Entire Agreement"),
    cl("8.1", "Governed by the laws of the State of New York. Disputes submitted to binding "
       "arbitration in New York County."),
    cl("8.2", "This Agreement supersedes all prior negotiations. No amendment valid unless in "
       "writing and signed by both parties. Not binding until deposit received."),
]

# Signature block
story += [
    spacer(0.3),
    thin_rule(),
    Paragraph("Signatures", article_head),
    Paragraph(
        "By signing below, both parties agree to the terms of this Agreement. "
        "This Agreement is not binding until executed by Caterer and the initial deposit has been received.",
        normal),
    spacer(0.2),
]

sig_data = [
    [Paragraph("Maison LeRoux Catering & Events, LLC", clause_bold),
     Paragraph("Client — James Whitfield & Camille Fontaine", clause_bold)],
    ["", ""],
    ["Signature: _____________________________",
     "Signature: _____________________________"],
    ["", ""],
    ["Printed Name: __________________________",
     "Printed Name: __________________________"],
    ["Title: _________________________________",
     ""],
    ["Date: __________________________________",
     "Date: __________________________________"],
]
sig_style = TableStyle([
    ("FONTNAME", (0,0), (-1,-1), "Times-Roman"),
    ("FONTSIZE", (0,0), (-1,-1), 10),
    ("TOPPADDING", (0,0), (-1,-1), 5),
    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ("VALIGN", (0,0), (-1,-1), "BOTTOM"),
])
story.append(Table(sig_data, colWidths=[3.1*inch, 3.1*inch], style=sig_style))
story.append(spacer(0.3))
story.append(HRFlowable(width="100%", thickness=0.5,
    color=colors.HexColor("#cccccc"), spaceAfter=8))
story.append(Paragraph(
    "Maison LeRoux Catering & Events, LLC  ·  Contract No. MLR-2025-0847  ·  "
    "Confidential — for named parties only",
    ParagraphStyle("footer", fontSize=8, fontName="Helvetica",
        alignment=TA_CENTER, textColor=colors.HexColor("#aaaaaa"))))

doc.build(story)
print(f"✓ Contract saved: {OUTPUT}")
