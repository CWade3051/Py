# IDLEX EXTENSION
from __future__ import print_function
##
##    Copyright(C) 2012 The Board of Trustees of the University of Illinois.
##    All rights reserved.
##
##    Developed by:   Roger D. Serwy
##                    University of Illinois
##
##    Permission is hereby granted, free of charge, to any person obtaining
##    a copy of this software and associated documentation files (the
##    "Software"), to deal with the Software without restriction, including
##    without limitation the rights to use, copy, modify, merge, publish,
##    distribute, sublicense, and/or sell copies of the Software, and to
##    permit persons to whom the Software is furnished to do so, subject to
##    the following conditions:
##
##    + Redistributions of source code must retain the above copyright
##      notice, this list of conditions and the following disclaimers.
##    + Redistributions in binary form must reproduce the above copyright
##      notice, this list of conditions and the following disclaimers in the
##      documentation and/or other materials provided with the distribution.
##    + Neither the names of Roger D. Serwy, the University of Illinois, nor
##      the names of its contributors may be used to endorse or promote
##      products derived from this Software without specific prior written
##      permission.
##
##    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
##    OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
##    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
##    IN NO EVENT SHALL THE CONTRIBUTORS OR COPYRIGHT HOLDERS BE LIABLE FOR
##    ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
##    CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH
##    THE SOFTWARE OR THE USE OR OTHER DEALINGS WITH THE SOFTWARE.
##
##
##
## An extension to allow IPython to work with IDLE's shell environment.
## The latest 0.12 version uses a two-process model with ZMQ.
##


config_extension_def = """
[IPyIDLE]
enable = 1
enable_shell = 1
enable_editor = 1

ipython = True
allow_restart = True

"""


# This extension relies on Terminal.py's behavior
# for the command line.
#
# This also expects that AutoComplete Calltips extensions
# are enabled (which is the default in IDLE)
#
#

#-----------------------------------------------------------------------------
# Parts of this code derives from IPython 0.12 which has the following notice:
#
# Copyright (C) 2011 The IPython Development Team
#
# Distributed under the terms of the BSD License. The full license is in
# the file COPYING, distributed as part of this software.
#-----------------------------------------------------------------------------

# Kernel manager launch code based on VIM integration
# by Paul Ivanov (http://pirsquared.org)

#----------------------------------------------
# Imports
#----------------------------------------------

HAS_PIL = True
try:
    from PIL import ImageTk
except:
    HAS_PIL = False


# python stdlib
import bdb
import signal
import sys
import time
import re
import marshal
import types
import traceback
from pprint import pprint
import time
from threading import Event, Lock, Thread
import string
import threading
import os
from base64 import decodestring
import tempfile
import shutil

if sys.version < '3':
    import Tkinter as tk
    import tkSimpleDialog
    import tkMessageBox
    import tkFileDialog
    from Queue import Queue, Empty
    from io import BytesIO
    import copy_reg as copyreg

else:
    import tkinter as tk
    import tkinter.simpledialog as tkSimpleDialog
    import tkinter.messagebox as tkMessageBox
    import tkinter.filedialog as tkFileDialog
    from queue import Queue, Empty
    from io import BytesIO
    import copyreg
    unicode = str   # runcode needs "unicode" for Python2


# IPython breaks code pickling in IDLE, must correct it...
try:
    _code_pickle_original = copyreg.dispatch_table.get(types.CodeType, None)
except:
    _code_pickle_original = None

HAS_IPYTHON = True

try:
    import IPython
    if IPython.__version__ < '0.12':
        HAS_IPYTHON = False
except:
    HAS_IPYTHON = False

if HAS_IPYTHON:
    # IPython
    from IPython.core import page
    from IPython.utils.warn import warn, error, fatal
    from IPython.utils import io as ipython_io
    from IPython.core.oinspect import call_tip
    from IPython.frontend.terminal.interactiveshell import TerminalInteractiveShell
    from IPython.utils.traitlets import Type
    from IPython.zmq.kernelmanager import (KernelManager, SubSocketChannel, HBSocketChannel,
                                           ShellSocketChannel, StdInSocketChannel)

    #from IPython.frontend.consoleapp import IPythonConsoleApp
    from IPython.config.loader import KeyValueConfigLoader
    from IPython.zmq.kernelapp import kernel_aliases
    from IPython.lib.kernel import find_connection_file

else:
    # pacify later code from errors
    TerminalInteractiveShell = object
    KernelManager = SubSocketChannel = HBSocketChannel = object
    ShellSocketChannel = StdInSocketChannel = object
    Type = lambda x: None

if _code_pickle_original:
    # FIX THE PICKLE DISPATCH TABLE
    copyreg.dispatch_table[types.CodeType] = _code_pickle_original


# IDLE
from idlelib.configHandler import idleConf
from idlelib.Delegator import Delegator
from idlelib.IdleHistory import History
import idlelib.AutoComplete         # circular import avoidance for AutoCompleteWindow
import idlelib.AutoCompleteWindow as AutoCompleteWindow
import idlelib.CallTipWindow as CallTipWindow
from idlelib.UndoDelegator import UndoDelegator
import idlelib.PyShell as PyShell
from idlelib.PyShell import ModifiedInterpreter
from idlelib.HyperParser import HyperParser
from idlelib.Percolator import Percolator
from idlelib import SearchDialog
from idlelib import Bindings
from idlelib.MultiCall import MultiCallCreator

# IdleX
from idlexlib import idlexMain
from idlexlib.extensions.SearchBar import SearchBar

#------------------------------------
# basic functions
#------------------------------------

jn = lambda x,y: '%i.%i' % (x,y)        # join integers to text coordinates
sp = lambda x: list(map(int, x.split('.')))   # convert tkinter Text coordinate to a li


def background(f):  # from IPython project
    """call a function in a simple thread, to prevent blocking"""
    t = Thread(target=f)
    t.start()
    return t

def debug(*args, **kw):
    print(*args, **kw)
debug = lambda *args, **kw: None

orig_ps1 = getattr(sys, 'ps1', None)
orig_ps2 = getattr(sys, 'ps2', None)

#-----------------------------------------------------------------------------
# IdleX IPython Kernel Channels
#-----------------------------------------------------------------------------

# AFAIK, Tkinter can't handle placing events on its event queue from a thread
# other than MainThread. IPython's 0MQ channels provides events in different
# threads, so these messages are placed into a Queue for Tkinter to handle
# from its MainThread.

##DISPLAY_MESSAGES = True
##GET_HISTORY = not DISPLAY_MESSAGES

DISPLAY_MESSAGES = False
GET_HISTORY = True


ChannelLock = Lock()
def channel_lock(func):     # lock decorator
    def f(*arg, **kw):
        with ChannelLock:
            return func(*arg,**kw)
    return f

MessageQueue = Queue()  # place all messages into here

class SimpleChannel(object):
    @channel_lock
    def call_handlers(self, msg):
        if DISPLAY_MESSAGES:
            print('[[%s]]' % self.channel_name, '-'*50)
            print('Thread: %r' % threading.currentThread().getName())
            if isinstance(msg, dict):
                msg2 = msg.copy()
                del msg2['parent_header']
            else:
                msg2 = msg
            pprint(msg2)
        # Place all messaged into a Queue so that
        # the Tkinter event loop in MainThread can process them.
        MessageQueue.put((self.channel_name, msg))


class IdleXSubSocketChannel(SimpleChannel, SubSocketChannel):
    channel_name = 'sub'

class IdleXShellSocketChannel(SimpleChannel, ShellSocketChannel):
    channel_name = 'shell'

class IdleXStdInSocketChannel(SimpleChannel, StdInSocketChannel):
    channel_name = 'stdin'

class IdleXHBSocketChannel(SimpleChannel, HBSocketChannel):
    channel_name = 'hb'
    time_to_dead = 1.0

