# Running natively in Python

## Installation
Install the bot from PyPi or GitHub.

### PyPi

```
pip install poglink
```
    
### GitHub

```bash
git clone https://github.com/FM-17/poglink.git
cd {cloned repo location}/poglink
pip install .
```
### Usage
To run the bot in Python you can either:
1. Execute via the CLI entrypoint: `poglink`, passing config parameters as described in [Configuration](https://github.com/FM-17/poglink/blob/main/docs/configuration.md) ; or
2. Import within your own Python code and execute `poglink.main.run`, passing in configuration parameters as keyword arguments.

#### Example:

Running `poglink` with data stored in `~/poglink/data` instead of default (`~/.poglink`)

 ```
 poglink --data-dir ~/poglink/data
 ```