Avro Data Model
=====

## Introduction
[Apache Avro](http://avro.apache.org/) is a data serialization framework. It has been widely used in data serialization (especially in Hadoop ecosystem) and RPC protocols. It has libraries to support many languages. The library supports code generation with static languages like Java, while for dynamic languages for example python, code generation is not necessary.

Avro schemas are also widely used in big data and streaming systems. When avro data is deserialized in Python environment, it was stored as a dictionary in memory. It looses all the interesting features provided by the avro schema, for example, you can modify an integer field with a string without getting any errors. It also doesn't provide any nice features from a normal class, for example, if an avro schema has `firstName` and `lastName` fields, it is not easy to define a function call to provide `fullName`.

## Use Cases of the Library
The reason I decided to develop this library is in use cases such as stream processing and RPC protocols, strict data types are required to make sure the system runs correctly. Although avro schema is introduced for this purpose, in Python, it is converted to a dictionary for in memory processing, which doesn't guarantee types and also doesn't provide class hierarchy. I am looking to develop a way so that a class can be build on top of an avro schema, so that it can keep correct data type and also has a class structure.

My solution is similar to what [SQLAlchemy ORM](https://www.sqlalchemy.org) does. Instead of manually defining all the fields of a SQL table in SQLAlchemy, schema definition is done through avro schema. The class allows method definitions of other properties or other validations. Please check the following examples for how to use the library.

However, this library should be restricted to places where static types are required. You will loose all the happiness playing with Python if applying this library everywhere.

**The project is still under development. Bugs are expected.**

## Example
### A Simple Example
**User.avsc**
```
{
  "type": "record",
  "name": "User",
  "fields": [
    {
      "name": "lastName",
      "type": "string"
    },
    {
      "name": "firstName",
      "type": "string"
    }
  ]
}
```
The following code defined a User class associated with the schema
```
@avro_schema(AvroDataNames(default_namespace="example.avro"), schema_file="User.avsc")
class User(object):
  def fullname(self):
    return "{} {}".format(self.firstName, self.lastName)
```
With this class definition, the full name can be obtained with the function call.
```
user = User({"firstName": "Alyssa", "lastName": "Yssa"})
print(user.fullname())
# Alyssa Yssa
```

### Avro Schema with Extra Validation
In some use cases, some extra validations are required, for example:
**Date.avsc**
```
{
  "name": "Date",
  "type": "record",
  "fields": [
    {
      "name": "year",
      "type": "int"
    },
    {
      "name": "month",
      "type": "int"
    },
    {
      "name": "day",
      "type": "int"
    }
  ]
}
```
The `month` and `day` of a date cannot be arbitrary integers. A extra validation can be done as following:
```
@avro_schema(AvroDataNames(default_namespace="example.avro"), schema_file="Date.avsc")
class Date(object):
  def __init__(self, value):
    if isinstance(value, datetime.date):
      value = {
          'year': value.year,
          'month': value.month,
          'day': value.day
      }
    super().__init__(value)

  def date(self):
    return datetime.date(self.year, self.month, self.day)

  def validate(self, data):
    return super().validate(data) \
        and datetime.date(data['year'], data['month'], data['day'])
```
The `Date` class can validate the input before assign it to then underlying avro schema
```
date = Date({"year": 2018, "month": 12, "date": 99})
# ValueError: day is out of range for month
date = Date(datetime.date(2018, 12, 12))
# No Error
```

## Contributing
After cloning/forking the repo, navigate to the directory and run
```
source init.sh
```
The python environment should be ready for you.

## Authors

* **Kun Fang** - (https://github.com/kun-fang)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

