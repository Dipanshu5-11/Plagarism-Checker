import os
import docx2txt
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from bs4 import BeautifulSoup
from language_tool_python import LanguageTool
import requests
import csv

# Get the file path from the user
file_path = input("Enter the file path to check plagiarism: ")

# Use os.listdir to get a list of all the text files in the directory
student_files = [doc for doc in os.listdir(file_path) if doc.endswith('.txt')]

# Use docx2txt to get a list of all the docx files in the directory
student_files += [doc for doc in os.listdir(file_path) if doc.endswith('.docx')]

# Use PyPDF2 to get a list of all the pdf files in the directory
student_files += [doc for doc in os.listdir(file_path) if doc.endswith('.pdf')]

# Use BeautifulSoup to get a list of all the html files in the directory
student_files += [doc for doc in os.listdir(file_path) if doc.endswith('.html')]

# Read the contents of each file and store them in a list called "student_notes"
student_notes = []
for file in student_files:
    file_path_name = os.path.join(file_path, file)
    if file.endswith('.txt'):
        with open(file_path_name, 'r') as f:
            student_notes.append(f.read())
    elif file.endswith('.docx'):
        student_notes.append(docx2txt.process(file_path_name))
    elif file.endswith('.pdf'):
        with open(file_path_name, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            df_text = [page.extract_text() for page in pdf_reader.pages]
            student_notes.append(' '.join(df_text))

    elif file.endswith('.html'):
        with open(file_path_name, 'r') as f:
            html_content = f.read()
            soup = BeautifulSoup(html_content, 'lxml')
            text = soup.get_text()
            student_notes.append(text)


# Define two lambda functions for vectorizing the text and computing similarity
def vectorize(Text):
    return TfidfVectorizer().fit_transform(Text).toarray()


def similarity(doc1, doc2):
    return cosine_similarity([doc1, doc2])


# Vectorize the student notes and zip them with the student files into a list of tuples
vectors = vectorize(student_notes)
s_vectors = list(zip(student_files, vectors))

# Define the function for checking plagiarism
import csv

import csv
from termcolor import colored


def check_plagiarism(output_file):
    plagiarism_results = set()
    global s_vectors
    for student_a, text_vector_a in s_vectors:
        new_vectors = s_vectors.copy()
        current_index = new_vectors.index((student_a, text_vector_a))
        del new_vectors[current_index]
        for student_b, text_vector_b in new_vectors:
            sim_score = similarity(text_vector_a, text_vector_b)[0][1]
            student_pair = sorted((student_a, student_b))
            score = (student_pair[0], student_pair[1], sim_score * 100)
            plagiarism_results.add(score)

    # Sort results in descending order of similarity score
    sorted_results = sorted(plagiarism_results, key=lambda x: x[2], reverse=True)

    # Write sorted results to a CSV file
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(
            [colored('Student 1', 'blue'), colored('Student 2', 'blue'), colored('Similarity Score', 'blue')])
        for result in sorted_results:
            writer.writerow(
                [colored(result[0], 'green'), colored(result[1], 'green'), colored(f"{result[2]:.2f}%", 'green')])

    return sorted_results


check_plagiarism('plagiarism_results123.csv')


def check_grammar(text):
    url = 'https://languagetool.org/api/v2/check'
    data = {
        'text': text,
        'language': 'en-US'
    }
    response = requests.post(url, data=data)
    if response.ok:
        results = response.json()
        grammar_errors = [error for error in results['matches'] if error['rule']['category']['id'] == 'grammar']
        return grammar_errors
    else:
        print('Error:', response.status_code, response.reason)
        return None


def process_student_notes(dir_path):
    # Get a list of all files in the directory
    files = os.listdir(dir_path)

    # Filter out non-text files
    text_files = [file for file in files if file.endswith(('.txt', '.docx', '.pdf', '.html'))]

    # Initialize an empty list to store student notes
    student_notes = []

    # Loop through the text files
    for file in text_files:
        file_path_name = os.path.join(dir_path, file)
        if file.endswith('.txt'):
            with open(file_path_name, 'r') as f:
                student_notes.append(f.read())
        elif file.endswith('.docx'):
            text = docx2txt.process(file_path_name)
            student_notes.append(text)
        elif file.endswith('.pdf'):
            with open(file_path_name, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                num_pages = len(pdf_reader.pages)
                df_text = [pdf_reader.pages[i].extract_text() for i in range(num_pages)]
                student_notes.append(' '.join(df_text))
        elif file.endswith('.html'):
            with open(file_path_name, 'r') as f:
                student_notes.append(f.read())

    # Check the grammar of each student's notes
    errors_list = []
    for i, note in enumerate(student_notes):
        errors = check_grammar(note)
        errors_list.append(errors)

    # Write the errors to a CSV file
    with open('grammar_errors.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['File', 'Errors'])
        for i, errors in enumerate(errors_list):
            writer.writerow([text_files[i], errors])

    return errors_list


# Get the directory path from the user
dir_path = input("Enter the directory path to check Grammar errors : ")

# Process the student notes and write the errors to a CSV file
process_student_notes(dir_path)
