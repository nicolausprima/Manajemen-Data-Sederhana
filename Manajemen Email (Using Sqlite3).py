import re
import sqlite3

conn = sqlite3.connect("emails.db")
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS emails (
    email TEXT PRIMARY KEY,
    password TEXT
)
""")
conn.commit()

def validate_email(email):
    return re.match(r"^[a-zA-Z][\w\.-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$", email)

class EmailManager:
    def __init__(self, email, password):
        self.__password = password
        self.email = email

    def get_email(self):
        return self.email

    def get_password(self):
        return self.__password

class Admin(EmailManager):
    ADMIN_KEY = "admin123"

    def admin_login(self, admin_key):
        return admin_key == self.ADMIN_KEY

    def view_all_emails(self):
        cur.execute("SELECT email, password FROM emails")
        rows = cur.fetchall()
        if rows:
            print("\nDaftar Email Terdaftar:")
            for email, pwd in rows:
                print(f"- {email} | {pwd}")
        else:
            print("Belum ada akun yang terdaftar.")

class User(EmailManager):
    def create_account(self):
        if not validate_email(self.email):
            print("Format email tidak valid.")
            return
        cur.execute("SELECT * FROM emails WHERE email=?", (self.email,))
        if cur.fetchone():
            print("Email sudah digunakan.")
            return
        cur.execute("INSERT INTO emails VALUES (?, ?)", (self.email, self.get_password()))
        conn.commit()
        print("Akun email berhasil dibuat.")

    def login(self):
        cur.execute("SELECT password FROM emails WHERE email=?", (self.email,))
        result = cur.fetchone()
        if result and result[0] == self.get_password():
            return True
        return False

    def delete_account(self):
        cur.execute("DELETE FROM emails WHERE email=?", (self.email,))
        conn.commit()
        print("Akun berhasil dihapus.")

    def change_password(self, new_password):
        if len(new_password) < 8:
            print("Password harus minimal 8 karakter.")
            return
        cur.execute("UPDATE emails SET password=? WHERE email=?",
                    (new_password, self.email))
        conn.commit()
        print("Password berhasil diubah.")

def menu_create_account():
    email = input("Masukkan email: ")
    password = input("Masukkan password (minimal 8 karakter): ")
    if len(password) < 8:
        print("Password terlalu pendek.")
        return
    user = User(email, password)
    user.create_account()

def menu_delete_account():
    email = input("Masukkan email: ")
    password = input("Masukkan password: ")
    user = User(email, password)
    if user.login():
        user.delete_account()
    else:
        print("Login gagal.")

def menu_change_password():
    email = input("Masukkan email: ")
    password = input("Masukkan password lama: ")
    user = User(email, password)
    if user.login():
        new_password = input("Masukkan password baru: ")
        user.change_password(new_password)
    else:
        print("Login gagal.")

def menu_admin_view():
    email = input("Masukkan email admin: ")
    password = input("Masukkan password admin: ")
    admin_key = input("Masukkan kunci admin: ")

    admin = Admin(email, password)
    if admin.admin_login(admin_key):
        admin.view_all_emails()
    else:
        print("Kunci admin salah.")

while True:
    print("\n" + "-" * 40)
    print("""Program Manajemen Email
1 - Membuat Akun Email
2 - Menghapus Akun Email
3 - Mengubah Password Email
4 - Melihat Data Email - Admin
5 - Keluar""")
    print("-" * 40)

    pilihan = input("Masukkan pilihan (1-5): ")

    if pilihan == "1":
        menu_create_account()
    elif pilihan == "2":
        menu_delete_account()
    elif pilihan == "3":
        menu_change_password()
    elif pilihan == "4":
        menu_admin_view()
    elif pilihan == "5":
        print("Terima kasih telah menggunakan program ini.")
        break
    else:
        print("Pilihan tidak valid.")

