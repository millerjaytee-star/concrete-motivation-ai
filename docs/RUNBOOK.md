# Version 3 Runbook

## Set up in VS Code

1. Open the repository folder in VS Code.
2. Open **Terminal → New Terminal**.
3. Confirm Python 3.11 or newer with `python --version` (use `python3` if needed).
4. Create an environment: `python -m venv .venv`.
5. Activate it:
   - macOS/Linux: `source .venv/bin/activate`
   - Windows PowerShell: `.venv\Scripts\Activate.ps1`
6. Install dependencies: `python -m pip install -r requirements.txt`.

No account, internet connection, API key, or `.env` file is required for offline mode.

## Run the Command Center

Run `python main.py`. The app prints the active provider, then shows the menu. Enter a number from 1 to 8 and describe the deliverable. The app then asks:

```text
Any specific audience, tone, or personal detail to include? Press Enter to skip.
```

Press Enter to keep the default Concrete Motivation audience, or add detail such as `for high school football players`, `make it about fatherhood`, `make it faith-based but not preachy`, or `make it intense for Instagram reels`. The response prints as structured Markdown and includes a `Concrete Motivation Angle` section. After each response the menu appears again. Enter `0` to exit.

## Run Offline

Offline is the default and safest mode:

```bash
python main.py
```

You can also force it:

```bash
CONCRETE_AI_PROVIDER=offline python main.py
```

## Enable OpenAI Mode

1. Copy the example environment file: `cp .env.example .env`.
2. Put your real API key in `.env`.
3. Set these values in the terminal session that runs the app:

```bash
export OPENAI_API_KEY=your_real_api_key
export CONCRETE_AI_PROVIDER=openai
python main.py
```

The app should print `Provider: openai`. If OpenAI is unavailable for a response, the app prints a calm fallback message and returns the offline response instead. To return to offline mode, set `CONCRETE_AI_PROVIDER=offline` or unset both variables.

## Verify the project

Run `python -m pytest`. A passing suite confirms the registry, prompt library, brand profile, personalization layer, provider factory, OpenAI prompt construction, offline fallback, runner, response structure, and important error paths.

## Troubleshooting

- **Python is not found:** install Python 3.11+ and restart VS Code.
- **pytest or openai is not found:** activate `.venv` and run the install command again.
- **Prompt file not found:** run from the repository checkout and restore the `prompts/` directory. Paths are resolved from the package, so the app does not depend on the terminal's current folder.
- **Input was rejected:** choose a menu number from 0 to 8 and enter a non-empty goal. The personalization follow-up is optional and can be blank.
- **OpenAI mode shows offline:** confirm `CONCRETE_AI_PROVIDER=openai` and `OPENAI_API_KEY` are both set in the same terminal session.
- **OpenAI generation failed:** the app automatically uses offline mode for that response. Check your key, billing, network connection, and package install before trying OpenAI mode again.
- **Stop the app:** enter `0`, press Ctrl+C, or send end-of-file (Ctrl+D on macOS/Linux; Ctrl+Z then Enter on Windows).

## Operating rhythm

Start with one clear business or content goal, select the best specialist, add any audience or personal context that matters, edit the draft in your own voice, verify factual or scriptural claims, and save the finished asset in the tool where it will be used. Version 3 offline mode does not store inputs or outputs; OpenAI mode sends the prompt context to OpenAI to generate the response.
