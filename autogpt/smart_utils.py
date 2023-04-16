import os
import re
import heapq
import chardet
import nltk
from nltk.corpus import stopwords
from collections import Counter, defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def extract_keywords(file_path, num_keywords=10):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        file_encoding = result['encoding']

    with open(file_path, 'r', encoding=file_encoding) as f:
        text = f.read()

    # Remove special characters and digits
    formatted_text = re.sub('[^a-zA-Z]', ' ', text)
    formatted_text = re.sub(r'\s+', ' ', formatted_text)

    # Convert text to lowercase and tokenize
    words = formatted_text.lower().split()

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]

    # Calculate word frequencies and extract top keywords
    word_freq = Counter(words)
    top_keywords = heapq.nlargest(num_keywords, word_freq, key=word_freq.get)

    return top_keywords

def cluster_documents(file_paths, num_clusters=5):
    documents = []

    for file_path in file_paths:
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            result = chardet.detect(raw_data)
            file_encoding = result['encoding']

        with open(file_path, 'r', encoding=file_encoding) as f:
            text = f.read()
            documents.append(text)

    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(documents)

    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(X)

    return kmeans.labels_

def summarize_contents(working_directory):
    total_files = 0
    total_size = 0
    file_extensions = {}
    file_keywords = []
    all_file_paths = []

    # Specify allowed file extensions
    allowed_extensions = ['.txt', '.md', '.py']

    for root, dirs, files in os.walk(working_directory):
        for file in files:
            file_extension = os.path.splitext(file)[-1].lower()

            # Skip non-text files
            if file_extension not in allowed_extensions:
                continue

            total_files += 1
            file_path = os.path.join(root, file)
            total_size += os.path.getsize(file_path)
            all_file_paths.append(file_path)

            # Extract file extension and count occurrences
            if file_extension in file_extensions:
                file_extensions[file_extension] += 1
            else:
                file_extensions[file_extension] = 1

            # Extract file keywords
            keywords = extract_keywords(file_path)
            file_keywords.append(keywords)

    if len(all_file_paths) >= 5:
        file_clusters = cluster_documents(all_file_paths)
    else:
        print("Not enough documents for clustering")
        file_clusters = "Not enough documents for clustering"

    max_keywords_to_display = 10
    max_clusters_to_display = 5

    summary = f"Directory Summary:\n"
    summary += f"Total files: {total_files}\n"
    summary += f"Total size: {total_size} bytes\n"
    summary += f"File types:\n"

    for ext, count in file_extensions.items():
        summary += f"{ext}: {count}\n"

    summary += f"Top {max_keywords_to_display} Keywords Across All Files:\n"
    all_keywords = [keyword for keywords in file_keywords for keyword in keywords]
    keyword_freq = Counter(all_keywords)
    top_keywords = heapq.nlargest(max_keywords_to_display, keyword_freq, key=keyword_freq.get)
    for keyword in top_keywords:
        summary += f"{keyword}: {keyword_freq[keyword]}\n"

    summary += f"File Clusters:\n"
    cluster_summary = defaultdict(list)
    for i, cluster in enumerate(file_clusters):
        cluster_summary[cluster].append(i + 1)

    for cluster, files in list(cluster_summary.items())[:max_clusters_to_display]:
        summary += f"Cluster {cluster}: {files}\n"

    return summary



# todo: figure out how to use GPT-3 to evaluate a directory and suggest actions to improve it
def evaluate_directory(gpt, directory):
    directory_summary = get_directory_summary(directory)

    prompt = f"Evaluate the following directory summary and suggest what actions should be taken to improve the organization and synthesis of the information:\n\n{directory_summary}"

    response = gpt.generate(prompt)

    # Process the GPT-generated suggestions and take appropriate actions based on these suggestions.
    # This may involve reorganizing files, creating new folders, or synthesizing information from different files.
    # You may need to implement this part based on the specific suggestions provided by GPT.

    return response