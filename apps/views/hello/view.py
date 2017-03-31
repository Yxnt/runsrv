from . import hello


@hello.route('/')
def hello():
    return "hello"
