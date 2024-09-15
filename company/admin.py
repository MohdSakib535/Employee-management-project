from django.contrib import admin
from company.models import Manager,PerformanceReview,Project

# Register your models here.
admin.site.register(Manager)
admin.site.register(PerformanceReview)
admin.site.register(Project)
