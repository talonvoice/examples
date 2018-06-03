import threading
import math

from talon import app, ui
from talon.api import lib, ffi
from talon.audio import record, noise
from talon.engine import engine

class AudioTimeline:
    def __init__(self, seconds=4, rate=44100):
        self.width = int(ui.main_screen().width)
        self.chunk = int((seconds * rate) / self.width)
        self.seconds = seconds
        self.history = []
        self.tmp = []
        self.events = []
        self.lock = threading.Lock()
        self.odd = False
        self.hissing = False
        self.offset = 0

    def append(self, count, samples):
        with self.lock:
            self.tmp += [samples[i] for i in range(count)]
            while len(self.tmp) > self.chunk:
                chunk, self.tmp = max(self.tmp[:self.chunk]), self.tmp[self.chunk:]
                chunk = (max(0, chunk) * 2) ** 0.5
                if self.odd:
                    chunk = -chunk
                self.odd = not self.odd
                self.history.append(chunk)
            offset = len(self.history) - self.width
            if offset > 0:
                self.offset -= offset
                for event in self.events:
                    event[0] -= offset
            self.events = [event for event in self.events if event[0] > -self.width]
            self.history = self.history[-self.width:]

    def draw(self, vg, x, y, width, height):
        with self.lock:
            history = self.history[:]
            events = self.events[:]

        lib.nvgBeginPath(vg)
        lib.nvgRect(vg, x, y, width, height)
        lib.nvgStrokeWidth(vg, 2)
        lib.nvgStrokeColor(vg, lib.nvgRGBA(0, 0, 0, 40))
        lib.nvgFillColor(vg, lib.nvgRGBA(0, 0, 0, 180))
        lib.nvgStroke(vg)
        lib.nvgFill(vg)

        lib.nvgStrokeWidth(vg, 3)
        for i in range(self.seconds * 10):
            lib.nvgBeginPath(vg)
            if i % 10 == 0:
                lib.nvgStrokeColor(vg, lib.nvgRGBA(0, 0, 255, 80))
            else:
                lib.nvgStrokeColor(vg, lib.nvgRGBA(128, 128, 128, 120))
            pos = i / 10 / self.seconds * self.width
            pos = (pos + self.offset) % self.width
            lib.nvgMoveTo(vg, x + pos, y)
            lib.nvgLineTo(vg, x + pos, y + height)
            lib.nvgStroke(vg)
        lib.nvgStrokeWidth(vg, 2)

        waveheight = height * 8 / 10
        wavemid = y + waveheight / 2 + height * 0.5 / 10
        lib.nvgStrokeColor(vg, lib.nvgRGBA(0, 255, 0, 120))
        for x, amp in enumerate(history):
            lib.nvgBeginPath(vg)
            lib.nvgMoveTo(vg, x, wavemid)
            lib.nvgLineTo(vg, x, wavemid + 1 + amp * waveheight / 2)
            lib.nvgStroke(vg)

        colors = {
            'hiss_start': lib.nvgRGBA(255, 0, 0, 255),
            'hiss_end': lib.nvgRGBA(255, 0, 0, 255),
            'pop': lib.nvgRGBA(255, 255, 0, 255),

            'p.begin': lib.nvgRGBA(0, 255, 0, 255),
            'p.hypothesis': lib.nvgRGBA(128, 255, 0, 255),
            'p.end': lib.nvgRGBA(255, 255, 0, 255),
        }
        offsets = {
            'hiss_start': (-5, 5),
            'hiss_end': (5, -5),
            'p.begin': (-5, 5),
            'p.hypothesis': (0, 0),
            'p.end': (5, -5),
            'pop': (0, 0),
        }
        for x, event in events:
            ot, ob = offsets[event]
            lib.nvgStrokeColor(vg, colors[event])
            lib.nvgBeginPath(vg)
            lib.nvgMoveTo(vg, x + ob, wavemid - waveheight / 2 + 5)
            lib.nvgLineTo(vg, x + ot, wavemid + waveheight / 2 - 5)
            lib.nvgStroke(vg)

font = None
timeline = AudioTimeline()

def on_noise(noise):
    with timeline.lock:
        timeline.events.append([len(timeline.history), noise])

def on_phrase(m):
    if m['cmd'] in ('p.begin', 'p.end') and m['grammar'] == 'talon':
        with timeline.lock:
            timeline.events.append([len(timeline.history), m['cmd']])

def on_overlay(vg, width, height):
    global font
    if font is None:
        font = lib.nvgCreateFont(vg, 'courier'.encode('utf8'), '/Library/Fonts/Courier New Bold.ttf'.encode('utf8'));
    lib.nvgFontFaceId(vg, font)
    lib.nvgFontSize(vg, 18)

    timeline.draw(vg, 0, height * 4/5, width, height/5)

noise.register('noise', on_noise)
record.register('record', timeline.append)
app.register('overlay', on_overlay)
engine.register('phrase', on_phrase)
