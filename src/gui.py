import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox, QTextEdit, QCheckBox, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from main import reseau  # ReseauFerroviaire déjà initialisé
from graph import Gare

# --- Fonction pour convertir minutes en format h:mm ---
def format_temps(minutes: int) -> str:
    if minutes < 60:
        return f"{minutes} min"
    heures = minutes // 60
    mins = minutes % 60
    return f"{heures}h{mins:02d}"

# --- Fonction pour transformer le trajet en texte ---
def trajet_vers_texte(trajet, segments):
    texte = []
    chemin_str = " -> ".join(g.nom for g in trajet)
    texte.append(f"Trajet : {chemin_str}\n")
    total_temps = sum(seg["temps"] for seg in segments)
    total_prix = sum(seg["prix"] for seg in segments)
    lignes = set((seg["ligne"], seg["type_train"]) for seg in segments)
    texte.append("Lignes utilisées :")
    for ligne, type_train in sorted(lignes):
        texte.append(f"  {ligne} ({type_train})")
    texte.append("\nDétail par segment :")
    for seg in segments:
        texte.append(
            f"  {seg['depart']} -> {seg['arrivee']} : "
            f"{format_temps(seg['temps'])}, {seg['prix']} €, "
            f"Ligne : {seg['ligne']} ({seg['type_train']})"
        )
    texte.append("\nTotal :")
    texte.append(f"  Temps : {format_temps(total_temps)}")
    texte.append(f"  Prix  : {total_prix} €")
    return "\n".join(texte), total_temps, total_prix

