from customtkinter import *
from tkinter import messagebox
import config
import json
from PIL import Image
# Defining a class for the Application
class SmartDocsApp:
    # Initializing the application with a root window
    def __init__(self, root):
        self.logo_color = "#d48b18"
        self.backg_color = "#09090b"
        self.bd_color = "#7d6922"
        self.dropdown_color = '#282831'
        upload_image_path = "items\\upload-button.png"
        self.upload_image= CTkImage(dark_image=Image.open(upload_image_path),size=(50,50))
        right_arrow_path = "items\\right-arrow.png"
        self.right_arrow= CTkImage(dark_image=Image.open(right_arrow_path),size=(40,40))
        left_arrow_path = "items\\left-arrow.png"
        self.left_arrow= CTkImage(dark_image=Image.open(left_arrow_path),size=(40,40))
        info_path = "items\\info.png"
        self.info = CTkImage(dark_image=Image.open(info_path),size=(20,20))
        # moon_path = os.getcwd() + "\\SmartDocs\\items\\moon button.png"
        # self.moon = CTkImage(dark_image=Image.open(moon_path),size=(10,10))
        # sun_path = os.getcwd() + "\\SmartDocs\\items\\sun button.png"
        # self.sun = CTkImage(dark_image=Image.open(sun_path),size=(10,10))
        export_path = "items\\export.png"
        self.export = CTkImage(dark_image=Image.open(export_path),size=(40,40))
        send_button_path = "items\\send-button.png"
        self.send_button = CTkImage(dark_image=Image.open(send_button_path),size=(40,40))



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
        self.main_frame = CTkFrame(self.root, border_width=0, corner_radius=0,fg_color=self.backg_color)
        self.main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)        

        self.main_screen()
        # self.open_query_interface()

        ###  Dropdown Menu and Buttons  ###
    def main_screen(self):

        def write_to_json(data):
            with open("config.json", "w") as f:
                json.dump(data, f)
            
        def on_model_select(new_selection):
            if new_selection == "High":
                new_selection = "Meta-Llama-3.1-405B-Instruct"
            elif new_selection == "Medium":
                new_selection = "Meta-Llama-3.1-70B-Instruct"
            elif new_selection == "Low":
                new_selection = "Meta-Llama-3.1-8B-Instruct"
            data = {"model": new_selection}
            write_to_json(data)

        with open("config.json", "w") as f:
            json.dump({"model": "Meta-Llama-3.1-405B-Instruct"}, f)
        
        logo = CTkLabel(self.main_frame, text="SMART DOCS", text_color=self.logo_color, font=('Helvetica',32,'bold'))
        logo.place(relx=0.02 , rely=0.02)
        
        self.model_label = CTkLabel(self.main_frame, text="Model Smartness:", text_color=self.logo_color, 
                                    font=('Helvetica',20,'bold'))
        self.model_label.place(relx=0.335, rely=0.13)
        
        model_frame = CTkFrame(self.main_frame, fg_color=self.backg_color , border_width=1 , border_color=self.bd_color , corner_radius=5)
        model_frame.place(relx=0.46, rely=0.12 , relwidth=0.2 ,relheight = 0.05)
        
        self.model_menu = CTkOptionMenu(model_frame,fg_color=self.backg_color,button_color=self.backg_color ,
                            values=["High",
                            "Medium",
                            "Low"] ,
                            font=('Helvetica',18) ,corner_radius = 5 , height=35, width=300, button_hover_color='#1e1a10',
                            dropdown_hover_color='#1e1a10',dropdown_fg_color=self.backg_color , 
                            dropdown_text_color=self.logo_color,
                            command=on_model_select,dynamic_resizing=True)
        self.model_menu.place(relx=0.015, rely=0.015,)# relwidth=0.2, relheight=0.1)

        

        self.upload_button = CTkButton(self.main_frame,fg_color=self.backg_color,hover_color='#14120d',image=self.upload_image ,text='UPLOAD PDF' ,
                                  anchor='center' , corner_radius=8 , border_width=1,border_color=self.bd_color , compound='top',
                                  font=('',18,'bold') , text_color=self.logo_color,
                            command = self.upload_pdf)
        self.upload_button.place(relx=0.33, rely=0.18,relwidth=0.33,relheight=0.25)

        self.proceed_button = CTkButton(self.main_frame, fg_color='#d8b238',text="Start Process   ", text_color='black',
                                   font=('',18,'bold'),image=self.right_arrow ,compound='right',
                                   corner_radius=8 , hover_color='#6a581c', state='disabled',
                            command=self.process_pdf)
        self.proceed_button.place(relx=0.33, rely=0.45,relwidth=0.33,relheight=0.05) 

        # self.theme_menu = CTkOptionMenu(self.main_frame,fg_color='#1e1a10',button_color='#1e1a10' ,
        #                                 corner_radius=5,button_hover_color='#1e1a10' , dropdown_hover_color='#1e1a10',dropdown_fg_color=self.backg_color ,
        #             values=["Dark", "Light"],dropdown_font=('',18),dropdown_text_color=self.logo_color,
        #             font=("Helvetica", 18),height=50, width=170, command=self.change_theme)
        # self.theme_menu.place(relx=0.02, rely=0.35,)# relwidth=0.2, relheight=0.1)

        self.info_button = CTkButton(self.main_frame, fg_color=self.backg_color,hover_color='#161206',image=self.info ,
                                anchor='center' ,text='' ,corner_radius=5 , border_width=1,border_color='#75611f',
                            command= self.info_button_click)
        self.info_button.place(relx=0.9, rely=0.9,relwidth=0.05,relheight=0.065 )

        ###  Output Frame  ###
        self.output_textbox = CTkTextbox(self.main_frame,fg_color='#0a0a0a',corner_radius=8,border_width=1,border_color='#473c18',
                                    text_color='#ac8e2e',font=('fira code',14), wrap = "word",activate_scrollbars=True)
        self.output_textbox.place(relx=0.2, rely=0.515, relwidth=0.6, relheight=0.45)
        self.output_textbox.insert("end", """>>> Welcome to SmartDocs! Start by uploading a PDF file.\n""")
        self.output_textbox.configure(state="disabled")





    ## Function to change the theme
    def change_theme(self, theme):
        set_appearance_mode(theme)
    
    ## Function to open the about.txt file
    def info_button_click(self):
        about = open(config.ABOUT_PATH, "r")  # Open the about.txt file
        self.output_textbox.configure(state="normal")
        self.output_textbox.insert("end", f"\n{about.read()}\n")
        self.output_textbox.configure(state="disabled")

    ## Function to upload a PDF
    def upload_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])  # Open file dialog to select a PDF
        if file_path:
            self.output_textbox.configure(state="normal")
            self.output_textbox.insert("end", "\n>>> Loading PDF...\n")
            self.input_pdf = file_path  # Set the input PDF path
            self.output_textbox.insert("end", f"\n>>> PDF file loaded: {file_path}\n")
            self.output_textbox.configure(state="disabled")
            self.proceed_button.configure(state="normal")
        else:
            self.output_textbox.configure(state="normal")
            self.output_textbox.insert("end", "\n>>> No PDF file selected.\n")
            self.output_textbox.configure(state="disabled")
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
        self.output_textbox.configure(state="normal")
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
            self.output_query_textbox.insert("end", f"\n                               \n\n")
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
                                fg_color=self.backg_color,corner_radius=10,border_width=1,border_color=self.bd_color,
                                text_color=self.logo_color,
                                 wrap="word",
                                )
        self.query_box.place(relx=0.16, rely=0.83, relwidth=0.6, relheight=0.15)

        self.query_box.bind("<KeyRelease>", lambda event: check_query_box())
        self.query_box.update()
        

        # Button to submit the query
        self.submit_button = CTkButton(self.main_frame, fg_color='#151517',image=self.send_button ,hover_color='#6a581c',
                                anchor='center' ,text='' ,corner_radius=8,
                                command=submit_query)
        self.submit_button.place(relx=0.765, rely=0.84, relwidth=0.1, relheight=0.08)
        

        # Button to go back to the main screen
        self.back_button = CTkButton(self.main_frame, fg_color=self.backg_color,hover_color='#161206',image=self.left_arrow,
                                corner_radius=5 , text='',
                                command=back_to_main)
        self.back_button.place(relx=0.01, rely=0.05, relwidth=0.1, relheight=0.08)


        # Buttton to export the conversation in a .txt file
        self.export_button = CTkButton(self.main_frame, fg_color=self.backg_color,hover_color='#161206',
                                corner_radius=5 , text='',image=self.export,
                                command=self.export_query)
        self.export_button.place(relx=0.91, rely=0.05, relwidth=0.1, relheight=0.08)


        # Creating the Output Panel
        self.output_query_textbox = CTkTextbox(self.main_frame, font=("Helvetica", 18),
                                border_width=0, corner_radius=0, state="disabled",
                                wrap="word",fg_color='#151517',text_color=self.logo_color,border_color=self.logo_color)
        self.output_query_textbox.place(relx=0.1, rely=0.05, relwidth=0.8, relheight=0.75)
        self.output_query_textbox.insert(f"end", f"\n>>> Talking to SmartDocs...\n\n")
        



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