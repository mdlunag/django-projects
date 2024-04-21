from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from datetime import datetime

class Command(BaseCommand):
    help = 'Send an email with an attachment using Django management command'

    def handle(self, *args, **options):
        # Your email details
        formatted_date = datetime.now().strftime('%Y-%m-%d')
        subject = f'Moneitas Backup From {formatted_date}'
        message = """
        Hi,

        Please find attached the moneitas database backup. If you want to restore it at some point, just run:

        python manage.py loaddata -i <filename>

        Moneitas Team
        """
        html_message = """
        <p>Hi,
         <br><br>
        Please find attached the moneitas database backup. If you want to restore it at some point, just run:
         <br><br>

        <i>python manage.py loaddata -i <filename> </i>

        <br><br>
        Regards,
        <br>
        <strong>Moneitas Team</strong>
        </p>
        """
        from_email = 'moneitas@no-reply.com'
        recipient_list = ['maria.delunag@gmail.com']

        # Create an EmailMessage instance
        email = EmailMessage(subject, html_message, from_email, recipient_list)

        # Attach a file (replace 'path/to/your/file.txt' with the actual file path)
        file_path = '/home/mdelunag/backups/moneitas_backup_' + datetime.now().strftime('%Y%m%d') + '.json'
        print(file_path)
        email.attach_file(file_path)
        email.content_subtype = "html"  # Main content is now text/html


        # Send the email
        email.send()
