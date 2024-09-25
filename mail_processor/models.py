from django.db import models


class EmailAccount(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=255)
    server = models.CharField(max_length=255)
    port = models.IntegerField()


class ParsedFile(models.Model):
    upload_date = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=255)
    data = models.JSONField()


class ParsingRule(models.Model):
    email_account = models.ForeignKey(EmailAccount,
                                      related_name='parsing_rule',
                                      on_delete=models.CASCADE)
    excel_column = models.IntegerField(help_text="Номер колонки в Excel")
    db_column = models.CharField(max_length=255, help_text="Поле в БД")
