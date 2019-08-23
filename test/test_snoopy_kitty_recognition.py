from snoopy_kitty_recognition import snoopy_kitty_recognition


def test_fib() -> None:
    assert snoopy_kitty_recognition.fib(0) == 0
    assert snoopy_kitty_recognition.fib(1) == 1
    assert snoopy_kitty_recognition.fib(2) == 1
    assert snoopy_kitty_recognition.fib(3) == 2
    assert snoopy_kitty_recognition.fib(4) == 3
    assert snoopy_kitty_recognition.fib(5) == 5
    assert snoopy_kitty_recognition.fib(10) == 55
