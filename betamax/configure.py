from .cassette import Cassette


class Configuration(object):

    """This object acts as a proxy to configure different parts of Betamax.

    You should only ever encounter this object when configuring the library as
    a whole. For example:

    .. code::

        with Betamax.configure() as config:
            config.cassette_library_dir = 'tests/cassettes/'
            config.default_cassette_options['record_mode'] = 'once'
            config.default_cassette_options['match_requests_on'] = ['uri']
            config.define_cassette_placeholder('<URI>', 'http://httpbin.org')
            config.preserve_exact_body_bytes = True

    """

    # REVIEW: This method makes it seem like configurations are being handled in
    # some clean way. But with the exception of the define_cassette_placeholder()
    # helper method, this is just directly modifying global variables:
    # - Configuration.CASSETTE_LIBRARY_DIR
    # - Cassette.default_cassette_options
    # And the helper method is only a very light wrapper around one of those.
    # Why bother with a class / context manager? Why not access the globals
    # directly / move the helper method into a module-level function?
    #
    # Possible guesses:
    # - Docstrings for properties.
    # - Being able to override __setattr__ to use simple assignment to do more
    #   complex operations.
    # - It looks cool (context managers!).
    # - Configuration / Cassette don't need to be exposed in __init__.py.
    # - Can instantiate and put a copy on a Betamax instance.
    #   - But then modifying the attributes of what appears to be an instance
    #     variable, will actually change global settings.

    CASSETTE_LIBRARY_DIR = 'vcr/cassettes'

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def __setattr__(self, prop, value):
        if prop == 'preserve_exact_body_bytes':
            # REVIEW: Why does the value get ignored?
            self.default_cassette_options[prop] = True
        else:
            super(Configuration, self).__setattr__(prop, value)

    @property
    def cassette_library_dir(self):
        """Retrieve and set the directory to store the cassettes in."""
        return Configuration.CASSETTE_LIBRARY_DIR

    # REVIEW: Good use of @property.setter
    @cassette_library_dir.setter
    def cassette_library_dir(self, value):
        Configuration.CASSETTE_LIBRARY_DIR = value

    # REVIEW: Why not make a copy of Cassette.default_cassette_options as an
    # instance variable? Why modify it?
    @property
    def default_cassette_options(self):
        """Retrieve and set the default cassette options.

        The options include:

        - ``match_requests_on``
        - ``placeholders``
        - ``re_record_interval``
        - ``record_mode``
        - ``preserve_exact_body_bytes``

        Other options will be ignored.
        """
        return Cassette.default_cassette_options

    @default_cassette_options.setter
    def default_cassette_options(self, value):
        Cassette.default_cassette_options = value

    def define_cassette_placeholder(self, placeholder, replace):
        """Define a placeholder value for some text.

        This also will replace the placeholder text with the text you wish it
        to use when replaying interactions from cassettes.

        :param str placeholder: (required), text to be used as a placeholder
        :param str replace: (required), text to be replaced or replacing the
            placeholder
        """
        self.default_cassette_options['placeholders'].append({
            'placeholder': placeholder,
            'replace': replace
        })
