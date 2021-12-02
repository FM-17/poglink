# Running Natively

1. Get the code via either of the following two options

    a) Download & extract the [latest bot release](https://github.com/FM-17/ark_discord_bot/releases/latest)

    b) Clone the repo via `git clone https://github.com/FM-17/ark_discord_bot.git` 

2. Copy `sample_config.yaml` and rename it to `config.yaml`
3. Open `config.yaml` and fill in the required values.


4. Install the bot. I recommend doing this within a virtual environment.

    ```bash
    # navigate to download location
    cd {download location}/ark-discord-bot/

    # [optional] create a virtual environment and set as default for current directory
    pyenv install 3.6.9
    pyenv virtualenv 3.6.9 {virtualenv name}
    pyenv local {virtualenv name} 

    # install bot
    pip install .
    ```