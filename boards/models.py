from django.db import models
# Create your models here.

class Hostels(models.Model):
    gender_male="m"
    gender_female="f"
    gender_other="o"
    gender_choices=(
        (gender_male,'male'),
        (gender_female,'female'),
        (gender_other,'other'),
    )
    gender=models.CharField(max_length=1,choices=gender_choices)
    year_choice=(
        (1,'First'),
        (2,'Second'),
        (3,'Third'),
        (4,'Fourth'),
    )
    year=models.PositiveIntegerField(choices=year_choice,default=1)
    hname=models.CharField(max_length=50,unique=True,primary_key=True)
    size=models.PositiveIntegerField(null=False)
    asize=models.PositiveIntegerField(null=False)
    class Meta:
        verbose_name_plural="Hostels"
        verbose_name="Hostel"
    def __str__(self):
        return self.hname

class Hostel(models.Model):
    roomn=models.PositiveIntegerField(null=False)
    size=models.PositiveIntegerField(null=False)
    asize=models.PositiveIntegerField(null=False)
    status_choice=(
        (0,'Full'),
        (1,'Unavailable'),
        (2,'Blocked'),
        (3,'Available'),
    )
    status=models.PositiveIntegerField(choices=status_choice,default=3)
    floor=models.PositiveIntegerField(null=False)
    hname=models.ForeignKey(Hostels, related_name='hosteldetails', on_delete=models.CASCADE, null=False)
    class Meta:
        unique_together=("hname","roomn")
        verbose_name_plural="Rooms"
        verbose_name="Room"

    def __str__(self):
        return 'Room '+str(self.roomn)

class Student(models.Model):
    usn=models.CharField(max_length=10, unique=True,primary_key=True)
    lname=models.CharField(max_length=30);
    fname=models.CharField(max_length=30);
    gender_male="m"
    gender_female="f"
    gender_other="o"
    gender_choices=(
        (gender_male,'male'),
        (gender_female,'female'),
        (gender_other,'other'),
    )
    bill_choices=(
        (1,'Single Room'),
        (2,'Double Room'),
        (3,'Triple Room'),
    )
    gender=models.CharField(max_length=1,choices=gender_choices)
    bill=models.PositiveIntegerField(unique=True)
    priority=models.PositiveIntegerField(default=1)
    room=models.ForeignKey(Hostel, related_name='books', on_delete=models.CASCADE, null=True)
    billcategory=models.PositiveIntegerField(choices=bill_choices)
    hostel=models.ForeignKey(Hostels, related_name='billfor',on_delete=models.CASCADE, null=False)
    #prefRoommate1=models.ForeignKey('self', related_name='prefRoommate', null=True, on_delete=modls.SET_NULL)
    #prefRoommate2=models.ForeignKey('self', related_name='prefRoommate', null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.usn
