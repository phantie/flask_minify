"""Fixed CSS minifying. Does not break calc(). Tested on a large project."""

import re

# Constants for use in compression level setting.
NONE = 0
SIMPLE = 1
NORMAL = 2
FULL = 3


REPLACERS = {
  NONE: None,                           # dummy
  SIMPLE: ((r'\/\*.{4,}?\*\/', ''),       # comment
           (r'\n\s*\n', r"\n"),           # empty new lines
           (r'(^\s*\n)|(\s*\n$)', "")),   # new lines at start or end
  NORMAL: ((r'/\*.{4,}?\*/', ''),         # comments
           (r"\n", ""),                   # delete new lines
           ('[\t ]+', " "),               # change spaces and tabs to one space
           (r'\s?([;:{},>])\s?', r"\1"), # delete space where it is not needed, change ;} to }
           (r';}', "}"),                  # because semicolon is not needed there
           (r'}', r"}\n")),               # add new line after each rule
  FULL: ((r'\/\*.*?\*\/', ''),            # comments
         (r"\n", ""),                     # delete new lines
         (r'[\t ]+', " "),                # change spaces and tabs to one space
         (r'\s?([;:{},>])\s?', r"\1"),   # delete space where it is not needed, change ;} to }
         (r';}', "}")),                   # because semicolon is not needed there
}


def minimalize(css, level=NORMAL):
    css = css.replace("\r\n", "\n") # get rid of Windows line endings, if they exist
    for rule in REPLACERS[level]:
        css = re.compile(rule[0], re.MULTILINE|re.UNICODE|re.DOTALL).sub(rule[1], css)

    return css

def minify_css(file, **kwargs):
    return minimalize(file.read(), level=FULL)
