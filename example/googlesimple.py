#!/usr/bin/env python
from ezrest import host, model, parameter

class ResponseModel(model.Model):
    ''' Model built to handle a response itself '''
    def response(self, response):
        print 'TODO: Handle the response'

class GoogleHostController(host.HostController):

    def __init__(self):
        ''' Shortcut for init, simply init with google as our host destination '''
        super(GoogleHostController, self).__init__('http://www.google.com')

    def handle_response(self, instance, response):
        ''' Use our ResponseModels to handle the responses '''
        if isinstance(instance, ResponseModel):
            instance.response(response)
        return super(GoogleHostController, self).handle_response(instance, response)

    def get_request_headers(self, method, url, get_data=None, post_data=None, instance=None):
        ''' Build request headers to simulate a request from Firefox '''
        d = super(GoogleHostController, self).get_request_headers(method, url, get_data=get_data, post_data=post_data, instance=instance)
        d['User-agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:13.0) Gecko/20100101 Firefox/13.0'
        d['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        return d

class GoogleSearch(ResponseModel):

    query = parameter.TextParameter(remote_name='q', read=True)
    occurrences_of_the_word_ezrest = parameter.IntegerParameter()

    class Meta:
        controller = '/search'

    def __init__(self, query):
        self.query = query

    def response(self, response):
        self.occurrences_of_the_word_ezrest = response.read().count('ezrest')

if __name__ == '__main__':
    ghc = GoogleHostController()
    search = GoogleSearch('ezrest')
    ghc.read(search) # updates the search with the faux results after the response is received
    print search.parameters('occurrences_of_the_word_ezrest').to_get() # Serialize our results for the fun of it
    print search.occurrences_of_the_word_ezrest                        # Print out the value updated from the response


