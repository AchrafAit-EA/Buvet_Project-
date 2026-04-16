import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from clinique_logic import Medcin, MedcinChef, Patient, Clinique

# ============================================================
#  COULEURS & STYLE
# ============================================================
BG_MAIN     = "#0f172a"
BG_CARD     = "#1e293b"
BG_INPUT    = "#334155"
ACCENT      = "#38bdf8"
ACCENT2     = "#0ea5e9"
SUCCESS     = "#22c55e"
WARNING     = "#f59e0b"
DANGER      = "#ef4444"
TEXT_WHITE  = "#f1f5f9"
TEXT_GRAY   = "#94a3b8"
FONT_TITLE  = ("Helvetica", 22, "bold")
FONT_SUB    = ("Helvetica", 13, "bold")
FONT_BODY   = ("Helvetica", 11)
FONT_BTN    = ("Helvetica", 11, "bold")
FONT_SMALL  = ("Helvetica", 9)

# ============================================================
#  CLINIQUE (objet global)
# ============================================================
clinique = Clinique("Clinique Chadi")
clinique.load_json("data.json")

# ============================================================
#  HELPERS
# ============================================================
def make_entry(parent, placeholder=""):
    frame = tk.Frame(parent, bg=BG_INPUT, bd=0)
    frame.pack(fill="x", pady=4)
    e = tk.Entry(frame, bg=BG_INPUT, fg=TEXT_WHITE, insertbackground=TEXT_WHITE,
                 font=FONT_BODY, bd=0, highlightthickness=0, relief="flat")
    e.pack(fill="x", padx=10, pady=8)
    if placeholder:
        e.insert(0, placeholder)
        e.config(fg=TEXT_GRAY)
        def on_focus_in(event):
            if e.get() == placeholder:
                e.delete(0, tk.END)
                e.config(fg=TEXT_WHITE)
        def on_focus_out(event):
            if e.get() == "":
                e.insert(0, placeholder)
                e.config(fg=TEXT_GRAY)
        e.bind("<FocusIn>", on_focus_in)
        e.bind("<FocusOut>", on_focus_out)
    return e

def make_label(parent, text, font=FONT_BODY, color=TEXT_GRAY, pady=2):
    tk.Label(parent, text=text, font=font, bg=BG_CARD, fg=color).pack(anchor="w", pady=pady)

def make_btn(parent, text, color, command, width=22):
    tk.Button(parent, text=text, font=FONT_BTN, bg=color, fg="white",
              activebackground=color, activeforeground="white",
              bd=0, cursor="hand2", width=width, pady=8,
              command=command).pack(pady=6)

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def save():
    clinique.sauvegarder_json("data.json")

# ============================================================
#  FENETRE PRINCIPALE
# ============================================================
root = tk.Tk()
root.title("🏥 Clinique Chadi")
root.geometry("950x650")
root.state("zoomed")
root.configure(bg=BG_MAIN)
root.resizable(False, False)

# ============================================================
#  SIDEBAR (gauche)
# ============================================================
sidebar = tk.Frame(root, bg=BG_CARD, width=220)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

# Logo
try:
    img = Image.open("logo.png")
    img = img.resize((90, 90))
    photo = ImageTk.PhotoImage(img)
    tk.Label(sidebar, image=photo, bg=BG_CARD).pack(pady=(20, 5))
    sidebar.image = photo
except:
    tk.Label(sidebar, text="🏥", font=("Helvetica", 40), bg=BG_CARD, fg=ACCENT).pack(pady=(30, 5))

tk.Label(sidebar, text="Clinique Chadi", font=("Helvetica", 13, "bold"),
         bg=BG_CARD, fg=TEXT_WHITE).pack()
tk.Label(sidebar, text="Système de Gestion", font=FONT_SMALL,
         bg=BG_CARD, fg=TEXT_GRAY).pack(pady=(2, 20))

ttk.Separator(sidebar, orient="horizontal").pack(fill="x", padx=15, pady=5)

