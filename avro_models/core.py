from avro.schema import Names, SchemaFromJSONData, AvroException
import json
from io import IOBase
from six import string_types

from avro_models.models import create_data_model


class AvroDataNames(Names):
  def __init__(self, default_namespace=None):
    super(AvroDataNames, self).__init__(default_namespace=default_namespace)
    self._schema_map = {}

  def register_model(self, schema, wrapper_cls):
    model_cls = create_data_model(schema, wrapper_cls, self)
    self._schema_map[schema.fullname] = model_cls
    return model_cls

  def get_avro_model(self, schema_full_name):
    return self._schema_map[schema_full_name]

  def has_schema(self, schema_full_name):
    return schema_full_name in self._schema_map

  def __repr__(self):
    return str(self._schema_map)


def import_schema(schema_json=None, schema_file=None):
  if schema_json:
    if isinstance(schema_json, string_types):
      schema_json = json.loads(schema_json)
  elif schema_file:
    if isinstance(schema_file, string_types):
      with open(schema_file, "rb") as f:
        schema_json = json.load(f)
    if isinstance(schema_file, IOBase):
      schema_json = json.loads(schema_file.read())
  if isinstance(schema_json, dict):
    return schema_json
  raise AvroException("invalid input schema")


def avro_schema(names, **kwargs):
  schema_json = import_schema(**kwargs)

  def wrapper(cls):
    schema = SchemaFromJSONData(schema_json, names)
    return names.register_model(schema, cls)
  return wrapper