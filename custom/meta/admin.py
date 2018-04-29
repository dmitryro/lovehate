from django.contrib import admin
from custom.meta.models import MetaProp
from custom.meta.models import ContactMetaProp
from custom.meta.models import ProfileMetaProp

################################
#  Register with Django Admin  #
################################

class MetaPropAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['title','keywords','description','h1header','content','author','analytics']}),)
    list_display = ('id','title','keywords','description','h1header','content','author','analytics')
    list_editable = ('title','keywords','description','h1header','content','author','analytics')

    class Meta:
         verbose_name = 'SEO Property'
         verbose_name_plural = 'SEO Properties'


class ContactMetaPropAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': ['title','address1','address2','from_email','to_email','city','zip','state','phone','fax','hours','days','note']}),)
    list_display = ('id','title','address1','address2','city','zip','state','phone','fax','hours','days','note')
    list_editable = ('title','address1','address2','city','zip','state','phone','fax','hours','days','note')



class ProfileMetaPropAdmin(admin.ModelAdmin):
    fields = ('title','email','from_email','to_email','to_email_secondary','to_email_third','smtp_server','smtp_port','user_name','password','message')
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(ProfileMetaPropAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'message':
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield

admin.site.register(MetaProp,MetaPropAdmin)
admin.site.register(ContactMetaProp)
admin.site.register(ProfileMetaProp)

