Tests to see how JSON schema are resolved.

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
