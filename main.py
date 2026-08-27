import os
import time
import requests

TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"


def enviar_rich_message(chat_id):
    payload = {
        "chat_id": chat_id,
        "rich_message": {
            "blocks": [
                {
                    "type": "heading",
                    "text": "📚 SUPERCOLEÇÕES",
                    "size": 2
                },
                {
                    "type": "paragraph",
                    "text": "Escolha uma coleção:"
                },
                {
                    "type": "buttons",
                    "buttons": [
                        {
                            "text": "Superman",
                            "callback_data": "superman",
                            "style": "primary"
                        },
                        {
                            "text": "Batman",
                            "callback_data": "batman"
                        },
                        {
                            "text": "He-Man",
                            "callback_data": "heman"
                        }
                    ],
                    "align": "center"
                }
            ]
        }
    }

    resposta = requests.post(
        f"{BASE_URL}/sendRichMessage",
        json=payload,
        timeout=30
    )

    print(resposta.text)


def main():
    offset = 0

    while True:
        resposta = requests.get(
            f"{BASE_URL}/getUpdates",
            params={
                "offset": offset,
                "timeout": 30
            },
            timeout=35
        ).json()

        for update in resposta.get("result", []):
            offset = update["update_id"] + 1

            mensagem = update.get("message")

            if mensagem and mensagem.get("text") == "/teste":
                chat_id = mensagem["chat"]["id"]
                enviar_rich_message(chat_id)

        time.sleep(1)


if __name__ == "__main__":
    main()
