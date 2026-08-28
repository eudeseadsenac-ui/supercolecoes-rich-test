import os
import time
import requests

TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"


def menu_principal():
    return {
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


def menu_superman():
    return {
        "blocks": [
            {
                "type": "heading",
                "text": "🦸 SUPERMAN",
                "size": 2
            },
            {
                "type": "paragraph",
                "text": "Escolha uma editora:"
            },
            {
                "type": "buttons",
                "buttons": [
                    {
                        "text": "Abril",
                        "callback_data": "superman_abril",
                        "style": "primary"
                    },
                    {
                        "text": "Panini",
                        "callback_data": "superman_panini"
                    },
                    {
                        "text": "EBAL",
                        "callback_data": "superman_ebal"
                    }
                ],
                "align": "center"
            },
            {
                "type": "buttons",
                "buttons": [
                    {
                        "text": "⬅️ Voltar",
                        "callback_data": "voltar"
                    }
                ],
                "align": "center"
            }
        ]
    }


def enviar_rich_message(chat_id):
    payload = {
        "chat_id": chat_id,
        "rich_message": menu_principal()
    }

    resposta = requests.post(
        f"{BASE_URL}/sendRichMessage",
        json=payload,
        timeout=30
    )

    print(resposta.text)


def editar_rich_message(chat_id, message_id, rich_message):
    payload = {
        "chat_id": chat_id,
        "message_id": message_id,
        "rich_message": rich_message
    }

    resposta = requests.post(
        f"{BASE_URL}/editMessageText",
        json=payload,
        timeout=30
    )

    print(resposta.text)


def responder_callback(callback_query_id):
    requests.post(
        f"{BASE_URL}/answerCallbackQuery",
        json={
            "callback_query_id": callback_query_id
        },
        timeout=30
    )


def main():
    offset = 0

    while True:
        try:
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

                callback = update.get("callback_query")

                if callback:
                    callback_id = callback["id"]
                    dados = callback.get("data")
                    mensagem_callback = callback.get("message")

                    responder_callback(callback_id)

                    if mensagem_callback:
                        chat_id = mensagem_callback["chat"]["id"]
                        message_id = mensagem_callback["message_id"]

                        if dados == "superman":
                            editar_rich_message(
                                chat_id,
                                message_id,
                                menu_superman()
                            )

                        elif dados == "voltar":
                            editar_rich_message(
                                chat_id,
                                message_id,
                                menu_principal()
                            )

        except Exception as erro:
            print("ERRO:", erro)
            time.sleep(5)

        time.sleep(1)


if __name__ == "__main__":
    main()
