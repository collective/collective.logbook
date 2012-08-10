

class ErrorTestView(object):
    """
    Raise some error for testing purposes.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        """

        """
        raise RuntimeError("collective.logbook test error")
