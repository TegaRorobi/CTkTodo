'''
Developer : Tega Andrew Rorobi
email   : rorobitega@gmail.com
twitter : @Tega_Rorobi
github  : https://github.com/TegaRorobi
last_modidified: 
''' 

import customtkinter as ctk


class TodoApp(ctk.CTk):

	default_appearance_mode = 'Dark'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		ctk.set_appearance_mode(self.default_appearance_mode)
		ctk.set_default_color_theme('green')

		# Configuring the window
		self.title("A Customtkinter todo app made by Deciphrexx Labs. Inc.")
		self.geometry("600x400")
		# self.resizable(0, 0)

		self.build_app()

	def build_app(self):
		self.grid_columnconfigure(0, weight=1)
		self.grid_rowconfigure(0, weight=1)

		self.prepare_login_frame()
		self.prepare_main_frame()

		self.login_frame.grid(row=0, column=0, sticky='nsew', padx=90, pady=30)
		# self.main_frame.grid(row=0, column=0, sticky='nsew') # show the main frame

	def prepare_login_frame(self):
		self.login_frame = ctk.CTkFrame(master=self, corner_radius=0)
		self.login_frame.grid_columnconfigure((0), weight=1)

		self.welcome_label = ctk.CTkLabel(master=self.login_frame, text='Welcome!', font=('Fira Code', 40))
		self.welcome_label.grid(row=0, column=0, pady=(20, 15), columnspan=2, sticky='nsew')

		# username_label = ctk.CTkLabel(master=self.login_frame, text='Username:', font=('Fira Code', 15))
		# username_label.grid(row=1, column=0, pady=20, padx=15, sticky='nsew')

		self.username_entry = ctk.CTkEntry(master=self.login_frame, font=('Fira Code', 15), placeholder_text='Username')
		self.username_entry.grid(row=1, column=0, pady=15, padx=120, sticky='nsew')

		# password_label = ctk.CTkLabel(master=self.login_frame, text='Password:', font=('Fira Code', 15))
		# password_label.grid(row=2, column=0, pady=20, padx=15, sticky='nsew')

		self.password_entry = ctk.CTkEntry(master = self.login_frame, show='X', font=('Fira Code', 15), placeholder_text='Password')
		self.password_entry.grid(row=2, column=0, pady=15, padx=120, sticky='nsew')

		self.login_btn = ctk.CTkButton(master=self.login_frame, text='Login', font=('Fira Code', 15), command=self.login)
		self.login_btn.grid(row=3, column=0, columnspan=2, padx=120, pady=15, sticky='nsew')

		self.remember_me = ctk.CTkCheckBox(master=self.login_frame, text='Remember me')
		self.remember_me.grid(row=4, column=0, columnspan=2, pady=(15, 20))

		return

	def prepare_main_frame(self):
		self.main_frame = ctk.CTkFrame(master=self, corner_radius=0)
		self.main_frame.grid_columnconfigure(1, weight=1)
		self.main_frame.grid_rowconfigure(0, weight=1)

		# the sidebar
		self.sidebar_frame = ctk.CTkFrame(master=self.main_frame, width=150)
		self.sidebar_frame.grid(row=0, column=0, sticky='ns')
		


		# the home frame
		self.home_frame = ctk.CTkFrame(master=self.main_frame)
		self.home_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

		return

	def login(self):
		self.username = self.username_entry.get()
		self.password = self.password_entry.get()

		if self.username and self.password and self.password.__len__() >= 4:
			self.login_frame.grid_forget()    # clear the login frame 

			self.prepare_main_frame()
			self.main_frame.grid(row=0, column=0, sticky='nsew') # show the main frame
		else:
			print("Login failed, password too short!")

		return

	def set_appearance_mode(self, mode):
		ctk.set_appearance_mode(mode)





if __name__ == '__main__':
	app = TodoApp()
	app.mainloop()
