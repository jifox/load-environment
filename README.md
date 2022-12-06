# Collect-Env

Collect-Env helps to setup 12-factor compatible (development) environments.

## Features

- **init_collect - Python helper for installation**
  - Install required scripts
  - optionally install auto-run functionality triggerd during python virtualenv activation
  - `local_bash_rc.sh` script to further initialize the environment (e.g. start development containers).
- **loadEnv - bash script**
  - optional: encrypt files on change
- **Collect multiple .env files**
  - write merged .env variables to `collected.env`
  - write merged .env variables as `export VAR=xxx` statements to `export_collected.env`
- **Optionally use `ansible-vault` to create encrypted files**

  This allows storing in git repository.

  - uses **key-file** or **password-based** encryption is supported.
  - encrypted content of `collected.env` is stord in `collected.env.vault`
  - encrypted content of `export_collected.env` is stord in `export_collected.env.vault`

## Configuration

To initialize the collect-env environment run  `init_collect_env`.

```bash
$ init_collect_env
usage: init_collect_env.py [-h] [-i INST_PATH] [-a] [-d] [-e] [-l]
                           [-p PASSWORD_FILE] [-v ANSIBLE_VAULT_PATH]
                           env-files

positional arguments:
  env-files             Comma delimeted list of .env files to collect (e.g.
                        low-prio.env,higher-prio.env,highest-prio.env).

optional arguments:
  -h, --help            show this help message and exit
  -i INST_PATH, --inst_path INST_PATH
                        Installation path (Default: current directory).
  -a, --auto-activate   Automatically call loadEnv on venv activation.
  -d, --decrypt         Search for '*.env.vault', decrypt to '*.env' and
                        exit.
  -e, --enable-encryptinion
                        Enable the creation of encrypted '*.env.vault' files.
  -l, --list-env-files  Recursivly list all *.env in '-i INST_PATH' and exit.
  -p PASSWORD_FILE, --vault-password-file PASSWORD_FILE
                        Ansible-vault password file (Required if option '-e'
                        is set).
  -v ANSIBLE_VAULT_PATH, --ansible-vault-path ANSIBLE_VAULT_PATH
                        Path of 'ansible-vault'. (Required if option '-e' is
                        set and not in $PATH)
```

- all collected environment variables are defined in current terminal session
- `collected.env` contains all merged environment variables
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
