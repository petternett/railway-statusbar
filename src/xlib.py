#!/usr/bin/python
#
# Copyright 2010 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Library to get X events from Record.

This is designed to read events from X windows for keyboard and mouse
events.
"""

__author__ = 'Scott Kirkwood (scott+keymon@forusers.com)'
# Modified by Petter J. Barhaugen (petter@petternett.no)

from Xlib import display
from Xlib import X
from Xlib import XK
from Xlib.ext import record
from Xlib.protocol import rq
import sys
import time
import threading
import collections

class XEvent(object):
  """An event, mimics edev.py events."""
  def __init__(self, atype, value):
    self._type = atype
    self._value = value

  def get_type(self):
    """Get the type of event."""
    return self._type
  type = property(get_type)

  def get_value(self):
    """Get the value 0 for up, 1 for down, etc."""
    return self._value
  value = property(get_value)


class XEvents(threading.Thread):
  """A thread to queue up X window events from RECORD extension."""

  def __init__(self):
    threading.Thread.__init__(self)
    self.daemon = True
    self.name = 'Xlib-thread'
    self._listening = False
    self.record_display = display.Display()
    self.local_display = display.Display()
    self.ctx = None
    self.events = []  # each of type XEvent
    self.new_press = threading.Event()

  def run(self):
    """Standard run method for threading."""
    self.start_listening()

  def next_event(self):
    """Returns the next event in queue, or None if none."""
    if self.events:
      return self.events.pop(0)
    return None

  def start_listening(self):
    """Start listening to RECORD extension and queuing events."""
    if not self.record_display.has_extension("RECORD"):
      print("RECORD extension not found")
      sys.exit(1)
    self._listening = True
    self.ctx = self.record_display.record_create_context(
        0,
        [record.AllClients],
        [{
            'core_requests': (0, 0),
            'core_replies': (0, 0),
            'ext_requests': (0, 0, 0, 0),
            'ext_replies': (0, 0, 0, 0),
            'delivered_events': (0, 0),
            'device_events': (X.KeyRelease, X.MotionNotify),  # why only two, it's a range?
            'errors': (0, 0),
            'client_started': False,
            'client_died': False,
        }])

    self.record_display.record_enable_context(self.ctx, self._handler)

    # Don't understand this, how can we free the context yet still use it in Stop?
    self.record_display.record_free_context(self.ctx)
    self.record_display.close()

  def stop_listening(self):
    """Stop listening to events."""
    if not self._listening:
      return
    self.local_display.record_disable_context(self.ctx)
    self.local_display.flush()
    self.local_display.close()
    self._listening = False
    self.join(0.05)

  def listening(self):
    """Are you listening?"""
    return self._listening

  def _handler(self, reply):
    """Handle an event."""
    if reply.category != record.FromServer:
      return
    if reply.client_swapped:
      return
    data = reply.data
    while len(data):
      event, data = rq.EventField(None).parse_binary_value(
          data, self.record_display.display, None, None)
      if event.type == X.KeyRelease:
        self._handle_key(event, 1)


  def _handle_key(self, event, value):
    """Add key event to events.
    Params:
      event: the event info
      value: 1=down, 0=up
    """
    self.events.append(XEvent('EV_KEY', event.detail - 8))
    self.new_press.set()
