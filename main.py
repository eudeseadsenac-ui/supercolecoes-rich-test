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
    url = f"{SUPABASE_URL}/quadrinhos_supercolecoes"

    params = {
        "select": "personagem"
    }

    resposta = requests.get(
        url,
        headers=SUPABASE_HEADERS,
        params=params,
        timeout=30
    )

    personagens = []

    if resposta.ok:
        dados = resposta.json()

        for item in dados:
            personagem = str(item["personagem"])

            if personagem not in personagens:
                personagens.append(personagem)

    personagens.sort()

    botoes = []

    for personagem in personagens:

        callback = f"personagem|{personagem}"

        botoes.append({
            "text": personagem,
            "callback_data": callback
        })

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
                "buttons": botoes,
                "align": "center"
            }
        ]
    }
def menu_editoras(personagem):
    url = f"{SUPABASE_URL}/quadrinhos_supercolecoes"

    params = {
        "personagem": f"eq.{personagem}",
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
        botoes.append({
            "text": editora,
            "callback_data": f"editora|{personagem}|{editora}"
        })

    return {
        "blocks": [
            {
                "type": "heading",
                "text": f"📚 {personagem.upper()}",
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
def menu_colecoes(personagem, editora):
    url = f"{SUPABASE_URL}/quadrinhos_supercolecoes"

    params = {
        "personagem": f"eq.{personagem}",
        "editora": f"eq.{editora}",
        "select": "colecao"
    }

    resposta = requests.get(
        url,
        headers=SUPABASE_HEADERS,
        params=params,
        timeout=30
    )

    colecoes = []

    if resposta.ok:
        dados = resposta.json()

        for item in dados:
            colecao = str(item["colecao"])

            if colecao not in colecoes:
                colecoes.append(colecao)

    colecoes.sort()

    botoes = []

    for colecao in colecoes:
        botoes.append({
            "text": colecao,
            "callback_data": f"colecao|{personagem}|{editora}|{colecao}"
        })

    return {
        "blocks": [
            {
                "type": "heading",
                "text": f"📚 {personagem.upper()} — {editora.upper()}",
                "size": 2
            },
            {
                "type": "paragraph",
                "text": "Escolha uma coleção:"
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
                        "callback_data": f"personagem|{personagem}"
                    }
                ],
                "align": "center"
            }
        ]
    }





    
def menu_edicoes(personagem, editora, colecao):
    url = f"{SUPABASE_URL}/quadrinhos_supercolecoes"

    params = {
        "personagem": f"eq.{personagem}",
        "editora": f"eq.{editora}",
        "colecao": f"eq.{colecao}",
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
            "callback_data": f"edicao|{personagem}|{editora}|{colecao}|{edicao}"
        })

    return {
        "blocks": [
            {
                "type": "heading",
                "text": f"📚 {colecao.upper()} — {editora.upper()}",
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
                        "callback_data": f"editora|{personagem}|{editora}"
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

                        if dados.startswith("personagem|"): personagem = dados.split("|", 1)[1]; editar_rich_message(chat_id, message_id, menu_editoras(personagem))
                        elif dados.startswith("editora|"): _, personagem, editora = dados.split("|", 2); editar_rich_message(chat_id, message_id, menu_colecoes(personagem, editora))
                        elif dados.startswith("colecao|"): _, personagem, editora, colecao = dados.split("|", 3); editar_rich_message(chat_id, message_id, menu_edicoes(personagem, editora, colecao))
                        elif dados.startswith("edicao|"): _, personagem, editora, colecao, edicao = dados.split("|", 4); file_id = buscar_file_id(personagem, editora, colecao, edicao); enviar_documento(chat_id, file_id) if file_id else print("ARQUIVO NÃO ENCONTRADO:", dados, flush=True)
                        

                        
                            

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
