import time

import modal

stub = modal.Stub("example-parallel")


@stub.function
def step1(word):
    time.sleep(2)
    print("step1 done")
    return word


@stub.function
def step2(number):
    time.sleep(1)
    print("step2 done")
    if number == 0:
        raise ValueError("custom error")
    return number


if __name__ == "__main__":
    with stub.run() as app:
        # Start running a function and return a handle to its result.
        word_call = step1.submit("foo")
        number_call = step2.submit(2)

        # Print "foofoo" after 2 seconds.
        print(word_call.get() * number_call.get())

        # Alternatively, use `modal.gather(...)` as a convenience wrapper,
        # which returns an error if either call fails.
        results = modal.functions.gather(step1.submit("bar"), step2.submit(4))
        assert results == ["bar", 4]

        # Raise exception after 2 seconds.
        try:
            modal.functions.gather(step1.submit("bar"), step2.submit(0))
        except ValueError as exc:
            assert str(exc) == "custom error"
