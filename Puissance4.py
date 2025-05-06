import tkinter as tk
from tkinter import messagebox, simpledialog #Importe le module messagebox pour afficher des boîtes de dialogue.
import random

# Constantes
CELL_SIZE = 100
ROWS = 6
COLS = 7
CONNECT_N = 4    # Nombre de jetons alignés nécessaires pour gagner

#Couleur
RED = "red"
YELLOW = "yellow"
WHITE = "white"
BLUE = "blue"

# Variables globales
root = None # root est la fenêtre de base de l'application. Tous les autres éléments graphiques y sont attachés.
turn = 0  # Compteur de tours si le nombre est pair cela correspond au joueur 1 si le nombre impair correspond au joueur 2.
game_over = False  # Indique si la partie est terminée. 
                   # False = la partie continue, True = un joueur a gagné ou la grille est pleine.
canvas = None # Zone de dessin pour la grille
circles=[] # Stocke les cercles affichés sur le canvas
game_mode = "2joueurs" # Mode de jeu par défaut
moves=[]
sets_to_win = 3  # Nombre de manches à gagner pour remporter la partie
score_j1 = 0 # stock combien de manches chaque joueur a gagnées
score_j2 = 0 # stock combien de manches chaque joueur a gagnées
current_starter = 0  # 0 = joueur 1 commence, 1 = joueur 2 commence
current_set = 1 # Garde le compte de la manche en cours 
move_history = []
undo_used = False

def clear_window(): #Cette fonction est utilisée pour effacer tous les éléments graphiques de la fenêtre principale.
    for widget in root.winfo_children():
        widget.destroy() #Cette méthode supprime un widget de la fenêtre. Lorsqu'elle est appelée, le widget est détruit et retiré de l'interface graphique.

    
def main(): # Cette fonction initialise et affiche la fenêtre principale
    global root 
    root = tk.Tk() # Crée la fenêtre principale
    root.title("Puissance 4 - Jeu de stratégie") # Définit le titre de la fenêtre
    root.bind('<Escape>', lambda event:undo_last_move())
    show_menu()
    root.mainloop()# Lance la boucle principale de l'interface graphique
    

  
def show_menu():  # Cette fonction affiche le menu principal
    clear_window()

    frame_menu = tk.Frame(root, width=800, height=600)  # Définir la taille du Frame
    frame_menu.pack_propagate(False)  # Empêche l'extension du Frame
    frame_menu.pack()

    titre_jeu = tk.Label(frame_menu, text="PUISSANCE 4", font=("Arial", 74,"bold"))
    titre_jeu.pack(pady=50)
    
    bouton_play = tk.Button(frame_menu, text="Jouer", width=20, height=2, command=show_game_mode)
    bouton_play.pack(pady=20)
    bouton_play.bind("<Enter>", lambda event, b=bouton_play: on_hover(b, "lightgreen"))
    bouton_play.bind("<Leave>", lambda event, b=bouton_play: on_leave(b))

    bouton_quit = tk.Button(frame_menu, text="Quitter", width=20, height=2, command=root.quit)
    bouton_quit.pack(pady=20)
    bouton_quit.bind("<Enter>", lambda event, b=bouton_quit: on_hover(b, "red"))
    bouton_quit.bind("<Leave>", lambda event, b=bouton_quit: on_leave(b))


def show_game_mode():  # Cette fonction affiche le menu des modes de jeu
    clear_window()

    frame_game_mode = tk.Frame(root, width=800, height=600)  # Taille fixe pour le Frame
    frame_game_mode.pack_propagate(False)
    frame_game_mode.pack()

    mode_label = tk.Label(frame_game_mode, text="MODE DE JEU", font=("Arial", 74, "bold"))
    mode_label.pack(pady=50)

    btn_2j = tk.Button(frame_game_mode, text="2 Joueurs", width=20, height=2, command=choose_game_type_2players)
    btn_2j.pack(pady=50)
    btn_2j.bind("<Enter>", lambda event, b=btn_2j: on_hover(b, "lightyellow"))
    btn_2j.bind("<Leave>", lambda event, b=btn_2j: on_leave(b))

    btn_ia = tk.Button(frame_game_mode, text="Contre l'IA", width=20, height=2, command=choose_game_type_IA)
    btn_ia.pack(pady=20)
    btn_ia.bind("<Enter>", lambda event, b=btn_ia: on_hover(b, "lightblue"))
    btn_ia.bind("<Leave>", lambda event, b=btn_ia: on_leave(b))

    bouton_retour = tk.Button(frame_game_mode, text="RETOUR", width=20, height=2, command=show_menu)
    bouton_retour.pack(side="bottom", anchor="w", padx=10, pady=20)
    bouton_retour.bind("<Enter>", lambda event, b=bouton_retour: on_hover(b, "red"))
    bouton_retour.bind("<Leave>", lambda event, b=bouton_retour: on_leave(b))

