"""Command Help Message Dictionary"""

command_help = {
    "google": (
        "COMMAND: Google Search\n"
        "DESCRIPTION: Search Google for an input string\n"
        "ARGUMENTS:\n"
        "Input (str): The phrase to search Google for\n"
        "EXAMPLE: {'name': 'google', 'args': {'input': 'AI research breakthroughs'}}"
    ),
    "browse_website": (
        "COMMAND: Browse Website\n"
        "DESCRIPTION: Browse a website and find specific information based on the question provided\n"
        "ARGUMENTS:\n"
        "URL (str): The URL of the website to browse\n"
        "Question (str): The question describing the information you want to find on the website\n"
        "EXAMPLE: {'name': 'browse_website', 'args': {'url': 'https://example.com/history', 'question': 'What is the history of Example Inc.?'}}"
    ),
    "start_agent": (
        "COMMAND: Start GPT Agent\n"
        "DESCRIPTION: Start a GPT agent with a specified name, task, and prompt\n"
        "ARGUMENTS:\n"
        "Name (str): The name of the GPT agent\n"
        "Task (str): A short description of the task for the GPT agent\n"
        "Prompt (str): The initial prompt for the GPT agent\n"
        "EXAMPLE: {'name': 'start_agent', 'args': {'name': 'Agent1', 'task': 'Research AI', 'prompt': 'Tell me about the history of artificial intelligence'}}"
    ),
    "message_agent": (
        "COMMAND: Message GPT Agent\n"
        "DESCRIPTION: Send a message to a specific GPT agent based on the agent's key\n"
        "ARGUMENTS:\n"
        "Key (int): The key of the GPT agent to send the message to\n"
        "Message (str): The message to send to the GPT agent\n"
        "EXAMPLE: {'name': 'message_agent', 'args': {'key': 1, 'message': 'What are the applications of machine learning in healthcare?'}}"
    ),
    "list_agents": (
        "COMMAND: List GPT Agents\n"
        "DESCRIPTION: List all the active GPT agents\n"
        "ARGUMENTS: None\n"
        "EXAMPLE: {'name': 'list_agents', 'args': {}}"
    ),
    "delete_agent": (
        "COMMAND: Delete GPT Agent\n"
        "DESCRIPTION: Delete a specific GPT agent based on the agent's key\n"
        "ARGUMENTS:\n"
        "Key (int): The key of the GPT agent to delete\n"
        "EXAMPLE: {'name': 'delete_agent', 'args': {'key': 1}}"
    ),
    "clone_repository": (
        "COMMAND: Clone Repository\n"
        "DESCRIPTION: Clone a git repository to a specified directory\n"
        "ARGUMENTS:\n"
        "Repository URL (str): The URL of the git repository to clone\n"
        "Clone Path (str): The directory to clone the repository into\n"
        "EXAMPLE: {'name': 'clone_repository', 'args': {'repository_url': 'https://github.com/example/example.git', 'clone_path': '/path/to/clone'}}"
    ),
    "write_to_file": (
        "COMMAND: Write to File\n"
        "DESCRIPTION: Write text to a specified file, overwriting any existing content\n"
        "ARGUMENTS:\n"
        "File (str): The path to the file to write to\n"
        "Text (str): The text to write to the file\n"
        "EXAMPLE: {'name': 'write_to_file', 'args': {'file': '/path/to/file.txt', 'text': 'Hello, World!'}}"
    ),
    "read_file": (
        "COMMAND: Read File\n"
        "DESCRIPTION: Read the content of a specified text or PDF file\n"
        "ARGUMENTS:\n"
        "File (str): The path to the file to read\n"
        "EXAMPLE: {'name': 'read_file', 'args': {'file': '/path/to/file.txt'}}"
    ),
    "append_to_file": (
        "COMMAND: Append to File\n"
        "DESCRIPTION: Append text to a specified file\n"
        "ARGUMENTS:\n"
        "File (str): The path to the file to append to\n"
        "Text (str): The text to append to the file\n"
        "EXAMPLE: {'name': 'append_to_file', 'args': {'file': '/path/to/file.txt', 'text': '\\nNew line of text'}}"
    ),
    "delete_file": (
        "COMMAND: Delete File\n"
        "DESCRIPTION: Delete a specified file\n"
        "ARGUMENTS:\n"
        "File (str): The path to the file to delete\n"
        "EXAMPLE: {'name': 'delete_file', 'args': {'file': '/path/to/file.txt'}}"
    ),
    "copy_file": (
        "COMMAND: Copy File\n"
        "DESCRIPTION: Copy a file from one location to another\n"
        "ARGUMENTS:\n"
        "Source (str): The path to the source file\n"
        "Destination (str): The path to the destination file\n"
        "EXAMPLE: {'name': 'copy_file', 'args': {'source': '/path/to/source.txt', 'destination': '/path/to/destination.txt'}}"
    ),
    "move_file": (
        "COMMAND: Move File\n"
        "DESCRIPTION: Move a file from one location to another\n"
        "ARGUMENTS:\n"
        "Source (str): The path to the source file\n"
        "Destination (str): The path to the destination file\n"
        "EXAMPLE: {'name': 'move_file', 'args': {'source': '/path/to/source.txt', 'destination': '/path/to/destination.txt'}}"
    ),
    "rename_file": (
        "COMMAND: Rename File\n"
        "DESCRIPTION: Rename a file\n"
        "ARGUMENTS:\n"
        "Source (str): The path to the source file\n"
        "Destination (str): The path to the renamed file\n"
        "EXAMPLE: {'name': 'rename_file', 'args': {'source': '/path/to/old_name.txt', 'destination': '/path/to/new_name.txt'}}"
    ),
    "search_files": (
        "COMMAND: Search Files\n"
        "DESCRIPTION: Search for files in a specified directory\n"
        "ARGUMENTS:\n"
        "Directory (str): The path to the directory to search\n"
        "EXAMPLE: {'name': 'search_files', 'args': {'directory': '/path/to/directory'}}"
    ),
    "create_directory": (
        "COMMAND: Create Directory\n"
        "DESCRIPTION: Create a new directory at a specified path\n"
        "ARGUMENTS:\n"
        "Directory (str): The path to the directory to create\n"
        "EXAMPLE: {'name': 'create_directory', 'args': {'directory': '/path/to/new_directory'}}"
    ),
    "evaluate_resources": (
        "COMMAND: Evaluate Resources\n"
        "DESCRIPTION: Returns the number of files, the total size of all the files, how many files there are of each extension, top 10 keywords and their frequency across all the files, and a list of current files and folders\n"
        "ARGUMENTS: None\n"
        "EXAMPLE: {'name': 'evaluate_resources', 'args': {}}"
    ),
    "list_resources": (
        "COMMAND: List Resources\n"
        "DESCRIPTION: Lists the current files and folders\n"
        "ARGUMENTS: None\n"
        "EXAMPLE: {'name': 'list_resources', 'args': {}}"
    ),
    "task_complete": (
        "COMMAND: Task Complete (Shutdown)\n"
        "DESCRIPTION: Shutdown command that quits the program\n"
        "ARGUMENTS:\n"
        "Reason (str): The reason for shutting down the program\n"
        "EXAMPLE: {'name': 'task_complete', 'args': {'reason': 'All tasks completed'}}"
    ),
    "generate_image": (
        "COMMAND: Generate Image\n"
        "DESCRIPTION: Generate an image based on a specified prompt\n"
        "ARGUMENTS:\n"
        "Prompt (str): The prompt for generating the image\n"
        "EXAMPLE: {'name': 'generate_image', 'args': {'prompt': 'A beautiful sunset over the ocean'}}"
    ),
    "do_nothing": (
        "COMMAND: Do Nothing\n"
        "DESCRIPTION: A command that does nothing\n"
        "ARGUMENTS: None\n"
        "EXAMPLE: {'name': 'do_nothing', 'args': {}}"
    ),
    "get_filesystem_representation": (
        "COMMAND: Get Filesystem Representation\n"
        "DESCRIPTION: Returns a directory tree of the whole filesystem\n"
        "ARGUMENTS: None\n"
        "EXAMPLE: {'name': 'get_filesystem_representation', 'args': {}}"
    ),
    "evaluate_code": (
        "COMMAND: Evaluate Code\n"
        "DESCRIPTION: Analyzes the provided Python code for errors and potential improvements without executing it\n"
        "ARGUMENTS:\n"
        "Code (str): The full code string to evaluate\n"
        "EXAMPLE: {'name': 'evaluate_code', 'args': {'code': 'def hello_world():\\n    print(\"Hello, World!\")'}}"
    ),
    "improve_code": (
        "COMMAND: Improve Code\n"
        "DESCRIPTION: Suggest improvements for the provided Python code\n"
        "ARGUMENTS:\n"
        "Suggestions (List): A list of suggestions to consider\n"
        "Code (str): The full code string to improve\n"
        "EXAMPLE: {'name': 'improve_code', 'args': {'suggestions': ['optimization', 'readability'], 'code': 'def hello_world():\\n    print(\"Hello, World!\")'}}"
    ),
    "write_tests": (
        "COMMAND: Write Tests\n"
        "DESCRIPTION: Write tests for the provided Python code, focusing on specified areas\n"
        "ARGUMENTS:\n"
        "Code (str): The full code string to write tests for\n"
        "Focus (str): A list of focus areas for the tests\n"
        "EXAMPLE: {'name': 'write_tests', 'args': {'code': 'def hello_world():\\n    print(\"Hello, World!\")', 'focus': 'functionality, edge_cases'}}"
    ),
    "execute_python_file": (
        "COMMAND: Execute Python File\n"
        "DESCRIPTION: Execute a specified Python file\n"
        "ARGUMENTS:\n"
        "File (str): The path to the Python file to execute\n"
        "EXAMPLE: {'name': 'execute_python_file', 'args': {'file': '/path/to/script.py'}}"
    ),
    "execute_shell": (
        "COMMAND: Execute Shell Command\n"
        "DESCRIPTION: Execute a non-interactive shell command\n"
        "ARGUMENTS:\n"
        "Command Line (str): The shell command to execute\n"
        "EXAMPLE: {'name': 'execute_shell', 'args': {'command_line': 'ls -la'}}"
    ),
    "list_commands": (
        "COMMAND: List Commands\n"
        "DESCRIPTION: List all available commands\n"
        "ARGUMENTS: None\n"
        "EXAMPLE: {'name': 'list_commands', 'args': {}}"
    ),
    "help": (
        "COMMAND: Help\n"
        "DESCRIPTION: Get help with a command\n"
        "ARGUMENTS:\n"
        "Command (str): The command to get help with\n"
        "EXAMPLE: {'name': 'help', 'args': {'command': 'read_file'}}"
    ),
    "read_audio_from_file": (
        "COMMAND: Convert Audio to Text \n"
        "DESCRIPTION: Transcribe voice to text from an audio file\n"
        "ARGUMENTS:\n"
        "File (str): The path to the audio file to transcribe\n"
        "EXAMPLE: {'name': 'read_audio_from_file', 'args': {'file': 'speech.mp4'}}"
    ),
    "send_tweet": (
        "COMMAND: Send Tweet\n"
        "DESCRIPTION: Send a Tweet\n"
        "ARGUMENTS:\n"
        "Tweet (str): The command to get help with\n"
        "EXAMPLE: {'name': 'send_tweet', 'args': {'text': 'Hello humans!'}}"
    )
}