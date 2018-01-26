class TYPE:
    @staticmethod
    def is_dict(o):
        return type(o) is dict

    @staticmethod
    def is_list(o):
        return type(o) is list

    @staticmethod
    def is_str(o):
        return type(o) is str

    @staticmethod
    def is_int(o):
        return type(o) is int

    @staticmethod
    def is_bool(o):
        return type(o) is bool

    @staticmethod
    def is_tuple(o):
        return type(o) is tuple

    @staticmethod
    def is_none(o):
        return o is None
