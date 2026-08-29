import os
import time
import requests

TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

SUPABASE_HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}
def salvar_quadrinho(personagem, editora, colecao, edicao, file_id, nome_arquivo):
    url = f"{SUPABASE_URL}/quadrinhos_supercolecoes"

    dados = {
        "personagem": personagem,
        "editora": editora,
        "colecao": colecao,
        "edicao": edicao,
        "file_id": file_id,
        "nome_arquivo": nome_arquivo
    }

    headers = SUPABASE_HEADERS.copy()
    headers["Prefer"] = "resolution=merge-duplicates"

    resposta = requests.post(
        url,
        headers=headers,
        json=dados,
        timeout=30
    )

    print("SUPABASE SALVAR:", resposta.status_code, resposta.text)


def buscar_file_id(personagem, editora, colecao, edicao):
    url = f"{SUPABASE_URL}/quadrinhos_supercolecoes"

    params = {
        "personagem": f"eq.{personagem}",
        "editora": f"eq.{editora}",
        "colecao": f"eq.{colecao}",
        "edicao": f"eq.{edicao}",
        "select": "file_id"
    }

    resposta = requests.get(
        url,
        headers=SUPABASE_HEADERS,
        params=params,
        timeout=30
    )
    print("SUPABASE BUSCA:", resposta.status_code, resposta.text, flush=True)
    if resposta.ok:
        dados = resposta.json()

        if dados:
            return dados[0]["file_id"]

    return None
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
    url = f"{SUPABASE_URL}/quadrinhos_supercolecoes"

    params = {
        "personagem": "eq.Super-Homem",
        "select": "editora"
    }

    resposta = requests.get(
        url,
        headers=SUPABASE_HEADERS,
        params=params,
        timeout=30
    )

    editoras = []

    if resposta.ok:
        dados = resposta.json()

        for item in dados:
            editora = str(item["editora"])

            if editora not in editoras:
                editoras.append(editora)

    editoras.sort()

    botoes = []

    for editora in editoras:
        callback = editora.lower().replace(" ", "_")

        botoes.append({
            "text": editora,
            "callback_data": f"superman_{callback}"
        })

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
                "buttons": botoes,
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


def menu_superman_abril():
    return {
        "blocks": [
            {
                "type": "heading",
                "text": "🦸 SUPERMAN — ABRIL",
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
                        "text": "Super-Homem",
                        "callback_data": "super_homem",
                        "style": "primary"
                    }
                ],
                "align": "center"
            },
            {
                "type": "buttons",
                "buttons": [
                    {
                        "text": "⬅️ Voltar",
                        "callback_data": "voltar_superman"
                    }
                ],
                "align": "center"
            }
        ]
    }

def menu_super_homem():
    url = f"{SUPABASE_URL}/quadrinhos_supercolecoes"

    params = {
        "personagem": "eq.Super-Homem",
        "editora": "eq.Abril",
        "colecao": "eq.Super-Homem",
        "select": "edicao"
    }

    resposta = requests.get(
        url,
        headers=SUPABASE_HEADERS,
        params=params,
        timeout=30
    )

    edicoes = []

    if resposta.ok:
        dados = resposta.json()

        for item in dados:
            edicao = str(item["edicao"])

            if edicao not in edicoes:
                edicoes.append(edicao)

    def ordem_edicao(valor):
        try:
            return (0, int(valor))
        except ValueError:
            return (1, valor)

    edicoes.sort(key=ordem_edicao)

    botoes = []

    for edicao in edicoes:
        botoes.append({
            "text": edicao,
            "callback_data": f"super_homem_{edicao}"
        })

    return {
        "blocks": [
            {
                "type": "heading",
                "text": "🦸 SUPER-HOMEM — ABRIL",
                "size": 2
            },
            {
                "type": "paragraph",
                "text": "Escolha uma edição:"
            },
            {
                "type": "buttons",
                "buttons": botoes,
                "align": "center"
            },
            {
                "type": "buttons",
                "buttons": [
                    {
                        "text": "⬅️ Voltar",
                        "callback_data": "voltar_abril"
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

def enviar_documento(chat_id, file_id):
    requests.post(
        f"{BASE_URL}/sendDocument",
        json={
            "chat_id": chat_id,
            "document": file_id
        },
        timeout=30
    )
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
                channel_post = update.get("channel_post")

                if channel_post:
                    documento = channel_post.get("document")

                    if documento:
                        file_id = documento.get("file_id")
                        nome_arquivo = documento.get("file_name")
                        legenda = channel_post.get("caption", "")

                        print("NOVO ARQUIVO DETECTADO")
                        print("Arquivo:", nome_arquivo)
                        print("Legenda:", legenda)
                        print("FILE_ID:", file_id)
                        partes = [p.strip() for p in legenda.split("|")]

                        if len(partes) == 4:
                           personagem, editora, colecao, edicao = partes
                           chave = f"{personagem}|{editora}|{colecao}|{edicao}"

                           salvar_quadrinho(
        personagem,
        editora,
        colecao,
        edicao,
        file_id,
        nome_arquivo
    )

                           print("CATALOGADO:", chave)
                callback = update.get("callback_query")

                if callback:
                    callback_id = callback["id"]
                    dados = callback.get("data")
                    print("CALLBACK RECEBIDO:", dados, flush=True)
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

                        elif dados == "superman_abril":
                            editar_rich_message(
                                chat_id,
                                message_id,
                                menu_superman_abril()
                            )

                        elif dados == "super_homem":
                            editar_rich_message(
                                chat_id,
                                message_id,
                                menu_super_homem()
                            )
                        elif dados.startswith("super_homem_"): edicao = dados.replace("super_homem_", "", 1); file_id = buscar_file_id("Super-Homem", "Abril", "Super-Homem", edicao); enviar_documento(chat_id, file_id) if file_id else None
                        elif dados == "voltar_abril":
                            editar_rich_message(
                                chat_id,
                                message_id,
                                menu_superman_abril()
                            )

                        elif dados == "voltar_superman":
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
