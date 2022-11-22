from django.contrib import admin


from middleapp.models import *


class cms_application_Admin(admin.ModelAdmin):
    list_display = ["id","applicationId","acknowledgementNumber","departmentId","serviceId" , "apiKey"]
admin.site.register(cms_application , cms_application_Admin)


class serviceAdmin(admin.ModelAdmin):
    list_display = ["id","serviceId" , "serviceName" ,"apiKey", "departmentId" , "departmentName"]
admin.site.register(service , serviceAdmin)

admin.site.register(Invalid_CMS_Application)
