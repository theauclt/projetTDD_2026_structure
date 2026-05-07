from collections import defaultdict


class ServiceStatistiques:
    """
    Service responsable de l'analyse et de la manipulation des données.
    Fonctionne indépendamment du sport grâce aux modèles génériques.
    """

    def __init__(self):
        self.matchs = []
        # defaultdict initialise automatiquement les stats à 0
        # pour une équipe ou un joueur dès qu'on le rencontre.
        self.stats = defaultdict(
            lambda: {
                "joues": 0,
                "victoires": 0,
                "defaites": 0,
                "nuls": 0,
                "points_marques": 0,
            }
        )

    def charger_matchs(self, liste_matchs):
        """Charge un historique complet de matchs et met à jour les statistiques."""
        for match in liste_matchs:
            self.ajouter_match(match)

    def ajouter_match(self, match):
        """Ajoute un nouveau match et met à jour les caractéristiques en temps réel."""
        self.matchs.append(match)

        # 1. Mise à jour des matchs joués
        self.stats[match.equipe1]["joues"] += 1
        self.stats[match.equipe2]["joues"] += 1

        # 2. Mise à jour des points marqués (ou buts, ou sets)
        self.stats[match.equipe1]["points_marques"] += match.score1
        self.stats[match.equipe2]["points_marques"] += match.score2

        # 3. Détermination du gagnant et mise à jour du palmarès
        if match.score1 > match.score2:
            self.stats[match.equipe1]["victoires"] += 1
            self.stats[match.equipe2]["defaites"] += 1
        elif match.score2 > match.score1:
            self.stats[match.equipe2]["victoires"] += 1
            self.stats[match.equipe1]["defaites"] += 1
        else:
            self.stats[match.equipe1]["nuls"] += 1
            self.stats[match.equipe2]["nuls"] += 1

    def obtenir_classement_global(self):
        """
        Génère un classement global trié.
        Critère 1 : Nombre de victoires
        Critère 2 : Nombre de points marqués
        """
        classement = sorted(
            self.stats.items(),
            key=lambda item: (item[1]["victoires"], item[1]["points_marques"]),
            reverse=True,  # Ordre décroissant (du meilleur au pire)
        )
        return classement

    def obtenir_stats_entite(self, nom_entite):
        """Récupère les statistiques détaillées d'une équipe ou d'un joueur."""
        if nom_entite in self.stats:
            return self.stats[nom_entite]
        return None

    # --- MÉTHODES DE MANIPULATION COMPLEXES ---

    def obtenir_historique_equipe(self, nom_equipe):
        """Filtre la base de matchs pour ressortir l'historique d'une équipe."""
        return [match for match in self.matchs if match.implique_equipe(nom_equipe)]

    def calculer_classement_championnat(self, pts_victoire=3, pts_nul=1, pts_defaite=0):
        """
        Calcule le classement générique d'un tournoi (type championnat).
        Retourne un dictionnaire complexe avec toutes les stats agrégées.
        """
        # pm = points marqués, pe = points encaissés, diff = différence
        classement = defaultdict(
            lambda: {
                "joues": 0,
                "points": 0,
                "victoires": 0,
                "nuls": 0,
                "defaites": 0,
                "pm": 0,
                "pe": 0,
                "diff": 0,
            }
        )

        for match in self.matchs:
            eq1, eq2 = match.equipe1, match.equipe2

            classement[eq1]["joues"] += 1
            classement[eq2]["joues"] += 1

            # Utilisation des méthodes de la classe Match
            classement[eq1]["pm"] += match.obtenir_points_pour(eq1)
            classement[eq1]["pe"] += match.obtenir_points_contre(eq1)
            classement[eq2]["pm"] += match.obtenir_points_pour(eq2)
            classement[eq2]["pe"] += match.obtenir_points_contre(eq2)

            vainqueur = match.vainqueur()
            if vainqueur == eq1:
                classement[eq1]["victoires"] += 1
                classement[eq1]["points"] += pts_victoire
                classement[eq2]["defaites"] += 1
                classement[eq2]["points"] += pts_defaite
            elif vainqueur == eq2:
                classement[eq2]["victoires"] += 1
                classement[eq2]["points"] += pts_victoire
                classement[eq1]["defaites"] += 1
                classement[eq1]["points"] += pts_defaite
            else:
                classement[eq1]["nuls"] += 1
                classement[eq2]["nuls"] += 1
                classement[eq1]["points"] += pts_nul
                classement[eq2]["points"] += pts_nul

        # Calcul de la différence de points finale
        for equipe, stats in classement.items():
            stats["diff"] = stats["pm"] - stats["pe"]

        # Tri : Points > Différence > Points marqués
        return sorted(
            classement.items(),
            key=lambda x: (x[1]["points"], x[1]["diff"], x[1]["pm"]),
            reverse=True,
        )