def on_hover(button, color):
    button.config(bg=color)  # Change la couleur de fond du bouton

def on_leave(button): #Retablit la couleur d'origine du bouton
    button.config(bg="SystemButtonFace") 


def start_game(mode, sets):# Démarre le jeu avec le mode et les sets sélectionnés
    global game_mode, sets_to_win
    game_mode = mode
    sets_to_win = sets
    show_game()

def show_game(): # Affiche la grille du jeu
    clear_window()
    create_game_widgets()
    new_game()

def click_handler(event):#modif click handler
    global turn, game_over, undo_used, moves
    col = event.x // CELL_SIZE
    if col >= COLS:
        return 
    if game_over:
        return
    player = 1 if turn % 2 == 0 else 2
    if drop_piece(col, player):# Appelle la fonction pour mettre à jour la couleur
        moves.append(col)
        undo_used = False #reinitialiste le undo_used en false a chaque piece placée
        if check_win(player):
            end_game(player)
            return
        if all(board[row][col] != 0 for col in range(COLS) for row in range(ROWS)):
            match_nul()
            return  # Match nul = arrêt aussi
        turn += 1
    if game_mode == "ia" and not game_over:
            canvas.after(500, ia_joue)

def create_game_widgets():
    global canvas
    top = tk.Frame(root)
    top.pack(side="top", pady=5)
    tk.Button(top, text="Menu", command=show_menu).pack(side="left", padx=5)
    tk.Button(top, text="Sauvegarder", command=enregistrer_partie).pack(side="left", padx=5)
    tk.Button(top, text="Charger", command=charger_partie).pack(side="left", padx=5)
    tk.Button(top, text="Annuler", command=undo_last_move).pack(side="left", padx=5)
    canvas = tk.Canvas(root, width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE, bg=BLUE)
    canvas.pack()
    canvas.bind("<Button-1>", click_handler)
    

def draw_board():# Dessine la grille du jeu
    """
    Dessine la grille du jeu Puissance 4 sur le canvas.
    Chaque case est représentée par un cercle vide (blanc avec contour bleu).
    """
    global circles  # S'assurer que la liste circles est bien mise à jour
    circles = []

    for col in range(COLS):  
        column_circles = []  # Liste temporaire pour stocker les cercles d'une colonne

        for row in range(ROWS):
            # Calcul des coordonnées du cercle 
            x1, y1 = col*CELL_SIZE+5, row*CELL_SIZE+5
            x2, y2 = (col+1)*CELL_SIZE-5, (row+1)*CELL_SIZE-5
            circle = canvas.create_oval(x1, y1, x2, y2, fill=WHITE, outline="blue") # Crée un cercle blanc avec un contour bleu
            column_circles.append(circle) # Ajouter le cercle à la liste temporaire de la colonne

            canvas.tag_bind(circle, "<Enter>", lambda event, c=circle: highlight_circle(c))
            canvas.tag_bind(circle, "<Leave>", lambda event, c=circle: remove_highlight(c))

        circles.append(column_circles)


def highlight_circle(circle):
    canvas.itemconfig(circle, outline="red", width=3)

def remove_highlight(circle):
    canvas.itemconfig(circle, outline="blue", width=1)

def new_game():# Réinitialise le jeu
    global board, circles, turn, game_over
    board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    circles = []  # Réinitialise la liste des cercles affichés sur la grille
    turn = current_starter # Celui qui commence alterne 
    game_over, undo_used = False, False  # Réinitialise l'état du jeu à "en cours"
    draw_board()

def drop_piece(col, player):# Place un jeton dans la colonne choisie
    for row in range(ROWS):
        if board[row][col] == 0:
            board[row][col] = player # Place le jeton du joueur
            update_circle(row, col, player)
            move_history.append((row, col)) #(met le cercle placé dans la liste move_history)
            return True # Indique que le placement a été effectué avec succès
    return False #La colonne est pleine et qu'aucun jeton n'a pu être placé


