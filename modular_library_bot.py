from google.cloud import dialogflow
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import Flask, request, render_template, jsonify, session
import os
import uuid
from datetime import datetime

app = Flask(__name__)

class Config:
    SERVICE_ACCOUNT_PATH = "projeadiniz.json"  # service account dosyasının adı
    DIALOGFLOW_PROJECT_ID = "project-id"  # kendi project ID'niz
    MONGO_URI = "mongodb-connection-string"  # kendi MongoDB bağlantı bilgileriniz
    DB_NAME = "chatbot_db"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = Config.SERVICE_ACCOUNT_PATH

class DatabaseManager:
    @staticmethod
    def initialize():
        client = MongoClient(Config.MONGO_URI, server_api=ServerApi('1'))
        return client[Config.DB_NAME]

    @staticmethod
    def reserve_book(user, book):
        db = DatabaseManager.initialize()
        reservations = db['reservations']
        reservation = {
            "user": user,
            "book": book,
            "reservation_date": datetime.now(),
            "status": "active"
        }
        reservations.insert_one(reservation)
        return f"{book} kitabı {user} için başarıyla rezerve edildi."

    @staticmethod
    def borrow_book(user, book, return_date):
        db = DatabaseManager.initialize()
        loans = db['loans']
        loan = {
            "user": user,
            "book": book,
            "loan_date": datetime.now(),
            "return_date": datetime.strptime(return_date, '%Y-%m-%d'),
            "status": "borrowed"
        }
        loans.insert_one(loan)
        return f"{book} kitabı {user} tarafından ödünç alındı. İade tarihi: {return_date}."

    @staticmethod
    def suggest_books(genre):
        db = DatabaseManager.initialize()
        books = db['books']
        suggestions = books.find({"genre": genre}).limit(5)
        return [book['title'] for book in suggestions]

class DialogflowManager:
    @staticmethod
    def detect_intent_texts(project_id, session_id, texts, language_code="tr"):
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(project_id, session_id)

        responses = []
        for text in texts:
            text_input = dialogflow.TextInput(text=text, language_code=language_code)
            query_input = dialogflow.QueryInput(text=text_input)
            try:
                response = session_client.detect_intent(
                    request={"session": session, "query_input": query_input}
                )
                fulfillment_text = response.query_result.fulfillment_text
                intent_name = response.query_result.intent.display_name

                if intent_name == "RezervasyonYap":
                    book_name = response.query_result.parameters.get('book_name')
                    user = response.query_result.parameters.get('user')
                    if not book_name or not user:
                        responses.append("Kitap adı veya kullanıcı bilgisi eksik.")
                    else:
                        reserve_status = DatabaseManager.reserve_book(user, book_name)
                        responses.append(reserve_status)

                elif intent_name == "OduncAl":
                    book_name = response.query_result.parameters.get('book_name')
                    user = response.query_result.parameters.get('user')
                    return_date = response.query_result.parameters.get('return_date')
                    if not book_name or not user or not return_date:
                        responses.append("Kitap adı, kullanıcı bilgisi veya iade tarihi eksik.")
                    else:
                        borrow_status = DatabaseManager.borrow_book(user, book_name, return_date)
                        responses.append(borrow_status)

                elif intent_name == "KitapTuruOner":
                    genre = response.query_result.parameters.get('genre')
                    if not genre:
                        responses.append("Kitap türü belirtilmedi.")
                    else:
                        suggestions = DatabaseManager.suggest_books(genre)
                        if suggestions:
                            responses.append(f"{genre} türünde öneriler: {', '.join(suggestions)}.")
                        else:
                            responses.append(f"{genre} türünde öneri bulunamadı.")

                else:
                    responses.append(fulfillment_text)

            except Exception as e:
                responses.append("Bir hata oluştu. Lütfen tekrar deneyin.")

        return responses


@app.route("/", methods=["GET", "POST"])
def chatbot():
    # Session'ı başlat
    if 'chat_history' not in session:
        session['chat_history'] = []

    if request.method == "POST":
        user_input = request.form["user_input"]
        session_id = str(uuid.uuid4())
        responses = DialogflowManager.detect_intent_texts(
            Config.DIALOGFLOW_PROJECT_ID, session_id, [user_input]
        )
        bot_response = responses[0] if responses else "Üzgünüm, anlamadım."

        # Yeni mesajları chat geçmişine ekle
        session['chat_history'].append({
            'type': 'user',
            'content': user_input
        })
        session['chat_history'].append({
            'type': 'bot',
            'content': bot_response
        })

        # Session'ı kaydet
        session.modified = True

    return render_template("index.html", chat_history=session.get('chat_history', []))
@app.route('/clear_chat', methods=['POST'])
def clear_chat():
    session['chat_history'] = []
    return '', 204

@app.route("/webhook", methods=['POST'])
def webhook():
    req = request.get_json()

    intent_name = req['queryResult']['intent']['displayName']
    parameters = req['queryResult']['parameters']

    response_text = ""

    if intent_name == "RezervasyonYap":
        book_name = parameters.get('book_name')
        user = parameters.get('user')
        if not book_name or not user:
            response_text = "Kitap adı veya kullanıcı bilgisi eksik."
        else:
            response_text = DatabaseManager.reserve_book(user, book_name)

    elif intent_name == "OduncAl":
        book_name = parameters.get('book_name')
        user = parameters.get('user')
        return_date = parameters.get('return_date')
        if not book_name or not user or not return_date:
            response_text = "Kitap adı, kullanıcı bilgisi veya iade tarihi eksik."
        else:
            response_text = DatabaseManager.borrow_book(user, book_name, return_date)

    elif intent_name == "KitapTuruOner":
        genre = parameters.get('genre')
        if not genre:
            response_text = "Kitap türü belirtilmedi."
        else:
            suggestions = DatabaseManager.suggest_books(genre)
            if suggestions:
                response_text = f"{genre} türünde öneriler: {', '.join(suggestions)}."
            else:
                response_text = f"{genre} türünde öneri bulunamadı."

    return jsonify({
        'fulfillmentText': response_text
    })

if __name__ == "__main__":
    app.run(debug=True)