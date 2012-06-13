from ezrest import parameters
from ezrest.host import HostController
from ezrest.models import Model

class ResponseModel(Model):
    ''' Model built to handle a response itself '''
    def response(self, response):
        print 'TODO: Handle the response'

class MozillaClientHostController(HostController):

    def get_request_headers(self, method, url, get=None, post=None, instance=None):
        d = super(MozillaClientHostController, self).get_request_headers(method, url, get=get, post=post)
        d['User-agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:13.0) Gecko/20100101 Firefox/13.0'
        d['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        return d

class ResponseModelHostController(HostController):

    def handle_response(self, instance, response):
        if isinstance(instance, ResponseModel):
            instance.response(response)
        return instance

class GoogleHostController(MozillaClientHostController, ResponseModelHostController):

    def __init__(self):
        super(GoogleHostController, self).__init__('http://www.google.com')

class GoogleSearch(ResponseModel):

    query = parameters.TextParameter(remote_name='q', read=True)
    occurrences_of_the_word_pypi = parameters.IntegerParameter()

    def __init__(self, query):
        self.query = query

    class Meta:
        controller = '/search'

    def response(self, response):
        self.occurrences_of_the_word_pypi = response.read().count('pypi')

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.query)

if __name__ == '__main__':
    ghc = GoogleHostController()
    search = GoogleSearch('pypi ezrest')

    ghc.read(search) # updates the search with the faux results after the response is received

    print search.parameters('occurrences_of_the_word_pypi')
    print search.occurrences_of_the_word_pypi