class GUI(QWidget):
    def __init__(self, reseau):
        super().__init__()
        self.reseau = reseau
        self.trajet_actif_segments = None

        self.setWindowTitle("Planificateur de trajets ferroviaires")
        self.setGeometry(100, 100, 1300, 700)
        self.setWindowIcon(QIcon("icon.png"))

        main_layout = QHBoxLayout(self)
        # --- Partie carte ---
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        main_layout.addWidget(self.canvas, stretch=5)
        self.canvas.mpl_connect("motion_notify_event", self.survol_arrete)

        # --- Partie contrôle utilisateur ---
        control_layout = QVBoxLayout()
        main_layout.addLayout(control_layout, stretch=3)

        # Total temps / prix du trajet sélectionné
        self.summary_label = QLabel("Sélectionnez un trajet pour voir le temps et le prix")
        self.summary_label.setWordWrap(True)
        control_layout.addWidget(self.summary_label)

        # Gare départ / arrivée
        self.depart_combo = QComboBox()
        self.arrivee_combo = QComboBox()
        # --- tri alphabétique ---
        for g in sorted(self.reseau.graph.nodes, key=lambda x: x.nom): #On trie la liste dans le cas où elle ne l'était pas
            self.depart_combo.addItem(g.nom, g)
            self.arrivee_combo.addItem(g.nom, g)
        control_layout.addWidget(QLabel("Départ"))
        control_layout.addWidget(self.depart_combo)
        control_layout.addWidget(QLabel("Arrivée"))
        control_layout.addWidget(self.arrivee_combo)

        # Options train
        self.ter_checkbox = QCheckBox("TER")
        self.tgv_checkbox = QCheckBox("TGV")
        self.ter_checkbox.setChecked(True)
        self.tgv_checkbox.setChecked(True)
        control_layout.addWidget(self.ter_checkbox)
        control_layout.addWidget(self.tgv_checkbox)

        # Bouton rechercher
        self.search_btn = QPushButton("Rechercher trajets")
        self.search_btn.clicked.connect(self.rechercher_trajets)
        control_layout.addWidget(self.search_btn)

        # Liste des trajets
        control_layout.addWidget(QLabel("Trajets trouvés :"))
        self.trajets_list = QListWidget()
        control_layout.addWidget(self.trajets_list)

        # Label détails
        control_layout.addWidget(QLabel("Détails du trajet :"))
        self.trajet_details = QTextEdit()
        self.trajet_details.setReadOnly(True)
        control_layout.addWidget(self.trajet_details)

        # Label info survol
        self.survol_label = QLabel("Survol d'une arête : ")
        control_layout.addWidget(self.survol_label)

        # --- Affichage initial du réseau ---
        self.afficher_reseau()

    def afficher_reseau(self, trajet_segments=None):
        self.ax.clear()
        coords = {g: (g.x, g.y) for g in self.reseau.graph.nodes}
        self.edges_info = []

        # Compter combien d'arêtes passent entre chaque paire pour décaler
        edge_counts = {}
        for u, v, data in self.reseau.graph.edges(data=True):
            key = tuple(sorted([u.nom, v.nom]))
            edge_counts[key] = edge_counts.get(key, 0) + 1

        offsets = {}
        for u, v, data in self.reseau.graph.edges(data=True):
            x0, y0 = coords[u]
            x1, y1 = coords[v]
            key = tuple(sorted([u.nom, v.nom]))
            count = edge_counts[key]
            if key not in offsets:
                offsets[key] = 0
            dx = y1 - y0
            dy = -(x1 - x0)
            length = (dx**2 + dy**2)**0.5
            if length != 0:
                dx /= length
                dy /= length
            shift = offsets[key] * 0.15
            x0_shift = x0 + dx * shift
            y0_shift = y0 + dy * shift
            x1_shift = x1 + dx * shift
            y1_shift = y1 + dy * shift
            offsets[key] += 1

            is_in_trajet = False
            if trajet_segments:
                for seg in trajet_segments:
                    if ((seg["depart"] == u.nom and seg["arrivee"] == v.nom) or
                        (seg["depart"] == v.nom and seg["arrivee"] == u.nom)) \
                            and seg["ligne"] == data["ligne"] \
                            and seg["type_train"] == data["type_train"]:
                        is_in_trajet = True
                        break
            color = "red" if is_in_trajet else "grey"
            line = self.ax.plot([x0_shift, x1_shift], [y0_shift, y1_shift], color=color, zorder=1, linewidth=2)[0]

            self.edges_info.append({
                "line": line,
                "x0": x0_shift, "y0": y0_shift,
                "x1": x1_shift, "y1": y1_shift,
                "data": data
            })

        # Tracer les gares
        for g, (x, y) in coords.items():
            self.ax.scatter(x, y, s=120, color="blue", zorder=2)
            self.ax.text(x + 0.05, y + 0.05, g.nom, fontsize=10)

        xs = [g.x for g in self.reseau.graph.nodes]
        ys = [g.y for g in self.reseau.graph.nodes]
        margin = 0.5
        self.ax.set_xlim(min(xs) - margin, max(xs) + margin)
        self.ax.set_ylim(min(ys) - margin, max(ys) + margin)
        self.ax.set_aspect('equal')
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.canvas.draw()

    def survol_arrete(self, event):
        if event.xdata is None or event.ydata is None:
            self.survol_label.setText("Survol d'une arête : ")
            return
        for info in self.edges_info:
            x0, y0, x1, y1 = info["x0"], info["y0"], info["x1"], info["y1"]
            dx = x1 - x0
            dy = y1 - y0
            if dx == 0 and dy == 0:
                continue
            t = max(0, min(1, ((event.xdata - x0) * dx + (event.ydata - y0) * dy) / (dx*dx + dy*dy)))
            px = x0 + t * dx
            py = y0 + t * dy
            dist = ((event.xdata - px)**2 + (event.ydata - py)**2)**0.5
            if dist < 0.08:
                d = info["data"]
                self.survol_label.setText(
                    f"Survol : {d['ligne']} ({d['type_train']}) | "
                    f"Temps: {format_temps(d['temps'])} | Prix: {d['prix']} €"
                )
                return
        self.survol_label.setText("Survol d'une arête : ")

    def rechercher_trajets(self):
        depart = self.depart_combo.currentData()
        arrivee = self.arrivee_combo.currentData()

        type_train = []
        if self.ter_checkbox.isChecked():
            type_train.append("TER")
        if self.tgv_checkbox.isChecked():
            type_train.append("TGV")

        trajets = self.reseau.tout_trajets(depart, arrivee)
        trajets = [t for t in trajets if all(seg["type_train"] in type_train for seg in t[2])]

        self.trajets_list.clear()
        for i, t in enumerate(trajets):
            types_trains = set(seg["type_train"] for seg in t[2])
            if types_trains == {"TER"}:
                type_str = "TER"
            elif types_trains == {"TGV"}:
                type_str = "TGV"
            else:
                type_str = "Mixte"
            # déterminer plus rapide / moins cher
            critere = "moins cher" if sum(seg["prix"] for seg in t[2]) <= sum(seg["prix"] for seg in trajets[0][2]) else "plus rapide"
            item = QListWidgetItem(
                f"Trajet {i+1} : {t[0][0].nom} -> {t[0][-1].nom} ({type_str}, {critere})"
            )
            item.setData(Qt.ItemDataRole.UserRole, t)
            self.trajets_list.addItem(item)

        self.trajets_list.itemClicked.connect(self.afficher_details_trajet)

    def afficher_details_trajet(self, item):
        t = item.data(Qt.ItemDataRole.UserRole)
        self.trajet_actif_segments = t[2]
        texte, total_temps, total_prix = trajet_vers_texte(t[0], t[2])
        self.trajet_details.setPlainText(texte)
        self.summary_label.setText(f"<b>Temps total : {format_temps(total_temps)} | Prix total : {total_prix} €</b>")
        self.afficher_reseau(trajet_segments=t[2])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = GUI(reseau)
    gui.show()
    sys.exit(app.exec())