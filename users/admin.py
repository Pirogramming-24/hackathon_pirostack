from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     # list_display = ('user','role','nickname','name','phone_number','password')
#     list_display = ('name','role')
#     fields = ('user', 'role', 'name', 'nickname', 'phone_number',)

#     @admin.display(boolean=True, description='운영진 여부(staff)')
#     def is_staff_status(self,obj):
#         return obj.user.is_staff
    
# 1. '끼워넣을' 화면 정의 (인라인)
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False # 프로필만 따로 삭제 못하게 방지
    verbose_name_plural = '추가 프로필 정보'

# 2. 원래 있던 유저 관리 화면에 위에서 만든 '인라인'을 추가
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    # 유저 목록에서 바로 보고 싶은 항목들
    list_display = ('username', 'password', 'is_staff')

# 3. 원래 장고가 쓰던 User 설정은 지우고, 내가 새로 만든 UserAdmin을 등록
admin.site.unregister(User)
admin.site.register(User, UserAdmin)