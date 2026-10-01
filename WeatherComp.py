import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from data_loader import (
    charger_donnees,
    statistiques_mensuelles,
    pourcentage_jours_gel,
    FichierDonneesIntrouvable,
)

MOIS_LABELS = ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]

# =====================
# 1 fenetre principale
# =====================
root = tk.Tk()
root.title("WEATHER COMPARATOR")
root.geometry("1300x900")
root.configure(bg="#4B6584")

style = ttk.Style()
style.theme_use('clam')
style.configure("Card.TFrame", background="#718093", relief="raised", borderwidth=1)

# =======================
# 2 Haut de l interface
# =======================
control_frame = ttk.Frame(root, padding=10, style="Card.TFrame")
control_frame.pack(fill="x", padx=20, pady=15)

villes = ["Ottawa", "Toronto","Hamilton","London","Windsor","Kitchener"]
annees = ["2020","2021","2022","2023", "2024", "2025", "2026"]

tk.Label(control_frame, text="Ville 1 :", bg="#718093", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5)
combo_v1 = ttk.Combobox(control_frame, values=villes, width=15, state="readonly")
combo_v1.set("Ottawa")
combo_v1.grid(row=0, column=1, padx=10)

tk.Label(control_frame, text="Ville 2 :", bg="#718093", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=5)
combo_v2 = ttk.Combobox(control_frame, values=villes, width=15, state="readonly")
combo_v2.set("Toronto")
combo_v2.grid(row=0, column=3, padx=10)

tk.Label(control_frame, text="Annee :", bg="#718093", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=4, padx=5)
combo_annee = ttk.Combobox(control_frame, values=annees, width=10, state="readonly")
combo_annee.set("2025")
combo_annee.grid(row=0, column=5, padx=10)

# ====================
# 3 Graphiques 1 & 2
# ====================
middle_frame = tk.Frame(root, bg="#4B6584")
middle_frame.pack(fill="both", expand=True, padx=20, pady=10)

frame_g1 = ttk.Frame(middle_frame, padding=10, style="Card.TFrame")
frame_g1.pack(side="left", fill="both", expand=True, padx=(0, 10))
tk.Label(frame_g1, text="EVOLUTION TEMPORELLE DE LA TEMPERATURE", bg="#718093", fg="white", font=("Arial", 10, "bold")).pack()

fig1, ax1 = plt.subplots(figsize=(6, 3.5), facecolor="#718093")
canvas1 = FigureCanvasTkAgg(fig1, master=frame_g1)
canvas1.get_tk_widget().pack(fill="both", expand=True)

frame_g2 = ttk.Frame(middle_frame, padding=10, style="Card.TFrame")
frame_g2.pack(side="right", fill="both", expand=True, padx=(10, 0))
tk.Label(frame_g2, text="PRECIPITATIONS", bg="#718093", fg="white", font=("Arial", 10, "bold")).pack()

fig2, ax2 = plt.subplots(figsize=(6, 3.5), facecolor="#718093")
canvas2 = FigureCanvasTkAgg(fig2, master=frame_g2)
canvas2.get_tk_widget().pack(fill="both", expand=True)

# ================
# 4 Graphique 3
# ================
frame_g3 = ttk.Frame(root, padding=10, style="Card.TFrame")
frame_g3.pack(fill="both", expand=True, padx=20, pady=(10, 20))
tk.Label(frame_g3, text="REPARTITION ANNUELLE DE GEL", bg="#718093", fg="white", font=("Arial", 12, "bold")).pack()

fig3, (ax3_1, ax3_2) = plt.subplots(1, 2, figsize=(8, 2.5), facecolor="#718093")
canvas3 = FigureCanvasTkAgg(fig3, master=frame_g3)
canvas3.get_tk_widget().pack(fill="both", expand=True)


# =====================================================
# 5 Logique rafraichir (branchee aux csv)
# ====================================================
def dessiner_graphiques(v1, v2, annee):
    df1 = charger_donnees(v1, annee)
    df2 = charger_donnees(v2, annee)

    stats1 = statistiques_mensuelles(df1)
    stats2 = statistiques_mensuelles(df2)

    # Graph 1 temperatures mensuelles moyennes 
    positions_mois = range(12)
    ax1.clear()
    ax1.set_facecolor("#718093")
    ax1.plot(positions_mois, stats1["temp_max"], color="#00E5FF", label=v1)
    ax1.plot(positions_mois, stats2["temp_max"], color="#FF6B6B", label=v2)
    ax1.set_xticks(list(positions_mois))
    ax1.set_xticklabels(MOIS_LABELS)
    ax1.legend(fontsize=7)
    ax1.tick_params(colors="white", labelsize=8)
    fig1.tight_layout()
    canvas1.draw()

    # Graph2 precipitations mensuelles 
    ax2.clear()
    ax2.set_facecolor("#718093")
    largeur = 0.35
    positions = range(12)
    ax2.bar([p - largeur / 2 for p in positions], stats1["precip_mm"], largeur, color="#9B59B6", label=v1)
    ax2.bar([p + largeur / 2 for p in positions], stats2["precip_mm"], largeur, color="#3498DB", label=v2)
    ax2.set_xticks(list(positions))
    ax2.set_xticklabels(MOIS_LABELS)
    ax2.legend(fontsize=7)
    ax2.tick_params(colors="white", labelsize=8)
    fig2.tight_layout()
    canvas2.draw()

    #  Graph 3  % jours de gel 
    gel1 = pourcentage_jours_gel(df1)
    gel2 = pourcentage_jours_gel(df2)

    ax3_1.clear()
    ax3_1.pie([gel1, 100 - gel1], labels=["Gel", "Doux"], colors=["#3498DB", "#A8E6CF"], autopct='%1.1f%%')
    ax3_1.set_title(v1, color="white")

    ax3_2.clear()
    ax3_2.pie([gel2, 100 - gel2], labels=["Gel", "Doux"], colors=["#3498DB", "#A8E6CF"], autopct='%1.1f%%')
    ax3_2.set_title(v2, color="white")
    fig3.tight_layout()
    canvas3.draw()


def rafraichir_donnees():
    v1 = combo_v1.get()
    v2 = combo_v2.get()
    annee = combo_annee.get()

    if not v1 or not v2 or not annee:
        messagebox.showwarning("Selection incomplete", "Choisis une ville 1, une ville 2 et une annee.")
        return

    try:
        dessiner_graphiques(v1, v2, annee)
    except FichierDonneesIntrouvable as erreur:
        messagebox.showerror("Fichier introuvable", str(erreur))
    except Exception as erreur:
        messagebox.showerror("Erreur de traitement", f"Une erreur est survenue :\n{erreur}")


btn_refresh = tk.Button(control_frame, text="Rafraichir", command=rafraichir_donnees, bg="#A55EEE", fg="white", font=("Arial", 11, "bold"), padx=10)
btn_refresh.grid(row=0, column=6, padx=20)

root.mainloop()