# ============================================================
#  ZONE PRINCIPALE (droite)
# ============================================================
main_frame = tk.Frame(root, bg=BG_MAIN)
main_frame.pack(side="right", fill="both", expand=True)

content = tk.Frame(main_frame, bg=BG_MAIN)
content.pack(fill="both", expand=True, padx=25, pady=25)

# ============================================================
#  PAGES
# ============================================================

def show_accueil():
    clear_frame(content)
    tk.Label(content, text="Bienvenue 👋", font=FONT_TITLE,
             bg=BG_MAIN, fg=TEXT_WHITE).pack(anchor="w", pady=(0, 5))
    tk.Label(content, text="Tableau de bord de la Clinique Chadi",
             font=FONT_BODY, bg=BG_MAIN, fg=TEXT_GRAY).pack(anchor="w", pady=(0, 20))

    stats_frame = tk.Frame(content, bg=BG_MAIN)
    stats_frame.pack(fill="x", pady=10)

    patients = [p for p in clinique.ListPersonnes if isinstance(p, Patient)]
    medecins = [p for p in clinique.ListPersonnes if isinstance(p, Medcin) and not isinstance(p, MedcinChef)]
    chefs    = [p for p in clinique.ListPersonnes if isinstance(p, MedcinChef)]
    rdvs     = clinique.listRendez_vous

    def stat_card(parent, emoji, count, label, color):
        card = tk.Frame(parent, bg=BG_CARD, bd=0, padx=18, pady=14)
        card.pack(side="left", padx=8, fill="both", expand=True)
        tk.Label(card, text=emoji, font=("Helvetica", 24), bg=BG_CARD, fg=color).pack()
        tk.Label(card, text=str(count), font=("Helvetica", 26, "bold"), bg=BG_CARD, fg=color).pack()
        tk.Label(card, text=label, font=FONT_SMALL, bg=BG_CARD, fg=TEXT_GRAY).pack()

    stat_card(stats_frame, "🧑‍⚕️", len(patients), "Patients", ACCENT)
    stat_card(stats_frame, "👨‍⚕️", len(medecins), "Médecins", SUCCESS)
    stat_card(stats_frame, "⭐", len(chefs), "Chefs", WARNING)
    stat_card(stats_frame, "📅", len(rdvs), "Rendez-vous", DANGER)

    tk.Label(content, text="Utilisez le menu à gauche pour naviguer.",
             font=FONT_BODY, bg=BG_MAIN, fg=TEXT_GRAY).pack(pady=30)


def show_ajouter_patient():
    clear_frame(content)
    tk.Label(content, text="➕ Ajouter un Patient", font=FONT_TITLE,
             bg=BG_MAIN, fg=TEXT_WHITE).pack(anchor="w", pady=(0, 15))

    card = tk.Frame(content, bg=BG_CARD, padx=25, pady=20)
    card.pack(fill="x")

    make_label(card, "CIN")
    e_cin = make_entry(card, "Ex: P001")
    make_label(card, "Nom")
    e_nom = make_entry(card, "Ex: Benali")
    make_label(card, "Prénom")
    e_prenom = make_entry(card, "Ex: Ahmed")
    make_label(card, "Âge")
    e_age = make_entry(card, "Ex: 30")
    make_label(card, "Maladie")
    e_maladie = make_entry(card, "Ex: Diabète")
    make_label(card, "Numéro Dossier")
    e_dossier = make_entry(card, "Ex: D001")

    def ajouter():
        try:
            p = Patient(e_cin.get(), e_nom.get(), e_prenom.get(),
                        int(e_age.get()), e_maladie.get(), e_dossier.get())
            clinique.ajouter_personne(p)
            save()
            messagebox.showinfo("✅ Succès", f"Patient {e_nom.get()} ajouté avec succès!")
            show_ajouter_patient()
        except Exception as ex:
            messagebox.showerror("❌ Erreur", str(ex))

    make_btn(card, "➕ Ajouter Patient", SUCCESS, ajouter)


