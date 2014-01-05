#!/usr/bin/env python

import ast
import os
import sys

# TODO: Avoid hard-coding project path.
BASE_PATH = "Set this to the base path of the project"


def find_class_names(file_name, prefix):
    """
    Return a list of classes in the module `file_name` whose
    name starts with `prefix`.

    """
    with open(file_name) as f:
        tree = ast.parse(f.read())
    class_names = []
    for child in ast.iter_child_nodes(tree):
        if isinstance(child, ast.ClassDef):
            name = child.name
            if name.startswith(prefix):
                class_names.append(name)
    return class_names


def find_method_names(file_name, class_name, prefix):
    """
    Return a list of member functions of the class with name `class_name`
    in the module `file_name` whose name starts with `prefix`.

    """
    with open(file_name) as f:
        tree = ast.parse(f.read())

    for child in ast.iter_child_nodes(tree):
        if isinstance(child, ast.ClassDef) and child.name == class_name:
            break
    else:
        return []

    method_names = []
    for member in ast.iter_child_nodes(child):
        if isinstance(member, ast.FunctionDef):
            name = member.name
            if name.startswith(prefix):
                method_names.append(name)

    return method_names


def match_file_or_folder(base, partial):
    """Return a list of files or folders in the path specified by `base`
    whose dotted name begins with `partial`.

    """
    matches = []
    full_path = os.path.join(BASE_PATH, *base)
    if not os.path.isdir(full_path):
        return []
    for entry in os.listdir(full_path):
        if entry.startswith(partial):
            entry_path = os.path.join(full_path, entry)
            if os.path.isfile(entry_path):
                base, _ = os.path.splitext(entry)
                matches.append(base)
            else:
                matches.append(entry)
    return matches


def match_class_name(base, partial):
    """ Return a list of classes in the path specified by `base` whose
    dotted name begins with `partial`.

    """
    if len(base) == 0:
        return []

    file_name = base[-1] + ".py"
    full_path = os.path.join(BASE_PATH, *base[:-1])
    full_path = os.path.join(full_path, file_name)

    if not os.path.isfile(full_path):
        return []

    matches = find_class_names(full_path, partial)
    return matches


def match_method_name(base, partial):
    """ Return a list of methods in the path specified by `base` whose
    dotted name begins with `partial`.

    """
    if len(base) < 2:
        return []

    class_name = base[-1]
    path = base[:-1]

    # TODO: Code duplication with match_method_name
    file_name = path[-1] + ".py"
    full_path = os.path.join(BASE_PATH, *path[:-1])
    full_path = os.path.join(full_path, file_name)

    if not os.path.isfile(full_path):
        return []

    matches = find_method_names(full_path, class_name, partial)
    return matches


MATCH_ACTIONS = [
    match_file_or_folder,
    match_class_name,
    match_method_name,
]


def complete(cur):
    """ Return list of completions that match partial entry `cur`.
    """

    names = cur.split('.')
    base, partial = names[:-1], names[-1]

    completions = []
    for action in MATCH_ACTIONS:
        completions = action(base, partial)
        if completions:
            break

    return sorted(
        '.'.join(base + [c]) for c in completions
    )


if __name__ == "__main__":
    try:
        current = sys.argv[1]
    except IndexError:
        current = ''

    completions = complete(current)
    print ' '.join(completions)
