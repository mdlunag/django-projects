# your_app/management/commands/create_financial_records.py

from django.core.management.base import BaseCommand
from django.db.models import Q

from datetime import date
from dateutil.relativedelta import relativedelta

from moneitas.models import RecurrentRecord, FinancialRecord

class Command(BaseCommand):
    help = 'Create FinancialRecord instances based on RecurrentRecord entries'

    def handle(self, *args, **options):
        today = date.today()

        recurrent_records = RecurrentRecord.objects.filter(
            Q(date_from__lte=today),
            Q(date_to__gte=today) | Q(date_to__isnull=True),
            Q(next_create_date=today) | Q(next_create_date__isnull=True),
            Q(last_created_date__lt=today) | Q(last_created_date__isnull=True)
        )

        print(f"Found {len(recurrent_records)} Financial Record(s)")

        for recurrent_record in recurrent_records:
            cadence_day = recurrent_record.cadence_position
            next_create_date = recurrent_record.next_create_date
            new_next_create_date = False

            if recurrent_record.cadence_type == 'monthly':
                if not next_create_date:
                    next_create_date = date(today.year, today.month, cadence_day)

                if next_create_date < today or next_create_date == today:
                    new_next_create_date = next_create_date + relativedelta(months=1)

            elif recurrent_record.cadence_type == 'weekly':
                if not next_create_date:
                    days_difference = cadence_day - today.weekday()+1
                    next_create_date = today + relativedelta(days=days_difference)

                if next_create_date < today or next_create_date == today:
                    new_next_create_date = next_create_date + relativedelta(weeks=1)

            if not new_next_create_date:
                new_next_create_date = next_create_date

            # Create FinancialRecord if it's time
            if next_create_date == today:
                created = FinancialRecord.objects.create(
                    type=recurrent_record.type,
                    amount=recurrent_record.amount,
                    date=today,
                    label=recurrent_record.label,
                    comment=recurrent_record.comment,
                    user=recurrent_record.user,
                    method=recurrent_record.method,
                    income_paid=False
                )

                print(f"Created Financial record {created}")

                # Update last_created_date to the current date
                recurrent_record.last_created_date = today

            recurrent_record.next_create_date = new_next_create_date
            recurrent_record.save()

        self.stdout.write(self.style.SUCCESS('Successfully created FinancialRecords'))

