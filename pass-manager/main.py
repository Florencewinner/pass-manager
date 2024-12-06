import json
import hashlib
import re
from tkinter import Tk, Button, Toplevel, ttk, StringVar, Label, messagebox, Frame

root = Tk()

def delete_password(name):
    try:
        with open('passwords.json', 'r+', encoding='utf-8') as file:
            existing_data = json.load(file)
            existing_data = [entry for entry in existing_data if entry.get("name") != name]

            file.seek(0)
            json.dump(existing_data, file, indent=4, ensure_ascii=False)
            file.truncate()

            messagebox.showinfo("Удаление", f"Пароль '{name}' успешно удалён.")
            load_passwords()

    except (FileNotFoundError, json.JSONDecodeError) as e:
        messagebox.showerror("Ошибка", "Не удалось загрузить данные.")

password_list_frame = Frame(root, bg='gray22')
password_list_frame.pack(pady=20)

def load_passwords():
    try:
        with open('passwords.json', 'r', encoding='utf-8') as file:
            existing_data = json.load(file)
            # Очистка предыдущих записей
            for widget in password_list_frame.winfo_children():
                widget.destroy()

            for entry in existing_data:
                if isinstance(entry, dict):
                    name = entry.get("name", "Неизвестно")
                    password = entry.get("password", "Неизвестно")
                    
                    # Создаем отдельный Frame для каждого пароля
                    password_frame = Frame(password_list_frame, bg='gray22')
                    password_frame.pack(pady=5)

                    # Отображаем имя
                    name_label = Label(password_frame, text=f"{name}: [Защищено]", bg='gray22', fg='white')
                    name_label.pack(side='left')

                    # Создаем кнопку дешифровки пароля
                    decrypt_button = Button(password_frame, text="Показать", command=lambda p=password: show_password(p))
                    decrypt_button.pack(side='left', padx=5)

                    # Создаем кнопку удаления пароля
                    delete_button = Button(password_frame, text="Удалить", command=lambda n=name: delete_password(n))
                    delete_button.pack(side='left', padx=5)

    except (FileNotFoundError, json.JSONDecodeError):
        password_list.config(text="")
        
def show_password(password):
    messagebox.showinfo("Пароль", f"Пароль: {password}")

def new_pass():
    new = Toplevel(root)
    new.title('Добавить пароль')
    new.geometry('250x250')
    new.config(bg='gray22')
    
    # Метка и поле для ввода пароля
    label = Label(new, text="Введите пароль:")
    label.pack(pady=8)
    
    password_var = StringVar()
    entry = ttk.Entry(new, textvariable=password_var, show='*')
    entry.pack(padx=8, pady=8)

    # Функция показа пароля
    def toggle_password_visibility():
        if entry.cget('show') == '*':
            entry.config(show='')
            toggle_button.config(text='Скрыть пароль')
        else:
            entry.config(show='*')
            toggle_button.config(text='Показать пароль')

    # Кнопка для переключения видимости пароля
    toggle_button = Button(new, text='Показать пароль', command=toggle_password_visibility)
    toggle_button.pack(pady=5)

    # Метка и поле для ввода имени
    nlabel = Label(new, text='Введите имя:')
    nlabel.pack(pady=8)
    
    name_war = StringVar()
    nentry = ttk.Entry(new, textvariable=name_war) 
    nentry.pack(padx=8, pady=8)

    # Проверка ввода имени
    def validate_name_input(event):
        current_value = name_war.get()
        if not re.match("^[a-zA-Z]*$", current_value):
            name_war.set(re.sub("[^a-zA-Z]", "", current_value))

    nentry.bind("<KeyRelease>", validate_name_input)

    def confirm_password():
        name = name_war.get()
        password = password_var.get()
        value = hashlib.sha256(password.encode()).hexdigest()
        data = {
            "password": password,
            "name": name
        }

        # Запись данных в файл
        try:
            with open('passwords.json', 'r+', encoding='utf-8') as file:
                try:
                    existing_data = json.load(file)
                except json.JSONDecodeError:
                    existing_data = []
                existing_data.append(data)
                file.seek(0) 
                json.dump(existing_data, file, indent=4, ensure_ascii=False)
                file.truncate()

        except FileNotFoundError:
            with open('passwords.json', 'w', encoding='utf-8') as file:
                json.dump([data], file, indent=4, ensure_ascii=False)

        new.destroy()
        load_passwords()
        messagebox.showinfo('Успешно', 'Новый пароль успешно добавлен')

    confirm_button = Button(new, text='Подтвердить', command=confirm_password)
    confirm_button.pack(pady=10)

# Основное окно
root.title("Менеджер Паролей")
root.geometry("600x400")
img = 'D:/pass-manager/pass-manager.png'
root.iconbitmap(img)
root.config(bg='gray22')

# Кнопка для добавления пароля
but = Button(
    root,
    text='Добавить пароль',
    command=new_pass
)
but.pack(pady=20)

# Метка для отображения паролей
password_list = Label(root, width=50, font=("Helvetica", 10), bg='gray22', fg='white')
password_list.pack(pady=10)

# Загружаем пароли при запуске приложения
load_passwords()

# Инициализация окна    
root.mainloop()