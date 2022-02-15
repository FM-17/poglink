# Running as a `systemd` Service

## Installation
A script has been provided to assist in the installation process.

### Download
First, clone the project repository to some location of your choice:
```bash
git clone https://github.com/FM-17/poglink.git
cd {cloned repo location}/poglink
```

### (Optional) Creating a virtual environment
The installation script installs the `poglink` Python package in the Python environment that is currently active in the shell when the script is executed. It is highly recommended to use a virtual environment to install `poglink`. The script will warn you of this and subsequently exit unless `FORCE=true` is set before executing. 

To create and activate a new virtual environment (Python 3.7+), run the following commands:
```bash
cd <path to desired virtual env location>
python3 -m  venv venv    # Create a virtual environment named 'venv'
source venv/bin/activate # Activate the newly created virtual environment
```

### Running the Install Script
To begin the installation, ensure the script is executable then run:
```bash
chmod +x scripts/install-service.sh
# export DATA_DIR=<path to desired data directory> # Optional
scripts/install-service.sh
```
The script will do several things:
- Install `poglink` to the current Python environment
- Create a `systemd` service definition to execute `poglink`
- Check for a configuration file at the location specified by `DATA_DIR` (default `~/.poglink`); If not found, one will be created from sample values.

### Re-running the Install Script
The installation script can be run again to reinstall the service. This can be helpful when trying to change the default data directory, or the Python environment being used. 

When installing again, the `systemd` service file will be overwritten. A backup will be created at `/etc/systemd/system/poglink.service.bak`.


## Uninstalling
The service can be uninstalled via:
```bash
# Stop service and prevent from restarting
sudo systemctl stop poglink
sudo systemctl disable poglink

# Remove service definition and reload systemd
sudo rm -f /etc/systemd/system/poglink.service
sudo systemctl daemon-reload

# (Optional) Remove Python package
# pip uninstall poglink
# 
# or
#
# rm -rf <path/to/venv>
```

## Some Notes About the Service
1. When enabled, the service will restart on failures and on reboots. 
2. If the program crashes, it will wait 5 seconds before restarting to prevent runaway in the case of persistent errors.
3. If the program restarts more than 4 times in a 30 second period, it must be restarted again via `sudo systemctl start poglink` or by rebooting.
4. To modify any of the behaviour of the service after installation, edit the file at `/etc/system/systemd/poglink.service`.
5. To monitor real-time program logs from the service, execute `journalctl -fu poglink`. 