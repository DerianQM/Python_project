from settings import INSTALLED_APPS
from functools import reduce
from decorators import logs


def get_server_actions():
    modules = reduce(
        lambda value, item: value + [__import__(f'{item}.actions')],
        INSTALLED_APPS,
        []
    )
    actions = reduce(
        lambda value, item: value + [getattr(item,'actions',[])],
        modules,
        []
    )
    return reduce(
        lambda value, item: value + getattr(item,'actionnames',[]),
        actions,
        []
    )

@logs
def resolve(action_name,actions=None):
    actions_list = actions or get_server_actions()
    actions_mapping = {
        actions.get('action'): actions.get('controller')
        for actions in actions_list
    }
    return actions_mapping.get(action_name)