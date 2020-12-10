from django.contrib import admin
from .models import User, Patient, State, City
from .models import Vendor, AvailableServices, VendorUser, Chaperone


class ConstantValue(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', )


admin.site.register(Vendor)
admin.site.register(Chaperone)
admin.site.register(AvailableServices)
admin.site.register(User, ConstantValue)
admin.site.register(Patient)
admin.site.register(State)
admin.site.register(City)
admin.site.register(VendorUser, ConstantValue)
