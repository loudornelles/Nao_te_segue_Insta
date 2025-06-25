import requests
import time
import json

# --- CONFIGURAÇÕES INICIAIS ---

# Como achar os cookies e o user_id:
# 1. Abra o Instagram no navegador e faça login.
# 2. Abre teu perfil (achei mais fácil por esse caminho, mas deve dar por outro, sla).
# 3. Clique com o botão direito e seleciona "Inspecionar", depois "Network".
# 4. Clica nos teus seguidores.
# 5. Na aba "Network", procura por uma requisição que começa com "followers/?count=12..."
# 6. Clica nela e vai na aba "Headers".
# 7. Na seção "Request Headers", você vai ver os cookies e o user_id, mas não é fácil de achar, tem que procurar.
# 8. O user_id é o número que aparece no cookie "ds_user_id".
# Eu copiei todo o header e colei num doc do Word pra conseguir dar um cntrl f, só lembra que pra colar no doc tem que usar ctrl + shift + v, senão cola com formatação e não dá pra procurar direito.

user_id = '98267364470'  # Substitua pelo seu ds_user_id

cookies = {
    'sessionid': '76780784470%3APTvfdru4yWruJ3%3A23%3AFFKDJNluOyl97JHYHTGMjAkr90XU8DHGRT56PJhhpWQ', # Substitua pelo seu sessionid
    'ds_user_id': user_id,
    'csrftoken': 'N0OLSKJYKJDHGRT56GEcXbJlphbinrHj', # Substitua pelo seu csrftoken
}

params = {
    'count': 12  # Eu vi que 12 é o que o Insta na web puxa por vez, então não quis arriscar mais pra não levar ban
}

# não precisa mexer daqui pra baixo, só rodar o código, espero que funcione, dizem que o insta muda o tempo todo.
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    'x-ig-app-id': '936619743392459', 
    'x-csrftoken': cookies['csrftoken'],
    'x-requested-with': 'XMLHttpRequest'
}


# Funções para coletar seguidores e seguidos 
def Followers():
    base_url = f'https://www.instagram.com/api/v1/friendships/{user_id}/followers/'
    print("Iniciando coleta de seguidores...")

    usernames = []
    next_max_id = None

    while True:
        if next_max_id:
            params['max_id'] = next_max_id

        response = requests.get(base_url, headers=headers, cookies=cookies, params=params)

        if response.status_code == 200:
            data = response.json()
            users = data.get('users', [])
            for user in users:
                usernames.append(user['username'])

            print(f"Coletados: {len(usernames)} seguidores ate agora...")

            next_max_id = data.get('next_max_id')
            if not next_max_id:
                print("Fim da lista.")
                break

            time.sleep(3)
        else:
            print(f"Erro {response.status_code}: {response.text}")
            break

    with open('usernames_seguidores.txt', 'w', encoding='utf-8') as f:
        for uname in usernames:
            f.write(f"{uname}\n")

    print("Exportacao de seguidores finalizada.")
    return usernames


def Following():
    base_url = f'https://www.instagram.com/api/v1/friendships/{user_id}/following/'
    print("Iniciando coleta de seguidos...")

    usernames = []
    next_max_id = None

    while True:
        if next_max_id:
            params['max_id'] = next_max_id

        response = requests.get(base_url, headers=headers, cookies=cookies, params=params)

        if response.status_code == 200:
            data = response.json()
            users = data.get('users', [])
            for user in users:
                usernames.append(user['username'])

            print(f"Coletados: {len(usernames)} seguidos ate agora...")

            next_max_id = data.get('next_max_id')
            if not next_max_id:
                print("Fim da lista.")
                break

            time.sleep(3)
        else:
            print(f"Erro {response.status_code}: {response.text}")
            break

    with open('usernames_seguindo.txt', 'w', encoding='utf-8') as f:
        for uname in usernames:
            f.write(f"{uname}\n")

    print("Exportacao de seguidos finalizada.")
    return usernames


def Compare():
    seguindo = set(Following())  # converter para set para fazer diferença
    seguidores = set(Followers())

    nao_te_segue = sorted(seguindo - seguidores)

    print(f"Total que você segue mas não te segue de volta: {len(nao_te_segue)}")
    for username in nao_te_segue:
        print(username)

    with open('nao_te_segue.txt', 'w', encoding='utf-8') as f:
        for username in nao_te_segue:
            f.write(f"{username}\n")

    print("Resultado salvo em nao_te_segue.txt")

if __name__ == "__main__":
    Compare()