def show_ajouter_medcin():
    clear_frame(content)
    tk.Label(content, text="👨‍⚕️ Ajouter un Médecin", font=FONT_TITLE,
             bg=BG_MAIN, fg=TEXT_WHITE).pack(anchor="w", pady=(0, 15))

    card = tk.Frame(content, bg=BG_CARD, padx=25, pady=20)
    card.pack(fill="x")

    make_label(card, "CIN")
    e_cin = make_entry(card, "Ex: M001")
    make_label(card, "Nom")
    e_nom = make_entry(card, "Ex: Alami")
    make_label(card, "Prénom")
    e_prenom = make_entry(card, "Ex: Youssef")
    make_label(card, "Âge")
    e_age = make_entry(card, "Ex: 45")
    make_label(card, "Spécialité")
    e_spec = make_entry(card, "Ex: Cardiologie")
    make_label(card, "Salaire (DH)")
    e_sal = make_entry(card, "Ex: 15000")

    is_chef = tk.BooleanVar()
    chef_frame = tk.Frame(card, bg=BG_CARD)
    chef_frame.pack(anchor="w", pady=6)
    tk.Checkbutton(chef_frame, text="Médecin Chef ?", variable=is_chef,
                   bg=BG_CARD, fg=TEXT_WHITE, selectcolor=BG_INPUT,
                   activebackground=BG_CARD, font=FONT_BODY).pack(side="left")

    make_label(card, "Département (si Chef)")
    e_dept = make_entry(card, "Ex: Urgences")

    def ajouter():
        try:
            if is_chef.get():
                m = MedcinChef(e_cin.get(), e_nom.get(), e_prenom.get(),
                               int(e_age.get()), e_spec.get(),
                               float(e_sal.get()), e_dept.get())
            else:
                m = Medcin(e_cin.get(), e_nom.get(), e_prenom.get(),
                           int(e_age.get()), e_spec.get(), float(e_sal.get()))
            clinique.ajouter_personne(m)
            save()
            messagebox.showinfo("✅ Succès", f"Médecin {e_nom.get()} ajouté avec succès!")
            show_ajouter_medcin()
        except Exception as ex:
            messagebox.showerror("❌ Erreur", str(ex))

    make_btn(card, "➕ Ajouter Médecin", ACCENT, ajouter)


def show_rendez_vous():
    clear_frame(content)
    tk.Label(content, text="📅 Rendez-vous", font=FONT_TITLE,
             bg=BG_MAIN, fg=TEXT_WHITE).pack(anchor="w", pady=(0, 10))

    card = tk.Frame(content, bg=BG_CARD, padx=25, pady=15)
    card.pack(fill="x")

    tk.Label(card, text="Ajouter un Rendez-vous", font=FONT_SUB,
             bg=BG_CARD, fg=ACCENT).pack(anchor="w", pady=(0, 8))

    make_label(card, "CIN Patient")
    e_pat = make_entry(card, "Ex: P001")
    make_label(card, "CIN Médecin")
    e_med = make_entry(card, "Ex: M001")
    make_label(card, "Date")
    e_date = make_entry(card, "Ex: 2026/03/10")
    make_label(card, "Heure")
    e_heure = make_entry(card, "Ex: 10:00")

    def ajouter_rdv():
        try:
            pat = clinique.recherche_person_by_cin(e_pat.get())
            med = clinique.recherche_person_by_cin(e_med.get())
            if not pat or not isinstance(pat, Patient):
                raise Exception("Patient introuvable!")
            if not med or not isinstance(med, Medcin):
                raise Exception("Médecin introuvable!")
            clinique.ajouter_rendez_vous(pat, med, e_date.get(), e_heure.get())
            save()
            messagebox.showinfo("✅ Succès", "Rendez-vous ajouté!")
            show_rendez_vous()
        except Exception as ex:
            messagebox.showerror("❌ Erreur", str(ex))

    make_btn(card, "📅 Ajouter RDV", WARNING, ajouter_rdv)

    tk.Label(content, text="Liste des Rendez-vous", font=FONT_SUB,
             bg=BG_MAIN, fg=TEXT_WHITE).pack(anchor="w", pady=(15, 5))

    table_frame = tk.Frame(content, bg=BG_CARD)
    table_frame.pack(fill="both", expand=True)

    cols = ("Patient", "Médecin", "Date", "Heure")
    tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=8)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background=BG_CARD, foreground=TEXT_WHITE,
                    fieldbackground=BG_CARD, font=FONT_BODY, rowheight=28)
    style.configure("Treeview.Heading", background=BG_INPUT, foreground=ACCENT, font=FONT_BTN)

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=180, anchor="center")

    for rdv in clinique.listRendez_vous:
        pat = clinique.recherche_person_by_cin(rdv["patient"])
        med = clinique.recherche_person_by_cin(rdv["medcin"])
        pat_name = f"{pat._nom} {pat._prenom}" if pat else rdv["patient"]
        med_name = f"Dr. {med._nom} {med._prenom}" if med else rdv["medcin"]
        tree.insert("", "end", values=(pat_name, med_name, rdv["date"], rdv["heure"]))

    tree.pack(fill="both", expand=True, padx=5, pady=5)


