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

class OCRApp(App):

    def build(self):
        layout = BoxLayout(orientation='vertical')
        
        # Create a label for displaying OCR results
        self.result_label = Label(text="OCR Results will be displayed here")
        layout.add_widget(self.result_label)
        
        # Create a button for selecting an image
        self.select_image_button = Button(text="Select Image")
        self.select_image_button.bind(on_press=self.select_image)
        layout.add_widget(self.select_image_button)

        # Create a button for triggering OCR
        self.ocr_button = Button(text="Run OCR")
        self.ocr_button.bind(on_press=self.run_ocr)
        layout.add_widget(self.ocr_button)

        # File chooser for selecting an image
        self.file_chooser = FileChooserListView()
        self.file_chooser.path = '.'  # Set the initial path
        layout.add_widget(self.file_chooser)
        
        return layout

    def select_image(self, instance):
        # Open file chooser
        self.file_chooser.bind(on_submit=self.load_image)
        self.file_chooser.filters = ["*.jpg", "*.png", "*.jpeg"]

    def load_image(self, instance, selection, touch):
        # Load selected image
        selected_file = selection[0]
        self.image_path = selected_file
        print(f"Image '{selected_file}' selected successfully.")

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
            result_text = "\nHarmful Ingredients Detected:\n"
            for ingredient_name, description in found_harmful_ingredients:
                result_text += f"- Ingredient: {ingredient_name}\n  => Description: {description}\n"
        else:
            result_text = "No harmful ingredients detected."
        
        # Update the label with OCR results
        self.result_label.text = result_text
        print("Harmful ingredients detection completed.")

if __name__ == "__main__":
    OCRApp().run()
