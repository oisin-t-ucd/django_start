from django.contrib.auth.mixins import (  # Import UserPassesTestMixin here
    UserPassesTestMixin,
)


class AuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
