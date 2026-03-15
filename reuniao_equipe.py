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
        """Inicializa a interface gráfica do usuário (GUI) com layout de painel dividido e abas para edição."""
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

        # Editor de Texto - Agora usando Notebook (Abas)
        self.notebook = ttk.Notebook(self.editor_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        self.section_texts = {} # {section_name: text_widget}

    def parse_agent_file(self, content):
        """ Divide o conteúdo do arquivo .agent.md em seções baseadas em headers Markdown. """
        sections = {"Configuração (YAML)": ""}
        
        # Extrair YAML Frontmatter
        import re
        yaml_match = re.match(r'^---\n(.*?)\n---\n?', content, re.DOTALL)
        if yaml_match:
            sections["Configuração (YAML)"] = yaml_match.group(1).strip()
            rest = content[yaml_match.end():].strip()
        else:
            rest = content.strip()
            
        # Dividir por headers ##
        parts = re.split(r'\n(## .*)', "\n" + rest)
        
        # O primeiro elemento pode ser o título principal # Nome
        if parts[0].strip():
            sections["Cabeçalho"] = parts[0].strip()
            
        # Percorrer partes divididas
        current_header = None
        for i in range(1, len(parts)):
            if parts[i].startswith("## "):
                current_header = parts[i].replace("## ", "").strip()
            elif current_header:
                sections[current_header] = parts[i].strip()
                
        return sections

    def create_tabs_for_sections(self, sections):
        """ Cria as abas dinamicamente no Notebook para cada seção do agente. """
        # Limpar abas existentes
        for tab in self.notebook.tabs():
            self.notebook.forget(tab)
        self.section_texts = {}
        
        for section_name, content in sections.items():
            frame = tk.Frame(self.notebook, bg=self.bg_color)
            self.notebook.add(frame, text=section_name)
            
            text_area = scrolledtext.ScrolledText(frame, bg="#11111b", fg=self.text_color, insertbackground="white", font=("Consolas", 11), borderwidth=0, padx=10, pady=10)
            text_area.pack(fill=tk.BOTH, expand=True)
            text_area.insert(tk.INSERT, content)
            
            # Impedir edição da Configuração (YAML) para iniciantes (ou opcional)
            # if section_name == "Configuração (YAML)":
            #     text_area.config(state=tk.DISABLED) # Se quiser travar
                
            self.section_texts[section_name] = text_area

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
                sections = self.parse_agent_file(content)
                self.create_tabs_for_sections(sections)
                self.label_current.config(text=f"Editando: {os.path.basename(file_path)}", font=("Segoe UI", 11, "bold"))
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o arquivo: {e}")

    def save_content(self):
        """Reconstrói o arquivo original a partir das seções editadas e salva no disco."""
        if not self.current_file:
            messagebox.showwarning("Aviso", "Selecione um agente primeiro.")
            return
        
        try:
            # Recompor o conteúdo
            content = ""
            
            # YAML Frontmatter
            if "Configuração (YAML)" in self.section_texts:
                yaml_content = self.section_texts["Configuração (YAML)"].get(1.0, tk.END).strip()
                content += f"---\n{yaml_content}\n---\n\n"
            
            # Cabeçalho (geralmente # Nome do Agente)
            if "Cabeçalho" in self.section_texts:
                header_content = self.section_texts["Cabeçalho"].get(1.0, tk.END).strip()
                content += f"{header_content}\n\n"
            
            # Seções ##
            for section_name, text_widget in self.section_texts.items():
                if section_name in ["Configuração (YAML)", "Cabeçalho"]:
                    continue
                section_content = text_widget.get(1.0, tk.END).strip()
                content += f"## {section_name}\n\n{section_content}\n\n"
            
            with open(self.current_file, 'w', encoding='utf-8') as f:
                f.write(content.strip() + "\n")
            messagebox.showinfo("Sucesso", f"Agente '{os.path.basename(self.current_file)}' atualizado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ReuniaoEquipeApp(root)
    root.mainloop()
