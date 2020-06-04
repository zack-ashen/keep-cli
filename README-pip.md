
<h1 align="center">Keep-CLI</h1>
<p align="center">Keep-cli is a cli Google Keep client. You can add, delete, and manage your Google Keep notes.</p>


## Setup

### Installation

```sh
pip install keep-cli
```

### Configuration
In order to make a note you must have the `$EDITOR` environment variable set to a text editor.

## Usage

#### Run keep-cli visually:
```sh
keep-cli
```
#### Skip the intro animation (quick mode):
```sh
keep-cli --quick
```
#### Make a list or note:
For a note:
```sh
keep-cli --note
```
For a list:
```sh
keep-cli --list
```
