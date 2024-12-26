# chatbot_kutuphane

Kütüphane Dökümantasyon Sistemi Chatbot

Proje, kütüphane kullanıcılarının kütüphane hakkında bilgi edinmesini, kitapları sorgulamasını ve yazarlar ile ilgili detaylara kolayca ulaşmasını sağlar.
Amacımız, kütüphane kullanıcılarına daha modern ve etkili bir deneyim sunarken, aynı zamanda kütüphane personelinin iş yükünü azaltmaktır.

#Proje Nasıl Kurulur?
- Goggle cloud'a mail hesabınızı bağlayın ve proje oluşturun.
- Proje dosyanıza Goggle Dialogflow entegrasyonunu yapın.
- Proje dosyasını indirin
- Proje dosyasının içerisindeki Project_dialogflow.zip dosyasında bulunan dialogflow projesini, oluşturduğunuz dialofflow projesine entegre edin.
- Proje dosyasının içerisindeki database_api.py dosyasını açın, kod satırında bulunan "def initialize_db" fonksiyonunu bulun ve uri kısmında yer alan "Bağlantı URI'si" kısmını database bağlantınızı girin. Projede MangoDB kullandığımız için bu adımları MangoDB üzerinden anlatacğım. MangoDB Atlas üzerinden hesabınıza giriş yapın ve yeni bir Cluster oluşturun. Database Access menüsünden yeni bir database user oluşturun. Atlas'ta cluster'ınıza tıklayın, "Connect" butonuna tıklayın, Connect your application" seçeneğini seçin buradan size özel connection string'i kopyalayın. uri = "mongodb+srv://KULLANICI_ADINIZ:SIFRENIZ@CLUSTER_ADINIZ.xxxxx.mongodb.net/?retryWrites=true&w=majority" şeklinde olacak.
- moduler_libarary_bot.py dosyasında config sınıfının bilgilerini de kendi projenize göre değiştirmelisiniz.
- Bu aşamalar tamamlandıktan sonra projeyi rahatlıkla çalıştırabilirsiniz.

# Projede Kullanılan Materyaller ve Diller

- Dialogflow & Goggle Cloud
- MangoDB
- Python (google.cloud.dialogflow, pymongo, flask, os, uuid, datetime)
- HTML
- JavaScript

# Text Dosyası
- Text dosyasının içerisinde chatbot'a sorulabilecek örnek soru kalıpları verilmiştir.

- ![chatbot](https://github.com/user-attachments/assets/2477cf91-a425-4017-9529-1a9e1625edfa)

