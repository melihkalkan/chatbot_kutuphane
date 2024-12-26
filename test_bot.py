from modular_library_bot import DialogflowManager, Config
import uuid

def test_bot():
    session_id = str(uuid.uuid4())
    test_inputs = [
        "Merhaba",
        "1984 kitabı hakkında bilgi verir misin?",
        "Çıkış"
    ]

    for user_input in test_inputs:
        print(f"Kullanıcı: {user_input}")
        responses = DialogflowManager.detect_intent_texts(
            Config.DIALOGFLOW_PROJECT_ID, session_id, [user_input]
        )
        for response in responses:
            print(f"Chatbot: {response}")

if __name__ == "__main__":
    test_bot()
