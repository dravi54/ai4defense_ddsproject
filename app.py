from flask import Flask, request, render_template
import PyPDF2
import matplotlib.pyplot as plt
import numpy as np
import requests
import re
import os

app = Flask(__name__)

def count_word_occurrences(text, word):
    # Use regex to find all occurrences of the word (case insensitive)
    occurrences = re.findall(rf'\b{word}\b', text, re.IGNORECASE)
    return len(occurrences)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the input data
        pdf_link = request.form['pdf_link']
        words = request.form['words'].split(',')

        # Download the PDF document
        pdf_response = requests.get(pdf_link)
        with open('temp.pdf', 'wb') as f:
            f.write(pdf_response.content)

        # Extract the text from the PDF document
        reader = PyPDF2.PdfReader('temp.pdf')
        text = ''
        for page in reader.pages:
            text += page.extract_text()

        # Count the occurrences of each word
        word_freq = {}
        for word in words:
            word_freq[word] = count_word_occurrences(text, word)

        # Generate the graph
        fig, ax = plt.subplots()
        ax.bar(word_freq.keys(), word_freq.values())
        ax.set_title('Frequency of Words in PDF Document')
        ax.set_xlabel('Word')
        ax.set_ylabel('Frequency')
        
        # Save the graph in the static folder
        graph_path = os.path.join('static', 'graph.png')
        plt.savefig(graph_path)

        # Display the results
        return render_template('result.html', word_freq=word_freq, graph_url='static/graph.png')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)