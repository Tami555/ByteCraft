import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
import datetime
from datetime import datetime
import aiosmtplib
import asyncio

login = 'YOUR EMAIL ADDRESS FROM WHICH THE MAIL IS BEING SENT !!!!!'
password = 'YOUR PASSWORD FOR THIS EMAIL IS'
sender_email = 'YOUR EMAIL ADDRESS FROM WHICH THE MAIL IS BEING SENT !!!!!'

async def send_email(name, delivery_date, address, dev_type, email, number_order):
    # Настройки Mail.ru
    smtp_server = "smtp.mail.ru"
    smtp_port = 587
    # Создаем письмо
    msg = MIMEMultipart()
    
    # Форматирование отправителя
    sender_name = "ByteCraft 💻"
    msg['From'] = formataddr((sender_name, sender_email))
    msg['To'] = email
    msg['Subject'] = Header(f"Ваш заказ в ByteCraft готов к отправке!", 'utf-8')

    # Форматируем дату
    delivery_date = str(delivery_date).split(' ')[0].replace('-', '.')

    # Красивый HTML-шаблон с новой цветовой схемой
    html = f"""
    <html>
      <head>
        <style>
          body {{
            font-family: 'AKONY', sans-serif;
            line-height: 1.6;
            color: #333333;
            max-width: 600px;
            margin: 0 auto;
            padding: 0;
            background-color: #f5f5f5;
          }}
          .container {{
            background-color: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            margin: 20px auto;
          }}
          .header {{
            background-color: #096637;
            color: white;
            padding: 25px;
            text-align: center;
          }}
          .logo {{
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
          }}
          .content {{
            padding: 25px;
          }}
          .order-info {{
            margin: 25px 0;
            border-left: 3px solid #0E9956;
            padding-left: 15px;
          }}
          .info-row {{
            margin-bottom: 12px;
            display: flex;
          }}
          .info-label {{
            font-weight: bold;
            min-width: 150px;
            color: #474545;
          }}
          .info-value {{
            color: #333333;
          }}
          .footer {{
            background-color: #B7FFAF;
            padding: 20px;
            text-align: center;
            font-size: 12px;
            color: #396a53;
          }}
          .button {{
            display: inline-block;
            background-color: #0E9956;
            color: white;
            padding: 12px 25px;
            text-decoration: none;
            border-radius: 4px;
            margin-top: 15px;
            font-weight: bold;
            transition: background-color 0.3s;
          }}
          .button:hover {{
            background-color: #096637;
          }}
          .highlight {{
            color: #0E9956;
            font-weight: bold;
          }}
        </style>
      </head>
      <body>
        <div class="container">
          <div class="header">
            <div class="logo">ByteCraft 💻</div>
            <h2>Ваш заказ успешно оформлен!</h2>
          </div>
          
          <div class="content">
            <p>Уважаемый(ая) <strong>{name}</strong>,</p>
            <p>Благодарим вас за заказ в нашем интернет-магазине! Ваш заказ уже собран и готов к отправке.</p>
            
            <div class="order-info">
              <div class="info-row">
                <span class="info-label">Номер заказа:</span>
                <span class="info-value highlight">#{number_order}</span>
              </div>
              <div class="info-row">
                <span class="info-label">Дата получения:</span>
                <span class="info-value">{delivery_date}</span>
              </div>
              <div class="info-row">
                <span class="info-label">Способ получения:</span>
                <span class="info-value">{"Самовывоз" if dev_type == "pickup" else "Доставка курьером"}</span>
              </div>
              <div class="info-row">
                <span class="info-label">{"Пункт выдачи:" if dev_type == "pickup" else "Адрес доставки:"}</span>
                <span class="info-value">{address}</span>
              </div>
            </div>
            
            <p>{"Пожалуйста, не забудьте взять с собой документ, удостоверяющий личность, при получении заказа." 
            if dev_type == "pickup" 
            else "Наш курьер свяжется с вами в день доставки для уточнения времени."}</p>
            
            <center>
              <a href="" class="button">Отследить заказ</a>
            </center>
          </div>
          
          <div class="footer">
            <p>Если у вас есть вопросы, пожалуйста, ответьте на это письмо или свяжитесь с нами:</p>
            <p>Email: support@bytecraft.ru | Телефон: +7 (999) 888-77-33</p>
            <p>© {datetime.now().year} ByteCraft. Все права защищены.</p>
          </div>
        </div>
      </body>
    </html>
    """

    msg.attach(MIMEText(html, 'html', 'utf-8'))

    # Отправка письма
    try:
        # Используем только start_tls=True для Mail.ru
        await aiosmtplib.send(
            msg,
            hostname=smtp_server,
            port=smtp_port,
            username=login,
            password=password,
            start_tls=True 
        )
        print("Письмо успешно отправлено!")
        return True
    except aiosmtplib.SMTPException as e:
        print(f"SMTP ошибка при отправке: {str(e)}")
        return False
    except Exception as e:
        print(f"Общая ошибка при отправке: {str(e)}")
        return False