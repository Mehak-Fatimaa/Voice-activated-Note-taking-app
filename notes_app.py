import tkinter as tk
from tkinter import ttk, messagebox
import json
import pyttsx3
import speech_recognition as sr
import datetime

# Getting current date and time
today=datetime.datetime.now()

# Create the main window
root = tk.Tk()
root.title("Notes App")
root.geometry("850x600")
root.configure(bg="lightblue")

# Define the font style
font_style = ('Arial', 15)

# Set the font style for all the widgets in the GUI
root.option_add('*Font', font_style)

# Create the frame to hold the notes
notes_frame = ttk.Notebook(root)
notes_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

# Create the frame to hold the saved notes
saved_notes_frame = ttk.Notebook(root)
saved_notes_frame.pack(side=tk.RIGHT, padx=20, pady=10, fill=tk.Y)

# Load saved notes
notes = {}
try:
    with open("notes.json", "r") as f:
        notes = json.load(f)
except FileNotFoundError:
    pass

# Function to add a new note
def add_note():
    # adding main title of notes taking page 
    main_label = ttk.Label(notes_frame, text="ADD NEW NOTES")
    main_label.grid(row=0, column=1, padx=10, pady=10, sticky="W")

    # Create entry widgets for the title and content of the note
    title_label = ttk.Label(notes_frame, text="Title:")
    title_label.grid(row=1, column=0, padx=10, pady=10, sticky="W")

    title_entry = ttk.Entry(notes_frame, width=40)
    title_entry.grid(row=1, column=1, padx=10, pady=10)

    content_label = ttk.Label(notes_frame, text="Note:")
    content_label.grid(row=2, column=0, padx=10, pady=10, sticky="W")

    content_entry = tk.Text(notes_frame, width=40, height=10)
    content_entry.grid(row=2, column=1, padx=10, pady=10)

    # Function to save the note
    def save_note():
        # Get the title and content of the note
        title = title_entry.get()
        content = content_entry.get("1.0", tk.END)

        # Add the current date to the title
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        title_with_date = f"{title} ({current_date})"

        # Add the note to the notes dictionary
        notes[title_with_date] = content.strip()

        # Save the notes dictionary to the file
        with open("notes.json", "w") as f:
            json.dump(notes, f)

        # Create a button to open the newly added note
        note_button = tk.Button(saved_notes_frame, text=title_with_date, command=lambda t=title_with_date, c=content: open_note(t, c))
        note_button.pack(padx=5, pady=5)

        # Clear the input fields after saving
        title_entry.delete(0, tk.END)
        content_entry.delete("1.0", tk.END)
        
    def add_note_from_speech():
        #using online
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Speak something...")
            audio = r.listen(source)
        try:
            content_speech = r.recognize_google(audio) 
            content_entry.insert(tk.END, content_speech)
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Error; {0}".format(e))
        
    # Add a speach button to the note frame
    speech_to_text_button = tk.Button(notes_frame, text="Add Note from Speech", bg="purple", fg="white", command=add_note_from_speech)
    speech_to_text_button.grid(row=4, column=1, padx=10, pady=10)

    # Add a save button to the note frame
    save_button = tk.Button(notes_frame, text="Save", bg="green", fg="white", command=save_note)
    save_button.grid(row=5, column=1, padx=10, pady=10)

# Load saved notes when the app starts
def load_notes():
    try:
        with open("notes.json", "r") as f:
            loaded_notes = json.load(f)
  
        for title, content in notes.items():
            title_with_date = title.split('(')
            # Check if the split resulted in at least two elements
            if len(title_with_date) >= 2:
                formatted_title = title_with_date[0].strip()
                date = title_with_date[1].replace(')', '')
                button_text = f"{formatted_title} ({date})"
                button = tk.Button(saved_notes_frame, text=button_text, command=lambda t=title, c=content: open_note(t, c))
                button.pack(padx=5, pady=5)
            
    except FileNotFoundError:
        # If the file does not exist, do nothing
        pass

# Function to open a saved note
def open_note(title, content):
    note_window = tk.Toplevel(root)
    note_window.title(title)
    
    # Create a label for the title
    title_label = tk.Label(note_window, text=title, font=('Arial', 16, 'bold'))
    title_label.pack(padx=10, pady=10)
    
    # Create a text widget for the content
    content_text = tk.Text(note_window, width=40, height=10)
    content_text.insert(tk.END, content)
    content_text.pack(padx=10, pady=10)

    # Function to delete a note
    def delete_note(note_title):
        # Show a confirmation dialog
        confirm = messagebox.askyesno("Delete Note", f"Are you sure you want to delete {note_title}?")

        if confirm:
            # Remove the note from the notes dictionary
            notes.pop(note_title)
            #print(notes.pop(note_title))

            # Save the notes dictionary to the file
            with open("notes.json", "w") as f:
                json.dump(notes, f)

            # Update the saved notes frame after deletion
            for widget in saved_notes_frame.winfo_children():
                widget.destroy()
            load_notes()

    # Function to read notes
    def read_note(note_title):
        # initializing engine
        engine = pyttsx3.init()
        #setting speed of voice
        rate = engine.getProperty('rate')
        engine.setProperty('rate', 135)
        #setting voice, 0 for male, 1 for female voice
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
    
        #text to speech the current tab content
        engine.say(notes.get(note_title))
        engine.runAndWait()
        engine.stop()

    #creating read button
    read_button = tk.Button(note_window, text="Read Note", bg="blue", fg="white", command=lambda t=title: read_note(t))
    read_button.pack(side=tk.LEFT, padx=10, pady=10)

    # creating delete button 
    delete_button = tk.Button(note_window, text="Delete", bg="red", fg="white", command=lambda t=title: delete_note(t))
    delete_button.pack(side=tk.LEFT, padx=10, pady=10)
        
load_notes()
add_note()
root.mainloop()
