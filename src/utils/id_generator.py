""" Module for tracking unique str => int """


class IdGenerator(object):  # pylint: disable=too-few-public-methods
    """ Utility class for mapping unique strings to int ids """

    def __init__(self):
        self.ids = {}
        self.next_id = 1

    def get_id(self, string):
        """ Returns the id for a given string """
        if string in self.ids:
            return self.ids[string]
        else:
            sid = self.next_id
            self.ids[string] = sid

            self.next_id += 1

            return sid

ID_GENERATOR = IdGenerator()
