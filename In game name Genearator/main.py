import customtkinter as ctk
from dotenv import load_dotenv
# from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import SequentialChain
import os

#load enviornment variables from .env file
load_dotenv()

#access enviornment variables
api_key = os.getenv('OPENAI_KEY')

# application configuration
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.title("IGN Generator")
root.geometry("400x300")

#setup basic UI
title_label = ctk.CTkLabel(root, text="In-Game Name Generator", text_color="blue", font=("Helvetica", 20, "bold"))
title_label.grid(row=0, column=1, pady=20)

label_option = ctk.CTkLabel(root, text="Select Genre:")
label_option.grid(row=1, column=0, padx=20, pady=10)

#dropdown box
options = ["Greek", "Japanese", "Latin", "Indian", "English", "French", "Chinese"]
dropdown = ctk.CTkComboBox(root, values=options)
dropdown.grid(row=1, column=1, columnspan=2, pady=10)

output_label = ctk.CTkLabel(root, text="")
output_label.grid(row=2, column=0, columnspan=3, pady=10)

if __name__ == '__main__':
    root.mainloop()