def show_afficher_tous():
    clear_frame(content)
    tk.Label(content, text="📋 Toutes les Personnes", font=FONT_TITLE,
             bg=BG_MAIN, fg=TEXT_WHITE).pack(anchor="w", pady=(0, 10))

    table_frame = tk.Frame(content, bg=BG_CARD)
    table_frame.pack(fill="both", expand=True)

    cols = ("CIN", "Nom", "Prénom", "Âge", "Rôle", "Info")
    tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=15)
    style = ttk.Style()
    style.configure("Treeview", background=BG_CARD, foreground=TEXT_WHITE,
                    fieldbackground=BG_CARD, font=FONT_BODY, rowheight=28)
    style.configure("Treeview.Heading", background=BG_INPUT, foreground=ACCENT, font=FONT_BTN)

    widths = [80, 120, 120, 60, 100, 200]
    for col, w in zip(cols, widths):
        tree.heading(col, text=col)
        tree.column(col, width=w, anchor="center")

    for p in clinique.ListPersonnes:
        if isinstance(p, Patient):
            info = f"Maladie: {p.maladie}"
        elif isinstance(p, MedcinChef):
            info = f"Dept: {p.departement}"
        elif isinstance(p, Medcin):
            info = f"Spec: {p.specialite}"
        else:
            info = ""
        tree.insert("", "end", values=(p.get_cin(), p._nom, p._prenom, p._age, p.get_role(), info))

    tree.pack(fill="both", expand=True, padx=5, pady=5)


def show_salaires():
    clear_frame(content)
    tk.Label(content, text="💰 Salaires des Médecins", font=FONT_TITLE,
             bg=BG_MAIN, fg=TEXT_WHITE).pack(anchor="w", pady=(0, 10))

    table_frame = tk.Frame(content, bg=BG_CARD)
    table_frame.pack(fill="both", expand=True)

    cols = ("CIN", "Nom", "Prénom", "Spécialité", "Rôle", "Salaire (DH)")
    tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=15)
    style = ttk.Style()
    style.configure("Treeview", background=BG_CARD, foreground=TEXT_WHITE,
                    fieldbackground=BG_CARD, font=FONT_BODY, rowheight=28)
    style.configure("Treeview.Heading", background=BG_INPUT, foreground=WARNING, font=FONT_BTN)

    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=130, anchor="center")

    for p in clinique.ListPersonnes:
        if isinstance(p, Medcin):
            tree.insert("", "end", values=(
                p.get_cin(), p._nom, p._prenom,
                p.specialite, p.get_role(), f"{p.salaire} DH"
            ))

    tree.pack(fill="both", expand=True, padx=5, pady=5)


