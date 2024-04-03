# chai_chatbot

Python script for CLI with Chai AI chatbot.

## Usage

```bash
python chai_cli.py
```

## Design Choices

**1. bot_memory:** Excluded persistent bot_memory between sessions. Would be implemented in the same fashion as persistent bot_name.

**2. bot_memory:** Used a rudimentary summarizer to ensure bot memory wouldn't overfill. (Optional)
