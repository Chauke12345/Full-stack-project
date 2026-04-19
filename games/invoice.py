from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("output.pdf")
styles = getSampleStyleSheet()

content = []

content.append(Paragraph("MyGameStore™", styles['Heading2']))

doc.build(content)

content.append(Paragraph("Payment Method: Visa **** 4242", styles['Normal']))

from reportlab.platypus import HRFlowable
content.append(HRFlowable())