# task-creation-helper

Utility for Jira task creation. Positioned as simpler tool than UI related analogs when used together with Copilot in VSCode.

## Installation

1. Clone the repository
2. Set up a virtual environment (venv)
3. Install dependencies
4. Create a `.env` file with your Jira credentials in `/app` directory. The file should look like this:
    ```text
    JIRA_EMAIL=your-email@example.com
    JIRA_API_TOKEN=your-api-token
    ```

## Usage

1. Open `tasks.yaml` file in the `/app` directory. Consider comment lines at the beginning of the file as prompts for Copilot. Change them to your needs.
2. Create your tasks in the `tasks.yaml` file following the defined structure.
3. Open the command palette in VSCode (Ctrl+Shift+P) and run the command `Tasks: Run Task`.
4. Select the task `Create Jira Tasks`.
5. In terminal, you will see the output of the task creation process.
