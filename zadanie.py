from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
import mysql.connector
import os

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="anton",
        password="Test12345",
        database="bookstore_db"
    )

# Конфигурация Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Используй SMTP для Gmail
app.config['MAIL_PORT'] = 587  # Порт (для Gmail)
app.config['MAIL_USE_TLS'] = True  # TLS
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'infobookshop2025@gmail.com'  # email
app.config['MAIL_PASSWORD'] = 'yconixsaletunjkh'  # пароль (или пароль приложения, если Gmail)
app.config['MAIL_DEFAULT_SENDER'] = 'garantantony@gmail.com'  # Адрес отправителя

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
         # Сохранение в базу данных
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO messages (name, email, message) VALUES (%s, %s, %s)", (name, email, message))
        db.commit()
        cursor.close()
        db.close()
        
        # Создание сообщения
        msg = Message('Новое сообщение с сайта', recipients=['infobookshop2025@gmail.com'])  # email получателя
        msg.body = f"От: {name}\nEmail: {email}\n\nСообщение:\n{message}"
        
        try:
            mail.send(msg)  # Отправка email
            return redirect(url_for('success'))  # Перенаправление на страницу успеха
        except Exception as e:
            return f"Ошибка при отправке сообщения: {e}"

    return render_template('contacts.html')

@app.route('/success')
def success():
    return 'Спасибо за ваше сообщение! Мы с вами свяжемся.'

@app.route('/books')
def books():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT b.title, b.genre, b.price, b.publication_year, b.stock, b.short_description, b.author_name
        FROM Books b
    """)
    books = cursor.fetchall()
    cursor.close()
    db.close()

    # Словарь для изображений книг с внешними ссылками
    additional_images = {
        'Гарри Поттер и философский камень': 'https://avatars.mds.yandex.net/get-mpic/12288829/2a00000191193d149afe88270b7fde920eb6/orig',
        '1984': 'https://cdn1.ozone.ru/s3/multimedia-l/6350703849.jpg',
        'Хоббит': 'https://ir.ozone.ru/multimedia/c1000/1003862713.jpg',
        'Евгений Онегин': 'https://cdn1.ozone.ru/s3/multimedia-x/6000057993.jpg',
        'Гарри Поттер и тайная комната': 'https://avatars.mds.yandex.net/get-mpic/4407413/img_id3460457214731718137.jpeg/orig',
        'Гарри Поттер и узник Азкабана': 'https://avatars.mds.yandex.net/get-mpic/5238069/img_id7344419894101235815.jpeg/orig',
        '1984: Антиутопия': 'https://avatars.mds.yandex.net/i?id=07678609c7a014f034c53eca1b078bd8_l-7607859-images-thumbs&n=13',
        'Скотный двор': 'https://avatars.mds.yandex.net/get-mpic/5068955/img_id9077815909815014537.jpeg/orig',
        'Два ток в пустоши': 'https://static10.labirint.ru/books/594437/cover.jpg',
        'Сильмариллион': 'https://avatars.mds.yandex.net/get-mpic/12525950/2a0000018e84b770bb7658a16f334d181a2c/orig',
        'Руслан и Людмила': 'https://avatars.mds.yandex.net/get-mpic/1859495/img_id8788799357320999703.jpeg/orig',
        'Капитанская дочка': 'https://cdn1.ozone.ru/s3/multimedia-1-2/7220524178.jpg'
    }

    # Добавляем ссылки на изображения
    for book in books:
        title = book['title']
        if title in additional_images:
            book['image_url'] = additional_images[title]
        else:
            book['image_url'] = 'https://via.placeholder.com/150'  # Если нет изображения

    return render_template('books.html', books=books)
 
@app.route('/authors')
def authors():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Authors")
    authors = cursor.fetchall()
    cursor.close()
    db.close()

    # Фотографии авторов, добавленные вручную
    additional_photos = {
        'Роулинг': 'https://upload.wikimedia.org/wikipedia/commons/5/5d/J._K._Rowling_2010.jpg',
        'Оруэлл': 'https://cdn.ruwiki.ru/commonswiki/files/thumb/7/7e/George_Orwell_press_photo.jpg/800px-George_Orwell_press_photo.jpg',
        'Tolkien': 'https://static.wikia.nocookie.net/seigneur-desanneauximages5/54J._R._R._Tolkien.jpg/revision/latest/scale-to-width-down/1200?cb=20210211225900&path-prefix=fr',
        'Пушкин': 'https://avatars.mds.yandex.net/get-yapic/64336/AST2sLbdMvlT5mNst2KsahPsVOQ-1/orig'
    }

    # Добавляем фотографии вручную и биографии из базы данных
    for author in authors:
        last_name = author['last_name']
        if last_name in additional_photos:
            author['photo_url'] = additional_photos[last_name]
        else:
            author['photo_url'] = 'https://via.placeholder.com/100'  # если нет фото

    return render_template('authors.html', authors=authors)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)


