from importlib import import_module
from packaging.version import parse
from pkg_resources import get_distribution



def filter_deps(dependencies):
    """
    Filters a list of dependencies to only include remote packages
    if they are not already locally installed (with sufficient version number).

    In particular, avoids overriding existing local editable-installed packages,
    (e.g. packages installed via 'pip install -e .') unless necessary.
    """
    remote_deps = [dep for dep in dependencies if '@' in dep]
    local_deps = [dep for dep in dependencies if '@' not in dep]

    deps = [*local_deps]
    for dep in remote_deps:
        module_name = dep.split(' @ ')[0]

        try:
            # Check for existing local version
            local_module = import_module(module_name)

            # Check local version number against remote version number
            local_module_version = parse(get_distribution(module_name).version)
            remote_module_version = parse(dep.split('@')[-1])
            if remote_module_version > local_module_version:
                deps.append(dep)

        except ModuleNotFoundError:
            # No local version found
            deps.append(dep)

    return deps
