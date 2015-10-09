import pickle


def read_object_from(filename, object_type):
    # pickle からオブジェクとを読み取ります、欲しい object_type とマッチしているかをチェックします
    # object_type　がマッチしなければ、空の object_type を return します

    try:
        read_object = pickle.load(open(filename, 'rb'))
        assert type(read_object) is object_type
        return read_object

    except FileNotFoundError:
        return object_type()

    except AssertionError:
        print('         The object read from', filename, 'is not a', object_type, '!')
        return object_type()

    except Exception:
        return object_type()

