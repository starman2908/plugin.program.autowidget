import xbmc
import xbmcplugin

import sys

from resources.lib import manage
from resources.lib.common import directory
from resources.lib.common import utils

_handle = int(sys.argv[1])
_window = utils.get_active_window()


def root_menu():
    _create_menu()
    _groups_menu()
    _tools_menu()

    xbmcplugin.setContent(_handle, 'files')


def group_menu(group):
    not_media = xbmc.getCondVisibility('!Window.IsMedia')
    target = manage.get_group(group)['type']
    paths = manage.find_defined_paths(group)
    
    directory.add_menu_item(title='Add Path',
                            params={'mode': 'manage', 'action': 'add_path',
                                    'group': group, 'target': target},
                            isFolder=False)
    
    directory.add_menu_item(title='Remove Group',
                            params={'mode': 'manage',
                                    'action': 'remove_group',
                                    'group': group},
                            art={'icon': utils.get_art('folder-remove-outline.png')},
                            description='Remove this group definition. Cannot be undone.')

    for path in paths:
        widget = target == 'widget'
        directory.add_menu_item(title=path['name'] if widget else path['label'],
                                params={'mode': 'path',
                                        'action': 'call',
                                        'path': path['path'] if widget else path['action'],
                                        'target': path['type'] if widget else ''},
                                art={'icon': utils.get_art('share-outline.png')},
                                description='Show a list of shortcuts from the {} group.'
                                            .format(group.capitalize()),
                                isFolder=False)
    
    if len(paths) > 0:
        if target == 'widget':
            directory.add_menu_item(title='Random Path from {}'.format(group.capitalize()),
                                    params={'mode': 'path',
                                            'action': 'random',
                                            'group': group},
                                    art={'icon': utils.get_art('shuffle.png')},
                                    description='Use a random path from the {} group.'
                                                .format(group.capitalize()),
                                    isFolder=True)
        elif target == 'shortcut':
            directory.add_menu_item(title='Shortcuts from {}'.format(group.capitalize()),
                                    params={'mode': 'path',
                                            'action': 'shortcuts',
                                            'group': group},
                                    art={'icon': utils.get_art('share-outline.png')},
                                    description='Show a list of shortcuts from the {} group.'
                                                .format(group.capitalize()),
                                    isFolder=True)
    else:
        directory.add_menu_item(title='No AutoWidgets have been defined for this group.',
                                art={'icon': utils.get_art('alert-circle-outline.png')},
                                isFolder=not_media)
    
    xbmcplugin.setPluginCategory(_handle, group.capitalize())
    xbmcplugin.setContent(_handle, 'files')
    
    
def shortcut_menu(group):
    window = utils.get_active_window()
    paths = manage.find_defined_paths(group)
    
    if len(paths) > 0 and window == 'media':
        directory.add_menu_item(title=('Point a widget at this directory to get'
                                       ' a random widget from the following:'),
                                art={'icon': utils.get_art('shuffle.png')},
                                isFolder=False)
        directory.add_separator(group)
    
    for path in paths:
        directory.add_menu_item(title=path['label'],
                                params={'mode': 'path',
                                        'action': 'call',
                                        'path': path['action']},
                                art={'icon': path['thumbnail']})

    xbmcplugin.setPluginCategory(_handle, group.capitalize())
    xbmcplugin.setContent(_handle, 'files')
    
    
def random_path_menu(group):
    window = utils.get_active_window()
    paths = manage.find_defined_paths(group)
    
    if len(paths) > 0 and window == 'media':
        directory.add_menu_item(title=('Point a widget at this directory to get'
                                       ' a widget containing the following:'),
                                art={'icon': utils.get_art('share_outline.png')},
                                isFolder=False)
        directory.add_separator(group)
    
    for path in paths:
        directory.add_menu_item(title=path['name'],
                                params={'mode': 'path',
                                        'action': 'call',
                                        'path': path['path'],
                                        'target': path['type']},
                                isFolder=False)
    if window == 'home':
        unpack = utils.get_art('package-variant.png')
        sync = utils.get_art('sync.png')
        directory.add_menu_item(title='Initialize Widgets',
                        params={'mode': 'force'},
                        art={'icon': unpack, 'thumb': unpack, 'banner': unpack, 'poster': unpack},
                        description='Initialize this and any other AutoWidgets.')
    
    xbmcplugin.setPluginCategory(_handle, group.capitalize())
    xbmcplugin.setContent(_handle, 'files')
    
    
def _create_menu():
    if _window != 'home':
        return
    
    directory.add_menu_item(title='Create New Widget Group',
                            params={'mode': 'manage', 'action': 'add_group',
                                    'target': 'widget'},
                            art={'icon': utils.get_art('folder-plus-outline.png')},
                            description='Create a new group of widgets.')
                            
    directory.add_menu_item(title='Create New Shortcut Group',
                            params={'mode': 'manage', 'action': 'add_group',
                                    'target': 'shortcut'},
                            art={'icon': utils.get_art('share-outline.png')},
                            description='Create a new group of shortcuts.')
    
    
def _groups_menu():
    if _window != 'home':
        directory.add_separator(title='My Groups', char='/')
    
    for group in manage.find_defined_groups():
        group_name = group.get('name', '')
        directory.add_menu_item(title=group_name.capitalize(),
                                params={'mode': 'group',
                                        'group': group_name},
                                description='View the "{}" group.'
                                            .format(group_name),
                                art={'icon': utils.get_art('folder-outline.png')},
                                isFolder=True)
    
    
def _tools_menu():
    if _window != 'home':
        directory.add_separator(title='Tools', char='/')
    
    directory.add_menu_item(title='Force Refresh Widgets',
                            params={'mode': 'force'},
                            art={'icon': utils.get_art('refresh.png')},
                            description='Force all defined widgets to refresh.')
    directory.add_menu_item(title='Clean Old References',
                            params={'mode': 'clean'},
                            art={'icon': utils.get_art('trash-can-outline.png')},
                            description='Clean old references to widgets that are no longer defined.')
