# Version 1 Runbook

## Set up in VS Code

1. Open the repository folder in VS Code.
2. Open **Terminal → New Terminal**.
3. Confirm Python 3.11 or newer with `python --version` (use `python3` if needed).
4. Create an environment: `python -m venv .venv`.
5. Activate it:
   - macOS/Linux: `source .venv/bin/activate`
   - Windows PowerShell: `.venv\Scripts\Activate.ps1`
6. Install the test dependency: `python -m pip install -r requirements.txt`.

No account, internet connection, API key, or `.env` file is required.

## Run the Command Center

Run `python main.py`, enter a number from 1 to 8, and describe the deliverable. The response prints as structured Markdown. After each response the menu appears again. Enter `0` to exit.

## Verify the project

Run `python -m pytest`. A passing suite confirms the registry, prompt library, runner, response structure, and important error paths.

## Troubleshooting

- **Python is not found:** install Python 3.11+ and restart VS Code.
- **pytest is not found:** activate `.venv` and run the install command again.
- **Prompt file not found:** run from the repository checkout and restore the `prompts/` directory. Paths are resolved from the package, so the app does not depend on the terminal's current folder.
- **Input was rejected:** choose a menu number from 0 to 8 and enter a non-empty goal.
- **Stop the app:** enter `0`, press Ctrl+C, or send end-of-file (Ctrl+D on macOS/Linux; Ctrl+Z then Enter on Windows).

## Operating rhythm

Start with one clear business or content goal, select the best specialist, edit the draft in your own voice, verify factual or scriptural claims, and save the finished asset in the tool where it will be used. Version 1 intentionally does not store inputs or outputs.
