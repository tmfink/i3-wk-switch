#!/usr/bin/env python

"""Emulates xmonad's workspace switching behavior in i3 and sway"""

# pylint: disable=no-member,invalid-name,too-many-function-args

from __future__ import print_function

import argparse
import logging
import sys
from pprint import pformat
import time

import i3ipc

i3 = i3ipc.Connection()

LOG = logging.getLogger('i3-wk-switch')


def setup_logger(level, log_file=None, log_stderr=True):
    """Initializes logger with debug level"""
    LOG.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(levelname)s] [%(asctime)s] %(message)s')

    def add_logger(channel):
        """Configure logger channel"""
        channel.setLevel(level)
        channel.setFormatter(formatter)
        LOG.addHandler(channel)

    if log_file is not None:
        channel = logging.FileHandler(log_file)
        add_logger(channel)

    if log_stderr:
        channel = logging.StreamHandler(sys.stderr)
        add_logger(channel)

    # Eliminate warning: No handlers could be found for logger
    LOG.addHandler(logging.NullHandler())


def get_focused_workspace():
    """Get workspace that is currently focused"""
    actives = [wk for wk in i3.get_workspaces() if wk.focused]
    assert len(actives) == 1
    return actives[0]


def get_active_outputs():
    """Returns outputs (monitors) that are active"""
    return [outp for outp in i3.get_outputs() if outp.active]


def get_workspace(num):
    """Returns workspace with num or None of it does not exist"""
    want_workspace_cands = [wk for wk in i3.get_workspaces()
                            if wk.num == num]
    assert len(want_workspace_cands) in [0, 1]

    if not want_workspace_cands:
        return None

    return want_workspace_cands[0]


def switch_workspace(num):
    """Switches to workspace number"""
    i3.command('workspace %d' % num)


def move_workspace(s):
    """Move current workspace to output"""
    i3.command('move workspace to output %s' % s)


def swap_visible_workspaces(wk_a, wk_b):
    """Swaps two workspaces that are visible"""
    switch_workspace(wk_a.num)
    i3.command('move workspace to output %s' % wk_b.output)
    switch_workspace(wk_b.num)
    i3.command('move workspace to output %s' % wk_a.output)


def change_workspace(num):
    """
    Switches to workspace num like xmonad.

    Always sets focused output to workspace num. If the workspace is on
    another output, then the workspaces are "shifted" among the outputs.
    """

    # Allow for string or int type for argument
    num = int(num)
    focused_workspace = get_focused_workspace()
    original_output = focused_workspace.output

    LOG.debug(
        'Switching to workspace:%s on output:%s, display: %s:',
        num, focused_workspace.output, pformat(focused_workspace, indent=2))

    # Check if already on workspace
    if int(focused_workspace.num) == num:
        LOG.debug('Already on correct workspace')
        return

    # Get workspace we want to switch to
    want_workspace = get_workspace(num)
    if want_workspace is None:
        LOG.debug('Switching to workspace because it does not exist, i3 will create it')
        switch_workspace(num)
        return

    LOG.debug('Want workspace:%s', pformat(want_workspace, indent=2))

    # Save workspace originally showing on want_workspace's output
    other_output = [outp for outp in get_active_outputs()
                    if outp.name == want_workspace.output][0]
    LOG.debug('Other_output=%s', pformat(other_output, indent=2))
    other_workspace = [wk for wk in i3.get_workspaces()
                       if wk.name == other_output.current_workspace][0]
    LOG.debug('Other workspace:%s', pformat(other_workspace, indent=2))

    # Check if wanted workspace is on focused output
    if focused_workspace.output == want_workspace.output:
        LOG.debug('Wanted workspace already on focused output, '
                  'switching as normal')
        switch_workspace(num)
        return

    # Check if wanted workspace is on other output
    if not want_workspace.visible:
        LOG.debug('Workspace to switch to is hidden')

        # Switch to workspace on other output
        switch_workspace(num)
        move_workspace(original_output)
        time.sleep(.15)
        LOG.debug('Setting focus to %s', original_output)
        i3.command('focus output %s' % original_output)
        return

    LOG.debug('Wanted workspace is on other output')

    # Wanted workspace is visible, so swap workspaces
    swap_visible_workspaces(want_workspace, focused_workspace)

    # Focus other_workspace
    switch_workspace(other_workspace.num)

    # Focus on wanted workspace
    time.sleep(.15)
    LOG.debug('Setting focus to %s', original_output)
    i3.command('focus output %s' % original_output)


def main():
    "Main"
    parser = argparse.ArgumentParser(
        description='Switch i3 workspaces in the style of xmonad')
    parser.add_argument('workspace', metavar='WORKSPACE_NUM', type=int,
                        help='Workspace number to which to switch')
    parser.add_argument('--log-file', '-l', metavar='LOG_FILE',
                        help='Path to file to which to log')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Log to stderr')
    args = parser.parse_args()

    setup_logger(
        logging.DEBUG, log_file=args.log_file, log_stderr=args.verbose)
    change_workspace(args.workspace)


if __name__ == '__main__':
    main()