def update_circle(row, col, player):# Met à jour la couleur du cercle correspondant au joueur
    color = RED if player == 1 else YELLOW
    canvas.itemconfig(circles[col][ROWS - 1 - row], fill=color)

    

#****************************************************************************************************

def check_win(player):
    # Vérification horizontale
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col+i] == player for i in range(CONNECT_N)):
                return True

    # Vérification verticale
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == player for i in range(CONNECT_N)):
                return True

    # Diagonale montante
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row-i][col+i] == player for i in range(CONNECT_N)):
                return True

    # Diagonale descendante
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row+i][col+i] == player for i in range(CONNECT_N)):
                return True
    return False

def end_game(player):
    global game_over, score_j1, score_j2, current_starter, current_set
    game_over = True
    winner = ""
    
    if game_mode == "ia":
        winner = "Joueur Rouge" if player == 1 else "IA" # Détermine le gagnant en fonction du joueur si le mode IA est activé
    else:
        winner = "Joueur Rouge" if player == 1 else "Joueur Jaune"  # Détermine le gagnant si c’est une partie à deux joueurs humains
    
    if player == 1:
        score_j1 += 1 #Augmente le score du joueur gagnant
    else:
        score_j2 += 1 # Augmente le score de l'IA ou du Joueur Jaune selon le mode 
    
    messagebox.showinfo("Fin de manche", f"{winner} a gagné la manche {current_set} !")
    new_game()
    
    #On vérifies si le match est fini 
    if score_j1 == sets_to_win:
        messagebox.showinfo("Fin du match", "Joueur Rouge remporte le match !")
        reset_match()
        return
    elif score_j2 == sets_to_win: 
        messagebox.showinfo("Fin du match", "Joueur Jaune remporte le match !")
        reset_match()
        return
    # Prépare la manche suivante
    current_set += 1 #Sert a passer a la manche suivante 
    current_starter = 1 - current_starter  # Alterner le joueur qui commence la manche
    new_game()

def reset_match(): # réinitialiser tout et retourner au menu
    global score_j1, score_j2, current_set, current_starter, moves
    score_j1 = 0
    score_j2 = 0
    current_set = 1
    current_starter = 0
    moves.clear()
    show_menu()
    

def enregistrer_partie():
    # On transforme la liste en chaîne "3,4,2,5..."
    data = ",".join(str(c) for c in moves)
    with open("sauvegarde.txt", "w") as f:
        f.write(data)  # on écrit tout en une ligne
    messagebox.showinfo("Sauvegarde", "Partie enregistrée !")

def charger_partie():
    global moves, turn, board, game_over
    try:
        with open("sauvegarde.txt", "r") as f:
            line = f.read().strip()
        moves = [int(x) for x in line.split(",") if x != ""]

        # Recommence une nouvelle partie
        new_game()

        # Rejoue tous les coups un à un
        for i, col in enumerate(moves):
            player = 1 if i % 2 == 0 else 2
            drop_piece(col, player)
        
        turn = len(moves)  # Met à jour le tour courant
        game_over = False  # On relance le jeu normalement

    except FileNotFoundError:
        messagebox.showerror("Erreur", "Aucune sauvegarde trouvée.")
 
       
def match_nul():
    global game_over, current_set, current_starter
    game_over = True
    messagebox.showinfo("Match nul", "La grille est pleine sans vainqueur pour cette manche.")
    # Prépare la manche suivante
    # On avance au set suivant même s'il y a eu match nul.
    if sets_to_win == 1:
        #si c'etait une partie simple => Fin du match
        messagebox.showinfo("Fin du match", "Match terminé sans vainqueur")
        reset_match()
    else:
        #Sinon,c'est un match en sets => on continue
        current_set += 1
        current_starter = 1 - current_starter #Alterner qui commence
        new_game()

