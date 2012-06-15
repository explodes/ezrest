======================================
`ezrest` Python REST wrapper framework
======================================

**Project Goal**

This goal of this project is to supply a framework that makes writing REST API wrappers much faster.

**Code Goal**

Ensuring extensibility is the most important part. There are a million different API's and they are ALL different.
In no way will it be possible to make a framework that can wrap all API's. This framework will target API's that
conform to the most BASIC of REST protocols while supplying addons that conform the most advanced.

:Basic Features:
   The most basic features include CRUD.

:Advanced:
    The most advanced feature include different actions based on HTTP response codes.

README CONTENTS
---------------

:Package Contents:
    A summary of the package and the modules within

:Example Usage:
    A basic example used to search google

PACKAGE CONTENTS
----------------

:`example`:
    Contains examples.

:`example.google`:
    An example app for querying google, written intentionally complicated to demonstrate proper OOP techniques.

:`ezrest`:
    The framework layer

:`ezrest.model`:
    Base Model class and Metaclass details

:`ezrest.parameter`:
    Parameter class and subclasses.

:`ezrest.host`:
    Contains the simplest HostController. You can subclass it to suit your needs, or use it right out of the box. 

:`ezrest.exceptions`:
    Exception objects used in the app. All exceptions thrown must extend EZRestError.

:`tests`:
    Unit tests

EXAMPLE USAGE
-------------

This example uses REST to query Google under the /search controller.

This could all be replaced with

``urllib.urlopen('http://google.com/search?q=ezrest').read().count('ezrest')``

(Except that Google doesn't like requests from unknown clients, the appropriate headers are added below)

::

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

    $python testcase.py
    occurrences_of_the_word_ezrest=88
    88

The concept here is that you can create a model and supply attributes that get sent out with the requests.

After a Host is set up, it is just a matter of creating models.

Notice in GoogleSearch,

``query = parameter.TextParameter(remote_name='q', read=True)``

This could be rewritten as:

``q = parameter.TextParameter(read=True)``

But in the interest of legibility, the `local_name` is `query.`

In other models, we could have attributes like:

``id = parameter.IntegerParameter(read=True, create=True, update=True, delete=True)``

Which indicates that the parameter is to be send out with all of those host request types.

``occurrences_of_the_word_ezrest = parameter.IntegerParameter()`` is a plain parameter. Since it is not used in the API, we could have simply made it an instance variable.  However, ``print search.parameters('occurrences_of_the_word_ezrest').to_get()`` would then not print out serialized attributes and we wouldn't have had as much fun as we did!

