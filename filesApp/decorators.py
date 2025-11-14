from django.http import HttpResponseForbidden

def user_passes_test_with_path(test_func):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            path = kwargs.get("path")  # URL 패스 가져오기

            if not test_func(user, path):
                return HttpResponseForbidden("권한이 없습니다.")

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator