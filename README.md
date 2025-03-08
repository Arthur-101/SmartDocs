# 📄 SmartDocs – AI-Powered PDF Chatbot  

**SmartDocs** is an advanced AI-powered assistant that allows users to interact with PDF documents intelligently. It leverages state-of-the-art **Meta Llama 3.1 models (8B, 70B, 405B)** to provide accurate and context-aware answers based on the document’s content.  

With **SmartDocs**, you can:  
✔️ Upload a PDF and instantly extract its content  
✔️ Ask questions and get AI-driven responses based on the document  
✔️ Save your queries and responses for later reference  

Whether you're a researcher, student, or professional, **SmartDocs** streamlines the way you engage with PDFs, making information retrieval effortless and efficient.  

📹 **Watch the Demo Video**: [SmartDocs Demo](demo/SmartDocs_Preview.mp4)

---

## ✨ Features  

✔️ **Flexible AI Model Selection** – Choose between **Meta Llama 3.1 (8B, 70B, 405B)**  
✔️ **PDF Processing** – Extracts and chunks text for efficient retrieval  
✔️ **AI-Powered Query System** – Ask questions, get relevant answers instantly  
✔️ **Vector Database Integration** – Uses **FAISS** for fast & accurate information retrieval  
✔️ **Query Export** – Save your queries and responses as a `.txt` file  

---

## 🛠️ Tech Stack  

- **Python**  
- **Libraries:**  
  - `PyPDF2` – Extract text from PDFs  
  - `faiss` – Efficient vector search database  
  - `sentence_transformers` – Embedding text  
  - `openai` – AI model API for answering queries  
  - `customtkinter` – Modern GUI for user interaction  

---

## 📥 Installation  

### 1️⃣ Clone the Repository  
```bash
git clone https://github.com/yourusername/SmartDocs.git
cd SmartDocs
```
  
### 2️⃣ Install Dependencies
```bash
python PackageInstaller.py
```

## 🚀 Usage

### 1️⃣ Run SmartDocs
```bash
python Main.py
```

### 2️⃣ Select AI Model (Optional, default is Llama 405B)
Upon launching, you can choose between **Meta Llama 3.1 (8B, 70B, 405B)**. If no selection is made, the default 405B model will be used.

### 3️⃣ Upload a PDF
#### Once uploaded, **SmartDocs** will:
##### Extract text from the document
##### Split the text into smaller, meaningful chunks
##### Generate embeddings and store them in a FAISS vector database

### 4️⃣ Query the Document
A query window opens where you can type your questions
SmartDocs retrieves the most relevant answers based on the PDF’s content
### 5️⃣ Export Queries (Optional)
Users can save their queries and responses in .txt format for future reference

## 🔮 Future Plans
##### 1. Multi-PDF Support – Upload and process multiple PDFs at once
##### 2. Support for More File Formats – DOCX, TXT, and more
##### 3. TTS & STT Integration – Convert text to speech and speech to text

## 📜 License
This project is open-source under the [MIT License](MIT_License)
