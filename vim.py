from talon.voice import Word, Context, Key, Rep, Str, press
ctx = Context('vim')

from .std import keymap

keymap = keymap.copy()
keymap.update({
    'bson append doc begin': ['BSON_APPEND_DOCUMENT_BEGIN();', Key('left left')],
    'bson append doc end': ['bson_append_document_end();', Key('left left')],
    'bson append array begin': ['BSON_APPEND_ARRAY_BEGIN();', Key('left left')],
    'bson append array end': ['bson_append_array_end();', Key('left left')],

    'bson append end 32': ['BSON_APPEND_INT32();', Key('left left')],
    'bson append end 64': ['BSON_APPEND_INT64();', Key('left left')],
    'bson append double': ['BSON_APPEND_DOUBLE();', Key('left left')],
    'bson append you tf [8]': ['BSON_APPEND_UTF8();', Key('left left')],
    'bson append binary': ['BSON_APPEND_BINARY();', Key('left left')],

    'bson update index': ['bson_uint32_to_string(, &index, keystr, sizeof(keystr));', Key(('left ' * 34).strip())],

    'tip bson [tee]': 'bson_t ',
    'tip bson iter [tee]': 'bson_iter_t ',
    'tip eye dev': 'eye_dev *',
    'tip eye buff': 'ebuf **',
    'tip pie object': 'PyObject',
})
ctx.keymap(keymap)

def unload(): ctx.disable()
