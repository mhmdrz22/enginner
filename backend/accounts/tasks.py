from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_email_task(self, recipients, subject, message):
    """
    Celery task for sending emails asynchronously.
    
    Args:
        recipients: List of email addresses
        subject: Email subject
        message: Email body (can be Markdown)
    """
    try:
        logger.info(f"Sending email to {len(recipients)} recipients")
        
        sent_count = 0
        failed_emails = []
        
        for recipient in recipients:
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[recipient],
                    fail_silently=False,
                )
                sent_count += 1
                logger.info(f"Email sent successfully to {recipient}")
            except Exception as e:
                logger.error(f"Failed to send email to {recipient}: {str(e)}")
                failed_emails.append(recipient)
        
        result = {
            'sent_count': sent_count,
            'failed_count': len(failed_emails),
            'failed_emails': failed_emails,
            'total': len(recipients)
        }
        
        logger.info(f"Email task completed: {result}")
        return result
        
    except Exception as exc:
        logger.error(f"Email task failed: {str(exc)}")
        # Retry after 60 seconds
        raise self.retry(exc=exc, countdown=60)
