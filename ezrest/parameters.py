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

    def clean(self, value):
        self.validate(value)
        return self.escape(value)

    def escape(self, value):
        return urllib.quote(str(value))

    def validate(self, value):
        if value == UnsetParameter:
            raise exceptions.ParameterError('UnsetParameter %r cannot be serialized.' % self.local_name)

    def to_param(self, value):
        ''' Return parameterized key-value pairs. Raise ParameterError on validation error. Can return a list of lists of n lists of parameterized key-value pairs. 
        Multi-values return LIST of two-tuples.
        Single values return two-tuples.'''
        if value is None:
            return None
        clean = self.clean(value)
        return (self.remote_name, clean)

    @property
    def requires_multipart(self):
        return False

    def __str__(self):
        return '%s %s' % (self.__class__.__name__, self.local_name)

    def __repr__(self):
        return '%s(remote_name=%r, default=%r, create=%r, read=%r, update=%r, delete=%r)' % (self.__class__.__name__, self.remote_name, self.default, self.create, self.read, self.update, self.delete)


class TextParameter(Parameter):
    pass

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


class UnnumberedArrayParameter(Parameter):
    ''' Turns a list into foo[]=bar foo[]=baz foo[]=etc '''

    def to_param(self, value):
        if value is None:
            return None
        params = []
        if not isinstance(value, (list, tuple)):
            param = self.to_index_param(0, value)
            params.append(param)
        else:
            for index, item in enumerate(value):
                param = self.to_index_param(index, item)
                params.append(param)
        return params

    def to_index_param(self, index, value):
        clean = self.clean(value)
        param_name = '%s[]' % (self.remote_name)
        return (param_name, clean)

class UnnumberedIntegerArrayParameter(UnnumberedArrayParameter, IntegerParameter):
    pass

class NumberedArrayParameter(UnnumberedArrayParameter):
    ''' Turns a list into foo[0]=bar foo[1]=baz foo[2]=etc or 
    foo[1]=bar foo[2]=baz foo[3]=etc depending on the first_index
    init parameter'''

    def __init__(self, first_index=0, **kwargs):
        super(UnnumberedArrayParameter, self).__init__(**kwargs)
        self.first_index = first_index

    def to_index_param(self, index, value):
        clean = self.clean(value)
        param_name = '%s[%i]' % (self.remote_name, (self.first_index + index))
        return (param_name, clean)

class NumberedIntegerArrayParameter(NumberedArrayParameter, IntegerParameter):
    pass