class IdleXKernelManager(KernelManager):
    shell_channel_class = Type(IdleXShellSocketChannel)
    sub_channel_class = Type(IdleXSubSocketChannel)
    stdin_channel_class = Type(IdleXStdInSocketChannel)
    hb_channel_class = Type(IdleXHBSocketChannel)


class IPyProxy(object):

    shell_images = []
    socket = 0

    def __init__(self):

        self.active = None                  # reference to IPyIDLE instance
        self.active_pyshell = None          # reference to active PyShell editor instance
        self.switching = False              # flag for switching shell
        self.allow_restart = True           # flag for ScriptBinding.py behavior
        self._onetime_kernel_restart_message = False
        self.kernel_manager = None
        self.argv_changed = False
        self._shell = None

        self._saved_history = None
        self._reset()

    def _reset(self):
        self._output = Queue()          # for output to .text widget of PyShell
        self._output_pyerr = Queue()
        self._execute_queue = Queue()
        self.execution_state = None
        self._do_input = None
        self._got_pyin = False
        self._expected_execute_replies = []
        self.calltipwindow = None
        self.readline_canceled = False


    def get_fake_socket(self):
        self.socket += 1
        return self.socket

    @property
    def connection_file(self):
        return idlexMain.ipython_connection_file

    def start_km(self):
        self.stop_km()  # make sure old was stopped
        self._expected_execute_replies = []
        kwargs = {}

        found_cf = ''

        cf = self.connection_file
        if cf:
            found_cf = self.get_connection_file(cf)

        if idlexMain.ipython_argv:
            kwargs['extra_arguments'] = idlexMain.ipython_argv


        km = IdleXKernelManager()
        self.kernel_manager = km

        if found_cf:
            msg = '\n IPython using connection file:\n %s\n' % found_cf
            try:
                km.connection_file = found_cf
                km.load_connection_file()
            except IOError:
                connection_file = ''
                msg = '\n Unable to load connection file:\n %s\n' % found_cf
                km.connection_file = ''
                self.kernel_manager = km

            e = self.active_pyshell
            print(msg, file=sys.stderr)
            if e:
                self._output.put((True, 'stderr', msg))
                #e.text.insert('end', msg, tags='stderr')

        if not found_cf:
            km.start_kernel(**kwargs)

        km.start_channels()
        if GET_HISTORY:
            msg_id = km.shell_channel.history(hist_access_type='tail', n=1000)
        #km.shell_channel.execute('None', silent=True)
        self.switching = False
        km.hb_channel.unpause()
        self.active_pyshell.executing = 0

    def _windows_error(self, err):
        print('A Windows-specific error occurred:', file=sys.stderr)
        print(err,file=sys.stderr)

    def stop_km(self):
        km = self.kernel_manager
        if km:
            if not self.connection_file:
                try:
                    km.shutdown_kernel(restart=False)
                except WindowsError as err:
                    self._windows_error(err)
                except RuntimeError as err:
                    pass
                km.cleanup_connection_file()
            background(km.stop_channels)
            self.shell.execution_count = 1
            self.kernel_manager = None

        self._execute_queue = Queue()
        self._expected_execute_replies = []

        self._saved_history = None
        self.switching = False

    def interrupt(self):
        self.readline_canceled = True
        self.kernel_manager.interrupt_kernel()

    def request_kernel_restart(self):
        if self.switching:
            self.switching = False
            return False

        if not self.allow_restart:
            e = self.active_pyshell
            if not self._onetime_kernel_restart_message:
                self._onetime_kernel_restart_message = True
                msg = ('\n Kernel restart is not allowed.\n ' +
                       'To allow it, check "Allow IPython Kernel Restart" under "Shell".')
                self._output.put((True, 'stderr', msg))
            return False
        else:
            self._onetime_kernel_restart_message = False

        if self.argv_changed:
            self.argv_changed = False
            self.stop_km()
            self.start_km()
        else:
            if self.connection_file:
                e = self.active_pyshell
                msg = ('\n Will not restart kernel when connected ' +
                      'to a remote kernel:\n %s\n' % self.connection_file)
                self._output.put((True, 'stderr', msg))
                return False
            self._expected_execute_replies = []
            self.kernel_manager.restart_kernel()
            if GET_HISTORY:
                self.kernel_manager.shell_channel.history(hist_access_type='tail', n=1000)
            self.kernel_manager.shell_channel.execute('None', silent=True)
        self.shell.execution_count = 1
        self.regenerate_prompt_string()
        self.execution_state = 'idle'
        self.readline_canceled = True
        return True

    def cleanup_connection_file(self):
        if not self.connection_file:
            km = self.kernel_manager
            if km and km.has_kernel:
                km.cleanup_connection_file()

    @property
    def autocompletewindow(self):
        return self.active.autocompletewindow

    @property
    def executing(self):
        return ((self._execute_queue.qsize() > 0) or
                (len(self._expected_execute_replies) > 0))

    def enqueue_execute(self, source, *args, **kw):
        self._execute_queue.put((source, args, kw))

    def _exec_if_idle(self):
        # called from poll_subprocess
        #print('what', self.execution_state, len(self._expected_execute_replies))
        if (self.execution_state == 'idle' and
                len(self._expected_execute_replies) == 0):
            try:
                m = self._execute_queue.get_nowait()
            except Empty:
                return
            self.active_pyshell.executing = 0  # in case Ctrl+C aborted execution
            source, args, kw = m
            exec_callback = kw.pop('exec_callback')
            finish_callback = kw.pop('finish_callback')
            km = self.kernel_manager
            if exec_callback:
                try:
                    exec_callback()
                except Exception as err:
                    print('Exception in callback: %r' % err)
            msg_id = km.shell_channel.execute(source, *args, **kw)
            #print('sending: %s: %r' % (msg_id, source))
            self._expected_execute_replies.append((msg_id, finish_callback))

        if self.execution_state is None:
            self.execution_state = 'idle' # never got initialized

        if self.execution_state not in ['busy', 'idle']:
            print('Unknown execution state: %r' % self.execution_state)

        # TODO: failsafe if execute reply never gets received....
        #print('_exec_if_idle', self.execution_state, self._expected_execute_replies)

    def _get_console_output(self):
        # combine all the output for the console
        _output = self._output
        _output_pyerr = self._output_pyerr
        retval = []
        while 1:     # flush the stdout/stderr queue
            try:
                stuff = _output.get(block=False)
                retval.append(stuff)
            except Empty:
                break
        while 1:    # flush the pyerr queue
            try:
                stuff = _output_pyerr.get(block=False)
                retval.append(stuff)
            except Empty:
                break
        return retval

    def write_console_output(self):
        # handle console output, write before the prompt
        tkconsole = self.active_pyshell
        out = self._get_console_output()
        if out:
            text = tkconsole.text
            for before, name, data in out:
                if before:
                    # remember the location of iomark
                    text.mark_set('iomark2', 'iomark')
                    text.mark_gravity('iomark2', text.mark_gravity('iomark'))


                    text.mark_set('iomark', 'before_prompt')  # Undo Delegator
                    text.mark_gravity("before_prompt", "right")
                    if name in ['stdout', 'stderr']:
                        #print('%r' % data)
                        text.insert('before_prompt', data, tags=name)

                    elif name == 'image/png':
                        if HAS_PIL:
                            prior_root = tk._default_root  # Work around a bug in IDLE
                            tk._default_root=tkconsole.top

                            si = ShellImage(text, data, format='image/png')
                            text.window_create('before_prompt', window=si)
                            self.shell_images.append(si)

                            tk._default_root = prior_root

                        else:
                            text.insert('before_prompt',
                                        ("\nMissing 'ImageTk' from PIL to display image/png.\n" +
                                         'Please install Python Imaging Library with Tkinter support.\n' +
                                         'http://www.pythonware.com/products/pil/'
                                         ))
                    else:
                        print('Unsupported image type: %r' % name)

                    text.mark_gravity("before_prompt", "left")
                    if tkconsole.text.compare('iomark2', '<', 'before_prompt'):
                        tkconsole.text.mark_set('iomark2', 'before_prompt')

                    # restore iomark
                    text.mark_set('iomark', 'iomark2')
                    text.mark_unset('iomark2')

                else: # after prompt
                    if name in ['stdout', 'stderr']:
                        text.insert('end', data, tags=name)

            tkconsole.text.see('insert')

    def clear_shell_images(self):
        for i in self.shell_images:
            i.destroy()
        self.shell_images = []

    def regenerate_prompt_string(self):
        shell = self.shell
        shell.hooks.pre_prompt_hook()
        try:
            prompt = shell.separate_in + shell.prompt_manager.render('in')
        except Exception:
            traceback.print_exc()
            shell.showtraceback()

        sys.ps1 = prompt

        try:
            prompt = shell.prompt_manager.render('in2')
        except Exception:
            traceback.print_exc()
            shell.showtraceback()

        sys.ps2 = prompt

    @property
    def shell(self):
        if self._shell is None:
            e = self.active_pyshell
            idle_io = (e,  e.stdout, e.stderr)
            km = ipyProxy.kernel_manager
            self._shell = IPyIDLEShell(user_ns={},
                                      kernel_manager=km,
                                      io=idle_io)
        return self._shell

    def call_message_handlers(self, m):
        channel_name, msg = m
        if channel_name != 'hb':
            msg_type = msg['header']['msg_type']
            h = getattr(self, '_handle_%s_%s' % (channel_name, msg_type), None)
            if h:
                h(msg)
            else:
                print('Not Implemented: %s on %s channel' % (msg_type, channel_name))
                pprint(msg)
        else:
            print('heartbeat:', msg)

    def get_the_calltip(self, obj):
        # called from FakeSubProcess
        #print('get_the_calltip: %r' % obj)
        msg_id = self.kernel_manager.shell_channel.object_info(obj)


    def restore_IDLE_history(self):
        # forget the IPython command history and restore
        # what the normal IDLE shell had
        if self.active_pyshell and self._saved_history:
            h = History(active_pyshell.text)
            h.history = self._saved_history
            h.history_prefix = None
            h.history_pointer = None
            self._saved_history = None
            active_pyshell.history = h

    def set_IPython_history(self, items):
        #print('set_ipython_history', items)
        e = self.active_pyshell
        if e:
            history = IPythonHistory(e.text)
            history.history = items
            e.history = history
        else:
            print('Unable to set history - not active pyshell', file=sys.stderr)


    def _from_this_session(self, msg):
        km_session = ipyProxy.kernel_manager.session.session
        parent = msg['parent_header']
        if not parent:
            return True
        else:
            return parent.get('session') == km_session

    def get_connection_file(self, connection_file):
        try:
            connection_file = find_connection_file(connection_file)
        except IOError as err:
            s = 'Unable to find: %r' % connection_file
            print(s, file=sys.stderr)
            if self.active:
                tkMessageBox.showerror('IPython Connection File', message=s,
                                       parent=self.active.editwin.text)
            return ''
        return connection_file

    #-------------------------------
    # Channel Message Handlers
    #-------------------------------
    def check_session(func):
        def f(self, msg, *arg, **kw):
            if not self._from_this_session(msg):
                #print('not from session, call to %s' % func)
                return
            else:
                #print('is from session, call to %s' % func)
                return func(self, msg, *arg, **kw)
        return f


    @check_session
    def _handle_sub_stream(self, msg):
        datetime = msg['header']['date']
        before = True
        content = msg['content']
        name = content['name'] # stout or stderr
        data = content['data']
        self._output.put((before, name, data))

    @check_session
    def _handle_sub_status(self, msg):
        content = msg['content']
        ec = content['execution_state']
        self.execution_state = ec
        png_data = content.get('image/png')
        self._output_png_data(png_data)

    def _handle_sub_pyerr(self, msg):
        pass

    @check_session
    def _handle_sub_pyout(self, msg):
        content = msg['content']
        execution_count = int(content["execution_count"])
        self.shell.execution_count = execution_count
        format_dict = msg["content"]["data"]
        # from displayhook.py
        outprompt = self.shell.prompt_manager.render('out')   #write_output_prompt
        result_repr = format_dict['text/plain']
        if '\n' in result_repr:
            prompt_template = self.shell.prompt_manager.out_template
            if prompt_template and not prompt_template.endswith('\n'):
                result_repr = '\n' + result_repr
        last = self.shell.separate_out2

        out = outprompt + result_repr + last
        out += '\n'
        self._output.put((True, 'stdout', out))
        self._output_png_data(format_dict.get('image/png', None))


    def _handle_sub_pyin(self, msg):
        # acknowledgment of sent command
        pass

    def _handle_sub_shutdown_reply(self, msg):
        self._expected_execute_replies = []

    def _handle_shell_shutdown_reply(self, msg):
        pass

    @check_session
    def _handle_shell_execute_reply(self, msg):
        self.kernel_manager.sub_channel.flush()

        parent_id = msg['parent_header']['msg_id']

        content = msg['content']
        status = content['status']

        expecting = self._expected_execute_replies
        finish_callback = None

        expected_msg_id = [msg_id for msg_id,callback in expecting]

        a = [n for n, i in enumerate(expecting) if i[0] == parent_id]
        if a:
            if a[0] == 0:
                #print('in order')
                pass
            else:
                #print('out of order')
                pass

            emsgid, finish_callback = expecting.pop(a[0])
        else:
            #print('not expecting')
            pass

        ec = content.get("execution_count", None)
        if ec:
            if int(ec + 1) != self.shell.execution_count:
                self.shell.execution_count = int(ec + 1)
                self.regenerate_prompt_string()
        if status == 'error':
            name = 'stderr'
            self._output_pyerr.put((True, 'stderr', '\n'))
            for frame in content["traceback"]:
                self._output_pyerr.put((True, name, frame))
            self._output_pyerr.put((True, 'stderr', '\n'))

        if 'payload' in content:
            for item in content["payload"]:
                text = item.get('text', None)
                if text:
                    Pager(self.active.editwin.top,
                               'IDLE IPython Pager',
                               text)

                filename = item.get('filename', None)
                if filename:
                    flist = self.active_pyshell.flist
                    flist.open(filename)
                    # TODO: handle going to a line number

        if finish_callback:
            finish_callback()

    def _handle_shell_history_reply(self, msg):
        content = msg['content']
        items = content['history']

        # TODO: handle case if history request failed
        history_items = content['history']
        items = []
        last_cell = ""
        for _, _, cell in history_items:
            cell = cell.rstrip()
            if cell != last_cell:
                items.append(cell)
                last_cell = cell

        self.set_IPython_history(items)

    def _handle_shell_object_info_reply(self, msg):
        """ Display a call tip """
        # show call tip
        if self.calltipwindow:
            self.calltipwindow.hidetip()

        editwin = self.active.editwin
        self.calltipwindow = ctw = CallTipWindow.CallTip(editwin.text)

        content = msg['content']
        call_info, doc = call_tip(content, format_call=True)
        maxlines = 15
        # code from Qt console call_tip_widget.py
        if doc:
            match = re.match("(?:[^\n]*\n){%i}" % maxlines, doc)
            if match:
                doc = doc[:match.end()] + '\n[Documentation continues...]'
        else:
            doc = ''

        if call_info:
            doc = '\n\n'.join([call_info, doc])

        hp = HyperParser(editwin, "insert")
        sur_paren = hp.get_surrounding_brackets('(')
        try:
            if sur_paren:
                p1, p2 = sur_paren
                MARK_RIGHT = "calltipwindowregion_right"
                editwin.text.mark_set(MARK_RIGHT, p2)
                ctw.showtip(doc, p1, p2)
        except:
            print('CALLTIP ERROR', '-'*50)
            traceback.print_exc()


    def _handle_shell_complete_reply(self, msg):
        """ Display an AutoCompleteWindow with this reply """
        self.autocompletewindow.hide_window()
        m = msg['content'].get('matches', None)
        if not m:
            return

        comp_start = msg['content']['matched_text']

        # remove leading matched_text from the results
        # up to the last "."
        p = re.split("[./]", comp_start)

        if len(p) > 1:
            ignore = '.'.join(p[:-1])
            remain = p[-1]
            offset = len(ignore) + 1   # "+ 1" for the last .
            m = [i[offset:] for i in m]
            comp_start=remain

        # Take the result and make it compatible
        # with IDLE's autocomplete extension
        comp_lists = (m,m)
        mode = AutoCompleteWindow.COMPLETE_ATTRIBUTES
        userWantsWin = True
        complete = True
        self.autocompletewindow.show_window(comp_lists,
                                            "insert-%dc" % len(comp_start),
                                            complete,
                                            mode,
                                            userWantsWin)

    def _handle_stdin_input_request(self, msg):
        self.kernel_manager.sub_channel.flush()

        prompt = msg["content"]["prompt"]
        if not isinstance(prompt, (str, unicode)):
            prompt = str(prompt)

        self._do_input = prompt
        # _do_input is a flag used in poll_subprocess
        # to initialize readline.
        tkconsole = self.active_pyshell

        text = tkconsole.text
        text.mark_set('before_prompt', 'iomark linestart')
        text.mark_gravity("before_prompt", "left")
        text.insert('before_prompt', prompt)
        text.mark_set('iomark', 'end-1c')

        self.readline_canceled = False
        debug('ENTER READLINE')
        raw_data = tkconsole.readline()
        debug('EXIT READLINE: %r' % raw_data)
        if tkconsole.closing:
            # Note: tkconsole.closing must be tested in case
            # PyShell is closed during readline
            return

        if self.readline_canceled:
            # Ctrl+C or restart of kernel
            self.readline_canceled = False
            return

        raw_data = raw_data[:-1]  # eliminate \n
        debug('SENDING RAW_INPUT: %r' % raw_data)
        ipyProxy.kernel_manager.stdin_channel.input(raw_data)
        text.mark_set('before_prompt', 'insert')
        if self.active_pyshell:
            self.active_pyshell.resetoutput()

    def _handle_sub_display_data(self, msg):
        data = msg['content']['data']
        png_data = data.get('image/png', None)
        self._output_png_data(png_data)

    def _output_png_data(self, png_data):
        if png_data:
            png = decodestring(png_data.encode('ascii'))
            self._output.put((True, 'image/png', png))


