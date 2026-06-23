# Version 6 Runbook

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

Run `python main.py`. The app prints the active provider, then shows the menu. Enter a number from 1 to 8 and describe the deliverable. Enter `9` to view recent saved outputs. Enter `10` to build a weekly content calendar. Bot workflows ask:

```text
Any specific audience, tone, or personal detail to include? Press Enter to skip.
```

Press Enter to keep the default Concrete Motivation audience, or add detail such as `for high school football players`, `make it about fatherhood`, `make it faith-based but not preachy`, or `make it intense for Instagram reels`. The response prints as structured Markdown and includes a `Concrete Motivation Angle` section.

After each response, the app asks:

```text
Save this output to the content vault? [Y/n]
```

Press Enter or type `y` to save. Type `n` to skip. After that, the menu appears again. Enter `0` to exit.

## Build a Weekly Content Calendar

Choose menu option `10`. The app asks:

```text
What is the main theme for this week?
```

Then it asks:

```text
Any audience, platform, event, or business goal to include? Press Enter to skip.
```

The engine creates a 7-day calendar:

- Monday: Mindset Reel
- Tuesday: Podcast Clip
- Wednesday: Athlete/Youth Message
- Thursday: Fatherhood/Faith/Leadership Post
- Friday: Concrete Conversations Episode Push
- Saturday: Behind-the-Scenes / Story Post
- Sunday: Reflection / Reset / Weekly Challenge

Each day includes the day, content type, hook, short script or caption, call to action, recommended platform, and repurpose idea. The same save prompt appears after the calendar, and saved calendars go to `outputs/content_calendars`.

## Use the Content Vault

Saved outputs are local Markdown assets under `outputs/`, organized by bot:

- `outputs/speeches`
- `outputs/podcast_episodes`
- `outputs/social_posts`
- `outputs/outreach_messages`
- `outputs/business_growth`
- `outputs/operations`
- `outputs/faith_mindset`
- `outputs/brand`
- `outputs/content_calendars`

Each saved file includes metadata for bot name, goal, provider, fallback status, and creation timestamp, followed by the full Markdown response. Choose menu option `9` to see the 10 most recent saved files. Generated Markdown files are ignored by Git by default; the folder structure stays committed.

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

Run `python -m pytest`. A passing suite confirms the registry, prompt library, brand profile, personalization layer, provider factory, OpenAI prompt construction, offline fallback, output vault, content calendar engine, runner, response structure, and important error paths.

## Preview the Website

Open `website/index.html` in a browser. The site is static, so it does not require a backend, build step, deployment, payment integration, or live form service. The contact form is a placeholder until a form service is connected.

## Troubleshooting

- **Python is not found:** install Python 3.11+ and restart VS Code.
- **pytest or openai is not found:** activate `.venv` and run the install command again.
- **Prompt file not found:** run from the repository checkout and restore the `prompts/` directory. Paths are resolved from the package, so the app does not depend on the terminal's current folder.
- **Input was rejected:** choose a menu number from 0 to 10 and enter a non-empty goal or calendar theme. The personalization follow-up is optional and can be blank.
- **Output did not save:** press Enter or type `y` at the save prompt. Typing `n` skips saving.
- **Recent outputs are empty:** save at least one response first, then choose menu option `9`.
- **OpenAI mode shows offline:** confirm `CONCRETE_AI_PROVIDER=openai` and `OPENAI_API_KEY` are both set in the same terminal session.
- **OpenAI generation failed:** the app automatically uses offline mode for that response. Check your key, billing, network connection, and package install before trying OpenAI mode again.
- **Stop the app:** enter `0`, press Ctrl+C, or send end-of-file (Ctrl+D on macOS/Linux; Ctrl+Z then Enter on Windows).

## Operating rhythm

Start with one clear business or content goal, select the best specialist or build a weekly calendar, add any audience or personal context that matters, save useful drafts to the vault, edit the draft in your own voice, verify factual or scriptural claims, and move the finished asset into the tool where it will be used. Version 6 offline mode sends nothing over the internet; OpenAI mode sends bot prompt context to OpenAI to generate bot responses. Use the website as the first public-facing brand foundation.
