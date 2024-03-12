from tasks import models, database
import random
from barcode import EAN13
from barcode.writer import ImageWriter
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
from dotenv import load_dotenv
import base64

load_dotenv()


async def handle_form_submission(data:models.Person):
    conn, cursor = database.make_db()
    cwd = os.getcwd()
    """
    we are getting the following data
    time: str
    name: str
    email: str
    phone: str
    accommodation: str

    ALGO :
    1. Take the data
    2. Make a unique uid, unique one for them and generate a bar code
    3. Mail them the data
    4. Insert into the Table
    """
    # making the unique number
    uid = random.randint(1_000_000_000_000, 9_999_999_999_999 + 1)
    query = """
select uid from people;
    """
    cursor.execute(query)
    uids = cursor.fetchall()
    uids = [int(int(uid[0])/10) for uid in uids]
    while int(int(uid)/10) in uids:
        uid = random.randint(1_000_000_000_000, 9_999_999_999_999 + 1)
    print(f"unique uid genrated : {uid}")
    #  making the barcode
    unique_barcode = EAN13(str(uid), writer=ImageWriter())
    barcode_path = f"{cwd}/file_buffer/{str(unique_barcode)}"
    unique_barcode.save(barcode_path)
    barcode_path = f"{cwd}/file_buffer/{str(unique_barcode)}.png"
    print("barcode image saved to the file system")
    # sending the mail
    with open(barcode_path, 'rb') as barcode_file:
        barcode_data = barcode_file.read()
    barcode_base64 = base64.b64encode(barcode_data).decode('utf-8')
    sender_mail = os.getenv('SENDER_EMAIL')
    sender_pass = os.getenv('SENDER_APP_PASSWORD')
    subject = "Get Your Tickets Here"
    body_html = f"""
<html>
    <body>
      <p style="font-size: 16px; color: #333;">Hello Guys,</p>
      <p style="font-size: 16px; color: #333;">
        I am Armaan, your host, and I hope that you have a good time here at E Summit.
        <br>
        Besides that I wish you a very happy new year
      </p>
    </body>
</html>
    """
    msg = MIMEMultipart()
    msg['From'] = sender_mail
    msg['To'] = data.email
    msg['Subject'] = subject

    msg.attach(MIMEText(body_html, 'html'))
    image_attachment = MIMEImage(barcode_data, name=f'{str(unique_barcode)}.png')
    msg.attach(image_attachment)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_mail, sender_pass)
        server.sendmail(sender_mail, data.email, msg.as_string())
    print("Mail sent")
    os.remove(barcode_path)
    print("Barcode removed ")
    # making the new entry in the table
    query = f"""
insert into people values ('{str(uid)[0:12]}', '{data.name}', '{data.email}', '{data.phone}', '{data.accommodation}')
    """
    print(query)
    cursor.execute(query)
    conn.commit()
    print("User added to the DB")
    return {"message": "User Successfully Added"}
