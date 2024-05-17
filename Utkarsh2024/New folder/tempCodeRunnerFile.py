
def a():
    print("hello {}".format(threading.get_native_id()))


def b():
    print("hello {}".format(threading.get_native_id()))
    

a()