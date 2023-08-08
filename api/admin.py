from django.contrib import admin

from api.models import BusinessHours, Report, Status, Store, Timezone


@admin.register(BusinessHours)
class BusinessHoursAdmin(admin.ModelAdmin):
    pass


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    pass


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    pass


@admin.register(Timezone)
class TimezoneAdmin(admin.ModelAdmin):
    pass
