# Macchiato

Macchiato is an IPython notebook viewer with comments for discussing analysis.

## Goals of Macchiato

The goal of Macchiato is to provide an environment for users of IPython notebooks to add cell level comments and discussions in the style of a Medium blog. 

## Roadmap

Objectives:

1. Add notebook upload and convert functionality
    1. Use IPython's NBConvert module to convert documents
    1. Parse HTML and give cells distinct identifiers
    1. Give each notebook and cell a hash in the database
        1. Hash on distinct notebook\_id, cell\_id
1. Create Google Auth user account management

## Warnings

Initially Macchiato will be designed as an internal app so user account permissions will be set to open. User permissions might not even be implemented until much later.