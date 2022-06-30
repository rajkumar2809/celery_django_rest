from django.contrib import admin


from middleapp.models import *


class mdl_stringAdmin(admin.ModelAdmin):
    list_display = ["id","uid","name"]
admin.site.register(mdl_string , mdl_stringAdmin)

class cms_application_2_Admin(admin.ModelAdmin):
    list_display = ["id","acknowledgementNumber","departmentId","serviceId"]
admin.site.register(cms_application_2 , cms_application_2_Admin)


class encrypted_cmsAdmin(admin.ModelAdmin):
    list_display = ["id","enc_data"]
admin.site.register(encrypted_cms , encrypted_cmsAdmin)



class serviceAdmin(admin.ModelAdmin):

    list_display = ["id","serviceId" , "serviceName" ,"apiKey", "departmentId" , "departmentName"]
admin.site.register(service , serviceAdmin)
