from parameters import Parameter

def first(*args):
    func, sequence = args
    if sequence:
        if func:
            for x in sequence:
                if func(x):
                    return x
        else:
            return sequence[0]

class ModelOptions(object):

    def __init__(self, options=None):
        self.all_parameters = []
        self.create_parameters = []
        self.read_parameters = []
        self.update_parameters = []
        self.delete_parameters = []
        # Set default options
        self.controller = '/'
        self.requires_multipart = False
        # Override options by copying old options over
        if options is not None:
            for attr in dir(options):
                setattr(self, attr, getattr(options, attr))

class ModelMetaclass(type):

    def __new__(cls, name, bases, attrs):

        if 'Meta' in attrs:
            meta = ModelOptions(attrs.pop('Meta'))
        else:
            meta = ModelOptions()

        for key, value in attrs.iteritems():
            if isinstance(value, Parameter):
                cls.add_attribute(key, value, meta, attrs)

        attrs['_meta'] = meta

        return super(ModelMetaclass, cls).__new__(cls, name, bases, attrs)

    @classmethod
    def add_attribute(cls, name, parameter, meta, attrs):

        parameter.local_name = name

        meta.all_parameters.append(parameter)

        for rest in ['create', 'read', 'update', 'delete']:
            if getattr(parameter, rest) == True:
                meta_prop = '%s_parameters' % rest
                params_group = getattr(meta, meta_prop)
                params_group.append(parameter)

        if parameter.remote_name is None:
            parameter.remote_name = name

        attrs[name] = parameter.default

class Model(object):
    __metaclass__ = ModelMetaclass

    def _get_parameters_for_fields(self, parameters, *additional_locals):
        if parameters:
            parameters = parameters[:]
        else:
            parameters = []
        other_parameters = [first(lambda parameter: parameter.local_name == name, self._meta.all_parameters) for name in additional_locals]
        parameters.extend(other_parameters)
        return self._serialize([parameter.to_param(getattr(self, parameter.local_name)) for parameter in parameters])

    def _serialize(self, parameters):
        ps = []
        for p in parameters:
            if isinstance(p, (list, tuple)):
                p = self.serialize(p)
            if p is not None:
                ps.append(p)
        return '&'.join(ps)

    def parameters(self, *local_parameters):
        return self._get_parameters_for_fields(None, *local_parameters)

    def all_parameters(self, *additional_locals):
        return self._get_parameters_for_fields(self._meta.all_parameters, *additional_locals)

    def create_parameters(self, *additional_locals):
        return self._get_parameters_for_fields(self._meta.create_parameters, *additional_locals)

    def read_parameters(self, *additional_locals):
        return self._get_parameters_for_fields(self._meta.read_parameters, *additional_locals)

    def update_parameters(self, *additional_locals):
        return self._get_parameters_for_fields(self._meta.update_parameters, *additional_locals)

    def delete_parameters(self, *additional_locals):
        return self._get_parameters_for_fields(self._meta.delete_parameters, *additional_locals)

    def __str__(self):
        return self.__class__.__name__
    def __repr__(self):
        return '%s()' % (self.__class__.__name__,)
    def __unicode__(self):
        return unicode(str(self))
