# Macchiato

Macchiato is an IPython notebook viewer with inline, cell-level comments for discussing analysis.

## Goals of Macchiato

The goal of Macchiato is to provide an environment for users of IPython notebooks to add cell level comments and discussions in the style of a Medium blog. 

### Running Macchiato:

From the Macchiato directory run

`ipython Macchiatio.py -f <notebook folder>`

## Structure

Macchiato scans a directory of `.ipynb` files and gives each notebook and notebook cell an id used to track comments to objects. Comments are stored in a (currently SQLite3) database within the server's internals. 

A custom template file is loaded up and upon init (this will eventually be when a notebook is served and updated at regular intervals) uses nbconvert to create an HTML representation of a page with a JQuery script that loads comments (currently only on load, hopefully this too will change).

The underlying server is Tornado. The reasoning behind this is that IPython and NBViewer both run on Tornado and hopefully one day these things can work together (i.e. if NBViewer had the comment handlers from Macchiato and used the Macchiato custom template and JQuery script.).

### TODO:

Lots of things to be done:

* User authentication
* Autoupdating of cells
* Cleaning up the codebase
* Refactoring template and JQuery
* Delete cells
* Cell comment trees
* Better UI for comments
* Refactor CSS files



## Warnings

Macchiato is still very much alpha software. It doesn't come with or imply any sort of warrenty and is pretty much held together by duct-tape. Hopefully soon it will be pretty good.