def choose_game_type_2players():  # Fonction graphique pour choisir de jouer en plusieurs ou un seul set
    clear_window()

    frame_game_type = tk.Frame(root, width=800, height=600)  # Définir la taille du frame
    frame_game_type.pack_propagate(False)  # Empêche le frame de changer de taille en fonction du contenu
    frame_game_type.pack()

    type_label = tk.Label(frame_game_type, text="TYPE DE PARTIE", font=("Arial", 50, "bold"))
    type_label.pack(pady=50)

    # Champs de saisie pour les paramètres
    label_rows = tk.Label(frame_game_type, text="Nombre de lignes:")
    label_rows.pack(pady=5)
    entry_rows = tk.Entry(frame_game_type)
    entry_rows.pack(pady=5)
    entry_rows.insert(0, "6")  #met une valeur par défaut 

    label_cols = tk.Label(frame_game_type, text="Nombre de colonnes:")
    label_cols.pack(pady=5)
    entry_cols = tk.Entry(frame_game_type)
    entry_cols.pack(pady=5)
    entry_cols.insert(0, "7")  #met une valeur par défaut 

    label_connect = tk.Label(frame_game_type, text="Nombre de jetons à aligner:")
    label_connect.pack(pady=5)
    entry_connect = tk.Entry(frame_game_type)
    entry_connect.pack(pady=5)
    entry_connect.insert(0, "4")  #met une valeur par défaut 

    # Fonction pour valider et démarrer la partie
    def validate_parameters(sets):
        try:
            r = int(entry_rows.get())
            c = int(entry_cols.get())
            n = int(entry_connect.get())
            if r < 4 or c < 4 or n < 3 or n > min(r, c):
                raise ValueError
        
            global ROWS, COLS, CONNECT_N
            ROWS, COLS, CONNECT_N = r, c, n
            start_game("2joueurs", sets)  # Lance la partie avec les nouveaux paramètres
        except ValueError:
            messagebox.showerror("Erreur", "Valeurs invalides. Veuillez entrer des nombres valides.")

    # Boutons pour choisir le type de jeu
    btn_simple = tk.Button(frame_game_type, text="Partie simple (1 manche)", width=25, height=2, command=lambda: validate_parameters(1))
    btn_simple.pack(pady=20)
    btn_simple.bind("<Enter>", lambda event, b=btn_simple: on_hover(b, "lightblue"))
    btn_simple.bind("<Leave>", lambda event, b=btn_simple: on_leave(b))

    btn_sets = tk.Button(frame_game_type, text="Match en 3 sets", width=25, height=2, command=lambda: validate_parameters(3))
    btn_sets.pack(pady=20)
    btn_sets.bind("<Enter>", lambda event, b=btn_sets: on_hover(b, "lightgreen"))
    btn_sets.bind("<Leave>", lambda event, b=btn_sets: on_leave(b))

    bouton_retour = tk.Button(frame_game_type, text="RETOUR", width=20, height=2, command=show_game_mode)
    bouton_retour.place(relx=0.05, rely=0.95, anchor="sw")
    bouton_retour.bind("<Enter>", lambda event, b=bouton_retour: on_hover(b, "red"))
    bouton_retour.bind("<Leave>", lambda event, b=bouton_retour: on_leave(b))



def choose_game_type_IA():  # Fonction graphique pour choisir de jouer en plusieurs ou un seul set
    clear_window()

    frame_game_type = tk.Frame(root, width=800, height=600)  # Définir la taille du frame
    frame_game_type.pack_propagate(False)  # Empêche le frame de changer de taille en fonction du contenu
    frame_game_type.pack()

    type_label = tk.Label(frame_game_type, text="TYPE DE PARTIE", font=("Arial", 50, "bold"))
    type_label.pack(pady=50)

    # Champs de saisie pour les paramètres
    label_rows = tk.Label(frame_game_type, text="Nombre de lignes:")
    label_rows.pack(pady=5)
    entry_rows = tk.Entry(frame_game_type)
    entry_rows.pack(pady=5)
    entry_rows.insert(0, "6") #met une valeur par défaut 

    label_cols = tk.Label(frame_game_type, text="Nombre de colonnes:")
    label_cols.pack(pady=5)
    entry_cols = tk.Entry(frame_game_type)
    entry_cols.pack(pady=5)
    entry_cols.insert(0, "7") #met une valeur par défaut 

    label_connect = tk.Label(frame_game_type, text="Nombre de jetons à aligner:")
    label_connect.pack(pady=5)
    entry_connect = tk.Entry(frame_game_type)
    entry_connect.pack(pady=5)
    entry_connect.insert(0, "4") #met une valeur par défaut 

    # Fonction pour valider et démarrer la partie contre l'IA
    def validate_parameters(sets):
        try:
            r = int(entry_rows.get())
            c = int(entry_cols.get())
            n = int(entry_connect.get())

            if r < 4 or c < 4 or n < 3 or n > min(r, c):
                raise ValueError
            global ROWS, COLS, CONNECT_N
            ROWS, COLS, CONNECT_N = r, c, n
            start_game("ia", sets)  # Lance la partie avec les nouveaux paramètres
        except ValueError:
            messagebox.showerror("Erreur", "Valeurs invalides. Veuillez entrer des nombres valides.")

    # Boutons pour choisir le type de jeu
    btn_simple = tk.Button(frame_game_type, text="Partie simple (1 manche)", width=25, height=2, command=lambda: validate_parameters(1))
    btn_simple.pack(pady=20)
    btn_simple.bind("<Enter>", lambda event, b=btn_simple: on_hover(b, "lightblue"))
    btn_simple.bind("<Leave>", lambda event, b=btn_simple: on_leave(b))

    btn_sets = tk.Button(frame_game_type, text="Match en 3 sets", width=25, height=2, command=lambda: validate_parameters(3))
    btn_sets.pack(pady=20)
    btn_sets.bind("<Enter>", lambda event, b=btn_sets: on_hover(b, "lightgreen"))
    btn_sets.bind("<Leave>", lambda event, b=btn_sets: on_leave(b))

    bouton_retour = tk.Button(frame_game_type, text="RETOUR", width=20, height=2, command=show_game_mode)
    bouton_retour.place(relx=0.05, rely=0.95, anchor="sw")
    bouton_retour.bind("<Enter>", lambda event, b=bouton_retour: on_hover(b, "red"))
    bouton_retour.bind("<Leave>", lambda event, b=bouton_retour: on_leave(b))


