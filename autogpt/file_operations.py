import os
import os.path

from smart_utils import summarize_contents

# Set a dedicated folder for file I/O
working_directory = "auto_gpt_workspace"

# Create the directory if it doesn't exist
if not os.path.exists(working_directory):
    os.makedirs(working_directory)


def safe_join(base, *paths):
    """Join one or more path components intelligently."""
    new_path = os.path.join(base, *paths)
    norm_new_path = os.path.normpath(new_path)

    if os.path.commonprefix([base, norm_new_path]) != base:
        raise ValueError("Attempted to access outside of working directory.")

    return norm_new_path

# Ensure lower_snake_case filenames
def format_filename(filename):
    """Format a filename to be lowercase with underscores"""
    # Split the file path into directory and file name components
    directory, file_name = os.path.split(filename)
    
    # Replace any spaces in the file name with underscores
    file_name = file_name.replace(' ', '_')
    
    # Convert the file name to lowercase
    file_name = file_name.lower()
    
    # Rejoin the directory and file name components to create the full path
    formatted_filename = os.path.join(directory, file_name)
    
    return formatted_filename

def split_file(content, max_length=4000, overlap=0):
    """
    Split text into chunks of a specified maximum length with a specified overlap
    between chunks.

    :param text: The input text to be split into chunks
    :param max_length: The maximum length of each chunk,
        default is 4000 (about 1k token)
    :param overlap: The number of overlapping characters between chunks,
        default is no overlap
    :return: A generator yielding chunks of text
    """
    start = 0
    content_length = len(content)

    while start < content_length:
        end = start + max_length
        if end + overlap < content_length:
            chunk = content[start : end + overlap]
        else:
            chunk = content[start:content_length]
        yield chunk
        start += max_length - overlap


def read_file(filename) -> str:
    """Read a file and return the contents"""
    try:
        formatted_filename = format_filename(filename)
        filepath = safe_join(working_directory, formatted_filename)
        with open(filepath, "r", encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Error: {str(e)}"


def ingest_file(filename, memory, max_length=4000, overlap=200):
    """
    Ingest a file by reading its content, splitting it into chunks with a specified
    maximum length and overlap, and adding the chunks to the memory storage.

    :param filename: The name of the file to ingest
    :param memory: An object with an add() method to store the chunks in memory
    :param max_length: The maximum length of each chunk, default is 4000
    :param overlap: The number of overlapping characters between chunks, default is 200
    """
    try:
        print(f"Working with file {filename}")
        content = read_file(filename)
        content_length = len(content)
        print(f"File length: {content_length} characters")

        chunks = list(split_file(content, max_length=max_length, overlap=overlap))

        num_chunks = len(chunks)
        for i, chunk in enumerate(chunks):
            print(f"Ingesting chunk {i + 1} / {num_chunks} into memory")
            memory_to_add = (
                f"Filename: {filename}\n" f"Content part#{i + 1}/{num_chunks}: {chunk}"
            )

            memory.add(memory_to_add)

        print(f"Done ingesting {num_chunks} chunks from {filename}.")
    except Exception as e:
        print(f"Error while ingesting file '{filename}': {str(e)}")


def write_to_file(filename, text):
    """Write text to a file"""
    try:
        formatted_filename = format_filename(filename)
        filepath = safe_join(working_directory, formatted_filename)
        directory = os.path.dirname(filepath)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text)
        return "File " + filename + " written to successfully."
    except Exception as e:
        return "Error: " + str(e)


def append_to_file(filename, text):
    """Append text to a file"""
    try:
        formatted_filename = format_filename(filename)
        filepath = safe_join(working_directory, formatted_filename)
        with open(filepath, "a") as f:
            f.write(text)
        return "Text appended to " + filename + " successfully."
    except Exception as e:
        return "Error: " + str(e)


def delete_file(filename):
    """Delete a file"""
    try:
        formatted_filename = format_filename(filename)
        filepath = safe_join(working_directory, formatted_filename)
        os.remove(filepath)
        return "File "  + filename + " deleted successfully."
    except Exception as e:
        return "Error: " + str(e)
    

def copy_file(src_filename, dest_directory):
    try:
        formatted_src_filename = format_filename(src_filename)
        src_filepath = safe_join(working_directory, formatted_src_filename)
        dest_directory_path = safe_join(working_directory, dest_directory)
        dest_filepath = safe_join(dest_directory_path, os.path.basename(formatted_src_filename))

        if not os.path.exists(dest_directory_path):
            os.makedirs(dest_directory_path)

        shutil.copy2(src_filepath, dest_filepath)
        return "File copied successfully."
    except Exception as e:
        return "Error: " + str(e)
    
def move_file(src_filename, dest_directory):
    try:
        formatted_src_filename = format_filename(src_filename)
        src_filepath = safe_join(working_directory, formatted_src_filename)
        dest_directory_path = safe_join(working_directory, dest_directory)
        dest_filepath = safe_join(dest_directory_path, os.path.basename(formatted_src_filename))

        if not os.path.exists(dest_directory_path):
            os.makedirs(dest_directory_path)

        os.rename(src_filepath, dest_filepath)
        return "File moved successfully."
    except Exception as e:
        return "Error: " + str(e)

def rename_file(old_filename, new_filename):
    try:
        old_formatted_filename = format_filename(old_filename)
        new_formatted_filename = format_filename(new_filename)
        old_filepath = safe_join(working_directory, old_formatted_filename)
        new_filepath = safe_join(working_directory, new_formatted_filename)

        os.rename(old_filepath, new_filepath)
        return "File renamed successfully."
    except Exception as e:
        return "Error: " + str(e)

def search_files(directory):
    found_files = []

    if directory == "" or directory == "/":
        search_directory = working_directory
    else:
        search_directory = safe_join(working_directory, directory)

    if not os.path.isdir(search_directory):
        return "Error: directory does not exist"

    for root, _, files in os.walk(search_directory):
        for file in files:
            if file.startswith("."):
                continue
            relative_path = os.path.relpath(os.path.join(root, file), working_directory)
            found_files.append(relative_path)

    return found_files

def create_directory(directory):
    try:
        dir_path = safe_join(working_directory, directory)
        os.makedirs(dir_path, exist_ok=True)
        return f"Directory '{directory}' created successfully."
    except Exception as e:
        return "Error: " + str(e)

def list_resources(directory=None):
    if directory is None:
        directory = working_directory
        
    resource_list = []

    for entry in os.scandir(directory):
        if not entry.name.startswith('.'):
            if entry.is_dir():
                resource_list.append(f"Folder: {entry.name}")
                resource_list += list_resources(os.path.join(directory, entry.name))
            elif entry.is_file():
                resource_list.append(f"File: {entry.name}")

    return resource_list

def resources_to_string(resource_list):
    resources_string = "Resource file map:\n"
    for resource in resource_list:
        resources_string += f"{resource}\n"

    return resources_string

def summarize_resources():
    return f"Summary of contents:\n{summarize_contents(working_directory)}\n\nResource file map:\n{(list_resources())}"

def get_directory_summary(directory):
    summary = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                content = f.read()
            summary.append({'file_path': file_path, 'content': content})
    return summary
