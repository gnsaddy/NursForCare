from django.contrib import admin
from .models import User, Patient, State, City
from .models import VendorService, AvailableServices, VendorUser, Chaperone


class VendorList(admin.ModelAdmin):
    list_display = ('email', 'vendor_name', 'phone', 'state', 'city', 'vendor', 'created_at', 'days_active')
    list_display_links = ('email',)
    search_fields = ('email', 'vendor_name')
    list_per_page = 50
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at',)
    fields = ('first_name', 'last_name', 'vendor_name', 'email', 'password',
              'phone', 'state', 'city', 'vendor', 'active', 'last_login')
    actions = ('set_vendor_to_unavailable', 'set_vendor_to_available')

    def get_ordering(self, request):
        if request.user.is_superuser:
            return 'vendor_name', 'created_at'
        return 'vendor_name', 'created_at'

    def set_vendor_to_unavailable(self, request, queryset):
        count = queryset.update(vendor=False)
        self.message_user(request, f'{count} vendor(s) is/are now unavailable')

    set_vendor_to_unavailable.short_description = 'Mark Vendor Service unavailable'

    def set_vendor_to_available(self, request, queryset):
        count = queryset.update(vendor=True)
        self.message_user(request, f'{count} vendor(s) is/are now available')

    set_vendor_to_available.short_description = 'Mark Vendor Service available'


class ChaperoneList(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone', 'attendant', 'created_at', 'days_active')
    list_display_links = ('email',)
    search_fields = ('email', 'first_name' + 'last_name')
    list_per_page = 50
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at',)
    fields = ('first_name', 'last_name', 'email', 'password',
              'phone', 'attendant', 'active', 'last_login')
    actions = ('set_attendant_to_unavailable', 'set_attendant_to_available')

    def get_ordering(self, request):
        if request.user.is_superuser:
            return 'first_name', 'created_at'
        return 'first_name', 'created_at'

    def set_attendant_to_unavailable(self, request, queryset):
        count = queryset.update(attendant=False)
        self.message_user(request, f'{count} attendant(s) is/are now unavailable')

    set_attendant_to_unavailable.short_description = 'Mark attendant unavailable'

    def set_attendant_to_available(self, request, queryset):
        count = queryset.update(attendant=True)
        self.message_user(request, f'{count} attendant(s) is/are now available')

    set_attendant_to_available.short_description = 'Mark attendant available'


class CityList(admin.ModelAdmin):
    list_display = ('state', 'name')
    list_display_links = ('state', 'name')
    search_fields = ('state__name', 'name')
    list_per_page = 50


class PatientList(admin.ModelAdmin):
    list_display = ('holder', 'patient', 'mobile', 'address', 'city', 'state', 'bookingDate', 'days_active')
    list_display_links = ('patient', 'mobile')
    search_fields = ('holder__name', 'patient', 'mobile')
    list_per_page = 50
    date_hierarchy = 'bookingDate'

    def get_ordering(self, request):
        if request.user.is_superuser:
            return 'patient', 'bookingDate'
        return 'patient', 'bookingDate'


class VendorServiceList(admin.ModelAdmin):
    list_display = ('name', 'service', 'available', 'mobile', 'address', 'city', 'state')
    list_display_links = ('name', 'service')
    search_fields = ('service__name', 'name', 'mobile', 'address', 'state', 'city', 'pin')
    list_per_page = 50

    def get_ordering(self, request):
        if request.user.is_superuser:
            return 'name', 'available'
        return 'name', 'available'


admin.site.register(VendorService, VendorServiceList)
admin.site.register(Chaperone, ChaperoneList)
admin.site.register(AvailableServices)
admin.site.register(Patient, PatientList)
admin.site.register(State)
admin.site.register(City, CityList)
admin.site.register(VendorUser, VendorList)


class UserList(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'attendant', 'vendor', 'staff', 'admin', 'created_at')
    list_display_links = ('email',)
    search_fields = ('email', 'first_name' + 'last_name')
    list_per_page = 50
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at',)

    def get_ordering(self, request):
        if request.user.is_superuser:
            return 'first_name', 'created_at'
        return 'first_name', 'created_at'


admin.site.register(User, UserList)
