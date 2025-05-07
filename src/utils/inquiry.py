import inquirer

def unwanted_categories(categories) -> list:
    select = [inquirer.Checkbox(
        'unwanted_categories',
        message="Select categories for a new Suggestion then press ENTER to proceed",
        choices=[item for item in categories],
    )]
    answers = inquirer.prompt(select)  # returns a dict
    return answers['unwanted_categories']