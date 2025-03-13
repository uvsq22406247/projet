import tkinter as tk
from tkinter import messagebox #Importe le module messagebox pour afficher des boîtes de dialogue.

# Constantes
WIDTH = 700
HEIGHT = 600
#couleur
RED = "red"
YELLOW = "yellow"



# Variables globales
root = None # root est la fenêtre de base de l'application. Tous les autres éléments graphiques y sont attachés.
turn = 0  # Compteur de tours si le nombre est pair cela correspond au joueur 1 si le nombre impair correspond au joueur 2.
game_over = False  # Indique si la partie est terminée. 
                   # False = la partie continue, True = un joueur a gagné ou la grille est pleine.
canvas = None
WHITE = "white"



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

    bouton_quit = tk.Button(root, text="Quitter", width=20, height=2, command=root.quit)
    bouton_quit.pack(pady=20)
    
def show_game_mode():
    clear_window()
    
    mode_label = tk.Label(root, text="MODE DE JEU", font=("Arial", 55, "bold"))
    mode_label.pack(pady=50)

    btn_2j = tk.Button(root, text="2 Joueurs", width=20, height=2)
    btn_2j.pack(pady=50)

    bouton_retour = tk.Button(root, text="RETOUR",  width=20, height=2, command=show_menu)
    bouton_retour.place(x=10, y=550)

# Lancer le programme
if __name__ == "__main__":
    main()


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
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, cl=WHITE)
    canvas.pack()
    
    back_btn = tk.Button(root, text="Menu", command=show_main_menu)
    back_btn.place(x=10, y=10)
    
    canvas.bind("<Button-1>", click_handler)
