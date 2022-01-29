# Load Environment Variables

This repository helps to setup a 12-factor compatible development environment.

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

This i a script that uses collect_env.py 

