import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# 1. Configuration de la fenêtre principale 
root = tk.Tk()
root.title("WEATHER COMPARATOR")
root.geometry("1000x800")
root.configure(bg="#4B6584")  # Couleur de fond 

# Style 
style = ttk.Style()
style.theme_use('clam')
style.configure("Card.TFrame", background="#718093", relief="raised", borderwidth=1)

# =========================================================================
# 2. Haut de l'interface
# =========================================================================
control_frame = ttk.Frame(root, padding=10, style="Card.TFrame")
# 
control_frame.pack(fill="x", padx=20, pady=15)

# Variables 
villes = ["Ottawa", "Toronto", "Edmonton", "Montréal"]
annees = ["2023", "2024", "2025", "2026"]

tk.Label(control_frame, text="Ville 1 :", bg="#718093", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5)
combo_v1 = ttk.Combobox(control_frame, values=villes, width=15)
combo_v1.set("Ottawa")
combo_v1.grid(row=0, column=1, padx=10)

tk.Label(control_frame, text="Ville 2 :", bg="#718093", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=5)
combo_v2 = ttk.Combobox(control_frame, values=villes, width=15)
combo_v2.set("Toronto")
combo_v2.grid(row=0, column=3, padx=10)

tk.Label(control_frame, text="Année :", bg="#718093", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=4, padx=5)
combo_annee = ttk.Combobox(control_frame, values=annees, width=10)
combo_annee.set("2025")
combo_annee.grid(row=0, column=5, padx=10)

# Fonction "Rafraîchir" 
def rafraichir_donnees():
    v1 = combo_v1.get()
    v2 = combo_v2.get()
    annee = combo_annee.get()
    print(f"Mise à jour interactive : Chargement de {v1} et {v2} pour l'année {annee}...")

btn_refresh = tk.Button(control_frame, text="Rafraîchir", command=rafraichir_donnees, bg="#A55EEE", fg="white", font=("Arial", 11, "bold"), padx=10)
btn_refresh.grid(row=0, column=6, padx=20)

# =========================================================================
# 3. Graphiques 1 & 2
# =========================================================================
middle_frame = tk.Frame(root, bg="#4B6584")
middle_frame.pack(fill="both", expand=True, padx=20, pady=10)

# Graphique 1 
frame_g1 = ttk.Frame(middle_frame, padding=10, style="Card.TFrame")
frame_g1.pack(side="left", fill="both", expand=True, padx=(0, 10))
tk.Label(frame_g1, text="ÉVOLUTION TEMPORELLE DE LA TEMPÉRATURE", bg="#718093", fg="white", font=("Arial", 10, "bold")).pack()

fig1, ax1 = plt.subplots(figsize=(4, 3), facecolor="#718093")
ax1.set_facecolor("#718093")
# Exemple
ax1.plot(["J","F","M","A","M","J","J","A","S","O","N","D"], [-15,-10,-2,8,15,22,26,24,18,10,2,-8], color="#00E5FF", label="Ville 1")
canvas1 = FigureCanvasTkAgg(fig1, master=frame_g1)
canvas1.get_tk_widget().pack(fill="both", expand=True)

# Graphique 2 
frame_g2 = ttk.Frame(middle_frame, padding=10, style="Card.TFrame")
frame_g2.pack(side="right", fill="both", expand=True, padx=(10, 0))
tk.Label(frame_g2, text="PRÉCIPITATIONS", bg="#718093", fg="white", font=("Arial", 10, "bold")).pack()

fig2, ax2 = plt.subplots(figsize=(4, 3), facecolor="#718093")
ax2.set_facecolor("#718093")
# COR
ax2.bar(["Janv", "Fév", "Mars"], [80, 50, 95], color="#9B59B6")
canvas2 = FigureCanvasTkAgg(fig2, master=frame_g2)
canvas2.get_tk_widget().pack(fill="both", expand=True)

# =========================================================================
# 4. Graphique 3 
# =========================================================================
frame_g3 = ttk.Frame(root, padding=10, style="Card.TFrame")
frame_g3.pack(fill="both", expand=True, padx=20, pady=(10, 20))
tk.Label(frame_g3, text="RÉPARTITION ANNUELLE DE GEL", bg="#718093", fg="white", font=("Arial", 12, "bold")).pack()

fig3, (ax3_1, ax3_2) = plt.subplots(1, 2, figsize=(8, 2.5), facecolor="#718093")
# données pour les diagrammes en camembert
ax3_1.pie([35, 65], labels=["Gel", "Doux"], colors=["#3498DB", "#A8E6CF"], autopct='%1.1f%%')
ax3_1.set_title("Ville 1", color="white")
ax3_2.pie([55, 45], labels=["Gel", "Doux"], colors=["#3498DB", "#A8E6CF"], autopct='%1.1f%%')
ax3_2.set_title("Ville 2", color="white")

canvas3 = FigureCanvasTkAgg(fig3, master=frame_g3)
canvas3.get_tk_widget().pack(fill="both", expand=True)

root.mainloop()