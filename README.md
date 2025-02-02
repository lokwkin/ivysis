# Ivysis
To build a personal AI secretary who understands you and works for you proactively and confidentially.

## Overview
Ivysis (**IVY** **S**ecretarial **I**ntelligence **S**ystem) is an open-source project aimed to create a personal AI secretary (called Ivy) who assists you seamlessly across your personal and professional life, just like a real human-secretary.

Ivy proactively organizes, notifies and reminds you about the tasks or updates in your professional and personal life. She understands you so well that she only delivers what you need to know.

More importantly, Ivy runs totally on your machine to ensure privacy, so you can feel free granting Ivy accesses of your personal data, to best leverage Ivy to work for you.

## Getting Started
#### Prerequisites
* Python 3.12+
* Ollama (See [https://ollama.com](https://ollama.com))

```bash
# Install dependencies using poetry
poetry install

# Start serving local LLM using Ollama
ollama run qwen2.5:7b  # or other model of your choice
```

## Usage

Ivysis provides two main commands:
#### Build or update Persona:
```bash
poetry run python app.py persona --email_addr example@gmail.com --email_pwd 'your-app-password' [--load_checkpoint ./data/{run_id}/checkpoint_{idx}] [--days 3]

# Arguments:
#   --email_addr        Gmail address
#   --email_pwd        Gmail app password
#   --load_checkpoint  (Optional) Path to previous checkpoint directory
#   --days            (Optional) Number of days of emails to process (default: 3)
```
As a POC, we currently only support fetching emails from Gmail. 
Please see [App Passwords](https://knowledge.workspace.google.com/kb/how-to-create-app-passwords-000009237) on instruction on how to create a "App Password" which is the Google way to grant Gmail access to applications for access programmatically.

#### Build Memo Board
```bash
poetry run python app.py memoboard --load_persona ./persona.txt --email ./email.json

# Arguments:
#   --load_persona    Path to persona data file
#   --email          Path to email JSON file to process
```

## To Do and Roadmap

#### Phase 1
- [X] Fetch past emails
- [X] Persona Formation in text form (biography)
- [ ] Auto digest new in/out emails
- [ ] Memoboard Formation
- [ ] Today's tasks highlighter
- [ ] Persistent data storing and organizing with sqlite
- [ ] Basic UI for initial setup and chatting
- [ ] Package with docker compose
- [ ] Simplfied initial setup and onboarding

#### Phase 2
- [ ] Schedule and reminder
- [ ] Informative updates organization
- [ ] Proactive notifications triggered by system
- [ ] Support Outlook as datasource
- [ ] Support Slack as datasource


## Contributing

We welcome contributions from the community!
Feel free to open an issue or submit a pull request.
Or join our discord server at [https://discord.gg/VCBpySQ5](https://discord.gg/VCBpySQ5) to chat with us.

## License
Ivysis is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
