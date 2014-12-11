#!/usr/bin/env python
import csv
import re

# encodes a table of time referents with columns type, citation, line number
# and function as a tei:spanGrp of type time-referents where each tei:span
# has @type corresponding to the type column, the function is the inner
# text, and the line numbers are encoded as part of the span

# Edit this as necessary
header = """<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0"
    xmlns:ct="http://hocl.tk/schema/"
    version="5.0" >
    <teiHeader>
        <fileDesc>
            <titleStmt>
                <title>Time Referents in The Regiment of Princes</title>
                <author>Smyth, Karen</author>
            </titleStmt>
            <publicationStmt>
                <p>Encoded by Mark Watts</p>
                <date when="2012" />
            </publicationStmt>
            <sourceDesc>
                <p>Encoded from a tab-separated-values file, from a word document using trtotei.py</p>
            </sourceDesc>
        </fileDesc>
    </teiHeader>
    <text>
        <body>
"""
footer = "</body></text></TEI>"

def normalize_type(typestring):
    """ Turns the types into strings with no whitespace, all lowercase

    Parameters
    ----------
    typestring : str
        the string to normalize
    :return: The normalized string
    """
    (a,_) = remove_parentheticals(typestring.lower())
    a = colon_to_dot(a)
    a = a.strip()
    return collapse_spaces(a)

spaces_regex = re.compile('\s+', re.VERBOSE)
def collapse_spaces(s):
    return spaces_regex.sub("-", s)

def colon_to_dot(s):
    return re.sub(r"\s*:\s*", ".", s)

def remove_parentheticals(s):
    """ Removes any parenthetical statements with only one level of nesting """
    res = ""
    rest= ""
    depth = 0
    for i in range(len(s)):
        c = s[i]
        if c == "(":
            depth += 1
            continue
        if c == ")":
            depth -= 1
            continue
        if depth == 0:
            res += c
        else:
            rest += c

    return (res,rest)

def spans_from_string(s):
    return map(lambda x: map(int, re.split("\s*-\s*", x)), re.split(r"\s*,\s*", s))

def main():
    print(header)
    print "<spanGrp type='time-referents'>"
    with open("time-refs.tsv", 'r') as f:
        reader = csv.reader(f, delimiter="\t", quotechar="\"")
        next(reader) # skip the header
        for row in reader:
            # 1. parse the line number column. If it has more than
            #    one interval, then break it up into multiple spans
            #    with a linked interp. Not sure this is the right way...
            typestring = row[1]
            lines = row[3]
            (type_label, note) = remove_parentheticals(typestring)

            typestring = normalize_type(typestring)
            for x in spans_from_string(lines):
                # XXX: no idea how to appropiately encode a note on the type
                x = map(lambda e: "#line-"+str(e), x)

                if len(x) == 2:
                    targeting = "from='%s' to='%s'" % tuple(x)
                elif len(x) == 1:
                    targeting = "target='%s'" % x[0]
                else:
                    targeting ="ERROR IN TARGETING"

                if len(note) > 0:
                    notestring = "<note>"+note+"</note>"
                else:
                    notestring = ""

                print "<span ct:typeLabel='"+type_label+"' type='"+typestring+"' "+targeting+" >"+notestring+row[4]+"</span>"
    print("</spanGrp>")
    print(footer)

if __name__ == "__main__":
    main()
