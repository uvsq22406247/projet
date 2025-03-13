import tkinter as tk
from tkinter import messagebox #Importe le module messagebox pour afficher des boîtes de dialogue.

# Constantes
WIDTH = 700
HEIGHT = 600


# Variables globales
root = None # root est la fenêtre de base de l'application. Tous les autres éléments graphiques y sont attachés.
turn = 0  # Compteur de tours si le nombre est pair cela correspond au joueur 1 si le nombre impair correspond au joueur 2.
game_over = False  # Indique si la partie est terminée. 
                   # False = la partie continue, True = un joueur a gagné ou la grille est pleine.

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
    
    mode_label = tk.Label(root, text="MODE DE JEU", font=("Arial", 74, "bold"))
    mode_label.pack(pady=50)

# Lancer le programme
if __name__ == "__main__":
    main()