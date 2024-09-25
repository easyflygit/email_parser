from django.contrib import admin
from .models import EmailAccount, ParsingRule


@admin.register(EmailAccount)
class EmailAccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'server', 'port')


@admin.register(ParsingRule)
class ParsingRuleAdmin(admin.ModelAdmin):
    list_display = ('email_account', 'excel_column', 'db_column')

