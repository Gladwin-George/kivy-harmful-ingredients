import os
import csv
import cv2
import sqlite3
import easyocr
import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.spinner import Spinner
from kivy.core.window import Window

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



class LoginScreen(Screen):

    user_manager = ObjectProperty(None)

    def register_user(self, instance):
        self.manager.current = 'register'

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.user_manager = kwargs.get('user_manager')

        anchor_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        layout = BoxLayout(orientation='vertical', size_hint=(0.5, 0.3), spacing=20)

        self.username = TextInput(hint_text='Username', multiline=False)
        self.password = TextInput(hint_text='Password', multiline=False, password=True)

        self.login_button = Button(text='Login',background_color='#0096FF', background_normal="")
        self.login_button.bind(on_press=self.validate_user)
        self.register_button = Button(text='Register',background_color='#0096FF', background_normal="")
        self.register_button.bind(on_press=self.register_user)
        
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(self.login_button)
        layout.add_widget(self.register_button)

        anchor_layout.add_widget(layout)
        self.add_widget(anchor_layout)

    def validate_user(self, instance):
        username = self.username.text
        password = self.password.text
        if self.user_manager.validate_user(username, password):
            self.manager.current = 'main'
        else:
            print("Invalid username or password")
            


from kivy.uix.checkbox import CheckBox
from kivy.graphics import Color, Rectangle

