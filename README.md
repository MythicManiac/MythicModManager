# MythicModManager
A bootleg Mod Manager for Risk of Rain 2 with Thunderstore integration


## Development setup

Black
-----

This project uses [black](https://github.com/ambv/black) for code formatting.
Set it up following these instructions:
* Make sure the `pre-commit` command is available on your terminal. You can
install it either locally or globally with `pip install pre-commit`
* Install the hooks in this repository. This can be done with
`pre-commit install`
* Black will now be ran against all your changes before you make a commit, and
if there are formatting issues it will attempt to fix them, and prvent the
commit from happening.
* You should also add black to your code editor of choice. See the
[GitHub page](https://github.com/ambv/black) for more details.