class ServiceStatistiquesBasket(ServiceStatistiques):
    """Service spécialisé pour traiter les statistiques complexes de la NBA par phase."""

    def __init__(self):
        super().__init__()

        # 1. NOUVEAU : Un dictionnaire à deux niveaux (Phase -> Equipe -> Stats)
        self.stats_par_phase = defaultdict(
            lambda: defaultdict(
                lambda: {
                    "matchs_joues": 0,
                    "victoires": 0,
                    "defaites": 0,  # <-- Ajout des victoires ici pour le classement
                    "points_marques": 0,
                    "points_encaisses": 0,
                    "rebonds": 0,
                    "passes": 0,
                    "interceptions": 0,
                    "contres": 0,
                    "fg2m": 0,
                    "fg2a": 0,  # 2 points (réussis / tentés)
                    "fg3m": 0,
                    "fg3a": 0,  # 3 points
                    "ftm": 0,
                    "fta": 0,  # Lancers francs
                }
            )
        )

    def charger_matchs(self, matchs):
        super().charger_matchs(matchs)

        for match in matchs:
            # 2. NOUVEAU : On récupère la phase depuis le "sac à dos"
            phase = match.stats.get("type_match", "Regular Season")

            # === STATS POUR L'ÉQUIPE À DOMICILE (Equipe 1) ===
            d_home = self.stats_par_phase[phase][
                match.equipe1
            ]  # On ouvre le bon tiroir
            d_home["matchs_joues"] += 1
            d_home["points_marques"] += match.score1
            d_home["points_encaisses"] += match.score2

            # Calcul des victoires/défaites pour le classement de cette phase
            if match.score1 > match.score2:
                d_home["victoires"] += 1
            else:
                d_home["defaites"] += 1

            d_home["rebonds"] += float(match.stats.get("reb_home", 0))
            d_home["passes"] += float(match.stats.get("ast_home", 0))
            d_home["interceptions"] += float(match.stats.get("stl_home", 0))
            d_home["contres"] += float(match.stats.get("blk_home", 0))

            fgm_h = float(match.stats.get("fgm_home", 0))
            fga_h = float(match.stats.get("fga_home", 0))
            fg3m_h = float(match.stats.get("fg3m_home", 0))
            fg3a_h = float(match.stats.get("fg3a_home", 0))

            d_home["fg3m"] += fg3m_h
            d_home["fg3a"] += fg3a_h
            d_home["fg2m"] += fgm_h - fg3m_h
            d_home["fg2a"] += fga_h - fg3a_h
            d_home["ftm"] += float(match.stats.get("ftm_home", 0))
            d_home["fta"] += float(match.stats.get("fta_home", 0))

            # === STATS POUR L'ÉQUIPE À L'EXTÉRIEUR (Equipe 2) ===
            d_away = self.stats_par_phase[phase][
                match.equipe2
            ]  # On ouvre le bon tiroir
            d_away["matchs_joues"] += 1
            d_away["points_marques"] += match.score2
            d_away["points_encaisses"] += match.score1

            # Calcul des victoires/défaites pour l'extérieur
            if match.score2 > match.score1:
                d_away["victoires"] += 1
            else:
                d_away["defaites"] += 1

            d_away["rebonds"] += float(match.stats.get("reb_away", 0))
            d_away["passes"] += float(match.stats.get("ast_away", 0))
            d_away["interceptions"] += float(match.stats.get("stl_away", 0))
            d_away["contres"] += float(match.stats.get("blk_away", 0))

            fgm_a = float(match.stats.get("fgm_away", 0))
            fga_a = float(match.stats.get("fga_away", 0))
            fg3m_a = float(match.stats.get("fg3m_away", 0))
            fg3a_a = float(match.stats.get("fg3a_away", 0))

            d_away["fg3m"] += fg3m_a
            d_away["fg3a"] += fg3a_a
            d_away["fg2m"] += fgm_a - fg3m_a
            d_away["fg2a"] += fga_a - fg3a_a
            d_away["ftm"] += float(match.stats.get("ftm_away", 0))
            d_away["fta"] += float(match.stats.get("fta_away", 0))

    # 3. NOUVEAU : On redéfinit obtenir_classement_global pour inclure le paramètre "phase"
    def obtenir_classement_global(self, phase="Regular Season"):
        """Retourne le classement trié par victoires pour une phase spécifique."""
        stats_phase = self.stats_par_phase.get(phase, {})
        # On trie selon la clé 'victoires' en ordre décroissant (reverse=True)
        return sorted(
            stats_phase.items(), key=lambda x: x[1]["victoires"], reverse=True
        )

    # 4. MODIFIÉ : On ajoute le paramètre "phase"
    def obtenir_moyennes(self, equipe_id, phase="Regular Season"):
        """Calcule et retourne les moyennes par match pour une équipe selon la phase."""
        stats_phase = self.stats_par_phase.get(phase, {})
        s = stats_phase.get(equipe_id)

        if not s or s["matchs_joues"] == 0:
            return None

        m = s["matchs_joues"]

        def pct(reussis, tentes):
            return round((reussis / tentes) * 100, 1) if tentes > 0 else 0.0

        return {
            "pts_pour": round(s["points_marques"] / m, 1),
            "pts_contre": round(s["points_encaisses"] / m, 1),
            "rebonds": round(s["rebonds"] / m, 1),
            "passes": round(s["passes"] / m, 1),
            "interceptions": round(s["interceptions"] / m, 1),
            "contres": round(s["contres"] / m, 1),
            "pct_2pts": pct(s["fg2m"], s["fg2a"]),
            "pct_3pts": pct(s["fg3m"], s["fg3a"]),
            "pct_lf": pct(s["ftm"], s["fta"]),
        }


