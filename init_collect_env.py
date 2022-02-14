#!/usr/bin/env python3

import argparse
import os
import shutil
import sys
from pathlib import Path

def get_base_prefix_compat():
    """Get base/real prefix, or sys.prefix if there is none."""
    return getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix

def in_virtualenv():
    return get_base_prefix_compat() != sys.prefix

def list_env_files(base_directory=".", exclude_paths=[]):
    """List environment- and encrypted environment-files

    Args:
        base_directory (Path):   application directory where 'collected.env'
                                will be created. (Default: ".")
    """
    env_files, encrypted_files = search_env_files(base_directory, exclude_paths)
    print(f"{os.linesep}LIST of ENVIRONMENT-FILES ({base_directory}){os.linesep}")
    if env_files:
        print("    Environment files:")
        for fn in sorted(env_files):
            print("        ", fn)
    if encrypted_files:
        print("    Encrypted environment files:")
        for efn in sorted(encrypted_files):
            print("        ", efn)
    if not env_files and not encrypted_files:
        print("    No environment files found!")
    else:
        print("")

def replace_or_append_line(filename, search_for, replace_with):
    infile = Path(filename).resolve()


def _search_with_excludes(base_directory, pattern, exclude_list=[]):
    """Search env-files with considering exclude_list

    Args:
        base_directory (Path):  application directory where 'collected.env'
                                will be created. (Default: ".")
        pattern (str):          File pattern to search. Wildcards allowed.
        exclude_list (List[str], optional):  File pattern to search. 
                                Wildcards are allowed.

    Returns:
        List[str]: List of found files
    """
    res = []
    for envfile in list(Path(base_directory).glob(f"**/{pattern}")):
        found = False
        for exc in exclude_list:
            found = str(envfile).find(exc) > -1
            if found:
                break
        if not found:
            res.append(envfile)
    return res


def search_env_files(base_directory=".", exclude_list=[]):
    """Search for environment- and encrypted environment-files.

    Args:
        base_directory (Path):  application directory where 'collected.env'
                                will be created. (Default: ".")

    Returns:
        List[str]: List of environment filenames relative to base_directory.
        List[str]: List of encrypted environment filenames relative to base_directory.
    """
    env_files = []
    encrypted_files = []

    # Get list of plain text environment-files
    env_files.extend(_search_with_excludes(base_directory, ".env", exclude_list))
    env_files.extend(_search_with_excludes(base_directory, "*.env", exclude_list))

    # Get list of encrypted environment-files
    encrypted_files.extend(_search_with_excludes(base_directory, ".env.vault", exclude_list))
    encrypted_files.extend(_search_with_excludes(base_directory, "*.env.vault", exclude_list))

    return env_files, encrypted_files

def check_installation_exists(dirname):
    if Path(dirname).joinpath("loadEnv").exists():
        return True
    return False

def install_collectEnv(inst_dir, auto_activate):
    pass


if __name__ == "__main__":
    if not in_virtualenv():
        raise ValueError("""No virtual environment detected!
            Activate the virtual environment and retry again.
            """
            )

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--inst_path",
        type=Path,
        help="Installation path (Default: current directory).",
        default=str(Path().cwd().resolve().absolute())
    )
    parser.add_argument(
        "-a", "--auto-activate",
        dest='auto_activate',
        default=False,
        action='store_true',
        help="Automatically call loadEnv on venv activation."
    )
    parser.add_argument(
        "-d", "--decrypt",
        dest='decrypt',
        default=False,
        action='store_true',
        help="Search for '*.env.vault', decrypt to '*.env' and exit."
    )
    parser.add_argument(
        "-f", "--env-files",
        dest='env_files',
        default=".env",
        help="Comma delimeted list of .env files to collect (e.g. low-prio.env,higher-prio.env,highest-prio.env).",
    )
    parser.add_argument(
        "-e", "--enable-encryptinion",
        dest='enable_encryption',
        default=False,
        action='store_true',
        help="Enable the creation of encrypted '*.env.vault' files."
    )
    parser.add_argument(
        "-l", "--list-env-files",
        dest='listenv_files',
        default=False,
        action='store_true',
        help="Recursivly list all *.env in '-i INST_PATH' and exit.",
    )
    parser.add_argument(
        "-p", "--vault-password-file",
        dest='password_file',
        type=Path,
        help="Ansible-vault password file (Required if option '-e' is set).",
    )
    parser.add_argument(
        "-v", "--ansible-vault-path",
        type=Path,
        dest="ansible_vault_path",
        help="Path of 'ansible-vault'. (Required if option '-e' is set and not in $PATH)",
    )
    parser.add_argument(
        "-x", "--exclude-path",
        dest="exclude_paths",
        help="Comma delimted list of directories to exclude from search.",
    )
    p = parser.parse_args()

    inst_dir = Path(p.inst_path)
    if not inst_dir.is_dir():
        raise ValueError("""The install directory does not exist!
            Usage:
                init_collect [inst_path]

                    inst_path: (optional, Default: current directory) Installation directory.
            """
            )
    exclude_paths = []
    if p.exclude_paths:
        for pa in p.exclude_paths.split(','):
            exclude_paths.append(pa.strip())

    if p.listenv_files:
        list_env_files(inst_dir, exclude_paths)
        exit(0)

    if p.decrypt:
        if p.ansible_vault_path:
            vault = Path(p.ansible_vault_path)
        else:
            vault = shutil.which("ansible-vault")  # type:ignore
        if not vault or not Path(vault).exists():
            raise ValueError("""Error: 'ansible-vault' not found!
            Use parameter '--ansible-vault-path /path/to/ansible-vault' or
            install ansible-vault in current virtualenv
            'pip install ansible-vault'
            """)
        if not p.password_file or not Path(p.password_file).exists():
            raise ValueError("""Ansible password-file not found!
            Use parameter --vault-password-file to set the path of the password-file.py
            """)

    auto_activate = p.auto_activate
    # install_collectEnv(inst_dir, auto_activate)
