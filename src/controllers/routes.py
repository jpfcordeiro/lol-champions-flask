from flask import redirect, render_template, request, url_for
import urllib
import json

rankings = {
    "Ahri": {"winrate": 52.3, "pickrate": 7.4, "banrate": 2.1},
    "Yasuo": {"winrate": 48.7, "pickrate": 15.2, "banrate": 30.5},
}

builds = []

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

url_patch = 'https://ddragon.leagueoflegends.com/api/versions.json'
response = urllib.request.urlopen(url_patch)
versions = json.loads(response.read())
latest_version = versions[0] if versions else None

def translate_game_modes(game_modes):
    """Traduz os modos de jogo recebidos da API para português."""
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
            rankings.update(form_data)
            return redirect(url_for('show_rankings'))
        return render_template('rankings.html', rankings=rankings)
    

    @app.route('/builds', methods=['GET', 'POST'])
    def show_builds():
        if request.method == 'POST':
            champion = request.form.get('champion')
            runes = request.form.get('runes').split(",") 
            items = request.form.get('items').split(",")

            #Estou usando para remover espaços em branco
            runes = [rune.strip() for rune in runes]
            items = [item.strip() for item in items]

            builds.append({"champion": champion, "runes": runes, "items": items})
            return redirect(url_for('show_builds')) 

        return render_template('builds.html', builds=builds)
    

    @app.route('/champions', methods=['GET', 'POST'])
    @app.route('/champions/<id>', methods=['GET', 'POST'])
    def list_champion(id=None):
        if latest_version:
            url_champions = f'https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/pt_BR/championFull.json'
            response = urllib.request.urlopen(url_champions)
            data = json.loads(response.read())['data']
        else:
            data = []
            
        if id:
            champ_id = None
            for champ in data.values():
                if champ['name'].lower() == id.lower():
                    champ_id = champ["id"]
                    break

            if champ_id:
                champinfo_url = f'https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/pt_BR/champion/{champ_id}.json'
                response = urllib.request.urlopen(champinfo_url)
                print(champinfo_url)
                champ_data = json.loads(response.read())['data'][champ_id]
                return render_template('championsinfo.html', champion=champ_data)
            else:
                return 'Campeão não encontrado!', 404
        return render_template('champions.html', champions=data)
    

    @app.route('/gamemodes', methods=['GET', 'POST'])
    def show_gamemodes():
        gamemode_url = 'https://static.developer.riotgames.com/docs/lol/gameModes.json'
        response = urllib.request.urlopen(gamemode_url)
        game_modes_api = json.loads(response.read())

        translated_modes = translate_game_modes(game_modes_api)

        print(translated_modes)

        return render_template('gamemodes.html', gamemodes=translated_modes)
    

    @app.route('/itens', methods=['GET', 'POST'])
    def show_itens():
        items_url = f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/pt_BR/item.json"
        response = urllib.request.urlopen(items_url)
        items_data = json.loads(response.read())["data"]

        return render_template('items.html', items=items_data)

