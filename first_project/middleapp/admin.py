from django.contrib import admin


from middleapp.models import mdl_string


class mdl_stringAdmin(admin.ModelAdmin):
    list_display = ["id","uid","name"]
admin.site.register(mdl_string , mdl_stringAdmin)