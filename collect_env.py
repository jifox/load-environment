#!/usr/bin/env python3
import os
from pathlib import Path

class CollectEnvVars():
    envdata = {}
    existing_envdata = {}

    def __init__(self):
        env_files = os.getenv("ENVIRONMENT_FILES", ".env").split(",")
        # process list of environment files
        for current_filename in env_files:
            fil = Path(current_filename.strip())
            if fil.exists():
                self.collect_env_file(fil, self.envdata)
            else:
                print(f"    Missing: {current_filename}")
        # export collected data to file collected.env
        if len(self.envdata) > 0:
            self.write_env_files(show_log=True)

    def collect_env_file(self, fil, dict_to_update, show_log=True):
        if show_log:
            print(f"    read: {fil}")
        with fil.open("r") as stream:
            content = stream.read().splitlines(keepends=False)
            for line in content:
                stripped = line.lstrip()
                if len(stripped) > 0 and stripped[0] != "#":  # strip comment
                    parts = stripped.split("=", 1)
                    if len(parts) > 1:
                        dict_to_update.update( {parts[0]: parts[1]} )

    def write_env_files(self, show_log):
        if not Path("collected.env").exists():
            # check if is identical
            self.collect_env_file("collected.env", self.existing_envdata, show_log=False)
            if self.envdata == self.existing_envdata:
                # nothing changed
                return
        if show_log:
            print(f"    writing: collected.env")
        with Path("collected.env").open("w+") as ostream:
            for k, v in self.envdata.items():
                ostream.writelines([f"{k}={v}\n"])
        if show_log:
            print(f"    writing: export_collected.env")
        with Path("export_collected.env").open("w+") as ostream:
            for k, v in self.envdata.items():
                ostream.writelines([f"export {k}={v}\n"])
        # only current user has access rights to generated environment files
        Path("collected.env").chmod(0o600)
        Path("export_collected.env").chmod(0o600)




if __name__ == "__main__":
    collectEnvVars = CollectEnvVars()