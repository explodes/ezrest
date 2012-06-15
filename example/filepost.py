from ezrest import host, model, parameter

class ResponseModel(model.Model):
    ''' Model built to handle a response itself '''
    def response(self, response):
        print 'TODO: Handle the response'

class MozillaClientHostController(host.HostController):

    def get_request_headers(self, method, url, get_data=None, post_data=None, instance=None):
        d = super(MozillaClientHostController, self).get_request_headers(method, url, get_data=get_data, post_data=post_data, instance=instance)
        d['User-agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:13.0) Gecko/20100101 Firefox/13.0'
        d['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        return d

class ResponseModelHostController(host.HostController):

    def handle_response(self, instance, response):
        if isinstance(instance, ResponseModel):
            instance.response(response)
        return instance

class GoogleHostController(MozillaClientHostController, ResponseModelHostController):

    def __init__(self):
        super(GoogleHostController, self).__init__('http://www.google.com')

class FauxPost(ResponseModel):

    query = parameter.TextParameter(remote_name='q', read=True, create=True)
    upload = parameter.FileParameter(create=True)

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
    search = FauxPost('pypi ezrest')
    f = parameter.File(data='\x00\x44\x44\x09', file_name='fake.jpg')
    print f, repr(f)
    search.upload = f
    ghc.create(search) # updates the search with the faux results after the response is received

    print search.parameters('occurrences_of_the_word_pypi').to_get() # Serialize our results for the fun of it
    print search.occurrences_of_the_word_pypi # print out the raw value of our results


