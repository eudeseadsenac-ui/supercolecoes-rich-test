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


def
