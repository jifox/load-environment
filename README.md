# Load Environment Variables

This repository helps to setup a 12-factor compatible development environment.

## Configuration

Edit the `loadEnv` file and set this variables at the top of the file

```bash
# ENVIRONMENT_FILES: comma "," separated list of all environment files to collect. 
#                    highest priority at the end 
export ENVIRONMENT_FILES=development/dev.env,development/dev.override.env

# GENERATE_ENCRYPTED_ENV_FILES: Flag to generate encrypted environment files.
#        1: generate encrypted collected.env.vault and export_collected.env.vault
#           ensure ansible-vault is installed when set to '1' 
#           (pip3 install ansible-vault)
#        0: no encrypted files will be generated 
GENERATE_ENCRYPTED_ENV_FILES=1

# VAULT_PASSWORD_FILES: file to use as encryption key for `ansible-vault`
VAULT_PASSWORD_FILES=~/.ssh/ansible-vault
```







## Script: collected_env.py

The python script `collect_env.py` collects all `.env` files specified in the environemnt variable `ENVIRONMENT_FILES` and generate two output files:

- **collected.env**: merged environment variables
- **export_collected.env**: merged environment variables as bash 'export ...' statements

The latest specified environment filename in `ENVIRONMENT_FILES` will overwrite others.

### Example

Below the example environment files are liste.

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
ENVIRONMENT_FILES=./example/dev/file1.env,./example/prod/file2.env && collect_env.py
```

The two generated files will look like:

```bash
# collected.env
VAR1=Hello
VAR2=world
VAR3=foo
```

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

**local_bash_rc.sh**: if this script exists, this script will be exected at the end of the `loadEnv` script.

## Results

- all collected environment variables are defined in current terminal session
- `collected.env` contains the merged environment variables
- `export_collected.env` contains export statements for all environment variables
- if `GENERATE_ENCRYPTED_ENV_FILES == 1`
    - `collected_env.vault` is the encrypted `collected.env` file
    - `export_collected_env.vault` is the encrypted `export_collected.env` file

