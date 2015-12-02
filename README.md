# Git-Fame

Generate statistics and charts from a git repository.

## Setup

This project uses [Buildout](http://www.buildout.org/) to create an isolated environment without requirement for virtualenv.

Run the following commands in the project root to install dependencies and generate executables.

```bash
python bootstrap.py
./bin/buildout
```

## Usage

Git-fame generates charts from the git repository where it is run.

To create a pie chart of the commits by author from git-fame repository run:

```bash
./bin/git-fame commits
```

Git-fame provides a list of available sub-commands and information on their usage with the `--help` flag.


## License

Released under MIT License.
