from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from datetime import datetime
import uuid


def generate_receipt_pdf(user, game):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    transaction_id = str(uuid.uuid4())[:10].upper()

    elements = []

    elements.append(Paragraph("GAME STORE RECEIPT", styles['Title']))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph(f"User: {user.username}", styles['Normal']))
    elements.append(Paragraph(f"Game: {game.title}", styles['Normal']))
    elements.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    elements.append(Paragraph(f"Transaction ID: {transaction_id}", styles['Normal']))

    elements.append(Spacer(1, 15))

    data = [
        ["Item", "Price"],
        [game.title, f"${game.price}"]
    ]

    table = Table(data)
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))

    elements.append(table)

    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Thank you for your purchase!", styles['Italic']))

    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    return pdf