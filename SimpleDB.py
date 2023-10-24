import json
db = {}
class _EventDict(dict):
  global db
  def __init__(self, *args, **kwargs):
      super(_EventDict, self).__init__(*args, **kwargs)
      self._push()

  def _push(self):
      with open('data.json', 'w') as json_file:
          json_file.write(json.dumps(db))

  def __setitem__(self, key, value):
      super(_EventDict, self).__setitem__(key, value)
      self._push()

  def __delitem__(self, key):
      super(_EventDict, self).__delitem__(key)
      self._push()

  def update(self, *args, **kwargs):
      super(_EventDict, self).update(*args, **kwargs)
      self._push()

with open('data.json') as json_file:
  dict = json_file.read()
  if dict:
    db = _EventDict(json.loads(dict))
  else:
    db = _EventDict({})
