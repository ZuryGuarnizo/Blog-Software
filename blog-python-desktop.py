import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sqlite3
from datetime import datetime
import hashlib
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import customtkinter as ctk

class ModernBlogApp:
    def __init__(self):
        self.root = ThemedTk(theme="arc")
        self.root.title("Blog - Innova y Emprende")
        self.root.geometry("1200x800")
        
        # Configurar el estilo
        self.style = ttk.Style()
        self.style.configure('Modern.TFrame', background='#ffffff')
        self.style.configure('Modern.TLabel', background='#ffffff', foreground='#333333')
        self.style.configure('Header.TLabel', font=('Helvetica', 16, 'bold'))
        self.style.configure('Tag.TLabel', background='#e8f0fe', padding=5)
        
        # Usuario actual
        self.current_user = None
        
        # Inicializar base de datos
        self.init_database()
        
        # Crear el contenedor principal
        self.main_container = ttk.Frame(self.root, style='Modern.TFrame')
        self.main_container.pack(fill='both', expand=True)
        
        # Crear la barra de navegación
        self.create_navbar()
        
        # Crear los diferentes frames
        self.frames = {}
        for F in (HomeFrame, WritePostFrame, EditPostFrame, ViewPostFrame):
            frame = F(parent=self.main_container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Mostrar el frame inicial
        self.show_frame('HomeFrame')

    def create_navbar(self):
        """Crear barra de navegación moderna"""
        navbar = ttk.Frame(self.main_container, style='Modern.TFrame')
        navbar.pack(fill='x', padx=20, pady=10)
        
        # Logo/Título
        ttk.Label(navbar, text="Blog", style='Header.TLabel').pack(side='left')
        
        # Barra de búsqueda
        self.search_var = tk.StringVar()
        search_entry = ctk.CTkEntry(
            navbar,
            placeholder_text="Buscar...",
            width=300,
            height=35
        )
        search_entry.pack(side='left', padx=20)
        
        # Botones de navegación
        nav_buttons = ttk.Frame(navbar, style='Modern.TFrame')
        nav_buttons.pack(side='right')
        
        buttons = [
            ("Home", lambda: self.show_frame('HomeFrame')),
            ("Crear Post", lambda: self.show_frame('WritePostFrame')),
            ("Mis Posts", lambda: self.show_frame('ViewPostFrame')),
            ("Perfil", lambda: self.show_frame('ProfileFrame'))
        ]
        
        for text, command in buttons:
            ctk.CTkButton(
                nav_buttons,
                text=text,
                command=command,
                width=120,
                height=35,
                fg_color="#ffffff",
                text_color="#333333",
                hover_color="#e8f0fe"
            ).pack(side='left', padx=5)

    def show_frame(self, frame_name):
        """Mostrar el frame seleccionado"""
        frame = self.frames[frame_name]
        frame.tkraise()

class HomeFrame(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, style='Modern.TFrame')
        self.controller = controller
        
        # Contenedor de posts
        self.posts_container = ttk.Frame(self, style='Modern.TFrame')
        self.posts_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.refresh_posts()

    def refresh_posts(self):
        """Actualizar lista de posts con diseño moderno"""
        for widget in self.posts_container.winfo_children():
            widget.destroy()
        
        conn = sqlite3.connect('blog.db')
        c = conn.cursor()
        
        c.execute('''
            SELECT posts.*, users.username 
            FROM posts 
            JOIN users ON posts.user_id = users.id 
            ORDER BY posts.created_at DESC
        ''')
        posts = c.fetchall()
        
        for post in posts:
            post_frame = ttk.Frame(self.posts_container, style='Modern.TFrame')
            post_frame.pack(fill='x', pady=10)
            
            # Contenedor de información del post
            info_frame = ttk.Frame(post_frame, style='Modern.TFrame')
            info_frame.pack(fill='x', padx=10)
            
            # Título
            ttk.Label(
                info_frame,
                text=post[1],
                font=('Helvetica', 14, 'bold'),
                wraplength=800
            ).pack(anchor='w')
            
            # Metadata
            ttk.Label(
                info_frame,
                text=f"Por {post[4]} • {post[3][:16]}",
                foreground='#666666'
            ).pack(anchor='w')
            
            # Tags
            tags_frame = ttk.Frame(info_frame, style='Modern.TFrame')
            tags_frame.pack(anchor='w', pady=5)
            
            for tag in ['Emprendimiento', 'Negocios', 'Startup']:
                tag_label = ttk.Label(
                    tags_frame,
                    text=tag,
                    style='Tag.TLabel'
                )
                tag_label.pack(side='left', padx=2)
            
            # Preview del contenido
            content = post[2][:300] + "..." if len(post[2]) > 300 else post[2]
            ttk.Label(
                info_frame,
                text=content,
                wraplength=800,
                justify='left'
            ).pack(anchor='w', pady=10)
            
            # Botones de acción
            actions_frame = ttk.Frame(info_frame, style='Modern.TFrame')
            actions_frame.pack(fill='x', pady=5)
            
            ctk.CTkButton(
                actions_frame,
                text="Leer más",
                width=120,
                height=32,
                fg_color="#007bff",
                hover_color="#0056b3"
            ).pack(side='left')
            
            ttk.Separator(self.posts_container).pack(fill='x', pady=10)
        
        conn.close()

class WritePostFrame(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent, style='Modern.TFrame')
        self.controller = controller
        
        # Contenedor principal
        main_content = ttk.Frame(self, style='Modern.TFrame')
        main_content.pack(fill='both', expand=True, padx=40, pady=20)
        
        # Título
        ttk.Label(
            main_content,
            text="Escribe un nuevo post",
            font=('Helvetica', 20, 'bold')
        ).pack(anchor='w', pady=(0, 20))
        
        # Campo de título
        self.title_entry = ctk.CTkEntry(
            main_content,
            placeholder_text="Título",
            width=800,
            height=45
        )
        self.title_entry.pack(fill='x', pady=10)
        
        # Campo de tags
        self.tags_entry = ctk.CTkEntry(
            main_content,
            placeholder_text="Agregar tags (separados por coma)",
            width=800,
            height=45
        )
        self.tags_entry.pack(fill='x', pady=10)
        
        # Editor de contenido
        self.content_editor = scrolledtext.ScrolledText(
            main_content,
            height=15,
            font=('Helvetica', 12)
        )
        self.content_editor.pack(fill='both', expand=True, pady=10)
        
        # Botones de acción
        buttons_frame = ttk.Frame(main_content, style='Modern.TFrame')
        buttons_frame.pack(fill='x', pady=20)
        
        ctk.CTkButton(
            buttons_frame,
            text="Vista previa",
            width=120,
            height=35,
            fg_color="#6c757d",
            hover_color="#5a6268"
        ).pack(side='left', padx=5)
        
        ctk.CTkButton(
            buttons_frame,
            text="Publicar",
            width=120,
            height=35,
            fg_color="#28a745",
            hover_color="#218838",
            command=self.publish_post
        ).pack(side='left', padx=5)

    def publish_post(self):
        """Publicar nuevo post"""
        if not self.controller.current_user:
            messagebox.showerror("Error", "Debes iniciar sesión primero")
            return
        
        title = self.title_entry.get()
        content = self.content_editor.get('1.0', tk.END)
        tags = self.tags_entry.get()
        
        if not title or not content.strip():
            messagebox.showerror("Error", "El título y contenido son obligatorios")
            return
        
        conn = sqlite3.connect('blog.db')
        c = conn.cursor()
        
        try:
            c.execute('''
                INSERT INTO posts (title, content, user_id, created_at, tags)
                VALUES (?, ?, ?, ?, ?)
            ''', (title, content, self.controller.current_user['id'], 
                  datetime.now(), tags))
            conn.commit()
            messagebox.showinfo("Éxito", "Post publicado correctamente")
            
            # Limpiar campos
            self.title_entry.delete(0, tk.END)
            self.content_editor.delete('1.0', tk.END)
            self.tags_entry.delete(0, tk.END)
            
            # Volver a la página principal
            self.controller.show_frame('HomeFrame')
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al publicar: {str(e)}")
        
        finally:
            conn.close()

if __name__ == '__main__':
    app = ModernBlogApp()
    app.root.mainloop()
