import pytest
import requests


@pytest.fixture()
def stateful_handler(request):
    # same check for dynamically supplied parameters
    if hasattr(request, "param"):
        responses = request.param
    else:
        responses = ["OK", "BAD"]

    # Create a generator out of sequence of respnoses
    val_generator = (v for v in responses)

    # Handler returns next item in generator, and state is maintained until fixture is destroyed
    def my_handler(req):
        return next(val_generator)

    return my_handler


@pytest.fixture
def httpserver_dynamic(httpserver, stateful_handler):
    # https://pytest-httpserver.readthedocs.io/en/latest/howto.html#using-custom-request-handler
    httpserver.expect_request("/test", method="GET").respond_with_handler(
        stateful_handler
    )
    return httpserver


@pytest.fixture
def url_dynamic(httpserver_dynamic):
    return httpserver_dynamic.url_for("/test")


# Test that the handler steps through default generator items on successive calls
def test_handler(stateful_handler):
    assert stateful_handler(None) == "OK"
    assert stateful_handler(None) == "BAD"
    with pytest.raises(
        StopIteration
    ):  # because the handler is popping the next item from a generator, it's raising a different exception when it hits the end
        stateful_handler(None)


# Test that the handler steps through provided generator items on successive calls
@pytest.mark.parametrize(
    "stateful_handler", [["HELLO", "WORLD", "GOODBYE"]], indirect=True
)
def test_handler_parameterized(stateful_handler):
    assert stateful_handler(None) == "HELLO"
    assert stateful_handler(None) == "WORLD"
    assert stateful_handler(None) == "GOODBYE"
    with pytest.raises(
        StopIteration
    ):  # because the handler is popping the next item from a generator, it's raising a different exception when it hits the end
        stateful_handler(None)


# Test that the stateful handler works with httpserver
def test_confirm_sequence(httpserver_dynamic, url_dynamic):
    r = requests.get(url_dynamic)
    assert r.status_code == 200
    assert r.text == "OK"

    r = requests.get(url_dynamic)
    assert r.status_code == 200
    assert r.text == "BAD"

    r = requests.get(url_dynamic)
    with pytest.raises(StopIteration):
        httpserver_dynamic.check()


# Test that the stateful handler works with httpserver
@pytest.mark.parametrize("stateful_handler", [["HELLO", "WORLD"]], indirect=True)
def test_confirm_sequence_dynamic(httpserver_dynamic, url_dynamic):
    r = requests.get(url_dynamic)
    assert r.text == "HELLO"

    r = requests.get(url_dynamic)
    assert r.text == "WORLD"

    r = requests.get(url_dynamic)
    with pytest.raises(StopIteration):
        httpserver_dynamic.check()
