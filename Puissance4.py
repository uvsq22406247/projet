import tkinter as tk
from tkinter import messagebox #Importe le module messagebox pour afficher des boîtes de dialogue.

# Constantes
WIDTH = 700
HEIGHT = 600
CELL_SIZE = 100
ROWS = 6
COLS = 7

#couleur
RED = "red"
YELLOW = "yellow"
WHITE = "white"
BLUE = "blue"

# Variables globales
root = None # root est la fenêtre de base de l'application. Tous les autres éléments graphiques y sont attachés.
turn = 0  # Compteur de tours si le nombre est pair cela correspond au joueur 1 si le nombre impair correspond au joueur 2.
game_over = False  # Indique si la partie est terminée. 
                   # False = la partie continue, True = un joueur a gagné ou la grille est pleine.
canvas = None
circles=[]
game_mode = "2joueurs"

def clear_window(): #Cette fonction est utilisée pour effacer tous les éléments graphiques de la fenêtre principale.
    for widget in root.winfo_children():
        widget.destroy() #Cette méthode supprime un widget de la fenêtre. Lorsqu'elle est appelée, le widget est détruit et retiré de l'interface graphique.

    
def main():
    global root 
    root = tk.Tk() # Crée la fenêtre principale
    root.title("Puissance 4") # Définit le titre de la fenêtre
    root.geometry(f"{WIDTH}x{HEIGHT}")
    show_menu()
    root.mainloop()# Lance la boucle principale de l'interface graphique
    

    
def show_menu():
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


def show_game_mode():
    clear_window()
    
    mode_label = tk.Label(root, text="MODE DE JEU", font=("Arial", 55, "bold"))
    mode_label.pack(pady=50)

    btn_2j = tk.Button(root, text="2 Joueurs", width=20, height=2, command=lambda: start_game("2joueurs"))
    btn_2j.pack(pady=50)
    btn_2j.bind("<Enter>", lambda event, b=btn_2j: on_hover(b, "lightyellow"))
    btn_2j.bind("<Leave>", lambda event, b=btn_2j: on_leave(b))

    bouton_retour = tk.Button(root, text="RETOUR",  width=20, height=2, command=show_menu)
    bouton_retour.place(x=10, y=550)
    bouton_retour.bind("<Enter>", lambda event, b=bouton_retour: on_hover(b, "red"))
    bouton_retour.bind("<Leave>", lambda event, b=bouton_retour: on_leave(b))


def on_hover(button, color):
    button.config(bg=color)  # Change la couleur de fond du bouton

def on_leave(button):
    button.config(bg="SystemButtonFace") 


def start_game(mode):
    global game_mode
    game_mode = mode
    show_game()


def show_game():
    clear_window()
    create_game_widgets()
    new_game()


def click_handler(event):
    global turn, game_over

    # Si le jeu est terminé, ne rien faire
    if game_over:
        return
    if turn % 2 == 0:  # Tour du joueur 1 (rouge)
        player = 1
        color = RED
    else:               # Tour du joueur 2 (jaune)
        player = 2
        color = YELLOW


def create_game_widgets():
    global canvas
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=WHITE)
    canvas.pack()
    
    back_btn = tk.Button(root, text="Menu", command=show_menu)
    back_btn.place(x=10, y=10)
    
    canvas.bind("<Button-1>", click_handler)# appuie sur le bouton+1
    

def draw_board():
    """
    Dessine la grille du jeu Puissance 4 sur le canvas.
    Chaque case est représentée par un cercle vide (blanc avec contour bleu).
    """
    global circles  # S'assurer que la liste circles est bien mise à jour
    circles = []

    for col in range(COLS):  
        column_circles = []  # Liste temporaire pour stocker les cercles d'une colonne

        for row in range(ROWS):  
            x1 = col * CELL_SIZE + 10
            y1 = row * CELL_SIZE + 10
            x2 = x1 + CELL_SIZE - 20
            y2 = y1 + CELL_SIZE - 20

            circle = canvas.create_oval(x1, y1, x2, y2, fill=WHITE, outline="blue")

            column_circles.append(circle)

            canvas.tag_bind(circle, "<Enter>", lambda event, c=circle: highlight_circle(c))
            canvas.tag_bind(circle, "<Leave>", lambda event, c=circle: remove_highlight(c))

        circles.append(column_circles)


def highlight_circle(circle):
    canvas.itemconfig(circle, outline="red", width=3)

def remove_highlight(circle):
    canvas.itemconfig(circle, outline="blue", width=1)



def new_game():
    global board, circles, turn, game_over
    board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    circles = []
    turn = 0
    game_over = False
    draw_board()


# Lancer le programme
if __name__ == "__main__":
    main()