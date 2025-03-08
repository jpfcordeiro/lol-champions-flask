from flask import redirect, render_template, request, url_for
import urllib
import json

rankings = {
    "Ahri": {"winrate": 52.3, "pickrate": 7.4, "banrate": 2.1},
    "Yasuo": {"winrate": 48.7, "pickrate": 15.2, "banrate": 30.5},
}


roles = {
    'assassin': 'Assassino', 'fighter': 'Lutador', 'mage': 'Mago', 'marksman': 'Atirador', 'support': 'Suporte', 'tank': 'Tanque'
}

partypes = {
    'coragem': 'Coragem', 'furia': 'Fúria',
    'mana': 'Mana', 'energia': 'Energia',
    'deaquecimento': 'Aquecimento', 'nenhum': 'Nenhum',
    'escudo': 'Escudo', 'ferocidade': 'Ferocidade',
    'fluxo': 'Fluxo', 'impetovermelho': 'Ímpeto Vermelho',
    'ousadia': 'Ousadia', 'pocodesangue': 'Poço de Sangue',
}

game_modes_translation = {
    "CLASSIC": "Modo Clássico (Summoner's Rift e Twisted Treeline)",
    "ODIN": "Domínio/Cristal Escarlate",
    "ARAM": "ARAM (Todos Aleatórios, Uma Rota)",
    "TUTORIAL": "Modo Tutorial",
    "URF": "URF (Ultra Rápido e Furioso)",
    "DOOMBOTSTEEMO": "Bots da Perdição",
    "ONEFORALL": "Um Por Todos",
    "ASCENSION": "Ascensão",
    "FIRSTBLOOD": "Duelo de Sangue (Snowdown Showdown)",
    "KINGPORO": "Lenda do Rei Poro",
    "SIEGE": "Cerco ao Nexus",
    "ASSASSINATE": "Caçada Sangrenta",
    "ARSR": "Todos Aleatórios em Summoner's Rift",
    "DARKSTAR": "Estrela Negra: Singularidade",
    "STARGUARDIAN": "Invasão das Guardiãs Estelares",
    "PROJECT": "PROJETO: Caçadores",
    "GAMEMODEX": "Blitz do Nexus",
    "ODYSSEY": "Odisseia: Extração",
    "NEXUSBLITZ": "Blitz do Nexus",
    "ULTBOOK": "Livro Supremo de Feitiços"
}

data = {}
builds = [{'champion': 'Ahri', 'runes': 'Inspiração', 'items_selected': ['A Espátula Dourada', 'Abraço Demoníaco']}]


url_patch = 'https://ddragon.leagueoflegends.com/api/versions.json'
response = urllib.request.urlopen(url_patch)
versions = json.loads(response.read())
latest_version = versions[0] if versions else None


if latest_version:
    url_champions = f'https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/pt_BR/championFull.json'
    response = urllib.request.urlopen(url_champions)
    champion_data = json.loads(response.read())['data']
    
    data = {}
    for champ_key, champ_info in champion_data.items():
        champ_info['image_url'] = f'https://ddragon.leagueoflegends.com/cdn/{latest_version}/img/champion/{champ_info["image"]["full"]}'
        data[champ_key] = champ_info
        
    items_url = f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/pt_BR/item.json"
    response = urllib.request.urlopen(items_url)
    items_data = json.loads(response.read())["data"]
    

def translate_game_modes(game_modes):
    return [
        {
            "gameMode": mode["gameMode"],
            "description": game_modes_translation.get(mode["gameMode"], mode["description"])
        }
        for mode in game_modes
    ]


def init_app(app):
    
    
    @app.route('/')
    def home():
        return render_template('index.html')


    @app.route('/rankings', methods=['GET', 'POST'])
    def show_rankings():
        if request.method == 'POST':
            form_data = request.form.to_dict()

            champion = form_data.get('champion')
            winrate = form_data.get('winrate')
            pickrate = form_data.get('pickrate')
            banrate = form_data.get('banrate')

            if champion and winrate and pickrate and banrate:
                winrate = float(winrate)
                pickrate = float(pickrate)
                banrate = float(banrate)

                rankings[champion] = {
                    'winrate': winrate,
                    'pickrate': pickrate,
                    'banrate': banrate
                }

                return redirect(url_for('show_rankings'))

        return render_template('rankings.html', rankings=rankings, champions=data)


    @app.route('/builds', methods=['GET', 'POST'])
    def show_builds():
        global builds #tive que usar pois estava com problema de unbound
        if latest_version:
            try:
                url_runas = f'https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/pt_BR/runesReforged.json'
                response = urllib.request.urlopen(url_runas)
                runas_data = json.loads(response.read())
            except urllib.error.URLError as e:
                return f"Erro ao carregar dados das runas: {e}", 500
            
            if isinstance(items_data, dict):
                items_filtered = [item for item in items_data.values() if item.get("depth") == 3]
                items_sorted = sorted(items_filtered, key=lambda item: item["name"])
                seen = set()
                items_unique = []
                for item in items_sorted:
                    if item["name"] not in seen:
                        items_unique.append(item)
                        seen.add(item["name"])
                        
            else:
                items_unique = []
            
            if request.method == 'POST':
                champion = request.form.get('champion')
                main_rune = request.form.get('mainrune')
                items_slc = request.form.getlist('items-select')
                
                if champion and main_rune and items_slc:
                    builds.append({"champion": champion, "runes": main_rune, "items_selected": items_slc})
                    return redirect(url_for('show_builds'))
        return render_template('builds.html', builds=builds, champions=data, runas=runas_data, latest_version=latest_version, items=items_unique)



    @app.route('/champions', methods=['GET'])
    @app.route('/champions/<id>', methods=['GET'])
    def list_champion(id=None):
        if id:
            champ_id = next((champ["id"] for champ in data.values() if champ['name'].lower() == id.lower()), None)
            if champ_id:
                champinfo_url = f'https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/pt_BR/champion/{champ_id}.json'
                response = urllib.request.urlopen(champinfo_url)
                champ_data = json.loads(response.read())['data'][champ_id]
                return render_template('championsinfo.html', champion=champ_data)
            return 'Campeão não encontrado!', 404
        return render_template('champions.html', champions=data, roles=roles, partypes=partypes)


    @app.route('/gamemodes', methods=['GET'])
    def show_gamemodes():
        gamemode_url = 'https://static.developer.riotgames.com/docs/lol/gameModes.json'
        response = urllib.request.urlopen(gamemode_url)
        game_modes_api = json.loads(response.read())
        translated_modes = translate_game_modes(game_modes_api)
        gamemodes_sorted = sorted(translated_modes, key=lambda x: x['gameMode'])
        return render_template('gamemodes.html', gamemodes=gamemodes_sorted)


    @app.route('/itens', methods=['GET'])
    def show_itens():
        items_filtered = [item for item in items_data.values() if item.get("depth") == 3]
        items_sorted = sorted(items_filtered, key=lambda item: item["name"])
        seen = set()
        items_unique = []
        for item in items_sorted:
            if item["name"] not in seen:
                items_unique.append(item)
                seen.add(item["name"])
        return render_template('items.html', items=items_unique, latest_version=latest_version)
