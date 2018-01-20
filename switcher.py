from talon.voice import Word, Context, Key, Rep, Str, press
from talon import ui

apps = {}

def switch_app(m):
    name = str(m._words[1])
    full = apps.get(name)
    if not full: return
    for app in ui.apps():
        if app.name == name:
            app.focus()
            break

ctx = Context('switcher')
keymap = {
    'focus {switcher.apps}': switch_app,
}
ctx.keymap(keymap)

def update_lists():
    global apps
    apps = {}
    for app in ui.apps():
        for word in app.name.split(' '):
            if not word in apps:
                apps[word] = app.name
    ctx.set_list('apps', apps.values())

def ui_event(event, arg):
    if event in ('app_activate', 'app_deactivate', 'app_launch', 'app_close'):
        update_lists()

ui.register('', ui_event)
update_lists()

def unload():
    ctx.unload()
    ui.unregister('', update_lists)
