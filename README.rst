========
tally-ho
========


.. image:: https://travis-ci.org/talaniz/tally-ho.svg?branch=master
    :target: https://travis-ci.org/talaniz/tally-ho

.. raw:: html
    :file: img/coverage.svg



*What is it?*

`tally_ho` is a simple, python based command line interface that creates tallies. The functionality 
is intentionally kept simple to focus on different aspects of user experience, continuous integration
and deployment.

This software is free of use under the MIT license

Usage
-----

Create a category
`$ tally_ho category create --category bugs`

Create an item to tally
`$ tally_ho tally create --tally "debugging startup scripts`

Tally an item
`$ tally_ho tally update --tally "debugging startup scripts" --quantity 1`


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
