# Running within a Docker container

## Installation
Pull the latest docker image
```
docker pull fm17/poglink
```
## Usage
To run in a container, you can simply execute `docker run fm17/poglink`, passing in any relevant configuration parameters as environment variables or CLI arguments. In order to pass in a configuration file or to maintain persistent data between containers, **mount a volume** to the `/data` dir inside the container (or whichever data directory is configured via the `--data-dir` CLI argument or the `BOT_DATA_DIR` environment variable). 

In the example below, the host's `~/.poglink` directory has been mounted to the container's `/data` directory. Therefore the `config.yaml` file must be located in `~/.poglink` in order to be passed into the container. Both of these mounting directories can be modified as needed, see [Configuration](https://github.com/FM-17/poglink/blob/main/docs/configuration.md) for more details.

```
docker run -v ~/.poglink:/data poglink
```
The same can be achieved by using Docker Compose:

Example `docker-compose.yaml`
```yaml
version: "3"
services:
  bot:
    image: fm17/poglink:latest
    container_name: poglink
    volumes:
      - ~/.poglink:/data
    command: "" # provide CLI args here
    networks:
      - bot-net

networks:
  bot-net:
```
If you choose to use `docker-compose`, the bot can be started by navigating to the directory containing your `docker-compose.yaml` file and typing.
```
docker-compose up
```

>📝 Learn more about `docker-compose` [here](https://docs.docker.com/compose/)
