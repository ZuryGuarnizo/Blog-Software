import tkinter as tk
from tkinter import messagebox

# Crear la ventana principal
root = tk.Tk()
root.title("Galileo Design")
root.geometry("480x640")
root.config(bg="#f8fafc")

# Crear un marco para el contenido principal
main_frame = tk.Frame(root, bg="#f8fafc")
main_frame.pack(fill="both", expand=True)

# Función para manejar el botón de cerrar
def on_close_button_click():
    messagebox.showinfo("Cerrar", "Cerrando la aplicación...")

# Botón de cerrar (simula el botón con icono)
close_button = tk.Button(main_frame, text="X", font=("Arial", 16), bg="#f8fafc", fg="#0e141b", command=on_close_button_click)
close_button.pack(side="top", anchor="ne", padx=10, pady=10)

# Título "Post"
title_label = tk.Label(main_frame, text="Post", font=("Newsreader", 28, "bold"), fg="#0e141b", bg="#f8fafc")
title_label.pack(pady=10)

# Campo de búsqueda (simulando el input de búsqueda)
search_entry = tk.Entry(main_frame, font=("Arial", 14), bd=2, relief="solid", width=40)
search_entry.insert(0, "Search")
search_entry.pack(pady=20)

# Barra de navegación
navbar = tk.Frame(main_frame, bg="#f8fafc")
navbar.pack(side="bottom", fill="x", pady=20)

# Funciones para cada opción del menú
def on_nav_button_click(text):
    messagebox.showinfo("Navegación", f"Has clickeado en: {text}")

# Crear botones de navegación
buttons_text = ["Home", "Create Post", "My Posts", "Profile"]
for text in buttons_text:
    btn = tk.Button(navbar, text=text, font=("Arial", 12, "bold"), bg="#f8fafc", fg="#4e7397", command=lambda t=text: on_nav_button_click(t))
    btn.pack(side="left", padx=10)

# Ejecutar el bucle principal de la aplicación
root.mainloop()
