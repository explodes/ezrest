import base64
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
        return (self.remote_name, clean, self.content_type(value), self.content_transfer_encoding(value), self.content_disposition(value))

    def requires_multipart(self, value):
        return False

    def content_type(self, value):
        return 'text/plain'

    def content_transfer_encoding(self, value):
        return None

    def content_disposition(self, value):
        return 'form-data; name="%s"' % self.remote_name

    def __str__(self):
        return '%s %s' % (self.__class__.__name__, self.local_name)

    def __repr__(self):
        copy_vars = self._copy_vars()
        var_tuples = []
        for item in copy_vars.iteritems():
            var_tuples.append('%s=%r' % item)
        init_values = ', '.join(var_tuples)
        return '%s(%s)' % (self.__class__.__name__, init_values)

    def _copy_vars(self):
        return dict(
            remote_name=self.remote_name,
            default=self.default,
            create=self.create,
            read=self.read,
            update=self.update,
            delete=self.delete,
        )


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
                name, val = self.to_index_param(index, item)
                params.append((name, val, self.content_type, self.content_transfer_encoding, self.content_disposition))
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

    def _copy_vars(self):
        d = super(NumberedArrayParameter, self)._copy_vars()
        d['first_index'] = self.first_index
        return d

class NumberedIntegerArrayParameter(NumberedArrayParameter, IntegerParameter):
    pass

class File(object):

    def __init__(self, data=None, file_name=None, content_type='application/octet-stream'):
        self.data = data
        self.file_name = file_name
        self.content_type = content_type

    @property
    def base64(self):
        if hasattr(self.data, 'read'):
            text = self.data.read()
            if hasattr(self.data, 'seek'):
                self.data.seek(0)
        else:
            text = self.data
        return base64.b64encode(text)

    def __str__(self):
        return 'File %s' % (self.file_name)

    def __repr__(self):
        if self.data is None:
            data_str = None
        else:
            data_str = '<Omitted %s chars>' % len(self.data)
        return '%s(data=%s, file_name=%r, content_type=%r)' % (self.__class__.__name__, data_str, self.file_name, self.content_type)

class FileParameter(Parameter):

    def escape(self, value):
        if value:
            return value.base64

    def validate(self, value):
        if not isinstance(value, File):
            raise exceptions.ParameterValidationError('%s is not a File.' % value)
        super(FileParameter, self).validate(value)

    def requires_multipart(self, value):
        return bool(value)

    def content_type(self, value):
        return value.content_type

    def content_transfer_encoding(self, value):
        return 'base64'

    def content_disposition(self, value):
        file_name = value.file_name() if callable(value.file_name) else value.file_name
        return 'form-data; name="%s"; filename="%s"' % (self.remote_name, file_name)


