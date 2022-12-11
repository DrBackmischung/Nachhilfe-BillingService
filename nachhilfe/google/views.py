from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.http import FileResponse
from django.template.loader import render_to_string
from reportlab.pdfgen import canvas
import json
from PIL import Image
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from django.core.mail import EmailMessage
from django.utils.html import strip_tags
import reportlab
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
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
    message = '<html>    <head>    </head>    <body style="background-color: rgb(27, 27, 27);">         <img style="display: block;        margin-left: auto;        margin-right: auto;        max-width: 30%;        height: auto;" src="https://github.com/DrBackmischung/Kino-Dokumentation/blob/main/Kinovation.png?raw=true">        <h1 style="color: rgb(136, 71, 25);        text-align: center;        font-family: Arial, Helvetica, sans-serif;">Buchung abgeschlossen!</h1>        <h3 style="color: rgb(255, 255, 255);        text-align: center;        font-family: Arial, Helvetica, sans-serif;">Danke f&uuml;r deine Buchung, N-NAME! Deine Buchung f&uuml;r N-ARTIKEL wird hiermit best&auml;tigt.</h3>        <p style="color: rgb(255, 255, 255);        text-align: center;        font-family: Arial, Helvetica, sans-serif;">Name: N-NAME<br>Leistung: N-ANZAHL x N-ARTIKEL zu je N-PREIS (Gesamt: N-GESAMT)</p>        <p style="color: rgb(255, 255, 255);        text-align: center;        font-family: Arial, Helvetica, sans-serif;">Im Anhang findest du die Bestätigung/Rechnung.</p>        <img style="        display: block;        margin-left: auto;        margin-right: auto;        max-width: 3%;        height: auto;" src="https://github.com/DrBackmischung/Kino-Dokumentation/blob/main/KV.png?raw=true">        <p style="        color: rgb(114, 114, 114);        text-align: center;        font-family: Arial, Helvetica, sans-serif;        font-size: xx-small;"><a class="footer" href="https://kino-frontend.vercel.app/impressum">Impressum</a> <a class="footer" href="https://kino-frontend.vercel.app/">Homepage</a> <a class="footer" href="https://kino-frontend.vercel.app/agbs">AGB</a></p>    </body></html>'
    # message = render_to_string("https://raw.githubusercontent.com/DrBackmischung/Nachhilfe-Email/main/mail.html")
    email = EmailMultiAlternatives(subject, strip_tags(message), settings.EMAIL_HOST_USER, [mail])
    pdf = createPDF(name, mail, street+" "+houseNr+", "+zipCode+" "+city, article, price)
    email.attach('Rechnung.pdf', pdf, 'application/pdf')
    email.attach_alternative(message, "text/html")
    try: 
        email.send(fail_silently=False)
        response = {'message': 'Email sent'}
        return JsonResponse(response)
    except:
        response = {'message': 'Email not sent'}
        return JsonResponse(response)

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