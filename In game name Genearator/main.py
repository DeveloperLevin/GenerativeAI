import customtkinter as ctk
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
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
root.geometry("500x300")

def generate_output():
    #retrieve input values from user
    genre = dropdown.get()

    #Langchain setup
    model = ChatOpenAI(
        api_key=api_key, 
        temperature=0.8,
        model="gpt-3.5-turbo",
    )

    #prompt templates
    generate_name_prompt = PromptTemplate(
        input_variables = ["genre"],
        template = """I play competitive video games and want you to generate a fancy username that is no more than 7 character long, it should derive inspiration from {genre} history"""
    )
    generate_description_prompt = PromptTemplate(
        input_variables = ["username"],
        template = """Given player name {username}, i want you to generate a small descrption on what this name symbolizes, the description must be no more than 15 words"""
    )

    # Generate the username
    name_response = model.invoke(generate_name_prompt.format(genre=genre))
    username = name_response.strip()

    # Generate the description based on the username
    description_response = model.invoke(generate_description_prompt.format(username=username))
    description = description_response.strip()

    # Update the UI with the generated name and description
    output_name_label.configure(text=f"{username}", font=("Helvetica", 16, "bold"))
    output_desc_label.configure(text=f"{description}")

    print({"name": username, "desc": description})


#setup basic UI
title_label = ctk.CTkLabel(root, text="IGN Generator", text_color="blue", font=("Helvetica", 20, "bold"))
title_label.grid(row=0, column=1, pady=20)

label_option = ctk.CTkLabel(root, text="Select Genre:")
label_option.grid(row=1, column=0, padx=10, pady=10)

#dropdown box
options = ["Greek", "Japanese", "Latin", "Indian", "English", "French", "Chinese"]
dropdown = ctk.CTkComboBox(root, values=options)
dropdown.grid(row=1, column=1, pady=10)

generate_button = ctk.CTkButton(root, text="Generate", command=generate_output)
generate_button.grid(row=1, column=2, pady=10)

# Output data
output_name_label = ctk.CTkLabel(root, text="")
output_name_label.grid(row=2, column=0, columnspan=3, pady=10)

output_desc_label = ctk.CTkLabel(root, text="")
output_desc_label.grid(row=3, column=0, columnspan=3, pady=10)

if __name__ == '__main__':
    root.mainloop()