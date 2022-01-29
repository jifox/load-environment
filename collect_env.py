#!/usr/bin/env python3
import os
from pathlib import Path
from dotenv import dotenv_values, load_dotenv

class CollectEnvVars():
    envdata = {}

    def __init__(self):
        env_files = os.getenv("ENVIRONMENT_FILES", ".env").split(",")
        # process list of environment files
        for current_filename in env_files:
            fil = Path(current_filename.strip())
            if fil.exists():
                self.collect_env_file(fil)
        # export collected data to file collected.env
        if len(self.envdata) > 0:
            print(f"    writing: collected.env")
            with Path("collected.env").open("w+") as ostream:
                for k, v in self.envdata.items():
                    ostream.writelines([f"{k}={v}\n"])
            with Path("export_collected.env").open("w+") as ostream:
                for k, v in self.envdata.items():
                    ostream.writelines([f"export {k}={v}\n"])
            # only current user has access rights to generated environment files
            Path("collected.env").chmod(0o600)
            Path("export_collected.env").chmod(0o600)

    def collect_env_file(self, fil):
        print(f"    read: {fil}")
        with fil.open("r") as stream:
            content = stream.read().splitlines(keepends=False)
            for line in content:
                stripped = line.lstrip()
                if len(stripped) > 0 and stripped[0] != "#":  # strip comment
                    parts = stripped.split("=", 1)
                    if len(parts) > 1:
                        self.envdata.update( {parts[0]: parts[1]} )

if __name__ == "__main__":
    collectEnvVars = CollectEnvVars()