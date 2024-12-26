from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

def initialize_db():
    uri = "mongodb-connection-string"  # kendi MongoDB bağlantı bilgileriniz yazmalı
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['chatbot_db']
    return db

#Alttaki kısım için webhook entegrasyonu gerekir

def reserve_book(db, user, book):
    reservations = db['reservations']
    reservation = {
        "user": user,
        "book": book,
        "reservation_date": datetime.now(),
        "status": "active"
    }
    reservations.insert_one(reservation)
    return f"{book} kitabı {user} için başarıyla rezerve edildi."

def borrow_book(db, user, book, return_date):
    loans = db['loans']
    loan = {
        "user": user,
        "book": book,
        "loan_date": datetime.now(),
        "return_date": return_date,
        "status": "borrowed"
    }
    loans.insert_one(loan)
    return f"{book} kitabı {user} tarafından ödünç alındı. İade tarihi: {return_date}."

def suggest_books(db, genre):
    books = db['books']
    suggestions = books.find({"genre": genre}).limit(5)
    return [book['title'] for book in suggestions]


def add_book(kitap_adi, yazar, yayinevi=None, yayin_yili=None, isbn=None):
    db = initialize_db()
    collection = db['kitaplar']
    data = {key: value for key, value in {
        "kitapAdi": kitap_adi,
        "yazar": yazar,
        "yayinevi": yayinevi,
        "yayinYili": yayin_yili,
        "isbn": isbn
    }.items() if value is not None}
    result = collection.insert_one(data)
    return f"{kitap_adi} kitabı başarıyla eklendi!"

def get_book_info(kitap_adi):
    db = initialize_db()
    collection = db['kitaplar']
    book = collection.find_one({"kitapAdi": kitap_adi})
    if book:
        response = f"{kitap_adi} adlı kitap, {book['yazar']} tarafından yazılmıştır."
        if 'yayinevi' in book:
            response += f" Yayın evi: {book['yayinevi']}."
        if 'yayinYili' in book:
            response += f" Yayın yılı: {book['yayinYili']}."
        if 'isbn' in book:
            response += f" ISBN: {book['isbn']}."
        return response
    return f"{kitap_adi} adlı kitap veritabanında bulunamadı."

def get_recommendations(book_name):
    db = initialize_db()
    collection = db['kitaplar']
    book = collection.find_one({"kitapAdi": book_name})
    if not book:
        return f"{book_name} adlı kitap veritabanında bulunamadı."
    author = book.get('yazar')
    recommendations = collection.find({"yazar": author, "kitapAdi": {"$ne": book_name}})
    recommendations_list = [rec['kitapAdi'] for rec in recommendations]
    if recommendations_list:
        return f"{book_name} adlı kitabın yazarı {author}. Ayrıca şunları da öneririm: {', '.join(recommendations_list)}."
    return f"{book_name} adlı kitabın yazarı {author}. Ancak başka öneri bulunamadı."
