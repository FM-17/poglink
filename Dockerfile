FROM python:3.6-alpine as build

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install wheel \
    && pip wheel \
        -r requirements.txt \
        --wheel-dir /tmp/wheels


FROM python:3.6-alpine

# Copy python wheels from build stage
COPY --from=build /tmp/wheels /tmp/wheels
COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install \
        -r requirements.txt \
        --no-index \
        --find-links /tmp/wheels 

COPY ark_discord_bot ./ark_discord_bot
COPY setup.py .

RUN pip install . \
    && rm -rf \
        /tmp/wheels \
        requirements.txt \
        setup.py \
        ark_discord_bot


# Set up non-root user
ARG USERNAME=bot
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN apk add --no-cache shadow 
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

COPY entrypoint.sh .
COPY sample-config.yaml /sample-config.yaml

# Set output directory for persistent data
ENV BOT_DATA_DIR=/data
RUN mkdir -p $BOT_DATA_DIR && chown ${USER_UID}:${USER_GID} $BOT_DATA_DIR
COPY sample-config.yaml ${BOT_DATA_DIR}}

USER ${USERNAME}

ENTRYPOINT [ "sh", "entrypoint.sh" ]