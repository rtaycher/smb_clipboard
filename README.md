# smb_clipboard

smb_clipboard is a simple file sharing based syncing clipboard Manager

### Motivation
Years ago I needed to share snippets across many computers I was working on
that were all on the same network drive. I came up with this idea and started but didn't
finish it in C++.

I realized it might be easier in python so I slapped together something and it seemed to work.

### Dependencies:
 1. Python3.6+
 2. Pyside2

    (if you have trouble pip install PySide2==5.11.2 I had a bit of trouble
with Pyside2 5.12 version)

# Using it

Pick a Local Area Network file-sharing directory to save every bit of text you copy to.
On a different computer pick that same file sharing directory.
It should sync both ways (although delete may currently be a little wonky)

### Tested platforms & where it or may not work
Tested on Windows with UNC `\\server\share\folder` type filepaths

It doesn't work with `smb:server/share/folder paths since those aren't exposed to the filesystem

Theoretically it should work on OSX by using the folder smb is mounted to under `/Volumes`

Theoretically it should work on Linux by using the folder smb is mounted to under `/run/user/<uid>/gvfs`/`/$XDG_RUNTIME_DIR/gvfs` if using Gnome
or if mounted to a particular dir on the cmdline (KDE's kio doesn't seem to actually mount it anywhere)

Theoretically it might work with other networked mounts like SSHFS

