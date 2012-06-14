
class EZRestError(StandardError):
    pass

class HostError(EZRestError):
    pass

class HostHTTPError(HostError):
    pass

class HostURLError(HostError):
    pass

class ParameterError(EZRestError):
    pass

class ParameterValidationError(EZRestError):
    pass
