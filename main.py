from modular_library_bot import DialogflowManager, DatabaseManager, Config, app
from flask import request, jsonify
import uuid


@app.route('/', methods=['POST'])
def chat_endpoint():
    session_id = str(uuid.uuid4())
    user_input = request.json.get('message')

    responses = DialogflowManager.detect_intent_texts(
        Config.DIALOGFLOW_PROJECT_ID,
        session_id,
        [user_input]
    )

    DatabaseManager.add_document("chat_logs", {
        "user_input": user_input,
        "bot_response": responses
    })

    return jsonify({"response": responses})


def console_chat():
    session_id = str(uuid.uuid4())

    while True:
        user_input = input("Kullanıcı: ")

        if user_input.lower() in ["çıkış", "exit", "quit"]:
            print("Chatbot oturumunu sonlandırıyor...")
            break

        responses = DialogflowManager.detect_intent_texts(
            Config.DIALOGFLOW_PROJECT_ID,
            session_id,
            [user_input]
        )

        for response in responses:
            print(f"Chatbot: {response}")

        DatabaseManager.add_document("chat_logs", {
            "user_input": user_input,
            "bot_response": responses
        })


from modular_library_bot import app

if __name__ == "__main__":
    app.run(debug=True)