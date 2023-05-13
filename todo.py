'''
Developer : Tega Andrew Rorobi
email   : rorobitega@gmail.com
twitter : @Tega_Rorobi
github  : https://github.com/TegaRorobi
last_modidified: 
''' 

import customtkinter as ctk
from PIL import Image
import os, sqlite3, logging
from CTkMessagebox import CTkMessagebox

logging.basicConfig(format="%(asctime)+10s ... %(name)+7s : %(levelname)+9s -> %(message)s",datefmt="%D %I:%M:%S %p", level=logging.INFO)
logger = logging.getLogger(__file__.split('\\')[-1])
# logger.propagate = 

class TodoApp(ctk.CTk):
	CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
	DB_NAME = 'db.db'

	default_appearance_mode = 'Dark'
	default_color_theme = 'green'


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		ctk.set_appearance_mode(self.default_appearance_mode)
		ctk.set_default_color_theme(self.default_color_theme)

		# Configuring the window
		self.title("A Customtkinter todo app made by Deciphrexx Labs. Inc.")
		# self.resizable(0, 0)
		# self.minsize()
		# self.maxsize()

		self.build_app()

	def build_app(self):
		self.grid_columnconfigure(0, weight=1)
		self.grid_rowconfigure(0, weight=1)

		
		# start with the login frame
		self.prepare_login_frame()
		self.login_frame.grid(row=0, column=0, sticky='nsew', padx=90, pady=30)

		# self.prepare_main_frame()
		# self.main_frame.grid(row=0, column=0, sticky='nsew') # show the main frame

	def prepare_login_frame(self):
		self.geometry("600x400")
		self.resizable(0, 0)

		self.login_frame = ctk.CTkScrollableFrame(master=self, corner_radius=10)
		self.login_frame.grid_columnconfigure((0, 2), weight=1)
		self.login_frame.grid_rowconfigure((0, 7), weight=1)

		self.welcome_label = ctk.CTkLabel(master=self.login_frame, text='Welcome!', font=('Fira Code', 40))
		self.welcome_label.grid(row=1, column=1, pady=(25, 15), sticky='nsew')

		self.username_entry = ctk.CTkEntry(master=self.login_frame, font=('Fira Code', 16), placeholder_text='Username')
		self.username_entry.grid(row=2, column=1, pady=15, sticky='nsew')

		self.password_entry = ctk.CTkEntry(master = self.login_frame, show='0', font=('Fira Code', 16), placeholder_text='Password')
		self.password_entry.grid(row=3, column=1, pady=15, sticky='nsew')

		self.login_btn = ctk.CTkButton(master=self.login_frame, text='Login', font=('Fira Code', 16), command=self.login)
		self.login_btn.grid(row=4, column=1, pady=15, sticky='nsew')

		self.remember_me = ctk.CTkCheckBox(master=self.login_frame, text='Remember me', font=('', 16))
		self.remember_me.grid(row=5, column=1, pady=(15, 20))

		self.show_register_frame_btn = ctk.CTkButton(master=self.login_frame, text='Register', font=('Fira Code', 16), command=self.prepare_and_grid_register_frame)
		self.show_register_frame_btn.grid(row=6, column=1, pady=20)
		return

	def prepare_and_grid_register_frame(self):		
		self.login_frame.grid_forget() # clear the login frame

		# self.geometry("600x400")
		self.resizable(0, 0)

		self.register_frame = ctk.CTkFrame(master=self, corner_radius=0)
		self.register_frame.grid_columnconfigure((0, 2), weight=1)
		self.register_frame.grid_rowconfigure((0, 6), weight=1)

		self.register_label = ctk.CTkLabel(master=self.register_frame, text='Register', font=('Fira Code', 40))
		self.register_label.grid(row=1, column=1, pady=(20, 15), sticky='nsew')

		self.username_reg_entry = ctk.CTkEntry(master=self.register_frame, placeholder_text='Enter your username', width=230, font=('Fira Code', 16))
		self.username_reg_entry.grid(row=2, column=1, pady=15, sticky='nsew')

		self.password_reg_entry = ctk.CTkEntry(master=self.register_frame, placeholder_text='Enter your password', width=230, font=('Fira Code', 16))
		self.password_reg_entry.grid(row=3, column=1, pady=15, sticky='nsew')

		self.register_btn = ctk.CTkButton(master=self.register_frame, text='Register', width=200, font=('Fira Code', 15), command=self.register_user)
		self.register_btn.grid(row=4, column=1, pady=15, sticky='nsew')

		self.auto_signin_checkbox = ctk.CTkCheckBox(master=self.register_frame, text="Automatic Signin", font=('', 16))
		self.auto_signin_checkbox.configure(command=lambda :self.toggle_auto_signin())
		self.auto_signin_checkbox.grid(row=5, column=1, pady=(15, 20))

		self.auto_signin = False

		self.register_frame.grid(row=0, column=0, sticky='nsew', padx=90, pady=30) # show the register frame

	def prepare_main_frame(self):
		self.geometry('775x475')
		self.resizable(True, True)

		self.main_frame = ctk.CTkFrame(master=self, corner_radius=0)
		self.main_frame.grid_columnconfigure(1, weight=1)
		self.main_frame.grid_rowconfigure(0, weight=1)

		# the sidebar
		self.sidebar_frame = ctk.CTkFrame(master=self.main_frame, corner_radius=0)
		self.sidebar_frame.grid(row=0, column=0, sticky='nsew')
		self.sidebar_frame.grid_rowconfigure(5, weight=1)
		self.sidebar_frame.grid_columnconfigure(0, weight=1)



		self.logo_img = ctk.CTkImage(Image.open(os.path.join(self.CURRENT_DIR, 'images/logo.jpeg')), size=(40, 40))
		self.logo_label = ctk.CTkLabel(master=self.sidebar_frame, image=self.logo_img, text="Deciphrexx.ToDo", compound='left', font=('Fira Code', 18))
		self.logo_label.grid(row=0, column=0, sticky='ew', pady=(0, 20))

		self.home_btn_image = ctk.CTkImage(
			light_image=Image.open(os.path.join(self.CURRENT_DIR, 'images/home_dark.png')), # the image to be used in a light theme
			dark_image=Image.open(os.path.join(self.CURRENT_DIR, 'images/home_light.png')), # the image to be used in a dark theme
			size=(20, 20))
		self.home_btn = ctk.CTkButton(master=self.sidebar_frame, height=40, corner_radius=0, text=' Home', 
			fg_color='transparent', image=self.home_btn_image, text_color=("gray10", "gray90"), 
			hover_color=("gray70", "gray30"), font=('', 15), anchor='w', command=self.home_btn_event)
		self.home_btn.grid(row=1, column=0, sticky='ew')

		self.me_btn_image = ctk.CTkImage(
			light_image=Image.open(os.path.join(self.CURRENT_DIR, 'images/add_user_dark.png')), # the image to be used in a light theme
			dark_image=Image.open(os.path.join(self.CURRENT_DIR, 'images/add_user_light.png')), # the image to be used in a dark theme
			size=(20, 20))
		self.me_btn = ctk.CTkButton(master=self.sidebar_frame, height=40, corner_radius=0, text=' Me', 
			fg_color='transparent', image=self.me_btn_image, text_color=("gray10", "gray90"), 
			hover_color=("gray70", "gray30"), font=('', 15), anchor='w', command=self.me_btn_event)
		self.me_btn.grid(row=2, column=0, sticky='ew')

		self.faq_btn_image = ctk.CTkImage(
			light_image = Image.open(os.path.join(self.CURRENT_DIR, 'images/chat_dark.png')), 
			dark_image = Image.open(os.path.join(self.CURRENT_DIR, 'images/chat_light.png')), 
			size = (20, 20))
		self.faq_btn = ctk.CTkButton(master=self.sidebar_frame, height=40, corner_radius=0, text=' FAQ', 
			fg_color='transparent', image=self.faq_btn_image, text_color=('gray10', 'gray90'),
			hover_color=('gray70', 'gray30'), font=('', 15), anchor='w', command=self.faq_btn_event)
		self.faq_btn.grid(row=3, column=0, sticky='ew')

		self.logout_btn_image = None
		self.logout_btn = ctk.CTkButton(master=self.sidebar_frame, height=40, corner_radius=0, text=' Logout', 
			fg_color='transparent', image=self.faq_btn_image, text_color=('gray10', 'gray90'),
			hover_color=('gray70', 'gray30'), font=('', 15), anchor='w', command=self.logout)
		self.logout_btn.grid(row=4, column=0, sticky='ew')

		self.sidebar_buttons = self.home_btn, self.me_btn, self.faq_btn


		self.appearance_mode_optionmenu = ctk.CTkOptionMenu(master=self.sidebar_frame, values=['Light', 'Dark', 'System'], command=self.set_appearance_mode)
		self.appearance_mode_optionmenu.grid(row=7, column=0, pady=20, padx=20)
		self.appearance_mode_optionmenu.set(self.default_appearance_mode)






		# the home frame
		self.home_frame = ctk.CTkFrame(master=self.main_frame, fg_color='transparent')
		self.home_frame.grid_rowconfigure((0, 2, 6, 7, 8), weight=1)
		self.home_frame.grid_columnconfigure((0,1,2,3,4,5), weight=1)

		self.home_user_label = ctk.CTkLabel(master=self.home_frame, text=f"User: {self.query_result[1].title()}", font=('Fira Code', 25))
		self.home_user_label.grid(row=1, column=2, columnspan=2, pady=(15, 0))

		self.todo_scrollable_frame = ctk.CTkScrollableFrame(master=self.home_frame, corner_radius=10, width=400, fg_color=("gray80", "gray20"))
		self.todo_scrollable_frame.grid(row=3, column=1, columnspan=4, pady=(15,25), padx=30, sticky='news')
		self.todo_scrollable_frame.grid_columnconfigure(0, weight=1)
		# self.todo_scrollable_frame.grid_rowconfigure(0, weight=1)

		# self.main_textbox = ctk.CTkTextbox(master=self.textbox_scrollable_frame, font=("Fira Code", 16), corner_radius=10)
		# self.main_textbox.grid(row=0, column=0, sticky='news')

		self.todo_entry = ctk.CTkEntry(master=self.home_frame, font=("Fira Code", 16), height=35, placeholder_text="Enter your todos here...")
		self.todo_entry.grid(row=4, column=2, columnspan=2, padx=15, pady=15, sticky='ew')

		self.add_todo_btn = ctk.CTkButton(master=self.home_frame, hover_color=("gray70", "gray30"), text="Add Todo", fg_color='green', font=('Fira Code', 16), command=self.add_todo)
		self.add_todo_btn.grid(row=5, column=2, padx=15, sticky='ew')

		self.del_todo_btn = ctk.CTkButton(master=self.home_frame, hover_color=("gray70", "gray30"), text="Delete Todo", fg_color='red', font=('Fira Code', 16), command=self.delete_todo)
		self.del_todo_btn.grid(row=5, column=3, padx=15, sticky='ew')



		# the me frame
		self.me_frame = ctk.CTkFrame(master=self.main_frame, corner_radius=0, fg_color='transparent')


		# the faq frame
		self.faq_frame = ctk.CTkFrame(master=self.main_frame, corner_radius=0, fg_color='transparent')




		# setting some defaults
		self.home_btn_event()
		self.current_frame = self.home_frame
		self.lastgridrow = -1

		return

	def login(self, username=None, password=None):
		username = username or self.username_entry.get()
		password = password or self.password_entry.get()

		# create a connection and query the database to check for these credentials
		conn = sqlite3.connect(self.DB_NAME)
		c = conn.cursor()
		c.execute(f"SELECT * FROM users WHERE username=? AND password=? LIMIT 1", (username, password))
		self.query_result = c.fetchone()
		credentials_authorized = bool(self.query_result)
		if credentials_authorized:
			logger.info(f"User record found : {self.query_result}")
			self.login_frame.grid_forget()    # clear the login frame 

			self.prepare_main_frame()
			self.main_frame.grid(row=0, column=0, sticky='nsew') # show the main frame
		else:
			CTkMessagebox(
                title="Verification Failed : Invalid Credentials", 
                message="The username and password combination you entered is absent our database. Please verify your entries.", 
                font=('Fira Code', 13), 
                icon="cancel")

		return

	def toggle_auto_signin(self):
		try:
			self.auto_signin = not self.auto_signin
		except AttributeError:
			self.auto_signin = True

	def register_user(self):
		username = self.username_reg_entry.get()
		password = self.password_reg_entry.get()

		conn = sqlite3.connect(self.DB_NAME)
		c = conn.cursor()
		c.execute(f"INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
		conn.commit()
		c.execute("SELECT * FROM users WHERE users.username=? AND users.password=? LIMIT 1", (username, password))
		usr_obj = c.fetchone()
		if usr_obj: logger.info(f"User record : {usr_obj} inserted successfully.")

		self.register_frame.grid_forget() # clear the register frame

		logger.info(f'Auto signin : {self.auto_signin}')

		if self.auto_signin:
			self.query_result = usr_obj
			self.login(username, password)
			return

		# show the login frame so the user can login with their newly created user object
		self.login_frame.grid(row=0, column=0, sticky='nsew', padx=90, pady=30) 

	def logout(self):
		self.main_frame.grid_forget()
		self.prepare_login_frame()
		self.login_frame.grid(row=0, column=0, sticky='nsew', padx=90, pady=30)

	def add_todo(self):
		todo_txt = self.todo_entry.get()
		if todo_txt: 
			todo_label = ctk.CTkLabel(master=self.todo_scrollable_frame, text=todo_txt, font=("Fira Code", 16))
			todo_label.grid(row=self.lastgridrow+1, column=0, sticky='news', pady=10)
			todo_checkbox = ctk.CTkCheckBox(master=self.todo_scrollable_frame, text='', width=35)
			todo_checkbox.grid(row=self.lastgridrow+1, column=1, sticky='e')
			self.lastgridrow += 1
		else: pass
		self.todo_entry.delete(0, ctk.END)

	def delete_todo(self):
		pass

	def select_frame(self, frame):
		try:
			self.current_frame.grid_forget()
		except:
			pass 
		finally:
			frame.grid(row=0, column=1, sticky='nsew')
			self.current_frame = frame

	def home_btn_event(self):
		self.select_frame(self.home_frame)
		for button in self.sidebar_buttons:
			button.configure(fg_color='transparent')
		self.home_btn.configure(fg_color=('gray70', 'gray30'))

	def me_btn_event(self):
		self.select_frame(self.me_frame)
		for button in self.sidebar_buttons:
			button.configure(fg_color='transparent')
		self.me_btn.configure(fg_color=('gray70', 'gray30'))

	def faq_btn_event(self):
		self.select_frame(self.faq_frame)
		for button in self.sidebar_buttons:
			button.configure(fg_color='transparent')
		self.faq_btn.configure(fg_color=('gray70', 'gray30'))

	def set_appearance_mode(self, mode):
		ctk.set_appearance_mode(mode)


if __name__ == '__main__':
	app = TodoApp()
	app.mainloop()
