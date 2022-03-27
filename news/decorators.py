from django.http import HttpResponse

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.groups.exists():
                group = request.user.groups.all()
                for g in group:
                    if g.name in allowed_roles:
                        return view_func(request, *args, **kwargs)
                    else:
                        return HttpResponse('Not authorized')
            else:
                return HttpResponse('Not authorized')
        return wrapper_func
    return decorator