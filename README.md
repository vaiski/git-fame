# Git-Fame

Generate statistics and charts from a git repository.


## Setup

To install Git-Fame, run the following command in the project root:
```bash
python setup.py install
```


## Usage

Navigate to a git repository you want to analyze and run:

```bash
git fame [subcommand]
```

Git-fame provides a list of available sub-commands and information on their usage with the `--help` flag.


### Subcommands

`commits` Create a pie chart of the commits by author.

`changes` Create a pie and bar charts from the changes by the author.

`activity` Create a heatmap from the repository activity.


## Development

This project uses [Buildout](http://www.buildout.org/) to create an isolated environment without requirement for virtualenv.

Run the following commands in the project root to install dependencies and generate executables.

```bash
python bootstrap.py
./bin/buildout
```


## License

Released under MIT License.
