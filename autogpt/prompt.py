from colorama import Fore

from autogpt.config import Config
from autogpt.config.ai_config import AIConfig
from autogpt.config.config import Config
from autogpt.logs import logger
from autogpt.promptgenerator import PromptGenerator
from autogpt.setup import prompt_user
from autogpt.utils import clean_input

CFG = Config()


def get_prompt() -> str:
    """
    This function generates a prompt string that includes various constraints,
        commands, resources, and performance evaluations.

    Returns:
        str: The generated prompt string.
    """

    # Initialize the Config object
    cfg = Config()

    # Initialize the PromptGenerator object
    prompt_generator = PromptGenerator()

    # Add constraints to the PromptGenerator object
    prompt_generator.add_constraint(
        "~4000 word limit for short term memory. Your short term memory is short, so"
        " immediately save important information to files."
    )
    prompt_generator.add_constraint(
        "If you are unsure how you previously did something or want to recall past"
        " events, thinking about similar events will help you remember."
    )
    prompt_generator.add_constraint("No user assistance")
    prompt_generator.add_constraint(
        'Exclusively use a valid command listed in double quotes e.g. "command name"'
    )
    prompt_generator.add_constraint(
        "All content should be written in .md files using Markdown formatting unless a .csv file is warranted or you are creating a directory."
    )
    prompt_generator.add_constraint(
        "All responses must be in JSON and only JSON."
    )
    prompt_generator.add_constraint(
        "Do not create new files with the same content as existing files."
    )

    # Define the command list
    get_prompt.commands = [
        ("Google Search", "google", {"input": "<search>"}),
        (
            "Browse Website",
            "browse_website",
            {"url": "<url>", "question": "<what_you_want_to_find_on_website>"},
        ),
        
        # Agents
        (
            "Start GPT Agent",
            "start_agent",
            {"name": "<name>", "task": "<short_task_desc>", "prompt": "<prompt>"},
        ),
        (
            "Message GPT Agent",
            "message_agent",
            {"key": "<key>", "message": "<message>"},
        ),
        ("List GPT Agents", "list_agents", {}),
        ("Delete GPT Agent", "delete_agent", {"key": "<key>"}),

        # File stuff
        (
            "Clone Repository",
            "clone_repository",
            {"repository_url": "<url>", "clone_path": "<directory>"},
        ),
        ("Write to file", "write_to_file", {"file": "<file>", "text": "<text>"}),
        ("Read file", "read_file", {"file": "<file>"}),
        ("Append to file", "append_to_file", {"file": "<file>", "text": "<text>"}),
        ("Delete file", "delete_file", {"file": "<file>"}),
        ("Copy File", "copy_file", {"source": "<source>", "destination": "<destination>"}),
        ("Move File", "move_file", {"source": "<source>", "destination": "<destination>"}),
        ("Rename File", "rename_file", {"source": "<source>", "destination": "<destination>"}),
        ("Search Files", "search_files", {"directory": "<directory>"}),

        ("Create Directory", "create_directory", {"directory": "<directory>"}),
        ("Evaluate Resources", "evaluate_resources", {}),
        ("List Directories", "list_resources", {}),

        ("Generate Image", "generate_image", {"prompt": "<prompt>"}),
        ("Get Filesystem Representation", "get_filesystem_representation", {}),
        ("Evaluate Code", "evaluate_code", {"code": "<full_code_string>"}),
        (
            "Get Improved Code",
            "improve_code",
            {"suggestions": "<list_of_suggestions>", "code": "<full_code_string>"},
        ),
        (
            "Write Tests",
            "write_tests",
            {"code": "<full_code_string>", "focus": "<list_of_focus_areas>"},
        ),
        ("Execute Python File", "execute_python_file", {"file": "<file>"}),
        ("Command Help", "help", {"command": "<command>"}),
        ("List Commands", "list_commands", {}),
        ("Convert Audio to text", "read_audio_from_file", {"file": "<file>"}),
        ("Send Tweet", "send_tweet", {"text": "<text>"}),

    ]

    # Only add shell command to the prompt if the AI is allowed to execute it
    if cfg.execute_local_commands:
        get_prompt.commands.append(
            (
                "Execute Shell Command, non-interactive commands only",
                "execute_shell",
                {"command_line": "<command_line>"},
            ),
        )

    # Add these command last.
    # commands.append(
    #     ("Do Nothing", "do_nothing", {}),
    # )
    get_prompt.commands.append(
        ("Task Complete (Shutdown)", "task_complete", {"reason": "<reason>"}),
    )

    # Add commands to the PromptGenerator object
    for command_label, command_name, args in get_prompt.commands:
        prompt_generator.add_command(command_label, command_name, args)

    # Add resources to the PromptGenerator object
    prompt_generator.add_resource(
        "Internet access for searches and information gathering."
    )
    prompt_generator.add_resource("Long Term memory management.")
    prompt_generator.add_resource(
        "GPT-3.5 powered Agents for delegation of simple tasks."
    )
    prompt_generator.add_resource("File output.")

    # Add performance evaluations to the PromptGenerator object
    prompt_generator.add_performance_evaluation("Continuously review and analyze your actions to ensure you are performing to the best of your abilities and producing quality research output.")
    prompt_generator.add_performance_evaluation("Constructively evaluate the file system and implement strategies that allow information to coalesce into folders.")
    prompt_generator.add_performance_evaluation("Constructively self-criticize your big-picture behavior from time to time.")
    prompt_generator.add_performance_evaluation("Reflect on past decisions, strategies, and output to refine your approach.")
    prompt_generator.add_performance_evaluation("Every command has a cost, so be smart and efficient. Aim to complete tasks in the least number of steps.")

    # Generate the prompt string
    return prompt_generator.generate_prompt_string()


def construct_prompt() -> str:
    """Construct the prompt for the AI to respond to

    Returns:
        str: The prompt string
    """
    config = AIConfig.load(CFG.ai_settings_file)
    if CFG.skip_reprompt and config.ai_name:
        logger.typewriter_log("Name :", Fore.GREEN, config.ai_name)
        logger.typewriter_log("Role :", Fore.GREEN, config.ai_role)
        logger.typewriter_log("Goals:", Fore.GREEN, f"{config.ai_goals}")
    elif config.ai_name:
        logger.typewriter_log(
            "Welcome back! ",
            Fore.GREEN,
            f"Would you like me to return to being {config.ai_name}?",
            speak_text=True,
        )
        should_continue = clean_input(
            f"""Continue with the last settings?
Name:  {config.ai_name}
Role:  {config.ai_role}
Goals: {config.ai_goals}
Continue (y/n): """
        )
        if should_continue.lower() == "n":
            config = AIConfig()

    if not config.ai_name:
        config = prompt_user()
        config.save()

    # Get rid of this global:
    global ai_name
    ai_name = config.ai_name

    return config.construct_full_prompt()
