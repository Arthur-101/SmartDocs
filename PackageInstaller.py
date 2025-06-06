### This Program will install all the Necessary Libraries/Packages required 
### to Run the SmartDocs.
### Run this program before running the main file.


import subprocess

all_packages = ['PyPDF2', 'config', 'sentence_transformers', 'faiss-cpu', 'numpy', 'openai', 'customtkinter', 'CTkMessagebox']

def install_package(package_name):
    try:
        subprocess.check_call(["pip3", "install", package_name])
        print(f"Successfully installed {package_name}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package_name}. Error: {e}")

for package in all_packages:
    install_package(package)
