#!/usr/bin/env python

from distutils.core import setup
import sys

# Default to installing if no commands are given
if len (sys.argv) == 1:
	script_args = ["install"]
else:
	script_args = sys.argv [1:]



setup (name = "LiveWires",
       version = "2.0",
       description = "LiveWires package provides resources for people learning Python. It is intended for use with the LiveWires Python Course",
       author = "Richard Crook, Gareth McCaughan, Paul Wright, Rhodri James, Neil Turton",
       author_email = "python@livewires.org.uk",
       url = "http://www.livewires.org.uk/python/",
       packages = ['livewires'],
       script_args = script_args
      )

input("\n\nPress the enter key to exit.")
