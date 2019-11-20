from django.contrib import admin

# Register your models here.

from .models import Event,User

# from django.contrib.auth.models import Group
# from django.contrib.auth.models import User as admin_User

# admin.site.unregister(Group)
# admin.site.unregister(admin_User)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_name',)
    search_fields = ['user_name',]

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display =('CREATE_TIME','DISTRICT_NAME','STREET_NAME','COMMUNITY_NAME','EVENT_TYPE_NAME',
                   'MAIN_TYPE_NAME','SUB_TYPE_NAME','DISPOSE_UNIT_NAME','EVENT_SRC_NAME','EVENT_PROPERTY_NAME')
    list_filter = ['CREATE_TIME','DISTRICT_NAME','STREET_NAME','COMMUNITY_NAME','EVENT_TYPE_NAME',
                   'MAIN_TYPE_NAME','SUB_TYPE_NAME','DISPOSE_UNIT_NAME','EVENT_SRC_NAME','EVENT_PROPERTY_NAME']
    list_per_page = 200
    search_fields = ['CREATE_TIME','DISTRICT_NAME','STREET_NAME','COMMUNITY_NAME','EVENT_TYPE_NAME',
                   'MAIN_TYPE_NAME','SUB_TYPE_NAME','DISPOSE_UNIT_NAME','EVENT_SRC_NAME','EVENT_PROPERTY_NAME']
    date_hierarchy = "CREATE_TIME"

admin.site.site_header = '政府大数据实时治理分析系统后台管理'
admin.site.site_title = '政府大数据实时治理分析系统后台管理'