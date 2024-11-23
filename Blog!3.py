import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
from datetime import datetime
from ttkthemes import ThemedTk
import customtkinter as ctk


class ModernBlogApp:
    def __init__(self):
        self.root = ThemedTk(theme="arc")
        self.root.title("Blog - Innova y Emprende")
        self.root.geometry("1200x800")
        self.root.configure(bg="#faf3e0")  # Fondo pastel

        # Configurar estilo
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#faf3e0")
        self.style.configure("TLabel", background="#faf3e0", foreground="#6c757d")
        self.style.configure("Header.TLabel", font=("Helvetica", 20, "bold"))
        self.style.configure("Tag.TLabel", background="#eaf7f7", padding=5)

        # Inicializar base de datos
        self.init_database()

        # Crear el contenedor principal
        self.main_container = ttk.Frame(self.root, style="TFrame")
        self.main_container.grid(row=0, column=0, sticky="nsew")

        # Configuración de filas y columnas en el contenedor principal
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.main_container.rowconfigure(0, weight=1)
        self.main_container.columnconfigure(0, weight=1)

        # Crear barra de navegación
        self.create_navbar()

        # Crear los frames principales
        self.frames = {}
        for F in (HomeFrame, WritePostFrame, MyPostsFrame):  # Agregar MyPostsFrame
            frame = F(parent=self.main_container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Mostrar el frame inicial
        self.show_frame("HomeFrame")

    def init_database(self):
        """Inicializar la base de datos SQLite."""
        print("Inicializando base de datos...")
        conn = sqlite3.connect("blog.db")
        c = conn.cursor()

        # Crear tabla para los posts
        c.execute('''CREATE TABLE IF NOT EXISTS posts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        content TEXT NOT NULL,
                        created_at TEXT NOT NULL
                    )''')
        conn.commit()
        conn.close()

    def create_navbar(self):
        """Crear barra de navegación."""
        navbar = ttk.Frame(self.root, style="TFrame")
        navbar.grid(row=0, column=0, sticky="nsew", pady=10)

        # Título
        ttk.Label(navbar, text="Blog Innovador", style="Header.TLabel").grid(row=0, column=0, padx=20)

        # Botones de navegación
        buttons = [
            ("Inicio", lambda: self.show_frame("HomeFrame")),
            ("Crear Post", lambda: self.show_frame("WritePostFrame")),
            ("Mis Publicaciones", lambda: self.show_frame("MyPostsFrame")),  # Botón Mis Publicaciones
        ]

        for idx, (text, command) in enumerate(buttons):
            ctk.CTkButton(
                navbar,
                text=text,
                command=command,
                width=120,
                height=35,
                fg_color="#c8e6c9",  # Verde menta pastel
                hover_color="#b2dfdb",  # Turquesa suave
                text_color="#6c757d",
            ).grid(row=0, column=idx + 1, padx=10)

    def show_frame(self, frame_name):
        """Cambiar entre frames."""
        frame = self.frames[frame_name]
        frame.tkraise()


class HomeFrame(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, style="TFrame")
        self.controller = controller

        ttk.Label(self, text="Inicio", style="Header.TLabel").pack(pady=20)

        self.posts_container = ttk.Frame(self, style="TFrame")
        self.posts_container.pack(fill="both", expand=True, padx=20, pady=20)

        self.refresh_posts()

    def refresh_posts(self):
        """Actualizar y mostrar todos los posts."""
        for widget in self.posts_container.winfo_children():
            widget.destroy()

        conn = sqlite3.connect("blog.db")
        c = conn.cursor()
        c.execute("SELECT * FROM posts ORDER BY created_at DESC")
        posts = c.fetchall()
        conn.close()

        for post in posts:
            post_frame = ttk.Frame(self.posts_container, style="TFrame")
            post_frame.pack(fill="x", pady=10)

            ttk.Label(post_frame, text=post[1], font=("Helvetica", 16, "bold")).pack(anchor="w", pady=5)
            ttk.Label(post_frame, text=post[3], foreground="#7f8c8d").pack(anchor="w")
            ttk.Label(post_frame, text=post[2], wraplength=800, justify="left").pack(anchor="w", pady=10)


class WritePostFrame(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, style="TFrame")
        self.controller = controller

        ttk.Label(self, text="Escribir un Nuevo Post", style="Header.TLabel").pack(pady=20)

        self.title_entry = ctk.CTkEntry(
            self,
            placeholder_text="Título del post",
            width=800,
            height=45,
            fg_color="#fce4ec",  # Rosa pastel
            text_color="#6c757d",
        )
        self.title_entry.pack(pady=10)

        self.content_editor = scrolledtext.ScrolledText(self, height=15, font=("Helvetica", 12))
        self.content_editor.pack(pady=10, fill="both", expand=True)

        publish_button = ctk.CTkButton(
            self,
            text="Publicar",
            fg_color="#ffccbc",  # Durazno pastel
            hover_color="#ffe0b2",  # Amarillo suave
            text_color="#6c757d",
            width=120,
            height=35,
            command=self.publish_post,
        )
        publish_button.pack(pady=20)

    def publish_post(self):
        """Guardar un nuevo post en la base de datos."""
        title = self.title_entry.get()
        content = self.content_editor.get("1.0", tk.END).strip()

        if not title or not content:
            messagebox.showerror("Error", "El título y el contenido no pueden estar vacíos.")
            return

        conn = sqlite3.connect("blog.db")
        c = conn.cursor()
        c.execute(
            "INSERT INTO posts (title, content, created_at) VALUES (?, ?, ?)",
            (title, content, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "¡Post publicado correctamente!")
        self.title_entry.delete(0, tk.END)
        self.content_editor.delete("1.0", tk.END)
        self.controller.show_frame("HomeFrame")


class MyPostsFrame(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, style="TFrame")
        self.controller = controller

        ttk.Label(self, text="Mis Publicaciones", style="Header.TLabel").pack(pady=20)

        self.posts_container = ttk.Frame(self, style="TFrame")
        self.posts_container.pack(fill="both", expand=True, padx=20, pady=20)

        self.refresh_my_posts()

    def refresh_my_posts(self):
        """Actualizar y mostrar las publicaciones del usuario."""
        for widget in self.posts_container.winfo_children():
            widget.destroy()

        conn = sqlite3.connect("blog.db")
        c = conn.cursor()
        c.execute("SELECT * FROM posts ORDER BY created_at DESC")
        posts = c.fetchall()
        conn.close()

        for post in posts:
            post_frame = ttk.Frame(self.posts_container, style="TFrame")
            post_frame.pack(fill="x", pady=10)

            ttk.Label(post_frame, text=post[1], font=("Helvetica", 16, "bold")).pack(anchor="w", pady=5)
            ttk.Label(post_frame, text=post[3], foreground="#7f8c8d").pack(anchor="w")
            ttk.Label(post_frame, text=post[2], wraplength=800, justify="left").pack(anchor="w", pady=10)


if __name__ == "__main__":
    app = ModernBlogApp()
    app.root.mainloop()
