"""File operations for AutoGPT"""
import os
import os.path
from pathlib import Path
from typing import Generator, List
import shutil

from autogpt.smart_utils import summarize_contents

from pdfminer.high_level import extract_text

# Set a dedicated folder for file I/O
WORKING_DIRECTORY = Path(__file__).parent.parent / "auto_gpt_workspace"

# Create the directory if it doesn't exist
if not os.path.exists(WORKING_DIRECTORY):
    os.makedirs(WORKING_DIRECTORY)

WORKING_DIRECTORY = str(WORKING_DIRECTORY)


def safe_join(base: str, *paths) -> str:
    """Join one or more path components intelligently.

    Args:
        base (str): The base path
        *paths (str): The paths to join to the base path

    Returns:
        str: The joined path
    """
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

def split_file(
    content: str, max_length: int = 4000, overlap: int = 0
) -> Generator[str, None, None]:
    """
    Split text into chunks of a specified maximum length with a specified overlap
    between chunks.

    :param content: The input text to be split into chunks
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


def read_file(filename: str) -> str:
    """Read a file and return the contents

    Args:
        filename (str): The name of the file to read

    Returns:
        str: The contents of the file
    """
    try:
        formatted_filename = format_filename(filename)
        filepath = safe_join(WORKING_DIRECTORY, formatted_filename)
        # Check if the file is a PDF and extract text if so
        if is_pdf(filepath):
            text = extract_text(filepath)
            if not text:
                return "Error: Could not extract text from PDF"
            else:
                return text
        else:
            filepath = safe_join(WORKING_DIRECTORY, formatted_filename)
            with open(filepath, "r", encoding='utf-8') as f:
                content = f.read()
            return content
    except Exception as e:
        return handle_file_error("read", filename, str(e))


def ingest_file(
    filename: str, memory, max_length: int = 4000, overlap: int = 200
) -> None:
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


def write_to_file(filename: str, text: str) -> str:
    """Write text to a file

    Args:
        filename (str): The name of the file to write to
        text (str): The text to write to the file

    Returns:
        str: A message indicating success or failure
    """
    try:
        formatted_filename = format_filename(filename)
        filepath = safe_join(WORKING_DIRECTORY, formatted_filename)
        directory = os.path.dirname(filepath)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text)
        return "File " + filename + " written to successfully."
    except Exception as e:
        return handle_file_error("write", filename, str(e))


def append_to_file(filename: str, text: str) -> str:
    """Append text to a file

    Args:
        filename (str): The name of the file to append to
        text (str): The text to append to the file

    Returns:
        str: A message indicating success or failure
    """
    try:
        formatted_filename = format_filename(filename)
        filepath = safe_join(WORKING_DIRECTORY, formatted_filename)
        with open(filepath, "a") as f:
            f.write(text)
        return "Text appended to " + filename + " successfully."
    except Exception as e:
        return handle_file_error("append", filename, str(e))


def delete_file(filename: str) -> str:
    """Delete a file

    Args:
        filename (str): The name of the file to delete

    Returns:
        str: A message indicating success or failure
    """
    try:
        formatted_filename = format_filename(filename)
        filepath = safe_join(WORKING_DIRECTORY, formatted_filename)
        os.remove(filepath)
        return "File "  + filename + " deleted successfully."
    except Exception as e:
        return handle_file_error("delete", filename, str(e))
    

def copy_file(src_filename, dest_directory):
    try:
        formatted_src_filename = format_filename(src_filename)
        src_filepath = safe_join(WORKING_DIRECTORY, formatted_src_filename)
        dest_directory_path = safe_join(WORKING_DIRECTORY, dest_directory)
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
        src_filepath = safe_join(WORKING_DIRECTORY, formatted_src_filename)
        dest_directory_path = safe_join(WORKING_DIRECTORY, dest_directory)
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
        old_filepath = safe_join(WORKING_DIRECTORY, old_formatted_filename)
        new_filepath = safe_join(WORKING_DIRECTORY, new_formatted_filename)

        os.rename(old_filepath, new_filepath)
        return "File renamed successfully."
    except Exception as e:
        return "Error: " + str(e)

def search_files(directory: str) -> List[str]:
    """Search for files in a directory

    Args:
        directory (str): The directory to search in

    Returns:
        List[str]: A list of files found in the directory
    """
    found_files = []

    if directory in {"", "/"}:
        search_directory = WORKING_DIRECTORY
    else:
        search_directory = safe_join(WORKING_DIRECTORY, directory)

    if not os.path.isdir(search_directory):
        return "Error: directory does not exist"

    for root, dirs, files in os.walk(search_directory):
        for file in files:
            if file.startswith("."):
                continue
            relative_path = os.path.relpath(os.path.join(root, file), WORKING_DIRECTORY)
            found_files.append(relative_path)

    return found_files

def create_directory(directory):
    try:
        dir_path = safe_join(WORKING_DIRECTORY, directory)
        os.makedirs(dir_path, exist_ok=True)
        return f"Directory '{directory}' created successfully."
    except Exception as e:
        return "Error: " + str(e)

def list_resources(directory=None):
    if directory is None:
        directory = WORKING_DIRECTORY
        
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
    return f"Summary of contents:\n{summarize_contents(WORKING_DIRECTORY)}\n\nResource file map:\n{(list_resources())}"

def get_directory_summary(directory):
    summary = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                content = f.read()
            summary.append({'file_path': file_path, 'content': content})
    return summary

def is_pdf(file_path):
    with open(file_path, 'rb') as file:
        file_header = file.read(5)
    return file_header == b'%PDF-'

def get_filesystem_representation(path: str = WORKING_DIRECTORY, level: int = 0) -> str:
    """
    Generate a human-readable representation of a filesystem, starting from the given path.

    Args:
        path (str, optional): The starting path of the filesystem representation.
        Defaults to WORKING_DIRECTORY.
        level (int, optional): The current level of indentation. Defaults to 0.

    Returns:
        str: The filesystem representation as a formatted string.
    """
    if not os.path.exists(path):
        return ""

    representation = ""
    entries = sorted(os.listdir(path))
    indent = ">"
    file_prefix = "- "
    dir_prefix = "+ "

    for entry in entries:
        entry_path = os.path.join(path, entry)
        if os.path.isfile(entry_path):
            representation += indent * level + file_prefix + entry + "\n"
        elif os.path.isdir(entry_path):
            representation += indent * level + dir_prefix + entry + "\n"
            representation += get_filesystem_representation(entry_path, level + 1)

    return representation


def handle_file_error(operation: str, filename: str, error: str) -> str:
    """
    Handle file-related errors by printing a message with the current filesystem and the error.

    Args:
        operation (str): The operation being performed on the file.
        filename (str): The filename involved in the error.
        error (str): The error message.

    Returns:
        str: The full error message containing the operation, filename, error, and current filesystem.
    """
    current_filesystem = get_filesystem_representation(WORKING_DIRECTORY)
    error_message = f"Error trying to {operation} {filename} - File likely doesn't exist. Current filesystem:\n{current_filesystem}\nError: {error}"
    print(error_message)
    return error_message
