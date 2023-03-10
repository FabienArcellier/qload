import os

import alfred
import click

ROOT_DIR = os.path.realpath(os.path.join(__file__, "..", ".."))

@alfred.command("docs:build", help="build documentation portal")
def docs__build():
    """
    build the documentation portal into docs/build/html

    >>> $ alfred docs:build
    """
    doc_directory = os.path.join(ROOT_DIR, 'docs')

    make = alfred.sh("make", "make should be present")
    os.chdir(doc_directory)
    alfred.run(make, ['html'])

    click.echo("to display the documentation: alfred doc:display")


@alfred.command("docs:display", help="display the documentation")
def docs__display():
    """
    Display the local documentation into a browser

    >>> $ alfred docs:display
    """
    portal_index = os.path.join(ROOT_DIR, 'docs', "build", "html", "index.html")

    """
    The command to open a web page from the terminal is different if your dev station is on Mac OS or Ubuntu.

    You have to use `xdg-open` on Ubuntu to open a url in the browser by default. `open` exists but it has
    a different purpose.

    On Mac OS, `open` is used to open an url in the browser by default. xdg-open does not exist.
    """
    browse = alfred.sh(["xdg-open", "open"], "the command open or xdg-open does not exists in your environment to open a url")
    alfred.run(browse, [portal_index])


@alfred.command("docs:check", help="check the documentation of fixtup (links, ...)")
def docs__check():
    """
    Display the local documentation into a browser

    >>> $ alfred docs:check
    """
    is_windows = os.name == "nt"

    if not is_windows:
        doc_directory = os.path.join(ROOT_DIR, 'docs')

        make = alfred.sh("make", "make should be present")
        os.chdir(doc_directory)
        alfred.run(make, ['linkcheck'])
    else:
        print("dock checking is not supported on non posix platform as windows")
