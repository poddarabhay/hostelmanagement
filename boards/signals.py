from django.db.models.signals import pre_delete
from boards.models import Student
from django.dispatch import receiver

@receiver(pre_delete, sender=Student)
def delete_student_adjust(sender,instance,using, **kwargs):
    if instance.room !=None:
        instance.room.asize+=1
        instance.hostel.asize+=1
        if instance.room.status==0:
            instance.room.status+=1
        instance.room.save()
        instance.hostel.save()
