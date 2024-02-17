import os
import cv2
import easyocr
import numpy as np
import csv
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.username = TextInput(hint_text='Username', multiline=False)
        self.password = TextInput(hint_text='Password', multiline=False, password=True)
        self.login_button = Button(text='Login')
        self.login_button.bind(on_press=self.validate_user)
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(self.login_button)
        self.add_widget(layout)

    def validate_user(self, instance):
        username = self.username.text
        password = self.password.text
        # Add your authentication logic here
        if username == 'admin' and password == 'admin':  # This is just a placeholder for the actual authentication logic
            self.manager.current = 'main'

class MainScreen(Screen):
    # This is where your main application code goes
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.name = 'main'
        for widget in kwargs.get('children', []):
            self.add_widget(widget)
    

class OCRApp(App):

    def build(self):
        
        Window.size = (360, 640)  # Set window size for mobile dimensions

        layout = BoxLayout(orientation='vertical')
        
        # Create a label for displaying OCR results
        self.result_scrollview = ScrollView(size_hint=(1, 0.6))
        self.result_label = Label(text="OCR Results will be displayed here", size_hint_y=None, valign='top', halign='left')
        self.result_label.bind(width=lambda instance, value: setattr(self.result_label, 'text_size', (value, None)))
        self.result_label.bind(texture_size=self.result_label.setter('size'))
        self.result_scrollview.add_widget(self.result_label)
        layout.add_widget(self.result_scrollview)
                    
        # Create a button for selecting an image
        self.select_image_button = Button(text="Select Image", size_hint=(1, 0.2))
        self.select_image_button.bind(on_press=self.select_image)
        layout.add_widget(self.select_image_button)

        # Create a button for triggering OCR
        self.ocr_button = Button(text="Run OCR", size_hint=(1, 0.2))
        self.ocr_button.bind(on_press=self.run_ocr)
        layout.add_widget(self.ocr_button)

        # Create the screen manager and add the login and main screens
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main', children=[layout]))

        return sm

    def select_image(self, instance):
        # Create and open file chooser
        self.file_chooser = FileChooserListView()
        self.file_chooser.path = '.'  # Set the initial path
        self.file_chooser.filters = ["*.jpg", "*.png", "*.jpeg"]
        self.file_chooser.bind(on_submit=self.load_image)
        self.select_image_button.parent.add_widget(self.file_chooser)  # Add file chooser to layout

    def load_image(self, instance, selection, touch):
        # Load selected image
        selected_file = selection[0]
        self.image_path = selected_file
        selected_file_name = os.path.basename(selected_file)  # Get the base name of the selected file
        print(f"Image '{selected_file}' selected successfully.")

        # Update the label with the selected image message
        self.result_label.text = f"Image '{selected_file_name}' selected successfully."

        # Remove file chooser from layout
        self.select_image_button.parent.remove_widget(self.file_chooser)

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

        # Step 2: Load harmful ingredients from CSV into a dictionary
        harmful_ingredients_dict = {}
        with open('harmful_ingredients.csv', 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the first row (headings)
            for row in csv_reader:
                if len(row) >= 2 and row[0] and row[1]:  # Check if both columns have data
                    ingredient_name = row[0].strip()  # Assuming ingredient name is in the first column
                    harmful_ingredient_description = row[1].strip()  # Assuming harmful ingredient description is in the second column
                    harmful_ingredients_dict[ingredient_name.lower()] = harmful_ingredient_description

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
