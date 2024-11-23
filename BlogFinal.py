import tkinter as tk
import customtkinter as ctk
import sqlite3
from datetime import datetime

# Configuración de la base de datos SQLite
def init_db():
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

class BlogApp(ctk.CTk):
    def __init__(self):
        super().__init__()  # Inicializa la clase base (CTk)
        self.title("Blog Innovador")  # Título de la ventana
        self.geometry("800x600")  # Tamaño de la ventana
        self.configure(fg_color="#f8f9fa")  # Color de fondo de la ventana

        self.current_frame = None  # Frame actual visible
        self.init_ui()  # Inicializa la interfaz de usuario

    def init_ui(self):
        """
        Inicializa la interfaz de usuario con la barra de navegación y el contenido principal.
        """
        # Título principal de la aplicación
        self.header = ctk.CTkLabel(self, text="Blog Innovador", font=("Times New Roman", 32, "bold"), fg_color="#f8f9fa", text_color="#6c757d")
        self.header.pack(pady=10)

        # Barra de navegación
        self.navbar = ctk.CTkFrame(self, height=50, fg_color="#dee2e6")
        self.navbar.pack(side="top", fill="x")

        # Botones de navegación
        self.btn_home = ctk.CTkButton(self.navbar, text="Inicio", command=self.show_home, fg_color="#ced4da", text_color="#495057", hover_color="#adb5bd", font=("Times New Roman", 14))
        self.btn_create_post = ctk.CTkButton(self.navbar, text="Crear Post", command=self.show_create_post, fg_color="#ced4da", text_color="#495057", hover_color="#adb5bd", font=("Times New Roman", 14))
        self.btn_my_posts = ctk.CTkButton(self.navbar, text="Mis Publicaciones", command=self.show_my_posts, fg_color="#ced4da", text_color="#495057", hover_color="#adb5bd", font=("Times New Roman", 14))

        # Empaquetar los botones de la barra de navegación
        self.btn_home.pack(side="left", padx=10, pady=10)
        self.btn_create_post.pack(side="left", padx=10, pady=10)
        self.btn_my_posts.pack(side="left", padx=10, pady=10)

        # Mostrar la página de inicio al iniciar
        self.show_home()

    def clear_frame(self):
        # Limpia el frame actual de la interfaz para cambiar entre pantallas.
        if self.current_frame:
            self.current_frame.destroy()

    def show_home(self):
        # Muestra la página principal que lista todas las publicaciones del blog.
        self.clear_frame()
        self.current_frame = ctk.CTkFrame(self, fg_color="#f8f9fa")
        self.current_frame.pack(fill="both", expand=True)

        # Título de la página de inicio
        title = ctk.CTkLabel(self.current_frame, text="Inicio", font=("Times New Roman", 24, "bold"), text_color="#6c757d")
        title.pack(pady=20)

        # Obtener todas las publicaciones de la base de datos
        conn = sqlite3.connect("blog.db")
        cursor = conn.cursor()
        cursor.execute("SELECT title, content, created_at FROM posts ORDER BY created_at DESC")
        posts = cursor.fetchall()
        conn.close()

        # Mostrar las publicaciones en el frame
        for post in posts:
            post_frame = ctk.CTkFrame(self.current_frame, fg_color="#ffffff", corner_radius=10)
            post_frame.pack(pady=10, padx=20, fill="x")

            # Título de la publicación
            title_label = ctk.CTkLabel(post_frame, text=post[0], font=("Times New Roman", 16, "bold"), text_color="#343a40")
            title_label.pack(anchor="w")

            # Contenido de la publicación
            content_label = ctk.CTkLabel(post_frame, text=post[1], font=("Times New Roman", 12), text_color="#495057", wraplength=600)
            content_label.pack(anchor="w", pady=5)

            # Fecha de creación de la publicación
            date_label = ctk.CTkLabel(post_frame, text=post[2], font=("Times New Roman", 10), text_color="#868e96")
            date_label.pack(anchor="e")

    def show_create_post(self):
        #Muestra la pantalla para crear una nueva publicación.
        self.clear_frame()
        self.current_frame = ctk.CTkFrame(self, fg_color="#f8f9fa")
        self.current_frame.pack(fill="both", expand=True)

        # Título de la página de crear post
        title = ctk.CTkLabel(self.current_frame, text="Crear Post", font=("Times New Roman", 24, "bold"), text_color="#6c757d")
        title.pack(pady=20)

        # Campo para ingresar el título de la publicación
        title_label = ctk.CTkLabel(self.current_frame, text="Título:", font=("Times New Roman", 14), text_color="#495057")
        title_label.pack(anchor="w", padx=20, pady=5)
        self.title_entry = ctk.CTkEntry(self.current_frame, width=600, fg_color="#ffffff", corner_radius=10)
        self.title_entry.pack(padx=20, pady=5)

        # Campo para ingresar el contenido de la publicación
        content_label = ctk.CTkLabel(self.current_frame, text="Contenido:", font=("Times New Roman", 14), text_color="#495057")
        content_label.pack(anchor="w", padx=20, pady=5)
        self.content_text = ctk.CTkTextbox(self.current_frame, height=200, width=600, fg_color="#ffffff", corner_radius=10)
        self.content_text.pack(padx=20, pady=5)

        # Botón para publicar la nueva entrada
        submit_button = ctk.CTkButton(self.current_frame, text="Publicar", command=self.create_post, fg_color="#adb5bd", text_color="#495057", hover_color="#6c757d", font=("Times New Roman", 14))
        submit_button.pack(pady=20)

    def create_post(self):
        #Crea una nueva publicación en la base de datos con los datos del formulario
        title = self.title_entry.get() # Obtener el título ingresado
        content = self.content_text.get("1.0", "end").strip() # Obtener el contenido ingresado
        if title and content:
            conn = sqlite3.connect("blog.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO posts (title, content, created_at) VALUES (?, ?, ?)",
                           (title, content, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))) # Insertar en la base de datos
            conn.commit()
            conn.close()
            self.show_home() # Actualizar la vista para mostrar la nueva publicación
        else:
            tk.messagebox.showerror("Error", "Por favor, completa todos los campos.")

    def show_my_posts(self):
        self.clear_frame()
        self.current_frame = ctk.CTkFrame(self, fg_color="#f8f9fa")
        self.current_frame.pack(fill="both", expand=True)

        title = ctk.CTkLabel(self.current_frame, text="Mis Publicaciones", font=("Times New Roman", 24, "bold"), text_color="#6c757d")
        title.pack(pady=20)

        conn = sqlite3.connect("blog.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, content, created_at FROM posts ORDER BY created_at DESC")
        posts = cursor.fetchall()
        conn.close()

        for post in posts:
            post_frame = ctk.CTkFrame(self.current_frame, fg_color="#ffffff", corner_radius=10)
            post_frame.pack(pady=10, padx=20, fill="x")

            title_label = ctk.CTkLabel(post_frame, text=post[1], font=("Times New Roman", 16, "bold"), text_color="#343a40")
            title_label.pack(anchor="w")

            content_label = ctk.CTkLabel(post_frame, text=post[2], font=("Times New Roman", 12), text_color="#495057", wraplength=600)
            content_label.pack(anchor="w", pady=5)

            date_label = ctk.CTkLabel(post_frame, text=post[3], font=("Times New Roman", 10), text_color="#868e96")
            date_label.pack(anchor="e")

            # Botones de editar y eliminar
            edit_button = ctk.CTkButton(post_frame, text="Editar", command=lambda post_id=post[0]: self.show_edit_post(post_id), fg_color="#6c757d", text_color="#ffffff", hover_color="#e0a800", font=("Times New Roman", 12))
            edit_button.pack(padx=10, pady=10, side="left")

            delete_button = ctk.CTkButton(post_frame, text="Eliminar", command=lambda post_id=post[0]: self.delete_post(post_id), fg_color="#6c757d", text_color="#ffffff", hover_color="#c82333", font=("Times New Roman", 12))
            delete_button.pack(padx=10, pady=10, side="right")

    def show_edit_post(self, post_id):
        """
        Muestra la pantalla para editar una publicación.
        """
        self.clear_frame()
        self.current_frame = ctk.CTkFrame(self, fg_color="#f8f9fa")
        self.current_frame.pack(fill="both", expand=True)

        conn = sqlite3.connect("blog.db")
        cursor = conn.cursor()
        cursor.execute("SELECT title, content FROM posts WHERE id = ?", (post_id,))
        post = cursor.fetchone()
        conn.close()

        title = ctk.CTkLabel(self.current_frame, text="Editar Publicación", font=("Times New Roman", 24, "bold"), text_color="#6c757d")
        title.pack(pady=20)

        title_label = ctk.CTkLabel(self.current_frame, text="Título:", font=("Times New Roman", 14), text_color="#495057")
        title_label.pack(anchor="w", padx=20, pady=5)
        self.edit_title_entry = ctk.CTkEntry(self.current_frame, width=600, fg_color="#ffffff", corner_radius=10)
        self.edit_title_entry.insert(0, post[0])  # Cargar título actual
        self.edit_title_entry.pack(padx=20, pady=5)

        content_label = ctk.CTkLabel(self.current_frame, text="Contenido:", font=("Times New Roman", 14), text_color="#495057")
        content_label.pack(anchor="w", padx=20, pady=5)
        self.edit_content_text = ctk.CTkTextbox(self.current_frame, height=200, width=600, fg_color="#ffffff", corner_radius=10)
        self.edit_content_text.insert("1.0", post[1])  # Cargar contenido actual
        self.edit_content_text.pack(padx=20, pady=5)

        submit_button = ctk.CTkButton(self.current_frame, text="Guardar Cambios", command=lambda: self.update_post(post_id), fg_color="#6c757d", text_color="#ffffff", hover_color="#218838", font=("Times New Roman", 14))
        submit_button.pack(pady=20)

    def update_post(self, post_id):
        title = self.edit_title_entry.get()
        content = self.edit_content_text.get("1.0", "end").strip()
        if title and content:
            conn = sqlite3.connect("blog.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE posts SET title = ?, content = ? WHERE id = ?", (title, content, post_id))
            conn.commit()
            conn.close()
            self.show_my_posts()  # Actualizar vista
        else:
            tk.messagebox.showerror("Error", "Por favor, completa todos los campos.")

    def delete_post(self, post_id):
        conn = sqlite3.connect("blog.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        conn.commit()
        conn.close()
        self.show_my_posts()  # Actualizar vista

# Ejecutar la aplicación
if __name__ == "__main__":
    app = BlogApp()
    init_db()  # Inicializar base de datos
    app.mainloop()
