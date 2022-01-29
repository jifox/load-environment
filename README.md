# Load Environment Variables

This repository helps to setup a 12-factor compatible development environment.

The output is a file containig all vars collected from a given list of `.env` files.

## Results

- all collected environment variables are defined in current terminal session
- `collected.env` contains the merged environment variables
- `export_collected.env` contains export statements for all environment variables
- if `GENERATE_ENCRYPTED_ENV_FILES == 1`
  - `collected_env.vault` is the encrypted `collected.env` file
  - `export_collected_env.vault` is the encrypted `export_collected.env` file

## Configuration

Edit the `loadEnv` file and configure the variables at the top of the file.

```bash
# ENVIRONMENT_FILES: comma "," separated list of environment files to collect.
#                    Highest priority at the end.
export ENVIRONMENT_FILES=./example/dev/file1.env,./example/prod/file2.env

# GENERATE_ENCRYPTED_ENV_FILES: Flag to generate encrypted environment files.
#        1: generate encrypted files. (export_)collected.env.vault
#           Ensure ansible-vault is installed when set to '1'.
#           (pip3 install ansible-vault)
#        0: no encrypted files will not be generated
GENERATE_ENCRYPTED_ENV_FILES=1

# VAULT_PASSWORD_FILES: file to use as encryption-key for `ansible-vault`.
VAULT_PASSWORD_FILES=~/.ssh/ansible-vault
```

When activating encryption with `GENERATE_ENCRYPTED_ENV_FILES=1` the application `ansible-vault` must be installed.

```bash
# Setup a virtual python environment if required
$ python3 -m venv .
$ . bin/activate

# Install ansible-vault
$ pip3 install -r loadenv_requirements.txt

# Test installation
$ ansible-vault --help
usage: ansible-vault [-h] [--version] [-v] {create,decrypt,edit,view,encrypt,encrypt_string,rekey} ...

encryption/decryption utility for Ansible data files

positional arguments:
  {create,decrypt,edit,view,encrypt,encrypt_string,rekey}
    create              Create new vault encrypted file
    decrypt             Decrypt vault encrypted file
    edit                Edit vault encrypted file
    view                View vault encrypted file
    encrypt             Encrypt YAML file
    encrypt_string      Encrypt a string
    rekey               Re-key a vault encrypted file

optional arguments:
  --version             show program's version number, config file location, configured module search path, module
                        location, executable location and exit
  -h, --help            show this help message and exit
  -v, --verbose         verbose mode (-vvv for more, -vvvv to enable connection debugging)

See 'ansible-vault <command> --help' for more information on a specific command.
```

## Script: collected_env.py

The python script `collect_env.py` collects all `.env` files specified in the environemnt variable `ENVIRONMENT_FILES` and generates two output files:

- **collected.env**: merged environment variables
- **export_collected.env**: merged environment variables as bash 'export ...' statements

Environment vars of files listed later in `ENVIRONMENT_FILES` overwrites the values of files listed before

### Example

Below the example environment files are listed.

- **./example/dev/file1.env**

    ```bash
    VAR1=Hello
    VAR2=Universe
    VAR3=foo
    ```

- **./example/prod/file2.env**

    ```bash
    VAR2=world
    ```

To generate the output files use this command:

```bash
ENVIRONMENT_FILES=./example/dev/file1.env,./example/prod/file2.env && ./collect_env.py
```

The two generated files will look like:

```bash
# collected.env
VAR1=Hello
VAR2=world
VAR3=foo
```

```bash
# export_collected.env
export VAR1=Hello
export VAR2=world
export VAR3=foo
```

## loadEnv

This script is configuring the local environment.

In the terminal type `. loadEnv` or `source loadEnv` to execute the script

All collected environment variables will be defined in current terminal.

**local_bash_rc.sh**: if this script exists, this script will be executed at the end of the `loadEnv` script.