class RegisterScreen(Screen):

    user_manager = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        self.user_manager = kwargs.get('user_manager')

        anchor_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        layout = BoxLayout(orientation='vertical', spacing=20, padding=[40, 20, 40, 40])

        # Add these lines to change the background color
        with layout.canvas.before:
            Color(0, 74/255, 173/255, 1)   # Set the color (RGB and alpha)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_rect, pos=self._update_rect)

        #

        self.username = TextInput(hint_text='Username', multiline=False)
        self.password = TextInput(hint_text='Password', multiline=False, password=True)
        self.age = TextInput(hint_text='Age', multiline=False, input_filter='int')
        self.allergies = TextInput(hint_text='Allergies (type no if you dont have allergies)', multiline=False)

        label = Label(text='Fill these questions to help us to know you better', color=[1, 1, 1, 1])
        layout.add_widget(label)


        # Create a BoxLayout for each question
        self.obese = self.create_question('Are you obese?')
        self.diabetes = self.create_question('Do you have diabetes')
        self.blood_pressure = self.create_question('Do you have high blood pressure')
        self.cholesterol = self.create_question('Do you have high cholesterol')
        self.fatty_liver = self.create_question('Do you have Fatty liver')
        self.kidney_problem = self.create_question('Do you have Kidney problem')
        self.heart_problem = self.create_question('Do you have Heart problem')
        self.asthma = self.create_question('Do you have Asthma')

        self.register_button = Button(text='Register',background_color='#0096FF', background_normal="")
        self.register_button.bind(on_press=self.register_user)

        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(self.age)
        layout.add_widget(self.allergies)
        layout.add_widget(self.obese)
        layout.add_widget(self.diabetes)
        layout.add_widget(self.blood_pressure)
        layout.add_widget(self.cholesterol)
        layout.add_widget(self.fatty_liver)
        layout.add_widget(self.kidney_problem)
        layout.add_widget(self.heart_problem)
        layout.add_widget(self.asthma)

        layout.add_widget(self.register_button)

        anchor_layout.add_widget(layout)
        self.add_widget(anchor_layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


    def create_question(self, question_text):
        layout = BoxLayout(orientation='vertical',spacing=20)  # Change this line
        layout.add_widget(Label(text=question_text, color=[1, 1, 1, 1]))
        yes_no_layout = BoxLayout(orientation='horizontal')  # Add this line


        yes_checkbox = CheckBox(group=question_text)
        no_checkbox = CheckBox(group=question_text)

        yes_no_layout.add_widget(Label(text='Yes', color=[1, 1, 1, 1]))  # Add label for 'Yes'
        yes_no_layout.add_widget(yes_checkbox)
        yes_no_layout.add_widget(Label(text='No', color=[1, 1, 1, 1]))  # Add label for 'No'
        yes_no_layout.add_widget(no_checkbox)

        layout.add_widget(yes_no_layout)  # Add this line
        setattr(self, question_text.lower().replace(' ', '_') + '_yes', yes_checkbox)
        setattr(self, question_text.lower().replace(' ', '_') + '_no', no_checkbox)
        return layout

    def register_user(self, instance):
            username = self.username.text
            password = self.password.text
            age = self.age.text
            allergies = self.allergies.text
            obese = 'Yes' if self.obese_yes.active else 'No'
            diabetes = 'Yes' if self.diabetes_yes.active else 'No'
            blood_pressure = 'Yes' if self.blood_pressure_yes.active else 'No'
            cholesterol = 'Yes' if self.cholesterol_yes.active else 'No'
            fatty_liver = 'Yes' if self.fatty_liver_yes.active else 'No'
            kidney_problem = 'Yes' if self.kidney_problem_yes.active else 'No'
            heart_problem = 'Yes' if self.heart_problem_yes.active else 'No'
            asthma = 'Yes' if self.asthma_yes.active else 'No'
            self.user_manager.register_user(username, password, age, allergies, obese, diabetes, blood_pressure, cholesterol, fatty_liver, kidney_problem, heart_problem, asthma)
            self.manager.current = 'login'

class MainScreen(Screen):
    # This is where your main application code goes
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.name = 'main'
        for widget in kwargs.get('children', []):
            self.add_widget(widget)
    



class UserManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT, 
                password TEXT, 
                age INTEGER, 
                allergies TEXT, 
                obese TEXT, 
                diabetes TEXT, 
                high_blood_pressure TEXT, 
                cholesterol TEXT, 
                kidney_problem TEXT, 
                heart_problem TEXT, 
                asthma TEXT, 
                fatty_liver TEXT
            )
                            """
                            )

    def register_user(self, username, password, age, allergies, obese, diabetes, blood_pressure, cholesterol, kidney_problem, heart_problem, asthma, fatty_liver):
        self.cursor.execute("""
            INSERT INTO users 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (username, password, age, allergies, obese, diabetes, blood_pressure, cholesterol, kidney_problem, heart_problem, asthma, fatty_liver))
        self.conn.commit()

    def validate_user(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        return self.cursor.fetchone() is not None

from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle


class OCRApp(App):

    def build(self):
        
        Window.size = (360, 640)  # Set window size for mobile dimensions
        Window.clearcolor = (1, 1, 1, 1)

        layout = BoxLayout(orientation='vertical', padding=[20, 60, 20, 180], spacing=20)

        user_manager = UserManager('users.db')

        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login', user_manager=user_manager))
        sm.add_widget(RegisterScreen(name='register', user_manager=user_manager))

        
        # Create a label for displaying OCR results
        self.result_scrollview = ScrollView(size_hint=(1, 1))
        self.result_label = Label(text="Detected Harmful ingredients results will be displayed here:", size_hint_y=None, valign='top', halign='left',color=[0, 0, 0, 1])
        self.result_label.bind(width=lambda instance, value: setattr(self.result_label, 'text_size', (value, None)))
        self.result_label.bind(texture_size=self.result_label.setter('size'))

        self.result_scrollview.add_widget(self.result_label)
        layout.add_widget(self.result_scrollview)


        # Create a button for selecting an image
        self.select_image_button = Button(text="Select product ingredients Image", size_hint=(1, 0.2), background_color='#0437F2', background_normal="")
        self.select_image_button.bind(on_press=self.select_image)
        layout.add_widget(self.select_image_button)

        # Create a button for triggering OCR
        self.ocr_button = Button(text="Analyse the ingredients", size_hint=(1, 0.2), background_color='#0437F2', background_normal="")
        self.ocr_button.bind(on_press=self.run_ocr)
        layout.add_widget(self.ocr_button)

        # Create a button for sending email
        self.email_button = Button(text="Click to confirm with doctor", size_hint=(1, 0.2), background_color='#32CD32', background_normal="")
        self.email_button.bind(on_press=self.send_email)
        layout.add_widget(self.email_button)

        # Add the main screen to the screen manager
        sm.add_widget(MainScreen(name='main', children=[layout]))

        return sm
    
    def send_email(self, instance):
        # Set up the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # Login to the email account
        server.login("gladwinfiverr@gmail.com", "xfln ajez ektr gjru")

        # Compose the email
        msg = MIMEMultipart()
        msg['From'] = "gladwinfiverr@gmail.com"
        msg['To'] = "gladwinfiverr@gmail.com"
        msg['Subject'] = "OCR Result"
        body = self.result_label.text  # Assuming this is the OCR result you want to send
        msg.attach(MIMEText(body, 'plain'))

        # Send the email
        server.send_message(msg)
        server.quit()
        print("Email sent successfully")

    def select_image(self, instance):
        # Create and open file chooser
        self.file_chooser = FileChooserListView()

        self.file_chooser.path = '.'  # Set the initial path
        self.file_chooser.filters = ["*.jpg", "*.png", "*.jpeg"]
        self.file_chooser.bind(on_submit=self.load_image)
        self.select_image_button.parent.parent.add_widget(self.file_chooser)  # Add file chooser to main layout

    def load_image(self, instance, selection, touch):
        # Load selected image
        selected_file = selection[0]
        self.image_path = selected_file
        selected_file_name = os.path.basename(selected_file)  # Get the base name of the selected file
        print(f"Image '{selected_file}' selected successfully.")

        # Update the label with the selected image message
        self.result_label.text = f"Image '{selected_file_name}' selected successfully."

        # Remove file chooser from layout
        self.select_image_button.parent.parent.remove_widget(self.file_chooser)

    def run_ocr(self, instance):
        try:
            image_path = self.image_path
        except AttributeError:
            self.result_label.text = "Please select an image first"
            return

        # Step 1: Extract text from the image
        img = cv2.imread(image_path)
        reader = easyocr.Reader(['en'])
        text_results = reader.readtext(image_path)
        extracted_text = ' '.join([result[1] for result in text_results])

        # Step 2: Load harmful ingredients from SQLite database into a dictionary
        harmful_ingredients_dict = {}
        conn = sqlite3.connect('harmful_ingredients.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM harmful_ingredients")
        for row in cursor.fetchall():
            ingredient_name = row[0].strip()  # Assuming ingredient name is in the first column
            harmful_ingredient_description = row[1].strip()  # Assuming harmful ingredient description is in the second column
            harmful_ingredients_dict[ingredient_name.lower()] = harmful_ingredient_description
        conn.close()

        # Step 3: Identify harmful ingredients
        found_harmful_ingredients = []
        for ingredient_name, description in harmful_ingredients_dict.items():
            if ingredient_name in extracted_text.lower():
                found_harmful_ingredients.append((ingredient_name, description))

        # Output the found harmful ingredients along with their descriptions
        if found_harmful_ingredients:
            result_text = "\nHarmful Ingredients Detected:\n \n"
            for ingredient_name, description in found_harmful_ingredients:
                result_text += f"- Ingredient: {ingredient_name}\n  => Description: {description}\n \n"
                print(f"Found harmful ingredient: {ingredient_name}")
        else:
            result_text = "No harmful ingredients detected."
        
        # Update the label with OCR results
        self.result_label.text = result_text
        print("Harmful ingredients detection completed.")
  
    def _update_scroll_height(self, instance, value):
        self.result_scrollview.height = self.result_label.texture_size[1]





if __name__ == "__main__":
    OCRApp().run()
