import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class ReuniaoEquipeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reunião de Equipe - Gestão de Agentes")
        self.root.geometry("1000x700")
        
        # Configuração de Cores (Dark Mode Premium)
        self.bg_color = "#1e1e2e"
        self.sidebar_color = "#181825"
        self.text_color = "#cdd6f4"
        self.accent_color = "#89b4fa"
        self.save_button_color = "#a6e3a1"
        
        self.root.configure(bg=self.bg_color)
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.base_dir = os.getcwd()
        self.current_file = None
        self.agents = {} # {display_name: absolute_path}
        
        self.setup_ui()
        self.load_agents()

    def setup_ui(self):
        """Inicializa a interface gráfica do usuário (GUI) com layout de painel dividido."""
        # Layout principal: Sidebar (esquerda) e Editor (direita)
        self.paned_window = ttk.Panedwindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # Sidebar
        self.sidebar_frame = tk.Frame(self.paned_window, bg=self.sidebar_color, width=250)
        self.paned_window.add(self.sidebar_frame, weight=1)

        self.label_sidebar = tk.Label(self.sidebar_frame, text="SQUAD DE AGENTES", bg=self.sidebar_color, fg=self.accent_color, font=("Segoe UI", 12, "bold"), pady=10)
        self.label_sidebar.pack(fill=tk.X)

        self.listbox = tk.Listbox(self.sidebar_frame, bg=self.sidebar_color, fg=self.text_color, selectbackground=self.accent_color, borderwidth=0, highlightthickness=0, font=("Segoe UI", 10))
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.listbox.bind("<<ListboxSelect>>", self.on_agent_select)

        # Editor Area
        self.editor_frame = tk.Frame(self.paned_window, bg=self.bg_color)
        self.paned_window.add(self.editor_frame, weight=4)

        # Header do Editor
        self.header_frame = tk.Frame(self.editor_frame, bg=self.bg_color, pady=10)
        self.header_frame.pack(fill=tk.X)

        self.label_current = tk.Label(self.header_frame, text="Selecione um agente para editar", bg=self.bg_color, fg=self.text_color, font=("Segoe UI", 11, "italic"))
        self.label_current.pack(side=tk.LEFT, padx=15)

        self.save_btn = tk.Button(self.header_frame, text="SALVAR ALTERAÇÕES", bg=self.save_button_color, fg="#11111b", font=("Segoe UI", 9, "bold"), relief=tk.FLAT, padx=15, command=self.save_content)
        self.save_btn.pack(side=tk.RIGHT, padx=15)

        # Editor de Texto
        self.text_area = scrolledtext.ScrolledText(self.editor_frame, bg="#11111b", fg=self.text_color, insertbackground="white", font=("Consolas", 11), borderwidth=0, padx=10, pady=10)
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

    def load_agents(self):
        """Busca recursivamente por arquivos .agent.md"""
        self.agents = {}
        self.listbox.delete(0, tk.END)
        
        for root, dirs, files in os.walk(self.base_dir):
            if ".gemini" in root or ".git" in root or ".venv" in root:
                continue
            for file in files:
                if file.endswith(".agent.md"):
                    full_path = os.path.join(root, file)
                    display_name = file.replace(".agent.md", "").replace("_", " ").title()
                    # Tentar extrair o nome real do frontmatter
                    try:
                        with open(full_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if 'name: "' in content:
                                real_name = content.split('name: "')[1].split('"')[0]
                                display_name = f"{real_name} ({file})"
                    except:
                        pass
                    
                    self.agents[display_name] = full_path
                    self.listbox.insert(tk.END, display_name)

    def on_agent_select(self, event):
        selection = self.listbox.curselection()
        if not selection:
            return
        
        display_name = self.listbox.get(selection[0])
        file_path = self.agents[display_name]
        self.current_file = file_path
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.INSERT, content)
                self.label_current.config(text=f"Editando: {os.path.basename(file_path)}", font=("Segoe UI", 11, "bold"))
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o arquivo: {e}")

    def save_content(self):
        if not self.current_file:
            messagebox.showwarning("Aviso", "Selecione um agente primeiro.")
            return
        
        content = self.text_area.get(1.0, tk.END).strip()
        try:
            with open(self.current_file, 'w', encoding='utf-8') as f:
                f.write(content)
            messagebox.showinfo("Sucesso", f"Agente '{os.path.basename(self.current_file)}' atualizado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ReuniaoEquipeApp(root)
    root.mainloop()
