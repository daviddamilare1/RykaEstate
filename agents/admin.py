from django.contrib import admin
from agents.models import *








class AgentSpecializationInline (admin.TabularInline):
    model = AgentSpecialization



class AgentAdmin(admin.ModelAdmin):
    inlines = [AgentSpecializationInline]
    list_display = ['agent_image', 'full_name', 'email', 'verified', 'is_available']
    list_editable = ['verified', 'is_available']
    








admin.site.register(Agent, AgentAdmin)
admin.site.register(BrokerAgent)
admin.site.register(Notification)
admin.site.register(AgentSpecialization)
admin.site.register(AgentReview)