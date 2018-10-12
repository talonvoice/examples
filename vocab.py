from talon.voice import Context

ctx = Context('vocab_demo1', bundle='com.apple.Terminal')
ctx.vocab = [
    'docker',
    'talon',
]
ctx.vocab_remove = ['doctor', 'Doctor']

ctx2 = Context('vocab_demo2', bundle='com.tinyspeck.slackmacgap')
ctx2.vocab = [
    'Talon',
]
