import tkinter as tk
from tkinter import messagebox #Importe le module messagebox pour afficher des boîtes de dialogue.

# Constantes
WIDTH = 700
HEIGHT = 600
CELL_SIZE = 100
ROWS = 6
COLS = 7

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
 

def clear_window(): #Cette fonction est utilisée pour effacer tous les éléments graphiques de la fenêtre principale.
    for widget in root.winfo_children():
        widget.destroy() #Cette méthode supprime un widget de la fenêtre. Lorsqu'elle est appelée, le widget est détruit et retiré de l'interface graphique.

    
def main(): # Cette fonction initialise et affiche la fenêtre principale
    global root 
    root = tk.Tk() # Crée la fenêtre principale
    root.title("Puissance 4 - Jeu de stratégie") # Définit le titre de la fenêtre
    root.geometry(f"{WIDTH}x{HEIGHT}")
    show_menu()
    root.mainloop()# Lance la boucle principale de l'interface graphique
    

  
def show_menu():# Cette fonction affiche le menu principal
    clear_window()
    titre_jeu = tk.Label(root, text="PUISSANCE 4", font=("Arial", 74,"bold"))
    titre_jeu.pack(pady=50)

    bouton_play = tk.Button(root, text="Jouer", width=20, height=2, command=show_game_mode)
    bouton_play.pack(pady=20)
    bouton_play.bind("<Enter>", lambda event, b=bouton_play: on_hover(b, "lightgreen"))
    bouton_play.bind("<Leave>", lambda event, b=bouton_play: on_leave(b))

    bouton_quit = tk.Button(root, text="Quitter", width=20, height=2, command=root.quit)
    bouton_quit.pack(pady=20)
    bouton_quit.bind("<Enter>", lambda event, b=bouton_quit: on_hover(b, "red"))
    bouton_quit.bind("<Leave>", lambda event, b=bouton_quit: on_leave(b))


def show_game_mode():#Cette fonction affiche le menu principal
    clear_window()
    
    mode_label = tk.Label(root, text="MODE DE JEU", font=("Arial", 55, "bold"))
    mode_label.pack(pady=50)
    # Bouton pour démarrer la partie
    btn_2j = tk.Button(root, text="2 Joueurs", width=20, height=2, command= choose_game_type_2players)
    btn_2j.pack(pady=50)
    btn_2j.bind("<Enter>", lambda event, b=btn_2j: on_hover(b, "lightyellow"))
    btn_2j.bind("<Leave>", lambda event, b=btn_2j: on_leave(b))
    # Bouton pour quitter le jeu
    bouton_retour = tk.Button(root, text="RETOUR",  width=20, height=2, command=show_menu)
    bouton_retour.place(x=10, y=550)
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
        undo_used = False 
        if check_win(player):
            end_game(player)
            return
        if all(board[row][col] != 0 for col in range(COLS) for row in range(ROWS)):
            match_nul()
            return  # Match nul = arrêt aussi
        turn += 1


def create_game_widgets():# Crée le canvas du jeu et les boutons
    global canvas
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BLUE) 
    canvas.pack()
    
    back_btn = tk.Button(root, text="Menu", command=show_menu)
    back_btn.place(x=10, y=10)

    save_btn = tk.Button(root, text="Sauvegarder", command=enregistrer_partie)
    save_btn.place(x=100, y=10)

    load_btn = tk.Button(root, text="Charger", command=charger_partie)
    load_btn.place(x=220, y=10)


    
    canvas.bind("<Button-1>", click_handler)# Lie le bouton clique gauche avec click_handler
    

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
            x1 = col * CELL_SIZE + 10 # Coordonnée X du coin supérieur gauche
            y1 = row * CELL_SIZE + 10 # Coordonnée Y du coin supérieur gauche
            x2 = x1 + CELL_SIZE - 20 # Coordonnée X du coin inférieur droit
            y2 = y1 + CELL_SIZE - 20 # Coordonnée Y du coin inférieur droit
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
    game_over = False  # Réinitialise l'état du jeu à "en cours"
    draw_board()

def drop_piece(col, player):# Place un jeton dans la colonne choisie
    for row in range(ROWS):
        if board[row][col] == 0:
            board[row][col] = player # Place le jeton du joueur
            update_circle(row, col, player)
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
            if all(board[row][col+i] == player for i in range(4)):
                return True

    # Vérification verticale
    for col in range(COLS):
        for row in range(ROWS - 3):
            if all(board[row+i][col] == player for i in range(4)):
                return True

    # Diagonale montante
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row-i][col+i] == player for i in range(4)):
                return True

    # Diagonale descendante
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row+i][col+i] == player for i in range(4)):
                return True
    return False

def end_game(player):
    global game_over, score_j1, score_j2, current_starter, current_set
    game_over = True
    winner = ""
    
    if game_mode == "ia":
        winner = "Joueur Rouge" if player == 1 else "IA"
    else:
        winner = "Joueur Rouge" if player == 1 else "Joueur Jaune"
    
    if player == 1:
        score_j1 += 1 #Augmente le score du joueur gagnant
    else:
        score_j2 += 1
    
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
    current_set += 1
    current_starter = 1 - current_starter   # Alterner le joueur qui commence la manche
    new_game()

def choose_game_type_2players():#Fonction graphique pour choisir de jouer en plusieurs ou un seul set
    clear_window()

    type_label = tk.Label(root, text="TYPE DE PARTIE", font=("Arial", 50, "bold"))
    type_label.pack(pady=50)

    btn_simple = tk.Button(root, text="Partie simple (1 manche)", width=25, height=2, command=lambda: start_game("2joueurs", 1))
    btn_simple.pack(pady=20)
    btn_simple.bind("<Enter>", lambda event, b=btn_simple: on_hover(b, "lightblue"))
    btn_simple.bind("<Leave>", lambda event, b=btn_simple: on_leave(b))

    btn_sets = tk.Button(root, text="Match en 3 sets", width=25, height=2, command=lambda: start_game("2joueurs", 3))
    btn_sets.pack(pady=20)
    btn_sets.bind("<Enter>", lambda event, b=btn_sets: on_hover(b, "lightgreen"))
    btn_sets.bind("<Leave>", lambda event, b=btn_sets: on_leave(b))

    bouton_retour = tk.Button(root, text="RETOUR", width=20, height=2, command=show_game_mode)
    bouton_retour.place(x=10, y=550)
    bouton_retour.bind("<Enter>", lambda event, b=bouton_retour: on_hover(b, "red"))
    bouton_retour.bind("<Leave>", lambda event, b=bouton_retour: on_leave(b))

# Lancer le programme
if __name__ == "__main__":
    main()