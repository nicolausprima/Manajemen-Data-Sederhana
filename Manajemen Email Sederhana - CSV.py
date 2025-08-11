# Proyek Akhir - Manajemen Email dengan Python

# 1. Mengimport library yang dibutuhkan
import re 
import pandas as pd 

# 2. Membuat Class
class EmailManager:
    def __init__ (self, email, password):
        self.__password = password
        self.email = email

    def get_email(self):
        return self.email

    def get_password(self):
        return self.__password
    
    def set_password(self, new_password):
        if len(new_password) >= 8:
            self.__password = new_password
        else:
            print("Password harus memiliki minimal 8 karakter.")

class Admin(EmailManager):
    def __init__(self, email, password):
        super().__init__(email, password)

    def admin_login(self, admin_key, email, password):
        admin_pass = "admin123"  

        if admin_key == admin_pass:
            return Admin(email, password)
        else:
            print("Kunci admin salah. Akses ditolak.")
            return None
            
    def view_emails_with_pass(self, emails_path = "Emails.csv"):
        list_emails = pd.read_csv(emails_path, header=None)
        print("Daftar Email:")
        print(list_emails)

class User(EmailManager):
    def __init__(self, email, password):
        super().__init__(email, password)
        self.emails_path = "Emails.csv"

    def create_email(self):
        if re.search(r"^[a-zA-Z][\w]+\@gmail\.com$", self.email):
            pd.DataFrame([[self.email, self.get_password()]]).to_csv(self.emails_path, mode='a', header=False, index=False)
            print("Akun email berhasil dibuat.")
        else:
            print("Format email tidak valid.")

    def delete_email(self):
        try:
            list_emails = pd.read_csv(self.emails_path, header=None)
            if self.email in list_emails[0].values:
                list_emails = list_emails[list_emails[0] != self.email]
                list_emails.to_csv(self.emails_path, header=False, index=False)
                print("Akun email berhasil dihapus.")
            else:
                print("Email tidak ditemukan.")
        except FileNotFoundError:
            print("File tidak ditemukan")

    def change_password(self, new_password):    
        list_emails = pd.read_csv(self.emails_path, header=None)
        if self.email in list_emails[0].values:
            if len(new_password) >= 8:
                list_emails.loc[list_emails[0] == self.email, 1] = new_password
                list_emails.to_csv(self.emails_path, header=False, index=False)
                print("Password berhasil diubah.")
            else:
                print("Password harus memiliki minimal 8 karakter.")
        else:
            print("Email tidak ditemukan.")

# 3. Program Utama
while True:
    print("-" * 30)
    print("""Selamat data di Program Manajemen Email
1 - Membuat Akun Email
2 - Menghapus Akun Email
3 - Mengubah Password Email
4 - Melihat Data Email - Admin
5 - Keluar Program""")   
    print("-" * 30)

    input_menu = input("Masukkan pilihan Anda (1-5): ")
    if input_menu == "1":
        input_email = input("Masukkan nama email yang ingin digunakan: ")
        input_password = input("Masukkan password email (minimal 8 karakter): ")
        user = User(input_email, input_password)
        user.create_email()

    elif input_menu == "2":
        input_email = input("Masukkan nama email yang ingin dihapus: ")
        input_password = input("Masukkan password email: ")
        user = User(input_email, input_password)
        user.delete_email()

    elif input_menu == "3":
        input_email = input("Masukkan nama email yang ingin diubah passwordnya: ")
        input_password = input("Masukkan password email lama: ")
        new_password = input("Masukkan password baru (minimal 8 karakter): ")
        user = User(input_email, input_password)
        user.change_password(new_password)

    elif input_menu == "4":
        admin_key = input("Masukkan kunci admin: ")
        input_email = input("Masukkan email admin: ")
        input_password = input("Masukkan password admin: ")
        admin = Admin(input_email, input_password)
        admin_instance = admin.admin_login(admin_key, input_email, input_password)
        
        if admin_instance:
            admin_instance.view_emails_with_pass()

    elif input_menu == "5":
        print("Terima kasih telah menggunakan Program Manajemen Email")
        break

    print("Apakah Anda ingin melanjutkan? (y/n): ")
    if input().lower() != 'y':
        print("Program selesai")
        break