FROM python:3.6 

COPY setup.py .
COPY ark_discord_bot ./ark_discord_bot
COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install .

ENTRYPOINT [ "ark-discord-bot" ]