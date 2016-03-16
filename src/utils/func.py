""" Creates an anonymous lambda function from expression string """


def make_function(variable_names, expression, environment=globals()):
    """ Returns lambda given by expression and variables """
    arguments = ','.join([variable for variable in variable_names])
    statement = '(lambda {}: {})'.format(arguments, expression)

    return eval(statement, environment)  # pylint: disable=eval-used