class ServiceStatistiquesTennis(ServiceStatistiques):

    def __init__(self):
        super().__init__()
        # On ajoute les nouvelles statistiques dans le dictionnaire de base
        self.stats_joueurs = defaultdict(
            lambda: {
                "matchs_joues": 0,
                "victoires": 0,
                "defaites": 0,
                "total_aces": 0,
                "total_df": 0,
                "total_minutes": 0,
                "bp_sauvees": 0,
                "bp_concedees": 0,  # Défense (sur son service)
                "bp_converties": 0,
                "bp_obtenues": 0,  # Attaque (sur le service adverse)
                "palmares": [],  # Liste des tournois gagnés
            }
        )

    def nettoyer_valeur(self, valeur):
        try:
            return float(valeur) if valeur and str(valeur).lower() != "nan" else 0.0
        except ValueError:
            return 0.0

    def charger_matchs(self, matchs):
        for match in matchs:
            id_vainqueur = str(match.equipe1).replace(".0", "")
            id_perdant = str(match.equipe2).replace(".0", "")

            v = self.stats_joueurs[id_vainqueur]  # Vainqueur
            p = self.stats_joueurs[id_perdant]  # Perdant

            # --- PALMARÈS (Si c'est une Finale 'F', le vainqueur gagne le tournoi) ---
            if str(match.stats.get("round")) == "F":
                nom_tournoi = str(match.stats.get("tourney_name", "Tournoi"))
                v["palmares"].append(nom_tournoi)

            # --- STATS DU VAINQUEUR ---
            v["matchs_joues"] += 1
            v["victoires"] += 1
            v["total_aces"] += self.nettoyer_valeur(match.stats.get("w_ace", 0))
            v["total_df"] += self.nettoyer_valeur(match.stats.get("w_df", 0))
            v["total_minutes"] += self.nettoyer_valeur(match.stats.get("minutes", 0))

            # Balles de break sauvées par le vainqueur
            v["bp_sauvees"] += self.nettoyer_valeur(match.stats.get("w_bpSaved", 0))
            v["bp_concedees"] += self.nettoyer_valeur(match.stats.get("w_bpFaced", 0))
            # Balles de break converties (Balles affrontées par le perdant - Balles sauvées par le perdant)
            bp_faced_by_loser = self.nettoyer_valeur(match.stats.get("l_bpFaced", 0))
            bp_saved_by_loser = self.nettoyer_valeur(match.stats.get("l_bpSaved", 0))
            v["bp_obtenues"] += bp_faced_by_loser
            v["bp_converties"] += bp_faced_by_loser - bp_saved_by_loser

            # --- STATS DU PERDANT ---
            p["matchs_joues"] += 1
            p["defaites"] += 1
            p["total_aces"] += self.nettoyer_valeur(match.stats.get("l_ace", 0))
            p["total_df"] += self.nettoyer_valeur(match.stats.get("l_df", 0))
            p["total_minutes"] += self.nettoyer_valeur(match.stats.get("minutes", 0))

            # Balles de break sauvées par le perdant
            p["bp_sauvees"] += bp_saved_by_loser
            p["bp_concedees"] += bp_faced_by_loser
            # Balles de break converties par le perdant
            bp_faced_by_winner = self.nettoyer_valeur(match.stats.get("w_bpFaced", 0))
            bp_saved_by_winner = self.nettoyer_valeur(match.stats.get("w_bpSaved", 0))
            p["bp_obtenues"] += bp_faced_by_winner
            p["bp_converties"] += bp_faced_by_winner - bp_saved_by_winner

    def obtenir_moyennes_joueur(self, joueur_id):
        s = self.stats_joueurs.get(str(joueur_id))
        if not s or s["matchs_joues"] == 0:
            return None

        m = s["matchs_joues"]
        return {
            "victoires": s["victoires"],
            "defaites": s["defaites"],
            "aces_par_match": round(s["total_aces"] / m, 1),
            "df_par_match": round(s["total_df"] / m, 1),
            "minutes_moyennes": round(s["total_minutes"] / m, 1),
            # On passe les données brutes pour l'affichage (pas besoin de moyenne ici)
            "bp_sauvees": int(s["bp_sauvees"]),
            "bp_concedees": int(s["bp_concedees"]),
            "bp_converties": int(s["bp_converties"]),
            "bp_obtenues": int(s["bp_obtenues"]),
            "palmares": s["palmares"],
        }
