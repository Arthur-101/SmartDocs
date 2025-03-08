from customtkinter import *
from tkinter import messagebox
import config
import json

# Defining a class for the Application
class SmartDocsApp:
    # Initializing the application with a root window
    def __init__(self, root):
        self.root = root
        self.root.title("SmartDocs")  # Set the title of the application window
        set_appearance_mode('Dark')
        self.root.wm_state("zoomed")
        window_width = root.winfo_screenwidth()
        window_height = root.winfo_screenheight()
        self.root.geometry(f'{window_width}x{window_height}')

        # Initialize paths from config
        self.input_pdf = config.PDF_INPUT_PATH  # Default PDF input from config
        self.output_txt = config.EXTRACTED_TEXT_PATH  # Path for the extracted text
        self.chunk_folder = config.TEXT_CHUNKS_FOLDER  # Folder to save chunks
        self.index_path = config.FAISS_INDEX_PATH  # Path for the FAISS index

        #######   MAIN FRAME   #######
        self.main_frame = CTkFrame(self.root, border_width=0, corner_radius=0,)
        self.main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)        

        self.main_screen()
        # self.open_query_interface()

        ###  Dropdown Menu and Buttons  ###
    def main_screen(self):

        def write_to_json(data):
            with open("config.json", "w") as f:
                json.dump(data, f)
            
        def on_model_select(new_selection):
            data = {"model": new_selection}
            write_to_json(data)

        with open("config.json", "w") as f:
            json.dump({"model": "Meta-Llama-3.1-405B-Instruct"}, f)
        
        self.model_menu = CTkOptionMenu(self.main_frame,
                    values=["Meta-Llama-3.1-405B-Instruct",
                            "Meta-Llama-3.1-70B-Instruct",
                            "Meta-Llama-3.1-8B-Instruct"],
                    font=("Helvetica", 18), height=70, width=310,
                    command=on_model_select)
        self.model_menu.place(relx=0.42, rely=0.1,)# relwidth=0.2, relheight=0.1)

        

        self.upload_button = CTkButton(self.main_frame, text="Upload PDF",
                            font=("Helvetica", 18), height=70, width=310,
                            command = self.upload_pdf)
        self.upload_button.place(relx=0.4, rely=0.22, )

        self.proceed_button = CTkButton(self.main_frame, text=">",
                            font=("Helvetica", 22, "bold"), height=70, width=70, state="disabled",
                            command=self.process_pdf)
        self.proceed_button.place(relx=0.603, rely=0.22, )

        self.theme_menu = CTkOptionMenu(self.main_frame,
                    values=["Dark", "Light"],
                    font=("Helvetica", 18),height=50, width=170, command=self.change_theme)
        self.theme_menu.place(relx=0.02, rely=0.35,)# relwidth=0.2, relheight=0.1)

        self.info_button = CTkButton(self.main_frame, text="?", corner_radius=40,
                            font=("Helvetica", 18, "bold"), height=40, width=20,
                            command= self.info_button_click)
        self.info_button.place(relx=0.95, rely=0.35, )

        ###  Output Frame  ###
        self.output_textbox = CTkTextbox(self.main_frame,
                            font=("consolas", 18), text_color="#cacaca", fg_color="#0c0c0c",
                            border_width=1, corner_radius=0, wrap = "word")
        self.output_textbox.place(relx=0.02, rely=0.45, relwidth=0.96, relheight=0.54)
        self.output_textbox.insert("end", """>>> Welcome to SmartDocs! Start by uploading a PDF file.\n""")





    ## Function to change the theme
    def change_theme(self, theme):
        set_appearance_mode(theme)
    
    ## Function to open the about.txt file
    def info_button_click(self):
        about = open(config.ABOUT_PATH, "r")  # Open the about.txt file
        self.output_textbox.insert("end", f"\n{about.read()}\n")

    ## Function to upload a PDF
    def upload_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])  # Open file dialog to select a PDF
        if file_path:
            self.output_textbox.insert("end", "\n>>> Loading PDF...\n")
            self.input_pdf = file_path  # Set the input PDF path
            self.output_textbox.insert("end", f"\n>>> PDF file loaded: {file_path}\n")
            self.proceed_button.configure(state="normal")
        else:
            self.output_textbox.insert("end", "\n>>> No PDF file selected.\n")
            self.proceed_button.configure(state="disabled")


    ## Function to Process the PDF
    def process_pdf(self):
        self.upload_button.configure(state="disabled")
        self.proceed_button.configure(state="disabled")
        self.text_extract()
        self.chunk_text()
        self.embeddings_and_vector()
        self.open_query_interface()

    def text_extract(self):
        # Text Extraction
        self.output_textbox.insert("end", "\n>>> Extracting Text...\n")
        self.output_textbox.update()
        import Text_Extract
        Text_Extract.extract_and_save_text(self.input_pdf, self.output_txt)  # Calling function to extract and save text
        self.output_textbox.insert("end", f"\n>>> Text extracted to: {self.output_txt}\n")
        self.output_textbox.update()

    def chunk_text(self):
        # Chunking the text
        self.output_textbox.insert("end", "\n>>> Chunking Text...\n")
        self.output_textbox.update()
        import Divide_Chunk
        chunk_len = Divide_Chunk.chunk_and_save(input_file=self.output_txt, chunk_size=2000, overlap=200, output_dir=self.chunk_folder)
        self.output_textbox.insert("end", f"\n>>> Text chunked and saved in: {self.chunk_folder}\n")
        self.output_textbox.insert("end", f"\n>>> Total chunks: {chunk_len}\n")
        self.output_textbox.update()

    def embeddings_and_vector(self):
        # Generate Embeddings and storing it in FAISS vector Database
        self.output_textbox.insert("end", "\n>>> Generating Embeddings and storing it in Vector Database...\n")
        self.output_textbox.update()
        import Embedding_and_vector
        Embedding_and_vector.generate_embeddings_and_index(chunk_folder=self.chunk_folder, index_path=self.index_path)
        self.output_textbox.insert("end", f"\n>>> Embeddings generated and saved in: {self.index_path}\n")
        self.output_textbox.update()
        self.output_textbox.insert("end", "\n>>> Opening Query Interface...\n")
        self.output_textbox.update()

    ###   Opening query interface   ###
    def open_query_interface(self):
        import Query_Database as Query_Database

        # Destroying the children of the main_frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Submitting the query
        def submit_query():
            self.get_query()
            self.output_query_textbox.configure(state="normal")
            self.output_query_textbox.insert("end", f"\n-----------------------------------\n\n")
            self.output_query_textbox.insert("end", f"YOU :   {self.user_query}\n\n")
            self.output_query_textbox.update()
          
            # Clearing the query box
            self.query_box.delete("1.0", "end")
            self.query_box.update()

            # Querying the database with context
            try:
                response = Query_Database.query_faiss_snova(self.user_query, top_k=5,
                                                            chunk_folder=self.chunk_folder,
                                                            index_path=self.index_path,
                                                            )  # Query the database

                self.output_query_textbox.insert("end", f"SmartDocs : {response}\n\n")
                self.output_query_textbox.update()
            except Exception as e:
                self.output_query_textbox.insert("end", f"*An error occurred during querying* : {str(e)} !\n\n")

            self.output_query_textbox.configure(state="disabled")
            self.submit_button.configure(state="disabled")


        # Button to go back to the main screen
        def back_to_main():
            
            for widget in self.main_frame.winfo_children():
                widget.destroy()
            
            self.main_screen()


        # Creating the Query Box
        self.query_box = CTkTextbox(self.main_frame, font=("Helvetica", 18),
                                border_width=1, corner_radius=15, wrap="word",
                                )
        self.query_box.place(relx=0.16, rely=0.83, relwidth=0.6, relheight=0.15)

        self.query_box.bind("<KeyRelease>", lambda event: check_query_box())
        self.query_box.update()
        

        # Button to submit the query
        self.submit_button = CTkButton(self.main_frame, text="Submit", font=("Helvetica", 18),
                                border_width=2, corner_radius=20, state="disabled",
                                command=submit_query)
        self.submit_button.place(relx=0.765, rely=0.84, relwidth=0.08, relheight=0.13)
        

        # Button to go back to the main screen
        self.back_button = CTkButton(self.main_frame, text="Back", font=("Helvetica", 18),
                                border_width=2, corner_radius=0,
                                command=back_to_main)
        self.back_button.place(relx=0.01, rely=0.05, relwidth=0.08, relheight=0.05)


        # Buttton to export the conversation in a .txt file
        self.export_button = CTkButton(self.main_frame, text="Export", font=("Helvetica", 18),
                                border_width=2, corner_radius=0,
                                command=self.export_query)
        self.export_button.place(relx=0.91, rely=0.05, relwidth=0.08, relheight=0.05)


        # Creating the Output Panel
        self.output_query_textbox = CTkTextbox(self.main_frame, font=("Helvetica", 18),
                                border_width=0, corner_radius=0, state="disabled",
                                wrap="word")
        self.output_query_textbox.place(relx=0.1, rely=0.05, relwidth=0.8, relheight=0.75)
        



        # Enabling submit_button when query_box is not empty
        def check_query_box():
            if self.query_box.get("1.0", "end-1c").strip():  # Check if there's any text (ignores whitespace)
                self.submit_button.configure(state="normal")  # Enable the button
            else:
                self.submit_button.configure(state="disabled")  # Disable the button

        
    ## Getting the query from the user_query box ##
    def get_query(self):
        self.user_query = self.query_box.get("1.0", "end-1c").strip()

    def export_query(self):
        all_query = self.output_query_textbox.get("1.0", "end-1c").strip()

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                             filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:  # If the user selects a file
            with open(file_path, "w") as file:
                file.write(all_query)
        
        # show the pop up success message
        messagebox.showinfo("Success", "Queries exported successfully!")




# Main entry point of the application
if __name__ == "__main__":
    root = CTk()  # Create the main window
    app = SmartDocsApp(root)  # Initialize the application
    root.mainloop()  # Run the application
