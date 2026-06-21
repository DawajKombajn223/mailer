"""Prosty graficzny runner testów (Tkinter).

Funkcje:
- Wykrywa pliki w `tests/` zaczynające się od `test_`.
- Pozwala uruchomić wybrane testy lub wszystkie.
- Wyświetla output pytest w oknie.
- Pozwala uruchomić generator dokumentacji `.agents/agent_executor.py`.

Uruchomienie:
    python test_runner_gui.py

"""
import os
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

ROOT = os.path.dirname(__file__)
TESTS_DIR = os.path.join(ROOT, 'tests')
AGENT_EXEC = os.path.join(ROOT, '.agents', 'agent_executor.py')


class TestRunnerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Test Runner GUI')
        self.geometry('900x600')

        self.create_widgets()
        self.refresh_test_list()

    def create_widgets(self):
        main_pane = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        main_pane.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(main_pane, width=300)
        right_frame = ttk.Frame(main_pane)
        main_pane.add(left_frame, weight=1)
        main_pane.add(right_frame, weight=3)

        # Left: tests list and controls
        ttk.Label(left_frame, text='Pliki testowe').pack(anchor='w', padx=8, pady=4)
        self.test_listbox = tk.Listbox(left_frame, selectmode=tk.EXTENDED)
        self.test_listbox.pack(fill=tk.BOTH, expand=True, padx=8)

        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill=tk.X, padx=8, pady=8)
        ttk.Button(btn_frame, text='Odśwież', command=self.refresh_test_list).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text='Wybierz wszystko', command=self.select_all).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text='Uruchom wybrane', command=self.run_selected).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text='Uruchom wszystkie', command=self.run_all).pack(side=tk.LEFT, padx=4)

        # Docs / executor
        doc_frame = ttk.Frame(left_frame)
        doc_frame.pack(fill=tk.X, padx=8, pady=4)
        ttk.Button(doc_frame, text='Generuj docs (executor)', command=self.run_executor).pack(side=tk.LEFT)
        ttk.Button(doc_frame, text='Otwórz docs/', command=self.open_docs_folder).pack(side=tk.LEFT, padx=4)

        # Right: output
        ttk.Label(right_frame, text='Output').pack(anchor='w', padx=8, pady=4)
        self.output_text = tk.Text(right_frame, wrap=tk.NONE)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=8)

        out_btns = ttk.Frame(right_frame)
        out_btns.pack(fill=tk.X, padx=8, pady=4)
        ttk.Button(out_btns, text='Wyczyść', command=lambda: self.output_text.delete('1.0', tk.END)).pack(side=tk.LEFT)

    def refresh_test_list(self):
        self.test_listbox.delete(0, tk.END)
        if not os.path.isdir(TESTS_DIR):
            return
        for name in sorted(os.listdir(TESTS_DIR)):
            if name.startswith('test_') and name.endswith('.py'):
                self.test_listbox.insert(tk.END, os.path.join('tests', name))

    def select_all(self):
        self.test_listbox.select_set(0, tk.END)

    def run_selected(self):
        sel = [self.test_listbox.get(i) for i in self.test_listbox.curselection()]
        if not sel:
            messagebox.showinfo('Brak zaznaczeń', 'Wybierz przynajmniej jeden plik testowy.')
            return
        self._run_pytest(sel)

    def run_all(self):
        self._run_pytest(['tests'])

    def run_executor(self):
        if not os.path.exists(AGENT_EXEC):
            messagebox.showerror('Brak executor', f'Nie znaleziono {AGENT_EXEC}')
            return
        def target():
            self.append_output(f'Uruchamiam executor: {AGENT_EXEC} --module validators\n')
            proc = subprocess.Popen([sys_executable(), AGENT_EXEC, '--module', 'validators'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in proc.stdout:
                self.append_output(line)
            proc.wait()
            self.append_output(f'Executor zakończony z kodem {proc.returncode}\n')
        threading.Thread(target=target, daemon=True).start()

    def open_docs_folder(self):
        docs = os.path.join(ROOT, 'docs')
        if not os.path.exists(docs):
            messagebox.showinfo('Brak docs', 'Folder docs/ nie istnieje jeszcze.')
            return
        try:
            if os.name == 'nt':
                os.startfile(docs)
            else:
                subprocess.run(['xdg-open', docs])
        except Exception as e:
            messagebox.showerror('Błąd', str(e))

    def _run_pytest(self, targets):
        def target():
            cmd = [sys_executable(), '-m', 'pytest', '-q'] + targets
            self.append_output('Uruchamiam: ' + ' '.join(cmd) + '\n')
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            for line in proc.stdout:
                self.append_output(line)
            proc.wait()
            self.append_output(f'pytest zakończony z kodem {proc.returncode}\n')
        threading.Thread(target=target, daemon=True).start()

    def append_output(self, text):
        self.output_text.insert(tk.END, text)
        self.output_text.see(tk.END)


def sys_executable():
    import sys
    return sys.executable


if __name__ == '__main__':
    app = TestRunnerGUI()
    app.mainloop()