ipyProxy = IPyProxy()               # Launch a singleton for IPyProxy


class ShellImage(tk.Label):
    def __init__(self, text, data, format=None):
        # format - TODO allow for SVG in future
        # For now, only handle .png

        fid = BytesIO(data)
        im = ImageTk.Image.open(fid)
        try:
            tkim = ImageTk.PhotoImage(im)
        except ImportError:
            tkim = None
            pass
        tk.Label.__init__(self, text, image=tkim, takefocus=0, borderwidth=0)

        self.text = text
        self.tkim = tkim
        self.im = im
        self.bind('<4>', lambda e: text.event_generate('<4>'))
        self.bind('<5>', lambda e: text.event_generate('<5>'))
        self.bind('<3>', self.rmenu)

    def rmenu(self, event=None):
        # Do "save image"
        # Tkinter can not place an image on the clipboard.
        rmenu = tk.Menu(self.text, tearoff=0)

        rmenu.add_command(label='Save Image As...', command=self.saveas)
        rmenu.tk_popup(event.x_root, event.y_root)

    def saveas(self):
        s = tkFileDialog.SaveAs(parent=self.text,
                                filetypes=[('Portable Network Graphic', '*.png')])
        initial = str(self.tkim) + '.png'
        filename = s.show(initialfile=initial)
        if filename:
            try:
                self.im.save(filename, format='png')
            except Exception as err:
                traceback.print_exc()


