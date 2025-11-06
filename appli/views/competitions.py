from flask import render_template

from appli.app import app
from appli.models import ChampionnatIndividuel, ChampionnatEquipe, 


@app.route('/competitions/calendrier/')
def calendrier():
    list_comp_indiv = ChampionnatIndividuel.query.order_by(ChampionnatIndividuel.date_comp.desc()).all()
    list_comp_equipe = ChampionnatEquipe.query.order_by(ChampionnatEquipe.date_comp.desc()).all()
    return render_template('calendrier.html', title="Calendrier - Compétitions", comp_indiv=list_comp_indiv, comp_equipe=list_comp_equipe)

@app.route('/competitions/palmares/')
def palmares():
    return render_template('palmares.html', title="Palmarès - Competitions")


@app.route('/competitions/tournoi/<type_tournoi>/<int:idC>/')
def tournoi(type_tournoi: str, idC: int):
    if type_tournoi == "individuel":
        champ = ChampionnatIndividuel.query.get(idC)
        liste_stades = {}
        liste_dates = {}
        donnees = {}
    else:
        champ = ChampionnatEquipe.query.get(idC)
        liste_stades = {}
        liste_dates = {}
        donnees = {}
        for participant in champ.participer:
            id_equipe = participant.equipe.id
            donnees[id_equipe] = {}
            liste_stades[id_equipe] = []
            liste_dates[id_equipe] = []
            for match in Affronter.query.filter(Affronter.championnat == champ,
                                                Affronter.equipe == participant.equipe):
                if match.date_match not in donnees[id_equipe]:
                    donnees[id_equipe][match.date_match] = {match.stade : match}
                    if match.stade not in liste_stades[id_equipe]:
                        liste_stades[id_equipe].append(match.stade)
                    if match.date_match not in liste_dates[id_equipe]:
                        liste_dates[id_equipe].append(match.date_match)
                elif match.stade not in donnees[id_equipe][match.date_match]:
                    donnees[id_equipe][match.date_match][match.stade] = match
                    if match.stade not in liste_stades[id_equipe]:
                        liste_stades[id_equipe].append(match.stade)
            for date_match in liste_dates[id_equipe]:
                for stade in liste_stades[id_equipe]:
                    donnees[id_equipe][date_match].setdefault(stade, None)
            liste_stades[id_equipe].sort()
            liste_dates[id_equipe].sort()
    return render_template('tournoi.html', title="Tournoi - Competitions", championnat=champ,
                           type_champ=type_tournoi, matchs=donnees, stades=liste_stades,
                           dates=liste_dates)

@app.route('/competitions/tournois-internes/')
def internes():
    return render_template('internes.html', title="Tournois internes - Competitions")
