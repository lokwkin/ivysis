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

#### Quick start
```bash
# Install dependencies using poetry
poetry install

# Start serving local LLM using Ollama
ollama run qwen2.5:7b  # or other model of your choice

# Start the app

# usage: app.py [-h] [--email EMAIL] [--password PASSWORD] [--days DAYS] [--load_implications LOAD_IMPLICATIONS] [--load_biography LOAD_BIOGRAPHY] [--digest_email DIGEST_EMAIL]

# options:
#   -h, --help            show this help message and exit
#   --email EMAIL         Email address
#   --password PASSWORD   Password
#   --days DAYS           Days
#   --load_implications LOAD_IMPLICATIONS
#                         implications file path
#   --load_biography LOAD_BIOGRAPHY
#                         Biography file path
#   --digest_email DIGEST_EMAIL
#                         Email json file path

poetry run python app.py --email=example@gmail.com --password='1234 5678 abcd efgh' 
```
As a POC, we currently only support fetching emails from Gmail. 
Please see [App Passwords](https://knowledge.workspace.google.com/kb/how-to-create-app-passwords-000009237) on instruction on how to create a "App Password" which is the Google way to grant Gmail access to applications for access programmatically.


## Contributing

We welcome contributions from the community!
Feel free to open an issue or submit a pull request.
Or join our discord server at [https://discord.gg/VCBpySQ5](https://discord.gg/VCBpySQ5) to chat with us.

## License
Ivysis is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