#----------------------
# Delegators for Text
#----------------------
# Based on code from: http://wiki.ipython.org/Old_Embedding/Tkinter
ansi_colors =  {'0;30': '#000000', # black
                '0;31': '#880000', # red
                '0;32': '#008800', # green
                '0;33': '#664400', # brown
                '0;34': '#000088', # blue
                '0;35': '#880088', # purple
                '0;36': '#008888', # cyan
                '0;37': '#AAAAAA', # white

                '1;30': '#555555', # light black
                '1;31': '#AA0000', # light red
                '1;32': '#00AA00', # light green
                '1;33': '#888800', # light brown
                '1;34': '#0000AA', # light blue
                '1;35': '#AA00AA', # light purple
                '1;36': '#00AAAA', # light cyan
                '1;37': '#000000', # light white

                '01;30': '#555555', # light black
                '01;31': '#AA0000', # light red
                '01;32': '#00AA00', # light green
                '01;33': '#888800', # light brown
                '01;34': '#0000AA', # light blue
                '01;35': '#AA00AA', # light purple
                '01;36': '#00AAAA', # light cyan
                '01;37': '#000000', # light white
                }


ansi_re = re.compile(r'\x01?\x1b\[(.*?)m\x02?')
def strip_ansi(s):
    return ansi_re.sub("", s)

class AnsiColorDelegator(Delegator):
    # Colorize IPython ansi color codes
    def __init__(self, *args, **kw):
        Delegator.__init__(self, *args, **kw)

    def insert(self, index, chars, tags=None):
        chars = chars.replace('\r', '')
        delegate = self.delegate

        index = delegate.index(index)
        if tags:
            tags = tags.replace('stdout', '')

        m = ansi_re.search(chars)
        if not m:
            delegate.insert(index, chars, tags)
        else:
            if tags is None:
                tags = ''
            active_tag = ''
            prior = 0
            ic = 0
            while m:
                s = m.start()
                e = m.end()
                b = chars[prior:s]
                if len(b):
                    delegate.insert(index + '+%ic' % ic, b, tags + ' ' + active_tag)
                    ic += len(b)

                active_tag = ansi_re.split(chars[s:e])[1]
                prior = e
                m = ansi_re.search(chars, prior)

            delegate.insert(index + '+%ic' % ic, chars[prior:], tags + ' ' + active_tag)


class IPythonHistory(History):

    def history_store(self, source):
        debug('storing: ', source, self)
        source = source.rstrip()  # preserve leading whitespace
        if len(source) > 0: # avoid duplicates
            try:
                if source in self.history[-10:]:
                    self.history.remove(source)
            except ValueError:
                pass
            self.history.append(source)
        self.history_pointer = None
        self.history_prefix = None


#-----------------------------------------
# PyShell Subprocess-to-IPython Interface
#-----------------------------------------
eloop = """try:
    __IDLE_eventloop()
except NameError:
    pass
except Exception as err:
    __IDLE_eventloop_error(err)
"""  # EventLoop.py support

