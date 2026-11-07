"""Bloqueos de archivo no bloqueantes compatibles con Windows y Unix."""
import errno
import os

if os.name == 'nt':
    import msvcrt
else:
    import fcntl


def acquire_nonblocking_lock(file):
    if os.name == 'nt':
        file.seek(0, os.SEEK_END)
        if file.tell() == 0:
            file.write(b'\0')
            file.flush()
        file.seek(0)
        try:
            msvcrt.locking(file.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError as exc:
            if exc.errno in (errno.EACCES, errno.EAGAIN, errno.EDEADLK):
                raise BlockingIOError from None
            raise
    else:
        fcntl.flock(file, fcntl.LOCK_EX | fcntl.LOCK_NB)
