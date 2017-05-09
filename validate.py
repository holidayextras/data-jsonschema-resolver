import jsonschema
import json
import os

import sys
import argparse

class ConstantRefResolver(jsonschema.RefResolver):
    """Always force the schema resolution context to use BASE_URI.

    This means that schema-c will validate.
    """

    BASE_URI = ''

    @property
    def resolution_scope(self):
        return self.BASE_URI


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='127.0.0.1:<port> (start with SimpleHTTPServer)')
    parser.add_argument('--constant', action='store_true', help='Use Constant RefResolver')
    args = parser.parse_args()

    if args.host:
        # start background process `python -m SimpleHTTPServer <port> `
        # and use 127.0.0.1:<port> as host arg
        base_uri = 'http://' + args.host + '/schemas/'
    else:
        wd = os.path.dirname(os.path.abspath(__file__))
        base_uri = 'file://' + wd + '/schemas/'


    schemas = ["schemas/a/schema-a.json",
               "schemas/b/schema-b.json",
               "schemas/c/schema-c.json"]

    examples = ["examples/a/a.json",
                "examples/b/b.json",
                "examples/c/c.json"]

    for sf, ej in zip(schemas, examples):

        with open(sf) as fin:
            s = json.load(fin)
        with open(ej) as fin:
            e = json.load(fin)

        print "Validating ", sf,
        jsonschema.Draft4Validator.check_schema(s)

        if args.constant:
            print >> sys.stderr, "Using ConstantRefResolver"
            resolver = ConstantRefResolver(base_uri, s)
            resolver.BASE_URI = base_uri
        else:
            print >> sys.stderr, "Using Default Resolver"
            resolver = jsonschema.RefResolver(base_uri, s)

        jsonschema.Draft4Validator(s, resolver=resolver).validate(e)
        print ej, '..... Validated'


if __name__ == '__main__':
    main()
