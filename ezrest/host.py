import time
import urllib2

import exceptions

class HostController(object):

    def __init__(self, host_name):
        self.host_name = host_name

    ## { CREATE

    def create(self, instance, *additional_locals):
        kwargs = self.get_create_kwargs(instance, *additional_locals)
        method = self.get_create_method(instance)
        url = self.get_create_url(instance, instance._meta.controller)
        return self.request(instance, method, url, **kwargs)

    def get_create_method(self, instance):
        return 'GET'

    def get_create_kwargs(self, instance, *additional_locals):
        params = instance.create_parameters(*additional_locals)
        return dict(post=params)

    def get_create_url(self, instance, controller):
        return self.get_controller_url(controller)

    ## { READ

    def read(self, instance, *additional_locals):
        kwargs = self.get_read_kwargs(instance, *additional_locals)
        method = self.get_read_method(instance)
        url = self.get_read_url(instance, instance._meta.controller)
        return self.request(instance, method, url, **kwargs)

    def get_read_method(self, instance):
        return 'GET'

    def get_read_kwargs(self, instance, *additional_locals):
        params = instance.read_parameters(*additional_locals)
        return dict(get=params)

    def get_read_url(self, instance, controller):
        return self.get_controller_url(controller)

    ## { UPDATE

    def update(self, instance, *additional_locals):
        kwargs = self.get_update_kwargs(instance, *additional_locals)
        method = self.get_update_method(instance)
        url = self.get_update_url(instance, instance._meta.controller)
        return self.request(instance, method, url, **kwargs)

    def get_update_method(self, instance):
        return 'PUT'

    def get_update_kwargs(self, instance, *additional_locals):
        params = instance.update_parameters(*additional_locals)
        return dict(post=params)

    def get_update_url(self, instance, controller):
        return self.get_controller_url(controller)

    ## { DELETE

    def delete(self, instance, *additional_locals):
        kwargs = self.get_delete_kwargs(instance, *additional_locals)
        method = self.get_delete_method(instance)
        url = self.get_delete_url(instance, instance._meta.controller)
        return self.request(instance, method, url, **kwargs)

    def get_delete_method(self, instance):
        return 'DELETE'

    def get_delete_kwargs(self, instance, *additional_locals):
        params = instance.delete_parameters(*additional_locals)
        return dict(post=params)

    def get_delete_url(self, instance, controller):
        return self.get_controller_url(controller)

    ## { REQUEST

    def get_controller_url(self, controller):
        return '%s%s' % (self.host_name, controller)

    def get_request_headers(self, method, url, get_data=None, post_data=None, instance=None):
        length = len(post_data) if post_data else 0
        headers = {'Content-length' : length}
        return headers

    def request(self, instance, method, url, get=None, post=None):
        response = self.raw_request(method, url, get=get, post=post, instance=instance)
        return self.handle_response(instance, response)

    def raw_request(self, method, url, get=None, post=None, instance=None):
        if get:
            get = get.to_get()
            url = '%s?%s' % (url, get)

        headers = {}

        if post:
            if post.requires_multipart:
                print 'MULTIPART'
                boundary = self.create_multipart_boundary()
                post = post.to_multipart(boundary)
                headers['MIME-Version'] = '1.0'
                headers['Content-Type'] = 'multipart/mixed; boundary=%s' % boundary
            else:
                print 'NON-MULTIPART'
                post = post.to_post()

        new_headers = self.get_request_headers(method, url, get_data=get, post_data=post, instance=instance)
        headers.update(**new_headers)

        print 'RAW REQUEST: URL:', url
        print 'RAW REQUEST: METHOD:', method
        print 'RAW REQUEST: GET:', get
        print 'RAW REQUEST: POST:', post
        print 'RAW REQUEST: HEADERS:'
        for d in headers.iteritems():
            print '\t%s: %s' % d

        request = urllib2.Request(url, data=post, headers=headers)
        request.get_method = lambda: method

        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError, error:
            response_error = exceptions.HostHTTPError('%s: %s' % (error, error.read()))
            raise response_error
        except urllib2.URLError, error:
            request_error = exceptions.HostURLError(error)
            raise request_error

        return response

    def handle_response(self, instance, response):
        return instance

    def create_multipart_boundary(self):
        return 'MIMEMULTIPARTBOUNDARY%sMIMEMULTIPARTBOUNDARY' % (int(time.time()))