def undo_last_move(): #Annuler un coup
    global turn, game_over,undo_used
    if not move_history or game_over or undo_used:
        return
    row, col = move_history.pop()
    board[row][col] = 0
    canvas.itemconfig(circles[col][ROWS - 1 - row], fill=WHITE) #remet la couleur en blanc, comme une case vide
    turn -= 1
    undo_used = True #Tu bloques l’annulation pour qu’elle ne soit utilisable qu’une seule fois par manche.




def ia_choisir_colonne():
    for col in range(COLS): # Pour chaque colonne du plateau
        temp_board = [row[:] for row in board] # On crée une copie de la grille
        if simule_coup(temp_board, col, 2) and check_win_IA(temp_board, 2): # On simule un coup IA dans cette colonne   # On regarde si ce coup mène à la victoire
            return col # Si oui, on choisit cette colonne
    for col in range(COLS):
        temp_board = [row[:] for row in board]
        if simule_coup(temp_board, col, 1) and check_win_IA(temp_board, 1): # Simule un coup du joueur   # Si ça mène à une victoire pour lui
            return col # On bloque ce coup
    colonnes_valides = [c for c in range(COLS) if board[ROWS - 1][c] == 0] # Liste des colonnes jouables
    if colonnes_valides:  
        return random.choice(colonnes_valides)  # L’IA joue au hasard
    return None   # Grille pleine

def simule_coup(temp_board, col, player):
    for row in range(ROWS):
        if temp_board[row][col] == 0: # Si la case est vide (donc on peut y placer un jeton)
            temp_board[row][col] = player # On place le jeton du joueur dans la case simulée
            return True
    return False

def check_win_IA(temp_board, player):
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(temp_board[row][col+i] == player for i in range(CONNECT_N)):
                return True
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(temp_board[row+i][col] == player for i in range(CONNECT_N)):
                return True
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(temp_board[row-i][col+i] == player for i in range(CONNECT_N)):
                return True
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(temp_board[row+i][col+i] == player for i in range(CONNECT_N)):
                return True
    return False

def ia_joue():
    global turn, game_over, moves
    ia_col = ia_choisir_colonne() # L'IA choisit une colonne où elle veut jouer
    if ia_col is not None and drop_piece(ia_col, 2): # Si la colonne est valide et que le jeton peut être placé
        moves.append(ia_col) # On ajoute ce coup à la liste des coups joués (utile pour sauvegarde ou rejouer)
        if check_win(2): # Si ce coup fait gagner l'IA (joueur 2)
            end_game(2) # On termine la manche en déclarant l'IA gagnante
            return
        if all(board[row][col] != 0 for col in range(COLS) for row in range(ROWS)): # Si toutes les cases sont pleines => match nul
            match_nul()
            return
        turn += 1


# Lancer le programme
if __name__ == "__main__":
    main()