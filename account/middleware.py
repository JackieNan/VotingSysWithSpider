from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages


class AccountCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user  
        if user.is_authenticated:
            if user.user_type == '1':  # Admin
                if modulename == 'voting.views':
                    error = True
                    if request.path == reverse('fetch_ballot'):
                        pass
                    else:
                        messages.error(
                            request, "你没有访问此资源的权限")
                        return redirect(reverse('adminDashboard'))
            elif user.user_type == '2':  # Voter
                if modulename == 'administrator.views':
                    messages.error(
                        request, "你没有访问此资源的权限")
                    return redirect(reverse('voterDashboard'))
            else:  # 上述情况都没有，访问登录界面
                return redirect(reverse('account_login'))
        else:
            # 如果路径与登录或验证有关
            if request.path == reverse('account_login') or request.path == reverse('account_register') or modulename == 'django.contrib.auth.views' or request.path == reverse('account_login'):
                pass
            elif modulename == 'administrator.views' or modulename == 'voting.views':
                # 游客访问投票页面或者管理员页面，需要登录
                messages.error(
                    request, "你需要登录以执行此操作")
                return redirect(reverse('account_login'))
            else:
                return redirect(reverse('account_login'))
