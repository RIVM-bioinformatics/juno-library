import argparse
import subprocess
import pathlib
from typing import Sequence, Optional, Any
import inspect
import snakemake
import ast

# Helper functions for text manipulation


def color_text(text: str, color_code: int) -> str:
    """Function to convert normal text to color text"""
    formatted_text = "\033[0;" + str(color_code) + "m" + text + "\n\033[0;0m"
    return formatted_text


def message_formatter(message: str) -> str:
    """
    Function to convert normal text to yellow text (for an important
    message)
    """
    return color_text(text=message, color_code=33)


def error_formatter(message: str) -> str:
    """Function to convert normal text to red text (for an error)"""
    return color_text(text=message, color_code=31)


# Helper functions for file/dir validation and manipulation


def validate_is_nonempty_file(
    file_path: str | pathlib.Path, min_file_size: int = 0
) -> bool:
    file_path = pathlib.Path(file_path)
    return file_path.is_file() and file_path.stat().st_size >= min_file_size


def is_gz_file(filepath: str | pathlib.Path) -> bool:
    with open(filepath, "rb") as file_:
        return file_.read(2) == b"\x1f\x8b"


def validate_file_has_min_lines(
    file_path: str | pathlib.Path, min_num_lines: int = -1
) -> bool:
    """
    Test if gzip file contains more than the desired number of lines.
    Returns True/False
    """
    if not validate_is_nonempty_file(file_path, min_file_size=1):
        return False
    else:
        with open(file_path, "rb") as f:
            line = 0
            file_right_num_lines = False
            for _lines in f:
                line = line + 1
                if line >= min_num_lines:
                    file_right_num_lines = True
                    break
        return file_right_num_lines


# Helper functions for handling git repositories


def download_git_repo(version: str, url: str, dest_dir: str | pathlib.Path) -> None:
    """Function to download a git repo"""
    # If updating (or simply an unfinished installation is present)
    # the downloading will fail. Therefore, need to remove all
    # directories with the same name
    subprocess.run(["rm", "-rf", str(dest_dir)], check=True, timeout=60)

    dest_dir = pathlib.Path(dest_dir)
    dest_dir.parent.mkdir(exist_ok=True)

    subprocess.run(
        [
            "git",
            "clone",
            "-b",
            version,
            "--single-branch",
            "--depth=1",
            url,
            str(dest_dir),
        ],
        check=True,
        timeout=500,
    )


def get_repo_url(gitrepo_dir: str | pathlib.Path) -> str:
    """
    Function to get the URL of a directory. It first checks wheter it is
    actually a repo (sometimes the code is just downloaded as zip and it
    does not have the .git sub directory with the information that identifies
    it as a git repo
    """
    try:
        url_bytes = subprocess.check_output(
            ["git", "config", "--get", "remote.origin.url"],
            cwd=f"{str(gitrepo_dir)}",
        ).strip()
        url = url_bytes.decode()
    except:
        url = "Not available. This might be because this folder is not a repository or it was downloaded manually instead of through the command line."
    return url


def get_commit_git(gitrepo_dir: str | pathlib.Path) -> str:
    """
    Function to get the commit number from a folder (must be a git repo)
    """
    try:
        commit_bytes = subprocess.check_output(
            [
                "git",
                "--git-dir",
                f"{str(gitrepo_dir)}/.git",
                "log",
                "-n",
                "1",
                '--pretty=format:"%H"',
            ],
            timeout=30,
        )
        commit = commit_bytes.decode()
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        commit = "Not available. This might be because this folder is not a repository or it was downloaded manually instead of through the command line."
    return commit


class SnakemakeKwargsAction(argparse.Action):
    """
    Argparse Action that can be used in the argument parser of the Juno
    pipelines to store and process extra arguments (kwargs) that will be
    passed to the Snakemake API. Those arguments need to follow the arg=value
    (no spaces in between) format and use only arguments that are accepted
    by snakemake API. This is advanced usage.
    """

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: None | str | Sequence[str],
        option_string: Optional[str] = None,
    ) -> None:
        allowed_snakemake_args = inspect.getfullargspec(snakemake.snakemake).args
        snakemake_args: dict[str, Any] = dict()
        if not values:
            msg = f"No arguments and values were given to --snakemake-args. Did you try to pass an extra argument to Snakemkake? Make sure that you used the API format and that you use the argument int he form: arg=value."
            raise argparse.ArgumentTypeError(error_formatter(msg))
        for arg in values:
            try:
                key, val = arg.split("=")

                if key not in allowed_snakemake_args:
                    raise argparse.ArgumentTypeError(
                        error_formatter(
                            f"The argument {key} is not specified in the snakemake python API. Check it for typos or consult the api for the used snakemake version: {snakemake.__version__}"
                        )
                    )
                val = ast.literal_eval(val)
                snakemake_args[key] = val
            except ValueError as e:
                if "unpack" in str(e):
                    raise argparse.ArgumentTypeError(
                        error_formatter(
                            f"The argument {arg} is not valid. Did you try to pass an extra argument to Snakemake? Make sure that you used the API format and that you use the argument int he form: arg=value."
                        )
                    )
                elif "malformed" in str(e):
                    # For instance when val is simply a str it cannot be parsed by literal_eval
                    key, val = arg.split("=")
                    snakemake_args[key] = val
                elif "snakemake python API" in str(e):
                    raise e
                else:
                    raise e

        setattr(namespace, self.dest, snakemake_args)
