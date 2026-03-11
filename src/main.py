from graph import *

# --- Création des gares ---
belfort = Gare("Belfort", 0.0, 0.0)
stop = Gare("Stop", -1.2, 5)
montreVieux = Gare("Montre-Vieux", 1.3, 1.5)
dannemarie = Gare("Dannemarie", 0.2, 2.1)
altkirch = Gare("Altkirch", 1, 3.0)
dornach = Gare("Dornach", 1.6, 5)
mulhouse = Gare("Mulhouse", 2.4, 4.6)
wittelsheim = Gare("Wittelsheim", 1, 5.5)
than = Gare("Than", 0.3, 5.8)
bale = Gare("Bâle", 3, 3.6)
colmar = Gare("Colmar", 3.6, 7.5)
selestat = Gare("Sélestat", 3.9, 9.0)
molsheim = Gare("Molsheim", 4.5, 11.4)
strasbourg = Gare("Strasbourg", 4.8, 13.5)
zurich = Gare("Zurich", 7.5, 1.5)

gares = [belfort, stop, montreVieux, dannemarie, altkirch, dornach,
         mulhouse, wittelsheim, than, bale, colmar, selestat,
         molsheim, strasbourg, zurich]

gares_triees = sorted(gares, key=lambda g: g.nom) # trier pour les listes déroulantes

# --- Initialisation du réseau ---
reseau = ReseauFerroviaire()
for g in gares_triees:
    reseau.ajouter_gare(g)

# --- Liaisons Vallée de Than ---
reseau.ajouter_liaison(than, wittelsheim, 5, 1, "Vallée de Than", "TER")
reseau.ajouter_liaison(wittelsheim, dornach, 5, 1, "Vallée de than", "TER")
reseau.ajouter_liaison(dornach, mulhouse, 5, 1, "Vallée de than", "TER")

# --- Liaisons TER Belfort → Mulhouse ---
reseau.ajouter_liaison(belfort, mulhouse, 20, 16, "Express Belfort-Mulhouse", "TER")

reseau.ajouter_liaison(belfort, montreVieux, 15, 4, "TER Belfor-Mulhouse", "TER")
reseau.ajouter_liaison(montreVieux, dannemarie, 10, 3, "TER Belfort-Mulhouse", "TER")
reseau.ajouter_liaison(dannemarie, altkirch, 10, 3, "TER Belfort-Mulhouse", "TER")
reseau.ajouter_liaison(altkirch, mulhouse, 10, 3, "TER Belfort-Mulhouse", "TER")

# --- Liaisons TER Mulhouse → Colmar → Strasbourg ---
reseau.ajouter_liaison(mulhouse, colmar, 30, 8, "TER Alsace", "TER")
reseau.ajouter_liaison(colmar, selestat, 20, 6, "TER Alsace", "TER")
reseau.ajouter_liaison(selestat, molsheim, 25, 7, "TER Alsace", "TER")
reseau.ajouter_liaison(molsheim, strasbourg, 20, 7, "TER Alsace", "TER")

# --- Liaisons TGV ---
reseau.ajouter_liaison(molsheim, strasbourg, 10, 14, "TGV Alsace", "TGV")
reseau.ajouter_liaison(selestat, molsheim, 10, 14, "TGV Alsace", "TGV")
reseau.ajouter_liaison(colmar, selestat, 10, 12, "TGV Alsace", "TGV")
reseau.ajouter_liaison(mulhouse, colmar, 10, 12, "TGV Alsace", "TGV")

reseau.ajouter_liaison(belfort, stop, 15, 10, "TGV Est", "TGV")
reseau.ajouter_liaison(stop, strasbourg, 15, 10, "TGV Est", "TGV")

# --- Liaisons internationales ---
reseau.ajouter_liaison(mulhouse, bale, 10, 5, "TER Alsace", "TER")

reseau.ajouter_liaison(mulhouse, bale, 5, 10, "TGV Est/International", "TGV")
reseau.ajouter_liaison(bale, zurich, 90, 45, "TGV Est/International", "TGV")



def afficherTrajet(trajet, segments, afficher_lignes=True, afficher_details=True, afficher_total=True):
    chemin_str = " -> ".join(g.nom for g in trajet)
    print("Trajet :", chemin_str)

    if afficher_lignes:
        lignes = set((seg["ligne"], seg["type_train"]) for seg in segments)
        print("\nLignes utilisées :")
        for ligne, type_train in sorted(lignes):
            print(f"  {ligne} ({type_train})")

    if afficher_details:
        print("\nDétail par segment :")
        for seg in segments:
            print(
                f"  {seg['depart']} -> {seg['arrivee']} : "
                f"{seg['temps']} min, {seg['prix']} €, "
                f"Ligne : {seg['ligne']} ({seg['type_train']})"
            )

    if afficher_total:
        total_temps = sum(seg["temps"] for seg in segments)
        total_prix = sum(seg["prix"] for seg in segments)
        print("\nTotal :")
        print(f"  Temps : {total_temps} min")
        print(f"  Prix  : {total_prix} €")


def afficherMeilleurTrajets(resultats, depart, arrivee):

    titre = f"\nRésultat pour : {depart.nom} --> {arrivee.nom}\n"
    print(titre)

    print("Le plus rapide :")
    afficherTrajet(resultats[0][0], resultats[0][2])

    print("\nLe moins cher :")
    afficherTrajet(resultats[1][0], resultats[1][2])


def afficherToutLesTrajets(trajets):

    for trajet in trajets:

        if trajet[0] is not None:

            print("\n" + "=" * 60)
            afficherTrajet(trajet[0], trajet[2])
            print("=" * 60)


# TEST
'''
print("\n")

res = reseau.tout_trajets(belfort, mulhouse)

afficherToutLesTrajets(res)
'''