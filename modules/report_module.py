from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_pdf(filename, ui, data):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    y = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, ui["title"])
    y -= 40

    c.setFont("Helvetica", 12)
    c.drawString(50, y, f'{ui["income"]}: ₹ {data["income"]}')
    y -= 20
    c.drawString(50, y, f'{ui["expense"]}: ₹ {data["expense"]}')
    y -= 20
    c.drawString(50, y, f'{ui["savings"]}: ₹ {data["savings"]}')
    y -= 30

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, ui["ai_insight"])
    y -= 20

    c.setFont("Helvetica", 11)
    c.drawString(50, y, data["insight"])

    c.save()
