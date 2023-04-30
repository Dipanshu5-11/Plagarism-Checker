#Plagiarism Checker and Grammar Checker

main.py


This project is a plagiarism checker that allows a user to input a file path and check for plagiarism among text files in that directory and shows the result in GUI.
This is a Python program that checks plagiarism among different text files and checks for grammar errors in them. The program uses the following libraries:

os: for operating system related functionalities
docx2txt: for extracting text from DOCX files
PyPDF2: for extracting text from PDF files
sklearn: for vectorizing the text and computing cosine similarity between them
beautifulsoup4: for extracting text from HTML files
language_tool_python: for checking grammar errors
requests: for making HTTP requests
csv: for writing the results to a CSV file
termcolor: for coloring the output in the console
To run the program, enter the file path to the directory containing the text files that need to be checked for plagiarism. The program will extract the text from the text files, compute the cosine similarity between them, and write the results to a CSV file.

The program also includes a grammar checker that checks for grammar errors in the text files. To use the grammar checker, call the check_grammar function and pass in the text that needs to be checked. The function will return a list of grammar errors in the text.




GUI.py


GUI.py is a Python script that creates a graphical user interface (GUI) to display the results of two CSV files. The GUI is created using the tkinter module of Python, and it displays the data in a table format with headers and rows. The script reads the CSV files using the read_csv() function, which returns the data in the form of a list of lists. The CSVViewer class is used to create the main frame of the GUI, the heading, and the table to display the data. Finally, the script creates the main window and runs the CSV viewers using the run() function of the CSVViewer class.


After executing main.py it asks for the directory of the documents and then it saves tho files of plagarism results and grammar errors in csv file format. 
After excecuting GUI.py it combines the two csv files and displays it in GUI in a new window 





