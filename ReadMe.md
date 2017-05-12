Tests to see how JSON schema are resolved.

### Proposed format

(not implemented, work in progress)

1. All schema have a unique ID ($id)
2. All $ref will be fully qualified
3. All properties in a schema will be required 
4. On deploy we resolve all `$id` and `$ref` to a fully qualified target

e.g. deploy to a web server
we complete scheme and path in $id

deploy to a database we create scheme to indicate 

`$id` in schema is 
`"http://127.0.0.1:12345/c/schema-x.json"`
or 
`"c/schema-x.json"`

on deploy we write

`"$id": "http://schema.holidayextras.com/c/schema-x.json"`
or
`"$id": "mysql://schema.holidayextras.com/c/schema-x.json"`



Not clear if this is a python thing or a JSON schema thing.

The problem:

2nd order references.  In schema directory:

- `b` references `a`
- `c` references `b`

When validating an instance of `c`, we lookup `b` and indirectly `a`.
From `b`, the relative context of `a` will not be found (it is relative to
  b).  This feels like expected behaviour as there is no guarantee that `b` is
  in the same domain as `c`

Can work around this by forcing resolution to always be relative to a single base uri.
Or make every object explicit (which would involve a domain name, I believe).

To run

1. `brew install python` (using python2)
2. `pip install jsonschema` (or use a virtual env)
3. (Optional) `python -m SimpleHTTPServer 12345 &` to server schemas
4. `python validate.py [--host 127.0.0.1:12345] [--constant]` --constant flag
forces local resolution.
