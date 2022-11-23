class SetPrevUrlOnGetRequests:
    def __init__(self, get_response):
        self.get_response = get_response
        self.prev_post = 0
        # One-time configuration and initialization.

    def __call__(self, request):
        if not request.session.get('prev_url'):
            request.session['prev_url'] = '/'

        if request.method == 'POST':
            self.prev_post = 1

        elif request.method == 'GET':
            if self.prev_post:
                self.prev_post = 0
            else:
                request.session['prev_url'] = request.META.get('HTTP_REFERER', '/')

        response = self.get_response(request)

        return response
