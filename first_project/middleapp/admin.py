from django.contrib import admin


from middleapp.models import *


class mdl_stringAdmin(admin.ModelAdmin):
    list_display = ["id","uid","name"]
admin.site.register(mdl_string , mdl_stringAdmin)

class application_cmsAdmin(admin.ModelAdmin):
    list_display = ["id","action","acknowledgementNumber","departmentId","serviceId"]
admin.site.register(application_cms , application_cmsAdmin)


class encrypted_cmsAdmin(admin.ModelAdmin):
    list_display = ["id","enc_data"]
admin.site.register(encrypted_cms , encrypted_cmsAdmin)
