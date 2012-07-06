=============
infrae.scales
=============

Middleware to collect statistics about HTTP requests.

Example, in your paster configuration::

  [filter:scales]
  use = egg:infrae.scales
  publisher_signature = ++stats++
  name = silva
  scales_smi = .*\+\+rest\+\+
  scales_resources = .*\+\+static\+\+

Configuration options
---------------------

Those configuration options are usable inside paster configuration file.

``name``
  Prefix used to host statics.

``publisher_signature``
  URL prefix on which the statics will be accessible.

Option started with ``scales_``
  Prefix used to define statics prefixes. Any URL matching the given
  regular expression will have its statics collected under this
  prefix. If no given prefixes is match, the statics will be collected
  under the ``default`` prefix.
