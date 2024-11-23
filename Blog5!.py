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
        super().__init__()
        self.title("Blog Innovador")
        self.geometry("800x600")
        self.configure(fg_color="#f8f9fa")

        self.current_frame = None
        self.init_ui()

    def init_ui(self):
        # Título de la aplicación
        self.header = ctk.CTkLabel(self, text="Blog Innovador", font=("Times New Roman", 32, "bold"), fg_color="#f8f9fa", text_color="#6c757d")
        self.header.pack(pady=10)

        # Barra de navegación
        self.navbar = ctk.CTkFrame(self, height=50, fg_color="#dee2e6")
        self.navbar.pack(side="top", fill="x")

        self.btn_home = ctk.CTkButton(self.navbar, text="Inicio", command=self.show_home, fg_color="#ced4da", text_color="#495057", hover_color="#adb5bd", font=("Times New Roman", 14))
        self.btn_create_post = ctk.CTkButton(self.navbar, text="Crear Post", command=self.show_create_post, fg_color="#ced4da", text_color="#495057", hover_color="#adb5bd", font=("Times New Roman", 14))
        self.btn_my_posts = ctk.CTkButton(self.navbar, text="Mis Publicaciones", command=self.show_my_posts, fg_color="#ced4da", text_color="#495057", hover_color="#adb5bd", font=("Times New Roman", 14))

        self.btn_home.pack(side="left", padx=10, pady=10)
        self.btn_create_post.pack(side="left", padx=10, pady=10)
        self.btn_my_posts.pack(side="left", padx=10, pady=10)

        # Mostrar la página de inicio al iniciar
        self.show_home()

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

    def show_home(self):
        self.clear_frame()
        self.current_frame = ctk.CTkFrame(self, fg_color="#f8f9fa")
        self.current_frame.pack(fill="both", expand=True)

        title = ctk.CTkLabel(self.current_frame, text="Inicio", font=("Times New Roman", 24, "bold"), text_color="#6c757d")
        title.pack(pady=20)

        conn = sqlite3.connect("blog.db")
        cursor = conn.cursor()
        cursor.execute("SELECT title, content, created_at FROM posts ORDER BY created_at DESC")
        posts = cursor.fetchall()
        conn.close()

        for post in posts:
            post_frame = ctk.CTkFrame(self.current_frame, fg_color="#ffffff", corner_radius=10, padding=10)
            post_frame.pack(pady=10, padx=20, fill="x")

            title_label = ctk.CTkLabel(post_frame, text=post[0], font=("Times New Roman", 16, "bold"), text_color="#343a40")
            title_label.pack(anchor="w")

            content_label = ctk.CTkLabel(post_frame, text=post[1], font=("Times New Roman", 12), text_color="#495057", wraplength=600)
            content_label.pack(anchor="w", pady=5)

            date_label = ctk.CTkLabel(post_frame, text=post[2], font=("Times New Roman", 10), text_color="#868e96")
            date_label.pack(anchor="e")

    def show_create_post(self):
        self.clear_frame()
        self.current_frame = ctk.CTkFrame(self, fg_color="#f8f9fa")
        self.current_frame.pack(fill="both", expand=True)

        title = ctk.CTkLabel(self.current_frame, text="Crear Post", font=("Times New Roman", 24, "bold"), text_color="#6c757d")
        title.pack(pady=20)

        title_label = ctk.CTkLabel(self.current_frame, text="Título:", font=("Times New Roman", 14), text_color="#495057")
        title_label.pack(anchor="w", padx=20, pady=5)
        self.title_entry = ctk.CTkEntry(self.current_frame, width=600, fg_color="#ffffff", corner_radius=10)
        self.title_entry.pack(padx=20, pady=5)

        content_label = ctk.CTkLabel(self.current_frame, text="Contenido:", font=("Times New Roman", 14), text_color="#495057")
        content_label.pack(anchor="w", padx=20, pady=5)
        self.content_text = ctk.CTkTextbox(self.current_frame, height=200, width=600, fg_color="#ffffff", corner_radius=10)
        self.content_text.pack(padx=20, pady=5)

        submit_button = ctk.CTkButton(self.current_frame, text="Publicar", command=self.create_post, fg_color="#adb5bd", text_color="#495057", hover_color="#6c757d", font=("Times New Roman", 14))
        submit_button.pack(pady=20)

    def create_post(self):
        title = self.title_entry.get()
        content = self.content_text.get("1.0", "end").strip()
        if title and content:
            conn = sqlite3.connect("blog.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO posts (title, content, created_at) VALUES (?, ?, ?)",
                           (title, content, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
            conn.close()
            self.show_home()
        else:
            ctk.CTkMessagebox.show_error(title="Error", message="Por favor, completa todos los campos.")

    def show_my_posts(self):
        self.clear_frame()
        self.current_frame = ctk.CTkFrame(self, fg_color="#f8f9fa")
        self.current_frame.pack(fill="both", expand=True)

        title = ctk.CTkLabel(self.current_frame, text="Mis Publicaciones", font=("Times New Roman", 24, "bold"), text_color="#6c757d")
        title.pack(pady=20)

        conn = sqlite3.connect("blog.db")
        cursor = conn.cursor()
        cursor.execute("SELECT title, content, created_at FROM posts ORDER BY created_at DESC")
        posts = cursor.fetchall()
        conn.close()

        for post in posts:
            post_frame = ctk.CTkFrame(self.current_frame, fg_color="#ffffff", corner_radius=10, padding=10)
            post_frame.pack(pady=10, padx=20, fill="x")

            title_label = ctk.CTkLabel(post_frame, text=post[0], font=("Times New Roman", 16, "bold"), text_color="#343a40")
            title_label.pack(anchor="w")

            content_label = ctk.CTkLabel(post_frame, text=post[1], font=("Times New Roman", 12), text_color="#495057", wraplength=600)
            content_label.pack(anchor="w", pady=5)

            date_label = ctk.CTkLabel(post_frame, text=post[2], font=("Times New Roman", 10), text_color="#868e96")
            date_label.pack(anchor="e")

if __name__ == "__main__":
    init_db()
    app = BlogApp()
    app.mainloop()
