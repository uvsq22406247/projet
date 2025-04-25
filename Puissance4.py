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
    btn_2j = tk.Button(root, text="2 Joueurs", width=20, height=2, command=lambda: start_game("2joueurs"))
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


def start_game(mode):# Démarre le jeu avec le mode sélectionné
    global game_mode
    game_mode = mode
    show_game()


def show_game(): # Affiche la grille du jeu
    clear_window()
    create_game_widgets()
    new_game()


def click_handler(event):#Gère le clic sur une colonne de la grille
    global turn, game_over
    col = event.x // CELL_SIZE  # La colonne est basée sur la position horizontale du clic
    if col >= COLS:  # Si le clic est en dehors de la grille on ne renvoie rien 
        return 
    

    # Si le jeu est terminé, ne rien faire
    if game_over:
        return
    if turn % 2 == 0:  # Tour du joueur 1 (rouge)
        player = 1
    else:               # Tour du joueur 2 (jaune)
        player = 2
    if drop_piece(col, player):# Appelle la fonction pour mettre à jour la couleur
        moves.append(col)
        if check_win(player):
            end_game(player)
            return
        turn += 1 # Changer le tour du joueur


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
    turn = 0  # Remet le compteur de tours à 0 
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
    global game_over
    game_over = True
    winner = ""
    
    if game_mode == "ia":
        winner = "Joueur Rouge" if player == 1 else "IA"
    else:
        winner = "Joueur Rouge" if player == 1 else "Joueur Jaune"
    
    messagebox.showinfo("Fin de partie", f"{winner} a gagné !")
    new_game()

def enregistrer_partie():
    # On transforme la liste en chaîne "3,4,2,5..."
    data = ",".join(str(c) for c in moves)
    with open("sauvegarde.txt", "w") as f:
        f.write(data)  # on écrit tout en une ligne
    messagebox.showinfo("Sauvegarde", "Partie enregistrée !")

def charger_partie():

# Lancer le programme
if __name__ == "__main__":
    main()