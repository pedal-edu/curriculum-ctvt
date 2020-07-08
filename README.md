# curriculum-ctvt

A collection of Pedal mistake patterns and utilities specifically for the
[CT@VT curriculum](https://think.cs.vt.edu/ctvt).

# Installing

```
$> pip install -r requirements.txt
```

# Pedal Dev

If you want to work with a local version of Pedal, you'll want to use the
`requirements-dev.txt` file instead. That file assumes the `pedal` module's
source directory is a sibling to this directory on your computer, and will
`pip install -e` with it for an editable mode.

# Building for Skulpt

TODO: Need to make this reality.

You can build this module for Skulpt by running the following command from
the Skulpt directory (replacing `<fullpath>` with the ):

```
npm run compile_module curriculum_ctvt /full/path/to/curriculum-ctvt/
```
