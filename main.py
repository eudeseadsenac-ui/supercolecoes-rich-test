import os
import time
import requests

TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"
CANAL_PUBLICO = "@supercolecoes"
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
    

def enviar_menu_editora(chat_id, editora):
    url = f"{SUPABASE_URL}/quadrinhos_supercolecoes"

    params = {
        "editora": f"eq.{editora}",
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
        botoes.append({
            "text": personagem,
            "callback_data": f"editora|{personagem}|{editora}"
        })

    rich_message = {
        "blocks": [
            {
                "type": "heading",
                "text": f"📚 {editora.upper()}",
                "size": 2
            },
            {
                "type": "paragraph",
                "text": "Escolha um personagem ou coleção:"
            },
            {
                "type": "buttons",
                "buttons": botoes,
                "align": "center"
            }
        ]
    }

    payload = {
        "chat_id": chat_id,
        "rich_message": rich_message
    }

    resposta = requests.post(
        f"{BASE_URL}/sendRichMessage",
        json=payload,
        timeout=30
    )

    print("MENU EDITORA:", resposta.status_code, resposta.text, flush=True)
def publicar_menu_no_canal():
    payload = {
        "chat_id": CANAL_PUBLICO,
        "rich_message": menu_principal()
    }

    resposta = requests.post(
        f"{BASE_URL}/sendRichMessage",
        json=payload,
        timeout=30
    )

    print("PUBLICAR CANAL:", resposta.status_code, resposta.text, flush=True)
def publicar_catalogo_editoras():
    rich_message = {
        "blocks": [
            {
                "type": "heading",
                "text": "📚 CATÁLOGO POR EDITORAS",
                "size": 2
            },
            {
                "type": "paragraph",
                "text": "Organização das coleções e publicações por algumas das principais editoras de quadrinhos que marcaram a história do mercado brasileiro."
            },
            {
                "type": "paragraph",
                "text": "📕 EDITORA ABRIL\nUma das maiores editoras de quadrinhos do Brasil, responsável por décadas de publicações Disney, Marvel, DC, Star Wars, Turma da Mônica, Conan e muitos outros títulos."
            },
            {
                "type": "paragraph",
                "text": "📗 EBAL — EDITORA BRASIL-AMÉRICA\nPioneira na publicação de quadrinhos no Brasil. Publicou personagens e séries da DC Comics, Marvel, Tarzan, Flash Gordon, Príncipe Valente, Disney e inúmeros clássicos de aventura e super-heróis."
            },
            {
                "type": "paragraph",
                "text": "📘 BLOCH EDITORES\nFicou conhecida pelas revistas dos super-heróis Marvel nos anos 1970 e também por personagens como Zé Colmeia, Flintstones, Popeye, Jetsons e outros clássicos da Hanna-Barbera."
            },
            {
                "type": "paragraph",
                "text": "📙 RGE / EDITORA GLOBO\nA RGE, posteriormente incorporada à Editora Globo, publicou diversos personagens e coleções importantes, entre eles Fantasma, Mandrake, Recruta Zero e muitos outros."
            },
            {
                "type": "paragraph",
                "text": "📒 VECCHI / VEC\nPublicou quadrinhos de terror, faroeste e aventura, incluindo títulos como Kripta, Spektro, Sobrenatural e outras publicações marcantes."
            },
            {
                "type": "paragraph",
                "text": "📓 PANINI BRASIL\nUma das principais editoras atuais de quadrinhos no país. Publica Marvel, DC, Star Wars, Turma da Mônica, mangás e diversos outros títulos nacionais e internacionais."
            },
            {
                "type": "paragraph",
                "text": "📔 MYTHOS EDITORA\nConhecida principalmente pelas publicações de Tex, Zagor, Dylan Dog, Dampyr e outras séries de aventura, terror e faroeste."
            },
            {
                "type": "paragraph",
                "text": "📚 CONRAD / DEVIR / HQM\nEditoras responsáveis por importantes lançamentos de mangás, graphic novels, quadrinhos alternativos e obras independentes no mercado brasileiro."
            },
            {
                "type": "paragraph",
                "text": "📖 NONA ARTE / PIPOCA & NANQUIM\nEditoras voltadas para quadrinhos autorais, independentes, clássicos nacionais e internacionais e edições especiais."
            },
            {
                "type": "paragraph",
                "text": "📄 EDITORAS EXTINTAS OU RARAS\nEspaço dedicado a editoras como Taika, Graúna e outras que marcaram diferentes períodos da história dos quadrinhos no Brasil."
            },
                                    {
                "type": "buttons",
                "buttons": [
                    {
                        "text": "📕 Abril",
                        "url": "https://t.me/Supercolecoesdigitais_bot?start=abril"
                    },
                    {
                        "text": "📗 EBAL",
                        "url": "https://t.me/Supercolecoesdigitais_bot?start=ebal"
                    },
                    {
                        "text": "📘 Bloch",
                        "url": "https://t.me/Supercolecoesdigitais_bot?start=bloch"
                    },
                    {
                        "text": "📙 RGE / Globo",
                        "url": "https://t.me/Supercolecoesdigitais_bot?start=rge_globo"
                    },
                    {
                        "text": "📒 Vecchi",
                        "url": "https://t.me/Supercolecoesdigitais_bot?start=vecchi"
                    },
                    {
                        "text": "📓 Panini",
                        "url": "https://t.me/Supercolecoesdigitais_bot?start=panini"
                    },
                    {
                        "text": "📔 Mythos",
                        "url": "https://t.me/Supercolecoesdigitais_bot?start=mythos"
                    }
                ],
                "align": "center"
            }
        ]
    }

    payload = {
        "chat_id": CANAL_PUBLICO,
        "rich_message": rich_message
    }

    resposta = requests.post(
        f"{BASE_URL}/sendRichMessage",
        json=payload,
        timeout=30
    )

    print("CATALOGO EDITORAS:", resposta.status_code, resposta.text, flush=True)
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

                if mensagem and mensagem.get("text") == "/publicar":
                    chat_id = mensagem["chat"]["id"]

                    if chat_id == 735825670:
                        publicar_menu_no_canal()
                if mensagem and mensagem.get("text") == "/catalogo":
                    chat_id = mensagem["chat"]["id"]

                    if chat_id == 735825670:
                        publicar_catalogo_editoras()
                if mensagem and mensagem.get("text", "").startswith("/start "): parametro = mensagem.get("text", "").split(" ", 1)[1].strip().lower(); editoras_start = {"abril": "Abril", "ebal": "EBAL", "bloch": "Bloch", "rge_globo": "RGE / Globo", "vecchi": "Vecchi", "panini": "Panini", "mythos": "Mythos"}; editora = editoras_start.get(parametro); enviar_menu_editora(mensagem["chat"]["id"], editora) if editora else None
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

                        if dados.startswith("personagem|"):
                            personagem = dados.split("|", 1)[1]
                            editar_rich_message(chat_id, message_id, menu_editoras(personagem))

                        elif dados.startswith("editora|"):
                            _, personagem, editora = dados.split("|", 2)
                            editar_rich_message(chat_id, message_id, menu_colecoes(personagem, editora))

                        elif dados.startswith("colecao|"):
                            _, personagem, editora, colecao = dados.split("|", 3)
                            editar_rich_message(chat_id, message_id, menu_edicoes(personagem, editora, colecao))

                        elif dados.startswith("edicao|"):
                            _, personagem, editora, colecao, edicao = dados.split("|", 4)
                            file_id = buscar_file_id(personagem, editora, colecao, edicao)

                            if file_id:
                                enviar_documento(chat_id, file_id)
                            else:
                                print("ARQUIVO NÃO ENCONTRADO:", dados, flush=True)

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
