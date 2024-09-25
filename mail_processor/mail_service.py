import poplib
from email import parser
from email.policy import default
from django.core.files.base import ContentFile
import logging
from .models import EmailAccount, ParsedFile


logger = logging.getLogger(__name__)


def fetch_emails():
    logger.info("Начало проверки почты")
    try:
        accounts = EmailAccount.objects.all()
        for account in accounts:
            server = poplib.POP3_SSL(account.server, account.port)
            server.user(account.email)
            server.pass_(account.password)
            messages = [server.retr(i) for i in range(1, len(server.list()[1]) + 1)]
            server.quit()

            for msg in messages:
                raw_message = b"\n".join(msg[1])
                email_message = parser.BytesParser(policy=default).parsebytes(raw_message)
                for part in email_message.iter_attachments():
                    if part.get_content_type() in ['application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']:
                        file_data = part.get_payload(decode=True)
                        file_name = part.get_filename()
                        content_file = ContentFile(file_data, file_name)
                        handle_excel_file(content_file)


def handle_excel_file(file):
    # Используем pandas для парсинга файла
    import pandas as pd
    df = pd.read_excel(file)

    # Валидация данных (проверка на отсутствие пропущенных значений)
    if df.isnull().values.any():
        raise ValueError("Найдены пропущенные значения в Excel-файле")

    # Пример: расчет сумм и средних значений
    sum_value = df['excel_column'].sum()
    mean_value = df['excel_column'].mean()

    # Сохранение данных и метрик в БД
    ParsedFile.objects.create(file_name=file.name, data=df.to_dict())

def handle_file(file):
    if file.name.endswith('.xlsx'):
        df = pd.read_excel(file)
    elif file.name.endswith('.csv'):
        df = pd.read_csv(file)
    else:
        raise ValueError('Неподдерживаемый формат файла')

