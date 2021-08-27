from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from .models import Student

import os
from io import BytesIO, SEEK_SET
import qrcode


@receiver(post_save, sender=Student)
def generate_qrcode_post_save(sender, instance, created, **kwargs):
    if created or not instance.qrcode:
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=5
        )
        qr.add_data(instance.enrollment_no)
        qr.make(fit=True)

        path = os.path.join(settings.MEDIA_ROOT, "qrcode", f"{instance.enrollment_no}_id.png")

        if os.path.exists(path):
            os.remove(path)

        buffer = BytesIO()

        img = qr.make_image(fill="black", back_color="white")
        img.save(buffer, format="PNG")

        buffer.seek(SEEK_SET)

        instance.qrcode.save(f"{instance.enrollment_no}_id.png", buffer)