class FakeSubProcess(object):
    # used by BridgeInterpreter
    restarting = False
    def __init__(self, interp):
        self.interp = interp  # pointer to idleIPython instance
        self.sock = ipyProxy.get_fake_socket()

    def __getattr__(self, name):
        print('__getattr sub__', name)
        def f(*args, **kwargs):
            return None
        return f

    def putmessage(self, message):
        seq, resq = message
        how = resq[0]
        if how in ("CALL", "QUEUE"):
            cmd, method, code, d = resq[1]
            if cmd == 'exec' and method =='runcode':
                #self.interp.runcommand(code[0])  # for EventLoop.py
                self.interp.runcommand(eloop) # eventloop.py support only

    def remotecall(self, oid, methodname, args, kwargs):
        # pacify IDLE's default autocomplete and calltip extensions
        #print('remotecall', oid, methodname, args, kwargs)
        if methodname == "get_the_completion_list":
            # the <Tab> event handles autocomplete in class IPyIDLE
            return [], []
        elif methodname == "get_the_calltip":
            obj = args[0]  # get tip for this object string
            ipyProxy.get_the_calltip(obj)
            return None

    def close(self):
        pass


class BridgeInterpreter(ModifiedInterpreter):
    # IDLE creates a new instance of ModifiedInterpreter on each restart.
    # This relies on ipyProxy to do the actual interface to the IPython kernel

    def __init__(self, tkconsole):
        ModifiedInterpreter.__init__(self, tkconsole)
        ipyProxy.interp = self
        self.top = self.tkconsole.top
        self.poll_id = None             # poll_subprocess .after id
        self.debugger = None

        self.IMAGES = []

    def set_before_prompt(self):
        # mark set the "before_prompt" in the console window
        backlines = sys.ps1.count('\n')
        text = self.tkconsole.text
        text.mark_set('before_prompt', 'iomark linestart')
        if backlines:
            text.mark_set('before_prompt', 'before_prompt -%i lines' % backlines)
        text.mark_gravity("before_prompt", "left")

    def beginexecuting(self):
        debug('beginexecuting')
        tkconsole = self.tkconsole
        text = getattr(tkconsole, 'text', None)
        if text is None:
            # text can be None if the shell is closed after
            # the execution has been queued, but before it gets
            # executed. For example, press F5 and then quickly close the shell.
            print('.text not found during beginexecuting')
            return

        a = text.get('iomark', 'end')

        # remove excess whitespace due to newline and indent
        i1 = a.rfind('\n',0, len(a)-1) + 1
        text.delete('iomark+%ic' % i1, 'end-1c')

        tkconsole.resetoutput()
        text.mark_set('before_prompt', 'iomark linestart')
        text.mark_gravity("before_prompt", "left")
        tkconsole.executing = 1
        text.see('insert')

    def endexecuting(self):
        debug('endexecuting')
        tkconsole = self.tkconsole
        text = getattr(tkconsole, 'text', None)
        if text is None:
            print('.text not found during endexecuting')
            return
        ipyProxy.regenerate_prompt_string()
        tkconsole.resetoutput()
        tkconsole.showprompt()

        if not ipyProxy.executing:
            tkconsole.executing = 0
        tkconsole.canceled = 0


    def _finalize_init(self):
        # For an unknown reason (possibly a race condition), IPython
        # sometimes fails to send an execute reply over the 0MQ channels
        # for this no-op "None" command. For now, ignore it.
        # FIXME: Determine why IPython fails to send execute reply sometimes.
        return  # skip the execution of this command.
        def fcb():
            self.tkconsole.executing = 0
        ipyProxy.enqueue_execute('None',
                                 silent=True,
                                 exec_callback=None,
                                 finish_callback=fcb)

    def start_subprocess(self):
        #print('start_subprocess')
        welcome = ' Welcome to the IdleX IPython shell. '
        B = ['-'*len(welcome),
             welcome,
             '-'*len(welcome),
             ipyProxy.shell.banner]

        PyShell.PyShell.COPYRIGHT = '\n'.join(B)
        ipyProxy.regenerate_prompt_string()
        self._poll_cancel(reschedule=True)
        self.rpcclt = FakeSubProcess(self)
        self.transfer_path(with_cwd=True)
        self._finalize_init()
        self.restarting = False
        text = self.tkconsole.text
        return self.rpcclt

    def restart_subprocess(self, with_cwd=False):
        if self.restarting:
            return self.rpcclt
        self.rpcclt.restarting = True
        self.restarting = True

        if ipyProxy.request_kernel_restart():
            pass
        else:
            print('unable to restart kernel', file=sys.stderr)
            self.restarting = False
            self.rpcclt.restarting = False
            return

        console = self.tkconsole
        was_executing = console.executing

        if console.reading and ipyProxy.readline_canceled == True:
            console.reading = False
            console.top.quit()          # IDLE workaround

        # annotate restart in shell window and mark it
        console.text.delete("iomark", "end-1c")
        console.write('\n')
        if was_executing:
            console.write('\n')
        halfbar = ((int(console.width) - 16) // 2) * '='
        console.write(halfbar + ' RESTART ' + halfbar)
        console.text.mark_set("restart", "end-1c")
        console.text.mark_gravity("restart", "left")

        ipyProxy.regenerate_prompt_string()
        console.showprompt()
        self.set_before_prompt()
        self.transfer_path(with_cwd=with_cwd)
        self._finalize_init()
        self._poll_cancel(reschedule=True)
        self.rpcclt = FakeSubProcess(self) # fake out IDLE
        self.restarting = False
        return self.rpcclt

    def poll_subprocess(self):
        tkconsole = self.tkconsole
        km = ipyProxy.kernel_manager

        if (not self.restarting and not ipyProxy.kernel_manager.is_alive
                                                and not tkconsole.closing):
            self.tkconsole.write("\n\n Kernel Died.\n Returing to IDLE's shell...\n")
            self.tkconsole.text.event_generate('<<idleIPythonShell>>')
            return

        if not tkconsole.closing:
            self._poll_cancel(reschedule=True)

        while 1:
            try:
                m = MessageQueue.get_nowait()
            except Empty:
                break
            ipyProxy.call_message_handlers(m)

        ipyProxy.write_console_output()
        ipyProxy._exec_if_idle()


    def _poll_cancel(self, reschedule=False):
        """ For managing the poll_subprocess timer """
        if self.poll_id:
            self.top.after_cancel(self.poll_id)
        if reschedule:
            self.poll_id = self.top.after(25, self.poll_subprocess)

    def interrupt_subprocess(self):
        ipyProxy.interrupt()
        c = self.tkconsole

    def kill_subprocess(self):
        ipyProxy.restore_IDLE_history()
        self._poll_cancel()
        self.poll_id = None
        #self.compile = None

    def runsource(self, source):
        # Used by PyShell for the interactive prompt
        # Returns True if the prompt can accept more lines.
        #print('runsource %r' % source)
        shell = ipyProxy.shell
        r = shell.input_splitter.source_raw_reset()
        shell.input_splitter.push(source + '\n')
        more = shell.input_splitter.push_accepts_more()
        if not more:
            self.runcode(source, store_history=True, do_exec=True)
        return more

    def runcommand(self, source):
        # Used to run commands silently in IDLE,
        # like path initialization, etc...
        source = source.rstrip()  # Python 2.6 compatibility
        exec_callback = finish_callback = None
        ipyProxy.enqueue_execute(source, silent=True,
                                 exec_callback=exec_callback,
                                 finish_callback=finish_callback)

    def runcode(self, source, store_history=False, do_exec=True):
        # Called from runsource usually. ScriptBinding, SubCode, and RunSelection
        # call this as well. Used to run code objects originally.
        #print('runcode: %r' % source)
        if isinstance(source, types.CodeType):
            store_history = False
            f = source.co_filename
            if os.path.isfile(f):
                if sys.version < '3':
                    # Python3 really did fix the unicode problem of Python2.
                    try:
                        f = unicode(f.decode('utf8'))
                    except Exception as err:
                        print('Unable to decode filename: %r' % f)
                        pass
                # ScriptBinding's Run Module should invoke this code path...
                #source = "%%run %s" % f   # Only works with IPython 0.13
                # Using get_ipython() is compatible with 0.12 and 0.13
                f = f.replace('"', '\\"')
                f = f.replace("'", "\\'")

                runmagic = '%%run "%s"' % f
                source = """if 1:
    __iP__=get_ipython();
    __iP__.run_cell(%r); del(__iP__)""" % runmagic
                # run_line_magic only available in 0.13
            else:
                # regular code object - RunSelection.py should invoke this code path...
                source = """if 1: # Running a Code Object from IPyIDLE
    import marshal as __marshal
    exec(__marshal.loads(%r)); del __marshal""" % marshal.dumps(source)

        elif isinstance(source, (str, unicode)):
            if not store_history:
                # SubCode should invoke this codepath...
                source = """__iP__=get_ipython();__iP__.run_cell(%r); del(__iP__)""" % source
            else:
                # A string of the command from the interactive shell invokes this path...
                pass

        def do_exec_cb():
            self.beginexecuting()

        if do_exec:
            exec_callback = do_exec_cb
            finish_callback = self.endexecuting
        else:
            exec_callback = None
            def fcb():
                self.tkconsole.executing = 0
            finish_callback = fcb

        self.tkconsole.executing = 1 # console is executing
        ipyProxy.enqueue_execute(source, silent=not store_history,
                                 exec_callback=exec_callback,
                                 finish_callback=finish_callback)

        if not store_history:
            ipyProxy.enqueue_execute("""if 1:
    try:  # if pylab inline
        from IPython.zmq.pylab.backend_inline import flush_figures as __flush
        __flush(); del __flush
    except: pass""",
                                     silent=True,
                                     exec_callback=None,
                                     finish_callback=None)

    def getdebugger(self):
        pass

    def transfer_path(self, with_cwd=False):
        if with_cwd:        # Issue 13506
            path = ['']     # include Current Working Directory
            path.extend(sys.path)
        else:
            path = sys.path

        self.runcommand("""if 1:
        import sys as _sys
        _sys.path = %r
        del _sys
        \n""" % (path,))


class IPyIDLEShell(TerminalInteractiveShell):
    """A subclass of TerminalInteractiveShell that uses the 0MQ kernel"""
    _executing = False

    # The only reason this class exists is to access its input_splitter
    # and its prompt generating routines...

    def __init__(self, *args, **kwargs):
        self.km = kwargs.pop('kernel_manager')
        self.io = kwargs.pop('io')
        self.session_id = self.km.session.session
        super(IPyIDLEShell, self).__init__(*args, **kwargs)


    def init_io(self):
        stdin, stdout, stderr = self.io
        io = ipython_io
        io.stdout = stdout
        io.stdin = stdin
        io.stderr = stderr

    def init_completer(self):
        from IPython.core.completerlib import (module_completer,
                                               magic_run_completer, cd_completer)

        self.set_hook('complete_command', module_completer, str_key = 'import')
        self.set_hook('complete_command', module_completer, str_key = 'from')
        self.set_hook('complete_command', magic_run_completer, str_key = '%run')
        self.set_hook('complete_command', cd_completer, str_key = '%cd')


class Pager(tk.Toplevel):  #textView.py modified
    """A simple text viewer dialog for IDLE

    """
    def __init__(self, parent, title, raw_text):

        tk.Toplevel.__init__(self, parent)
        self.configure(borderwidth=5)

        self.geometry("=%dx%d+%d+%d" % (
            parent.winfo_width(),
            max([parent.winfo_height() - 40, 200]),
            parent.winfo_rootx() + 10,
            parent.winfo_rooty() + 10))

        self.bg = '#ffffff'
        self.fg = '#000000'

        self.CreateWidgets()
        self.title(title)
        self.protocol("WM_DELETE_WINDOW", self.Ok)
        self.parent = parent
        self.text.focus_set()
        self.bind('<Return>',self.Ok) #dismiss dialog
        self.bind('<Escape>',self.Ok) #dismiss dialog
        self.per = Percolator(self.text)
        self.ansi = AnsiColorDelegator()
        self.doc = PyShell.ModifiedUndoDelegator()

        self.per.insertfilter(self.ansi)
        self.per.insertfilter(self.doc)

        for code in ansi_colors:
            self.text.tag_config(code,
                            foreground=ansi_colors[code])

        self.text.insert(0.0, raw_text)
        self.apply_bindings()

        # get SearchBar working with this
        self.top = self
        self.sb = SearchBar(self)

        self.text.mark_set('iomark', 'end')
        self.text.mark_set('before_prompt', 'end')
        self.text.mark_set('insert', '1.0')



    def search(self):
        self.text.event_generate("<<find>>")


    def CreateWidgets(self):

        frameText = tk.Frame(self, relief=tk.SUNKEN, height=700)
        frameButtons = tk.Frame(self)
        self.buttonOk = tk.Button(frameButtons, text='Close',
                               command=self.Ok, takefocus=tk.FALSE)
        self.buttonSearch = tk.Button(frameButtons, text='Search /',
                               command=self.search, takefocus=tk.FALSE)

        self.scrollbarView = tk.Scrollbar(frameText, orient=tk.VERTICAL,
                                       takefocus=tk.FALSE, highlightthickness=0)
        width = idleConf.GetOption('main','EditorWindow','width')
        height = idleConf.GetOption('main', 'EditorWindow', 'height')

        text_options = {
                'name': 'text',
                'padx': 5,
                'wrap':tk.WORD,
                'highlightthickness':0,
                'fg':self.fg,
                'bg':self.bg,
                'width': width,
                'height': height}


        self.text = text = MultiCallCreator(tk.Text)(frameText, **text_options)
        fontWeight='normal'
        if idleConf.GetOption('main','EditorWindow','font-bold',type='bool'):
            fontWeight='bold'
        self.text.config(font=(idleConf.GetOption('main','EditorWindow','font'),
                idleConf.GetOption('main','EditorWindow','font-size'),
                fontWeight))


        self.scrollbarView.config(command=self.text.yview)
        self.text.config(yscrollcommand=self.scrollbarView.set)
        self.buttonSearch.pack(side=tk.LEFT)
        self.buttonOk.pack(side=tk.LEFT)
        self.scrollbarView.pack(side=tk.RIGHT,fill=tk.Y)
        self.text.pack(side=tk.LEFT,expand=tk.TRUE,fill=tk.BOTH)
        frameButtons.pack(side=tk.BOTTOM,fill=tk.X)
        frameText.pack(side=tk.TOP,expand=tk.TRUE,fill=tk.BOTH)

        # editwin mock (so SearchBar works)
        self.status_bar = frameButtons

    def Ok(self, event=None):
        self.destroy()

    def apply_bindings(self, keydefs=None):
        if keydefs is None:
            keydefs = Bindings.default_keydefs
        text = self.text
        text.keydefs = keydefs

        invalid = []
        for event, keylist in keydefs.items():
            if keylist:
                try:
                    text.event_add(event, *keylist)
                except tk.TclError as err:
                    invalid.append((event, keylist))
        text.event_add('<<find>>', '/')   # VIM key binding for search

#-------------------------------------
# The IDLE Extension
#-------------------------------------

EXT_NAME = 'IPyIDLE'

def get_cfg(cfg, type="bool", default=True):
    return idleConf.GetOption("extensions", EXT_NAME,
                         cfg, type=type, default=default)

def set_cfg(cfg, b):
    return idleConf.SetOption("extensions", EXT_NAME,
                      cfg,'%s' % b)




COMPLETE_CHARS = string.ascii_letters + string.digits + "_" + '.' + '/'

class OverBinding(object):
    """ class for replacing bindings of MultiCall-wrapped Widget """
    # Tkinter has no facility to recover the original Python function
    # bound to a Tk event. This is fundamentally a broken design.
    # Now, add on top of that broken design the MultiCall handler...

    def __init__(self, tkobj, basewidget=None):
        self.tkobj = tkobj
        if basewidget is None:
            raise Exception('Must specifiy a base widget class')
        self.basewidget = basewidget
        self.old = {}


    _tk_callback = r"""(?<=if {"\[)[\d]*[\S]*"""
    def _get_cb(self, cb):
        """ Parse out the TCL proc """
        # Tkinter .bind returns the TCL command that calls the internal CallWrapper
        # instance in the tkinter code. It needs to be parsed
        # to remove the actual callback...

        # For example, .bind may return
        # if {"[139690432888560callback %# %b %f %h %k %s %t %w %x %y %A %E %K %N %W %T %X %Y %D]" == "break"} break
        # when it ought to return 139690432888560callback

        m = re.search(self._tk_callback, cb)
        if m:
            cb = m.group()
        return cb


    def bind(self, event, newbind):
        cb = self.tkobj.bind(event)
        self.old[event]  = cb
        self.tkobj.bind(event, newbind)

    def call_original(self, event, tkev):
        """ Pass the event to the originally bound function. """

        tkobj = self.tkobj
        if event in self.old:
            if event.startswith('<<'):
                e = self._get_cb(self.old[event])
                # Assuming that the virtual event takes no arguments...
                tkobj.tk.call(e)
            else:
                func = tkobj.bind(event)
                tkobj.bind(event, self.old[event])
                tkobj.event_generate(event)
                tkobj.bind(event, func)
        else:
            tkobj.event_generate(event)

    def restore(self):
        # need to use basewidget because
        # Tkinter uses old-style classes in 2.x series,
        # so "super" doesn't work...
        # The purpose is to bypass MultiCall
        tkobj = self.tkobj
        old = self.old
        for virtual in old:
            cb = old[virtual]
            if virtual.startswith('<<'):
                cb = self._get_cb(cb)
            #print('Restoring: %r : %r' % (virtual, cb))
            self.basewidget.bind(tkobj, virtual, cb)

ipyList = []  # list of IPyIDLE instances

class IPyIDLE(object):
    menudefs = [('shell', [('!IPython Shell', '<<idleIPythonShell>>'),
                           ('!Allow IPython Kernel Restart', '<<idleIPythonAllowRestart>>'),
                           ('Adjust Kernel Arguments', '<<idleIPythonCmdLine>>'),
                           ])]

    def check_ipython(func):
        def f(self, *arg, **kw):
            if HAS_IPYTHON:
                return func(self, *arg, **kw)
            else:
                t = self.editwin.top
                tkMessageBox.showinfo('IPython Missing',
                                      'IPython not available',
                                      parent=t)
                self.editwin.setvar('<<idleIPythonShell>>', 0)
                self.editwin.setvar('<<idleIPythonAllowRestart>>', 0)
                return "break"
        return f


    def __init__(self, editwin):
        ipyList.append(self)
        # If IPython gets installed into the shell, then all open editors need
        # to be modified as well, hence the saving of IPyIDLE instances.

        self.text_binding = OverBinding(editwin.text, tk.Text)
        self._save_ps1 = None
        self._save_ps2 = None
        self._save_shell_title = None
        self._save_copyright = None
        self._save_squeezer = None

        self.first_load = True  # flag if shell is first starting and ipython needs to be loaded
        self.editwin = editwin
        self.console = editwin
        self.text = editwin.text

        if isinstance(editwin, PyShell.PyShell):
            self.is_shell = True
            self.text.bind('<<idleIPythonShell>>', self.toggle_IPython)
            self.text.bind('<<idleIPythonAllowRestart>>', self.toggle_restart)
            self.text.bind('<<idleIPythonCmdLine>>', self.adjust_command_line)
        else:
            self.is_shell = False

        if not HAS_IPYTHON:
            return

        self.last_codeline = ''

        # each editorwindow object gets an autocomplete window
        self.autocompletewindow = AutoCompleteWindow.AutoCompleteWindow(self.text)
        editwin.text.bind('<FocusIn>', self.focus_event, '+')


        enable = get_cfg('ipython', type="bool", default=True)
        if idlexMain.ipython_argv or idlexMain.ipython_connection_file:
            enable = True

        self.allow_restart = get_cfg('allow_restart', type="bool", default=True)
        if idlexMain.ipython_argv:
            enable = True
        self.use_ipython = enable

        if self.is_shell:
            if self.use_ipython:
                self.set_ipython_state(True)
            else:
                self.first_load = False  # not loading ipython on pyshell init
            self.set_restart_state(self.allow_restart)
        else:
            if self.use_ipython:
                for i in ipyList:
                    if i.is_shell:
                        self.install()
                        break

    def close(self):
        if self.is_shell:
            PyShell.ModifiedInterpreter = ModifiedInterpreter

            # restore IDLE's default event handlers
            # for the editors if shell is close
            self._uninstall_editors()

            ipyProxy.cleanup_connection_file()
            ipyProxy.stop_km()

        self.uninstall()

        if self in ipyList:
            ipyList.remove(self)
        else:
            print('IPY:', self)

    def focus_event(self, event=None):
        ipyProxy.active = self

    @check_ipython
    def toggle_IPython(self, ev=None):
        self.set_ipython_state(not self.use_ipython)

    def set_ipython_state(self, b=False):
        self.use_ipython = b
        set_cfg('ipython', '%s' % b)
        if b:
            self.install()
        else:
            self.uninstall()

        if self.is_shell:
            editwin = self.editwin
            try:
                editwin.setvar('<<idleIPythonShell>>', b)
            except Exception:
                print('Exception should not occur', file=sys.stderr)
                traceback.print_exc()

    @check_ipython
    def toggle_restart(self, ev=None):
        self.set_restart_state(not self.allow_restart)

    def set_restart_state(self, b=False):
        self.allow_restart = b
        set_cfg('allow_restart', '%s' % b)
        self.editwin.setvar('<<idleIPythonAllowRestart>>',  b)
        ipyProxy.allow_restart = b

    @check_ipython
    def adjust_command_line(self, event=None):
        current_argv = idlexMain.ipython_argv
        cf = idlexMain.ipython_connection_file
        args = ' '.join(current_argv)
        if cf:
            args += ' --existing %s' % cf

        while True:
            new_args = tkSimpleDialog.askstring('IPython Kernel Arguments',
                                          'Adjust the kernel start arguments:',
                                           parent=self.editwin.text,
                                           initialvalue=args
                                           )
            if new_args is None:
                idlexMain.ipython_argv = current_argv
                break
            else:
                new_argv = new_args.split()
                ipy_argv = idlexMain.handle_ipython_argv(new_argv)
                if new_argv:
                    # there should not be anything left in this:
                    tkMessageBox.showwarning('IDLE IPython',
                                             ('IDLE IPython does not support:\n' +
                                              ' '.join(new_argv)),
                                             parent=self.editwin.top)
                    args = new_args  # allow for repeat
                else:
                    if current_argv != ipy_argv:
                        ipyProxy.argv_changed = True
                    else:
                        ipyProxy.argv_changed = False
                    break

        if ipyProxy.argv_changed:
            restart = tkMessageBox.askyesno('IDLE IPython',
                                  ('Changes to the kernel will be applied on (re)start of kernel.\n\n' +
                                   'Do you want to start a new kernel?'),
                                            default=tkMessageBox.NO,
                                            parent=self.editwin.top)
            print('restart: %r %s' % (restart, type(restart)))
            if restart == True:
                if self.use_ipython:
                    self.editwin.interp.restart_subprocess()
                else:
                    self.set_ipython_state(True)


    def _install_editors(self):
        for i in ipyList:
            if not i.is_shell:
                i.install()

    def _uninstall_editors(self):
        for i in ipyList:
            if not i.is_shell:
                i.uninstall()

    def switch_message(self):
        if self.first_load:
            return
        hb = '=' * 10
        msg = '\n %(halfbar)s SWITCHING SHELL %(halfbar)s \n\n' % {'halfbar':hb}
        self.text.insert('end', msg)
        self.text.mark_set('iomark', 'end')


    def reset_shell(self):
        #print('reset_shell')
        e = self.editwin
        if e.reading:
            e.top.quit()
            e.reading = False
        if e.interp.rpcclt:
            e.interp.kill_subprocess()

        e.executing = False


    #------------------------------
    # UnInstall this instance
    #-----------------------------

    def uninstall(self):   # uninstall ipython and return to IDLE
        e = self.editwin

        self.text_binding.restore()

        s = self.editwin.extensions.get('CallTips', None)
        if s:
            try:
                self.text.bind('<<refresh-calltip>>', s.refresh_calltip_event)
            except Exception as err:
                print('Error restoring calltip binding: %r' % err)
                pass

        # Restore values
        if self.is_shell:
            closing = e.closing
            if not closing:   # switching
                self.reset_shell()
                self.switch_message()

            ipyProxy.stop_km()
            ipyProxy.restore_IDLE_history()
            self._uninstall_editors()
            ipyProxy.active_pyshell = None
            ipyProxy.calltipwindow = None

            if self._save_shell_title:
                PyShell.PyShell.shell_title = self._save_shell_title
            if self._save_copyright:
                PyShell.PyShell.COPYRIGHT = self._save_copyright
            if self._save_ps1 is not None:
                sys.ps1 = self._save_ps1
            if self._save_ps2 is not None:
                sys.ps2 = self._save_ps2
            PyShell.ModifiedInterpreter = ModifiedInterpreter

            s = self.editwin.extensions.get('Squeezer', None)
            if s and self._save_squeezer:
                s._MAX_NUM_OF_LINES = self._save_squeezer

            if not closing:  # then switching
                e.interp._poll_cancel()
                e.interp = ModifiedInterpreter(e)
                e.console.write('\n')
                e.per.removefilter(self.ansi)
                e.history = self._save_history
                e.executing = False
                e.begin()


    #---------------------------
    # Install into this instance
    #---------------------------

    def install(self):

        e = self.editwin

        # Save existing values
        if self.is_shell:
            self.text.mark_set('before_prompt', '1.0')
            self.reset_shell()
            ipyProxy._reset()
            self.switch_message()
            ipyProxy.active_pyshell = self.editwin
            ipyProxy.active = self
            ipyProxy.start_km()
            e.executing = 0
            self._save_shell_title = PyShell.PyShell.shell_title
            self._save_copyright = PyShell.PyShell.COPYRIGHT

            if self._save_ps1 is None:
                self._save_ps1 = getattr(sys, 'ps1', None)
                self._save_ps2 = getattr(sys, 'ps2', None)


            sys.ps1 = '>>> '     # temporary
            sys.ps2 = '... '     # temporary

            self._save_undo = e.undo

            e.interp = BridgeInterpreter(e)  # replace the existing interpreter
            PyShell.PyShell.shell_title = "IPython Shell"
            PyShell.ModifiedInterpreter = BridgeInterpreter

        def delay_install():
            # the purpose of delay_install is if "install_shell" is called
            # as part of the init routine for pyshell

            if self.is_shell:
                e.closing = False
                self._install_editors()
                self._save_history = e.history

                # Add Ansi Color Delegator
                self.ansi = AnsiColorDelegator()
                e.per.insertfilter(self.ansi)
                self.config_ansi_colors()

                s = self.editwin.extensions.get('Squeezer', None)
                if s:
                    self._save_squeezer = s._MAX_NUM_OF_LINES
                    s._MAX_NUM_OF_LINES = 10000

                e.console.write('\n')


                if not self.first_load:
                    ipyProxy.switching = True  # flag to avoid double launching kernels
                    e.begin()
                    ipyProxy.switching = False  # flag to avoid double launching kernels
                e.executing = False
                self.first_load = False  # no longer the case that the shell opened and needs ipython
                e.text.mark_set('before_prompt', 'iomark linestart')
                e.text.mark_gravity("before_prompt", "left")

            #self.text.configure(wrap="word")  # Uncomment to enable word-wrapping like QtConsole
            self.text_binding.bind('<Tab>', self.tab_event)
            if self.is_shell:
                self.text_binding.bind('<Control-Return>', self.control_enter_callback)
                self.text_binding.bind('<<clear-window>>', self.clear_window)
            self.text_binding.bind('<<toggle-debugger>>', self.toggle_debugger)
            self.text_binding.bind('<<refresh-calltip>>', self.refresh_calltip_event)

        self.text.after(1, delay_install)

    def config_ansi_colors(self):
        """ Configure the ansi color tags for the .text widget """
        text = self.text
        for code in ansi_colors:
            text.tag_config(code,
                            foreground=ansi_colors[code])

    def refresh_calltip_event(self, event=None):
        # this is a hack to make calltip hiding work with
        # CallTips.py refresh_calltip_event
        ctw = ipyProxy.calltipwindow
        if ctw:
            ctw.hidetip()
            self.text.event_generate('<<force-open-calltip>>')

    def tab_event(self, event=None):
        # AutoCompleteWindow event
        text = self.text

        lineno, col = sp(text.index('insert'))  # where the cursor is

        # Determine the start of the code for context
        if self.is_shell:
            IOMARK = 'iomark'
        else:
            IOMARK = 'insert linestart'

        ioline, iocol = sp(text.index(IOMARK)) # where the start of code is
        if lineno > ioline:
            scol = 0
            codecol = col
        else:
            scol = iocol
            codecol = col - iocol

        buf = text.get(IOMARK, 'insert')  # full cell for context
        codeline = text.get(jn(lineno, scol), 'insert') # the actual line of code


        # Assume that we will do a completion, unless it is not needed
        do_complete = True

        if not codeline.strip():
            if self.is_shell:
                if text.compare('insert', '>', 'iomark'):
                    do_complete = False   # So TAB works in multiline input
                else:
                    # To mimic the behavior of the IPython shell,
                    # do the completion when the prompt is blank
                    pass
            else:
                do_complete = False  # blank code line, not needed

        elif not self.is_shell:
            if codeline[-1] not in COMPLETE_CHARS:
                do_complete = False

        # Check if the window is already open
        if self.autocompletewindow and self.autocompletewindow.is_active():
            if codeline == self.last_codeline:
                # send twice to select it - logic of IDLE's ACW
                self.autocompletewindow.keypress_event(event)
                self.autocompletewindow.keypress_event(event)
                return "break"

        if do_complete:
            msg_id = ipyProxy.kernel_manager.shell_channel.complete(
                '',             # text
                codeline,       # line
                codecol,        # cursor_pos
                buf,            # block
                )
            self.last_codeline = codeline
        else:
            # call original binding
            self.text_binding.call_original('<Tab>', event)
        return "break"

    def toggle_debugger(self, event=None):
        tkMessageBox.showinfo('IDLE IPython',
                              'IDLE Debugger is not compatible with IPython (yet). Try using %pdb',
                              parent=self.editwin.top)
        self.editwin.setvar('<<toggle-debugger>>', 0)
        return "break"

    def control_enter_callback(self, event=None):
        # only in shell
        e = self.editwin
        if e.executing or e.reading:
            self.text_binding.call_original('<Control-Return>', event)
            return "break"

        if self.text.compare('insert', '>=', 'iomark'):
            e.newline_and_indent_event(event)
            return "break"

        self.text_binding.call_original('<Control-Return>', event)
        return "break"

    def clear_window(self, event):
        # forget all images
        ipyProxy.clear_shell_images()
        self.text_binding.call_original('<<clear-window>>', event)
