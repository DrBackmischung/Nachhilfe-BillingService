from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
from django.core.mail import send_mail
from django.conf import settings
from django.http import FileResponse
from reportlab.pdfgen import canvas
import json
from PIL import Image
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from django.core.mail import EmailMessage
import reportlab


def index(request):
    json_data = json.loads(request.body)
    name = json_data['name']
    mail = json_data['mail']
    street = json_data['street']
    houseNr = json_data['houseNr']
    zipCode = json_data['zipCode']
    city = json_data['city']
    article = json_data['article']
    price = json_data['price']

    subject = "Rechnung und Buchungsbestätigung"
    message = "Vielen Dank für die Buchung von: "+article+" zum Preis von "+price+"€."
    email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [mail])
    pdf = createPDF(name, mail, street+" "+houseNr+", "+zipCode+" "+city, article, price)
    email.attach('Rechnung.pdf', pdf, 'application/pdf')
    try: 
        email.send(fail_silently=False)
        return HttpResponse("Email gesendet")
    except:
        return HttpResponseServerError("Email nicht gesendet")

def createPDF(name, mail, address, article, price):
   
   buffer=BytesIO()
   c = canvas.Canvas(buffer, pagesize=A4)
   # Start writing

   c.setFont("Helvetica", 16, leading=None)
   c.drawString(100, 750, 'Buchungsbestätigung')
   c.line(100, 740, 500, 740)
   c.setFont("Helvetica", 12, leading=None)
   c.drawString(100, 720, 'Leistung: '+article+" ("+price+"€)")

   c.setFont("Helvetica", 16, leading=None)
   c.drawString(100, 660, 'Persönliche Angaben')
   c.line(100, 650, 500, 650)
   c.setFont("Helvetica", 12, leading=None)
   c.drawString(100, 630, 'Name: '+name+" ("+mail+")")
   c.drawString(100, 610, 'Adresse: '+address)

   c.setFont("Helvetica", 16, leading=None)
   c.drawString(100, 550, 'Bezahlung')
   c.line(100, 540, 500, 540)
   c.setFont("Helvetica", 12, leading=None)
   c.drawString(100, 520, "Bezahlung über Paypal ("+mail+")")
   c.drawString(100, 500, 'Leistung: 15 x '+article)
   c.drawString(100, 480, 'Gesamtpreis: '+price+"€")
   c.drawString(100, 460, 'darin enthaltene Mehrwertsteuer (19%): 1€')

   c.setFont("Helvetica", 6, leading=None)
   c.drawString(100, 130, "Nachhilfe XYZ")
   c.drawString(100, 120, "ABC Straße")
   c.drawString(100, 110, "68159 Mannheim")
   c.drawString(100, 100, "noreply.nachhilfe@gmail.com")
   # End writing
   c.showPage()
   c.save()
   pdf = buffer.getvalue()
   buffer.close()
   return pdf