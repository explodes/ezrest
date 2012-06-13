'''
Created on Jun 12, 2012

@author: evan
'''
import urllib

import exceptions

class _UnsetParameter(object):
    def __call__(self):
        return self
    def __str__(self):
        return '<Unset Parameter>'
    def __repr__(self):
        return 'UnsetParameter'
    def __unicode__(self):
        return unicode(str(self))
    def __eq__(self, other):
        return isinstance(other, _UnsetParameter)

UnsetParameter = _UnsetParameter()

class Parameter(object):

    def __init__(self, remote_name=None, default=UnsetParameter, create=False, read=False, update=False, delete=False):
        self.local_name = None
        self.remote_name = remote_name
        self.create = create
        self.read = read
        self.update = update
        self.delete = delete
        self.default = default

    def escape(self, value):
        return urllib.quote(str(value))

    def validate(self, value):
        if value == UnsetParameter:
            raise exceptions.ParameterError('UnsetParameter %r cannot be serialized.' % self.local_name)

    def to_param(self, value):
        ''' Return parameterized key-value pairs. Raise ParameterError on validation error. Can return a list of lists of n lists of parameterized key-value pairs. '''
        if value is None:
            return None
        self.validate(value)
        escaped = self.escape(value)
        return '%s=%s' % (self.remote_name, escaped)

    def __str__(self):
        return '%s %s' % (self.__class__.__name__, self.local_name)

    def __repr__(self):
        return '%s(remote_name=%r, default=%r, create=%r, read=%r, update=%r, delete=%r)' % (self.__class__.__name__, self.remote_name, self.default, self.create, self.read, self.update, self.delete)


class TextParameter(Parameter):
    pass


class PHPArrayParameter(Parameter):

    def to_param(self, value):
        if value is None:
            return None
        if not isinstance(value, (list, tuple)):
            self.validate(value)
            escaped = self.escape(value)
            return '%s[]=%s' % (self.remote_name, escaped)
        else:
            params = []
            for item in value:
                self.validate(item)
                escaped = self.escape(item)
                params.append('%s[]=%s' % (self.remote_name, escaped))
            return params

class IntegerParameter(Parameter):

    def escape(self, value):
        value = super(IntegerParameter, self).escape(value)
        if value[-1] == 'L':
            return value[:-1]
        return value

    def validate(self, value):
        super(IntegerParameter, self).validate(value)
        if not isinstance(value, (int, long)):
            raise exceptions.ParameterError('IntegerParameter %r has a non-integer value %s.' % (self.local_name, value))
