import pandas as pd
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, font

class NewspaperReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Newspaper Reader")

        # Font styles
        self.title_font = font.Font(family="Times New Roman", size=22, weight="bold")
        self.text_font = font.Font(family="Times New Roman", size=22)

        # Frame for articles list (narrower)
        self.frame_articles = ttk.Frame(root, width=200)
        self.frame_articles.pack(side='left', fill='y')

        # Treeview for articles (narrower)
        self.tree = ttk.Treeview(self.frame_articles, columns=('Date', 'Title'), show='headings')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Title', text='Title')
        self.tree.column('Date', width=80)
        self.tree.column('Title', width=120)
        self.tree.pack(side='left', fill='y', expand=False)

        # Load CSV button
        self.load_btn = ttk.Button(self.frame_articles, text="Load CSV", command=self.load_csv)
        self.load_btn.pack(side='top')

        # Article title and date display (more prominent)
        self.article_title = tk.Label(root, text="", font=self.title_font)
        self.article_title.pack(side='top', fill='x')

        # Scrollable text for article content (more space)
        self.article_content = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=self.text_font)
        self.article_content.pack(side='left', fill='both', expand=True)
        self.article_content.tag_configure("justify", justify='left')
        self.article_content.configure(padx=10, pady=10)

        # Event binding
        self.tree.bind('<<TreeviewSelect>>', self.on_article_select)

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.df = pd.read_csv(file_path)
            self.populate_articles()

    def populate_articles(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for index, row in self.df.iterrows():
            self.tree.insert('', tk.END, values=(row['date'], row['title']))

    def on_article_select(self, event):
        selected_item = self.tree.selection()[0]
        article = self.df.iloc[self.tree.index(selected_item)]
        self.article_title.config(text=f"{article['title']} - {article['date']}")
        self.article_content.delete('1.0', tk.END)
        self.article_content.insert(tk.INSERT, article['text'], "justify")

if __name__ == "__main__":
    root = tk.Tk()
    app = NewspaperReaderApp(root)
    root.mainloop()
