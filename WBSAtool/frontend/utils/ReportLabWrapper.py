from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, Table, TableStyle, SimpleDocTemplate, PageBreak
from tempfile import gettempdir

PAGE_PADDING = 10 * mm
styles = getSampleStyleSheet()
NORMAL = styles['Normal']
HEADING1 = styles['Heading1']
HEADING2 = styles['Heading2']
HEADING3 = styles['Heading3']
BULLET = styles['Bullet']
TITEL = styles['Title']


def wrap_text(text: str):
    return Paragraph(text, NORMAL)


class ReportLab:
    def __init__(self, titel=None, author=None):
        if titel is None:
            titel = "ReportLab PDF"
        if author is None:
            author = "a Python Script"
        self.file = gettempdir() + "sammelliste.pdf"
        self.pdf = SimpleDocTemplate(self.file, titel=titel, author=author,
                                     pagesize=A4,
                                     leftMargin=PAGE_PADDING,
                                     rightMargin=PAGE_PADDING,
                                     topMargin=PAGE_PADDING,
                                     bottomMargin=PAGE_PADDING
                                     )
        self.page_count = 1
        self.elements = []

    def render(self):
        self.pdf.build(
            self.elements
        )
        return self.file

    def new_page(self):
        self.elements.append(PageBreak())
        self.page_count += 1
        return self.page_count

    def write_text(self, text: str):
        self.elements.append(Paragraph(text, NORMAL))

    def write_bullet(self, text: str):
        self.elements.append(Paragraph(text, BULLET))

    def write_heading(self, text: str, size=1):
        if size == 1:
            FORM = HEADING1
        elif size == 2:
            FORM = HEADING2
        elif size == 3:
            FORM = HEADING3
        else:
            FORM = HEADING1
        self.elements.append(Paragraph(text, FORM))

    def write_titel(self, text: str):
        self.elements.append(Paragraph(text, TITEL))

    def create_table(self, table_dict_list: list):
        page_width = 190*mm
        table = Table(
            table_dict_list,
            colWidths=(0.25*page_width, 0.25*page_width, 0.5*page_width),
            style=TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),
                    ("BOX", (0, 0), (-1, -1), 0.25, colors.black),
                    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                    ('BACKGROUND',(0,0),(-1,0),colors.lightgrey),
                    ("LEADING",(0,0),(-1,0),20),
                ]
            )
        )
        self.elements.append(table)