def show_cout_consultations():
    clear_frame(content)
    tk.Label(content, text="🧾 Coût Total Consultations", font=FONT_TITLE,
             bg=BG_MAIN, fg=TEXT_WHITE).pack(anchor="w", pady=(0, 15))

    card = tk.Frame(content, bg=BG_CARD, padx=25, pady=25)
    card.pack(fill="x")

    make_label(card, "Nombre de jours", font=FONT_SUB, color=TEXT_WHITE)
    e_jours = make_entry(card, "Ex: 5")

    result_label = tk.Label(card, text="", font=("Helvetica", 18, "bold"),
                            bg=BG_CARD, fg=SUCCESS)
    result_label.pack(pady=10)

    def calculer():
        try:
            jours = int(e_jours.get())
            total = clinique.cout_total_consultations(jours)
            result_label.config(text=f"💰 Total : {total} DH")
        except Exception as ex:
            messagebox.showerror("❌ Erreur", str(ex))

    make_btn(card, "🧮 Calculer", ACCENT, calculer)


def show_recherche():
    clear_frame(content)
    tk.Label(content, text="🔍 Rechercher par CIN", font=FONT_TITLE,
             bg=BG_MAIN, fg=TEXT_WHITE).pack(anchor="w", pady=(0, 15))

    card = tk.Frame(content, bg=BG_CARD, padx=25, pady=20)
    card.pack(fill="x")

    make_label(card, "CIN")
    e_cin = make_entry(card, "Ex: P001")

    result_frame = tk.Frame(card, bg=BG_CARD)
    result_frame.pack(fill="x", pady=10)

    def rechercher():
        for w in result_frame.winfo_children():
            w.destroy()
        p = clinique.recherche_person_by_cin(e_cin.get())
        if p:
            tk.Label(result_frame, text=f"✅ Trouvé : {p.get_role()}",
                     font=FONT_SUB, bg=BG_CARD, fg=SUCCESS).pack(anchor="w")
            infos = [
                ("CIN", p.get_cin()), ("Nom", p._nom),
                ("Prénom", p._prenom), ("Âge", f"{p._age} ans"),
                ("Rôle", p.get_role())
            ]
            if isinstance(p, Patient):
                infos += [("Maladie", p.maladie), ("Dossier", p._num_dossier)]
            elif isinstance(p, MedcinChef):
                infos += [("Spécialité", p.specialite), ("Département", p.departement), ("Salaire", f"{p.salaire} DH")]
            elif isinstance(p, Medcin):
                infos += [("Spécialité", p.specialite), ("Salaire", f"{p.salaire} DH")]
            for label, val in infos:
                row = tk.Frame(result_frame, bg=BG_INPUT)
                row.pack(fill="x", pady=2, padx=2)
                tk.Label(row, text=f"  {label}:", font=FONT_BTN, bg=BG_INPUT, fg=TEXT_GRAY, width=14, anchor="w").pack(side="left")
                tk.Label(row, text=val, font=FONT_BODY, bg=BG_INPUT, fg=TEXT_WHITE).pack(side="left", padx=5)
        else:
            tk.Label(result_frame, text="❌ Personne introuvable",
                     font=FONT_SUB, bg=BG_CARD, fg=DANGER).pack(anchor="w")

    make_btn(card, "🔍 Rechercher", ACCENT, rechercher)

# ============================================================
#  BOUTONS SIDEBAR
# ============================================================
buttons = [
    ("🏠  Accueil",             BG_INPUT,  show_accueil),
    ("➕  Ajouter Patient",     SUCCESS,   show_ajouter_patient),
    ("👨‍⚕️  Ajouter Médecin",    ACCENT,    show_ajouter_medcin),
    ("📅  Rendez-vous",         WARNING,   show_rendez_vous),
    ("📋  Afficher Tous",       "#7c3aed", show_afficher_tous),
    ("💰  Salaires Médecins",   "#0d9488", show_salaires),
    ("🧾  Coût Consultations",  DANGER,    show_cout_consultations),
    ("🔍  Rechercher",          "#d97706", show_recherche),
]

for text, color, cmd in buttons:
    btn = tk.Button(sidebar, text=text, font=FONT_BTN, bg=color, fg="white",
                    activebackground=color, activeforeground="white",
                    bd=0, cursor="hand2", anchor="w", padx=15, pady=10,
                    command=cmd, relief="flat")
    btn.pack(fill="x", padx=10, pady=3)

# ============================================================
#  LANCER
# ============================================================
show_accueil()
root.mainloop()