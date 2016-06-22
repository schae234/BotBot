import io
import string
import random
import subprocess
import pytest

from botbot import fileinfo as fi

def test_hasher():
    test, result = io.BytesIO(b'hello, world!\n'), '910c8bc73110b0cd1bc5d2bcae782511'
    assert fi._hash(test) == result

def test_file_hasher(tmpdir):
    prev = tmpdir.chdir()
    testfile = tmpdir.join('test.txt')
    testfile.write('hello, world!\n')

    assert fi.get_file_hash('test.txt') == '910c8bc73110b0cd1bc5d2bcae782511' # Expected
    prev.chdir()

def test_arbitrary_hash():
    """Let's try the hasher with a lot of hashes, say 75 maybe?"""
    all_ascii = string.ascii_letters + string.digits
    for i in range(100):
        inbytes = ''.join(random.choice(all_ascii) for _ in range(500)).encode()
        testhash = fi._hash(io.BytesIO(inbytes))

        echo = subprocess.Popen(('/bin/echo', '-e', '-n', inbytes), stdout=subprocess.PIPE)
        syshash = subprocess.check_output('md5sum', stdin=echo.stdout).decode().split(' ')[0] # eww
        assert syshash == testhash

def test_importance_detection(tmpdir):
    prev = tmpdir.chdir()

    #C Create some files
    samtestfile = tmpdir.join('test.sam')
    samtestfile.write('')
    bamtestfile = tmpdir.join('test.bam')
    bamtestfile.write('')
    regtestfile = tmpdir.join('test.txt')
    regtestfile.write('')

    assert fi.FileInfo(samtestfile.basename)['important']
    assert fi.FileInfo(bamtestfile.basename)['important']
    assert not fi.FileInfo(regtestfile.basename)['important']

def test_reader_reads_correct_number_of_bytes():
    # Test both below and above 128 bytes
    for i in range(1, 2 ** 10):
        b = io.BytesIO(('a' * i).encode())
        tb = 0
        for r in fi._reader(b):
            tb += len(r)
        assert tb == i
