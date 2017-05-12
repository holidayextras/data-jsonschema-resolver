"""
Validate all the schema in the schema dir
"""

import json
import os
from collections import Counter

def all_nodes_for_name(obj, name):
    """Return the contests of every node with a given name, 
    used to check every object has $id and to check every $ref 
    regardless of where they occur in the object.
    """
    if not isinstance(obj, dict):
        raise ValueError("dict / object expected, got {}".format(obj))

    for key in obj:
        if key == name:
            yield obj[key]
        if isinstance(obj[key], dict):
            for x in all_nodes_for_name(obj[key], name):
                yield x

def all_nodes_with_name(obj, name):
    """Return every dict / object with 'properties'. 
    
    Used to check every declared property is required.
    """

    if not isinstance(obj, dict):
        raise ValueError("dict / object expected, got {}".format(obj))

    for key in obj:
        if key == name:
            yield obj
        if isinstance(obj[key], dict):
            for x in all_nodes_with_name(obj[key], name):
                yield x


def test_all_nodes_for_name():

    obj = {'a': 1,
           'b': {
               'a': 2,
               'b': ['x', 'y']
           },
           'c': {
               'd': {'a': 3}
           }}

    assert sorted([i for i in all_nodes_for_name(obj, 'a')]) == sorted([1, 2, 3])


def test_all_nodes_with_name():

    obj1 = {'a': 1}
    obj2 = {'b': 1}
    obj3 = {'a': 2}
    obj4 = {'a': obj1, 'b': obj2, 'c': obj3}

    expected = sorted([obj4, obj1, obj3])
    actual = sorted([i for i in all_nodes_with_name(obj4, 'a')])
    assert expected == actual


def all_properties_are_required(obj):

    if 'properties' not in obj:
        raise ValueError("'properties' key not in {}".format(obj))
    if 'required' not in obj:
        raise ValueError("'required' key not in {}".format(obj))

    req = obj['required']

    return all(k in req for k in obj['properties'].keys())


def all_json_files(schema_dir):

    for dirpath, dirnames, filenames in os.walk(schema_dir):
        for fn in [fn for fn in filenames if fn.endswith('.json')]:
            yield os.path.join(dirpath, fn), fn


def test_all_properties_are_required_in_schema():

    schema_dir = './schemas'
    properties = 'properties'
    fail_files = ['fail-schema-d.json']

    for jsonpath, jsonfile in all_json_files(schema_dir):
        with open(jsonpath) as fin:
            obj = json.load(fin)

        for p in all_nodes_with_name(obj, properties):
            if jsonfile in fail_files:
                assert not all_properties_are_required(p)
            else:
                assert all_properties_are_required(p)


def test_all_schema_have_single_id():

    schema_dir = './schemas'
    ID = '$id'
    fail_files = ['fail-schema-e.json']

    for jsonpath, jsonfile in all_json_files(schema_dir):
        with open(jsonpath) as fin:
            obj = json.load(fin)

        ids = list(all_nodes_for_name(obj, ID))

        if os.path.split(jsonfile)[-1] in fail_files:
            assert len(ids) != 1
        else:
            assert len(ids) == 1


def test_all_ids_are_unique():

    schema_dir = './schemas'
    ID = '$id'
    id_counter = Counter()
    fail_files = ['fail-schema-e.json']

    for jsonpath, jsonfile in all_json_files(schema_dir):
        with open(jsonpath) as fin:
            obj = json.load(fin)

        ids = list(all_nodes_for_name(obj, ID))

        if jsonfile not in fail_files:
            assert len(ids) == 1
            id_counter.update(ids)

    assert max(list(id_counter.itervalues())) == 1

