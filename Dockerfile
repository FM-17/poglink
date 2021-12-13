FROM python:3.7-alpine as build

# Build requirements
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install wheel \
    && pip wheel \
        -r requirements.txt \
        --wheel-dir /tmp/wheels

# Build application
COPY poglink ./poglink
COPY setup.py .
COPY setup.cfg .
COPY LICENSE .
COPY README.md .
ARG PYTHON_PACKAGE_VERSION=0.0.1
RUN pip wheel --wheel-dir /tmp/wheels .

FROM python:3.7-alpine

WORKDIR /app

# Copy pre-built wheels from build stage
COPY --from=build /tmp/wheels /tmp/wheels

# Install application and dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install \
        -r requirements.txt \
        --no-index \
        poglink \
        --find-links /tmp/wheels \
    && rm -r \
        requirements.txt \
        /tmp/wheels 

# Set up non-root user
ARG USERNAME=bot
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN apk add --no-cache shadow 
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

# Set up entrypoint script to check for config file
COPY entrypoint.sh .
COPY sample-config.yaml /sample-config.yaml

# Set output directory for persistent data
ENV BOT_DATA_DIR=/data
RUN mkdir -p $BOT_DATA_DIR && chown ${USER_UID}:${USER_GID} $BOT_DATA_DIR
COPY sample-config.yaml ${BOT_DATA_DIR}

USER ${USERNAME}

ENTRYPOINT [ "sh", "entrypoint.sh" ]