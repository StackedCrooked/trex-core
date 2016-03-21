import sys
import os
import warnings
import platform

# if not set - set it to default
TREX_STL_EXT_PATH = os.environ.get('TREX_STL_EXT_PATH')

# take default
if not TREX_STL_EXT_PATH:
    CURRENT_PATH        = os.path.dirname(os.path.realpath(__file__))
    # ../../../../external_libs
    TREX_STL_EXT_PATH   = os.path.abspath(os.path.join(CURRENT_PATH, os.pardir, os.pardir, os.pardir, os.pardir, 'external_libs'))


# the modules required
# py-dep requires python2/python3 directories
# arch-dep requires cel59/fedora and 32bit/64bit directories
CLIENT_UTILS_MODULES = [ {'name': 'dpkt-1.8.6'},
                         {'name': 'texttable-0.8.4'},
                         {'name': 'pyyaml-3.11', 'py-dep': True},
                         {'name': 'scapy-2.3.1', 'py-dep': True},
                         {'name': 'pyzmq-14.5.0', 'py-dep': True, 'arch-dep': True}
                        ]


def generate_module_path (module, is_python3, is_64bit, is_cel):
    platform_path = [module['name']]

    if module.get('py-dep'):
        platform_path.append('python3' if is_python3 else 'python2')

    if module.get('arch-dep'):
        platform_path.append('cel59' if is_cel else 'fedora18')
        platform_path.append('64bit' if is_64bit else '32bit')

    return os.path.normcase(os.path.join(TREX_STL_EXT_PATH, *platform_path))


def import_module_list(modules_list):

    # platform data
    is_64bit   = platform.architecture()[0] == '64bit'
    is_python3 = (sys.version_info >= (3, 0))
    is_cel     = os.path.exists('/etc/system-profile')


    

    # regular modules
    for p in modules_list:
        full_path = generate_module_path(p, is_python3, is_64bit, is_cel)

        if not os.path.exists(full_path):
            print("Unable to find required module library: '{0}'".format(p['name']))
            print("Please provide the correct path using TREX_STL_EXT_PATH variable")
            print("current path used: '{0}'".format(full_path))
            exit(0)

        sys.path.insert(1, full_path)





import_module_list(CLIENT_UTILS_MODULES)
