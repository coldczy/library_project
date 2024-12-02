import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class LibrarySystem:
    def __init__(self, root):
        self.root = root
        self.root.title("图书馆管理系统")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # 设置整体样式
        style = ttk.Style()
        style.configure("TNotebook", padding=5)
        style.configure("TButton", padding=5)
        style.configure("TLabel", padding=5)
        style.configure("Treeview", rowheight=25)
        
        # 指定数据库文件的完整路径
        db_path = "E:/code/python_code/liberal/library.db"
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
        
        # 创建主界面
        self.create_gui()
        
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                status TEXT DEFAULT '可借阅'
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS borrowing_records (
                id INTEGER PRIMARY KEY,
                book_id INTEGER,
                borrower_name TEXT,
                borrow_date TEXT,
                return_date TEXT,
                FOREIGN KEY (book_id) REFERENCES books(id)
            )
        ''')
        self.conn.commit()

    def create_gui(self):
        # 创建选项卡
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)
        
        # 添加图书选项卡
        self.add_book_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.add_book_frame, text="添加图书")
        self.create_add_book_widgets()
        
        # 查询图书选项卡
        self.search_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.search_frame, text="查询图书")
        self.create_search_widgets()
        
        # 借阅图书选项卡
        self.borrow_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.borrow_frame, text="借阅/归还")
        self.create_borrow_widgets()
        
        # 添加历史记录选项卡
        self.history_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.history_frame, text="借阅历史")
        self.create_history_widgets()

    def create_add_book_widgets(self):
        # 创建一个主框架来包含所有元素
        main_frame = ttk.Frame(self.add_book_frame, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建输入框框架
        input_frame = ttk.LabelFrame(main_frame, text="添加新图书", padding="10")
        input_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # 重新排列输入控件
        ttk.Label(input_frame, text="书名:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.title_entry = ttk.Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(input_frame, text="作者:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.author_entry = ttk.Entry(input_frame, width=30)
        self.author_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # 添加按钮使用单独的框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        ttk.Button(button_frame, text="添加图书", command=self.add_book).pack()

    def create_search_widgets(self):
        # 创建主框架
        main_frame = ttk.Frame(self.search_frame, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 搜索框架
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(search_frame, text="搜索:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="搜索", command=self.search_books).pack(side=tk.LEFT, padx=5)
        
        # 创建带滚动条的树形视图
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "书名", "作者", "状态"), 
                                show="headings", yscrollcommand=scrollbar.set)
        self.tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)
        
        # 设置列宽
        self.tree.column("ID", width=40)
        self.tree.column("书名", width=150)
        self.tree.column("作者", width=100)
        self.tree.column("状态", width=80)
        
        # 设置列标题
        for col in ("ID", "书名", "作者", "状态"):
            self.tree.heading(col, text=col)

    def create_borrow_widgets(self):
        # 创建主框架
        main_frame = ttk.Frame(self.borrow_frame, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建借阅信息框架
        borrow_frame = ttk.LabelFrame(main_frame, text="借阅/归还信息", padding="10")
        borrow_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # 重新排列输入控件
        ttk.Label(borrow_frame, text="图书ID:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.book_id_entry = ttk.Entry(borrow_frame, width=20)
        self.book_id_entry.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(borrow_frame, text="借阅人:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.borrower_entry = ttk.Entry(borrow_frame, width=20)
        self.borrower_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        ttk.Button(button_frame, text="借阅", command=self.borrow_book).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="归还", command=self.return_book).pack(side=tk.LEFT, padx=10)

    def create_history_widgets(self):
        # 创建主框架
        main_frame = ttk.Frame(self.history_frame, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 搜索框架
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(search_frame, text="搜索借阅人:").pack(side=tk.LEFT, padx=5)
        self.history_search_entry = ttk.Entry(search_frame, width=20)
        self.history_search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="搜索", command=self.search_history).pack(side=tk.LEFT, padx=5)
        
        # 创建带滚动条的树形视图
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 创建树形视图
        self.history_tree = ttk.Treeview(tree_frame, 
            columns=("借阅ID", "图书名称", "借阅人", "借阅日期", "归还日期", "状态"),
            show="headings", 
            yscrollcommand=scrollbar.set)
        
        self.history_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_tree.yview)
        
        # 设置列宽和标题
        columns = {
            "借阅ID": 60,
            "图书名称": 150,
            "借阅人": 100,
            "借阅日期": 100,
            "归还日期": 100,
            "状态": 80
        }
        
        for col, width in columns.items():
            self.history_tree.column(col, width=width)
            self.history_tree.heading(col, text=col)
        
        # 初始加载所有历史记录
        self.load_history()

    def load_history(self):
        # 清空现有显示
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 
                br.id,
                b.title,
                br.borrower_name,
                br.borrow_date,
                br.return_date,
                CASE 
                    WHEN br.return_date IS NULL THEN '未归还'
                    ELSE '已归还'
                END as status
            FROM borrowing_records br
            JOIN books b ON br.book_id = b.id
            ORDER BY br.borrow_date DESC
        """)
        
        for record in cursor.fetchall():
            self.history_tree.insert("", tk.END, values=record)

    def search_history(self):
        search_term = self.history_search_entry.get()
        
        # 清空现有显示
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 
                br.id,
                b.title,
                br.borrower_name,
                br.borrow_date,
                br.return_date,
                CASE 
                    WHEN br.return_date IS NULL THEN '未归还'
                    ELSE '已归还'
                END as status
            FROM borrowing_records br
            JOIN books b ON br.book_id = b.id
            WHERE br.borrower_name LIKE ?
            ORDER BY br.borrow_date DESC
        """, (f"%{search_term}%",))
        
        for record in cursor.fetchall():
            self.history_tree.insert("", tk.END, values=record)

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        
        if title and author:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
            self.conn.commit()
            messagebox.showinfo("成功", "图书添加成功！")
            self.title_entry.delete(0, tk.END)
            self.author_entry.delete(0, tk.END)
        else:
            messagebox.showerror("错误", "请填写完整信息！")

    def search_books(self):
        search_term = self.search_entry.get()
        cursor = self.conn.cursor()
        
        # 清空现有显示
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        cursor.execute("""
            SELECT * FROM books 
            WHERE title LIKE ? OR author LIKE ?
        """, (f"%{search_term}%", f"%{search_term}%"))
        
        for book in cursor.fetchall():
            self.tree.insert("", tk.END, values=book)

    def borrow_book(self):
        book_id = self.book_id_entry.get()
        borrower = self.borrower_entry.get()
        
        if book_id and borrower:
            cursor = self.conn.cursor()
            cursor.execute("SELECT status FROM books WHERE id=?", (book_id,))
            result = cursor.fetchone()
            
            if result and result[0] == "可借阅":
                cursor.execute("UPDATE books SET status=? WHERE id=?", ("已借出", book_id))
                cursor.execute("""
                    INSERT INTO borrowing_records (book_id, borrower_name, borrow_date)
                    VALUES (?, ?, ?)
                """, (book_id, borrower, datetime.now().strftime("%Y-%m-%d")))
                self.conn.commit()
                messagebox.showinfo("成功", "借阅成功！")
                self.load_history()  # 刷新历史记录
            else:
                messagebox.showerror("错误", "该图书不可借阅！")
        else:
            messagebox.showerror("错误", "请填写完整信息！")

    def return_book(self):
        book_id = self.book_id_entry.get()
        
        if book_id:
            cursor = self.conn.cursor()
            cursor.execute("SELECT status FROM books WHERE id=?", (book_id,))
            result = cursor.fetchone()
            
            if result and result[0] == "已借出":
                cursor.execute("UPDATE books SET status=? WHERE id=?", ("可借阅", book_id))
                cursor.execute("""
                    UPDATE borrowing_records 
                    SET return_date=? 
                    WHERE book_id=? AND return_date IS NULL
                """, (datetime.now().strftime("%Y-%m-%d"), book_id))
                self.conn.commit()
                messagebox.showinfo("成功", "归还成功！")
                self.load_history()  # 刷新历史记录
            else:
                messagebox.showerror("错误", "该图书未被借出！")
        else:
            messagebox.showerror("错误", "请输入图书ID！")

if __name__ == "__main__":
    root = tk.Tk()
    app = LibrarySystem(root)
    root.mainloop()
