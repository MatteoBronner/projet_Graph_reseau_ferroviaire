import networkx as nx


class Gare:
    def __init__(self, nom: str, x: float, y: float):
        self.nom = nom
        self.x = x
        self.y = y

    def __str__(self):
        return self.nom

    def __repr__(self):
        return f"Gare({self.nom})"

    def __eq__(self, other):
        return isinstance(other, Gare) and self.nom == other.nom

    def __hash__(self):
        return hash(self.nom)


class ReseauFerroviaire:
    def __init__(self):
        # MultiGraph = plusieurs liaisons entre deux gares
        self.graph = nx.MultiGraph()

    def ajouter_gare(self, gare):
        self.graph.add_node(gare)

    def ajouter_liaison(self, depart, arrivee, temps, prix, ligne, type_train):
        self.graph.add_edge(
            depart,
            arrivee,
            temps=temps,
            prix=prix,
            ligne=ligne,
            type_train=type_train
        )

    def plus_court_chemin(self, depart, arrivee, critere="temps", type_train=None):

        # --- Filtrage du graphe ---
        if type_train is None:
            graph_filtre = self.graph
        else:
            graph_filtre = nx.MultiGraph()
            graph_filtre.add_nodes_from(self.graph.nodes())

            for u, v, key, data in self.graph.edges(keys=True, data=True):
                if data["type_train"] == type_train:
                    graph_filtre.add_edge(u, v, **data)

        # --- Calcul Dijkstra ---
        chemin = nx.dijkstra_path(
            graph_filtre,
            source=depart,
            target=arrivee,
            weight=critere
        )

        total = nx.dijkstra_path_length(
            graph_filtre,
            source=depart,
            target=arrivee,
            weight=critere
        )

        # --- Reconstruction des segments ---
        segments = []

        for i in range(len(chemin) - 1):
            u = chemin[i]
            v = chemin[i + 1]

            edges = graph_filtre.get_edge_data(u, v)

            # si type_train demandé → on force ce type
            if type_train is not None:
                meilleure_arete = next(
                    e for e in edges.values()
                    if e["type_train"] == type_train
                )
            else:
                meilleure_arete = min(
                    edges.values(),
                    key=lambda d: d[critere]
                )

            segments.append({
                "depart": u.nom,
                "arrivee": v.nom,
                "temps": meilleure_arete["temps"],
                "prix": meilleure_arete["prix"],
                "ligne": meilleure_arete["ligne"],
                "type_train": meilleure_arete["type_train"]
            })

        return chemin, total, segments

    def meilleurs_trajets(self, depart, arrivee):

        trajets = []

        for type_train in ["TER", "TGV"]:
            for critere in ["temps", "prix"]:
                try:
                    chemin, total, segments = self.plus_court_chemin(
                        depart,
                        arrivee,
                        critere=critere,
                        type_train=type_train
                    )
                    trajets.append((chemin, total, segments))

                except nx.NetworkXNoPath:
                    continue

        if not trajets:
            return []

        plus_rapide = min(
            trajets,
            key=lambda t: sum(seg["temps"] for seg in t[2])
        )

        moins_cher = min(
            trajets,
            key=lambda t: sum(seg["prix"] for seg in t[2])
        )

        return [plus_rapide, moins_cher]

    def tout_trajets(self, depart, arrivee):

        resultats = []
        signatures_vues = []

        for type_train in ["TER", "TGV", None]:
            for critere in ["temps", "prix"]:

                try:
                    chemin, total, segments = self.plus_court_chemin(
                        depart,
                        arrivee,
                        critere=critere,
                        type_train=type_train
                    )

                    signature = (
                        tuple(g.nom for g in chemin),
                        tuple(
                            (seg["depart"], seg["arrivee"], seg["type_train"])
                            for seg in segments
                        )
                    )

                    if signature not in signatures_vues:
                        resultats.append((chemin, total, segments))
                        signatures_vues.append(signature)

                except nx.NetworkXNoPath:
                    continue

        return resultats