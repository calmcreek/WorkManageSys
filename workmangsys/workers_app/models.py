from django.db import models

# Create your models here.

GENDER_CHOICES =( 
('male','Male'),
('female','Female')
)

AVAILABILITY_CHOICES = (
('yes','Yes'),
('no','No')
)

WORKSTATUS_CHOICES = (
    ('0%','0%'),
    ('100%','100%'),
)

class Role(models.Model):
    role = models.CharField(max_length = 100, null = False)
    # role_description = models.CharField(max_length = 150)
    def __str__ (self):
        return self.role



class Work (models.Model):
    work_ID = models.IntegerField(default = 0,null = False)
    work_name = models.CharField(max_length = 100, null = False )
    start_date = models.DateField(null = False)
    duration_days = models.IntegerField(default = 0,null = False)
    priority = models.IntegerField(default = 0,null = False)
    roles_required = models.ManyToManyField(Role, through='WorkRoleRequirement',default=0)

    workstatus = models.CharField(choices = WORKSTATUS_CHOICES, max_length = 10,default = 0, null = False)
    def __str__(self):
        return f"{self.work_name}, {self.work_ID},{self.priority},{self.workstatus}"

    def save(self, *args, **kwargs):
        print("Saving work instance...")
        if self.workstatus == '100%':
            print("Work status is 100%, updating worker availability...")
            if self.assignments.exists():
                print("Assignments exist for this work.")
            # Update availability of workers assigned to this work to 'Yes'
            for assignment in self.assignments.all():
                print(f" Name: {assignment.worker.name}, Availability: {assignment.worker.availability}")
                assignment.worker.availability = 'yes'
                assignment.worker.save()
            else:
                print("No assignments found for this work.")
        super().save(*args, **kwargs)


class WorkRoleRequirement(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE,null = False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE,null = False)
    number_of_workers_required = models.IntegerField(null = False) 
    def __str__(self):
        return f"{self.role.role} for {self.work.work_name}"

class Worker(models.Model):
    # image = models.ImageField(upload_to='person')
    name = models.CharField(max_length = 100, null = False )
    role = models.ForeignKey(Role, on_delete = models.CASCADE, null = False)
    skill_level = models.IntegerField(default = 0)
    email = models.EmailField(null = False)
    phones = models.CharField(max_length=15, null = False)
    address = models.CharField(max_length = 100, null = False)
    platform = models.CharField(max_length = 100, null = False)
    gender= models.CharField(choices = GENDER_CHOICES, max_length = 10)
    availability= models.CharField(choices = AVAILABILITY_CHOICES, max_length = 10, null = False)
    assigned_works = models.ManyToManyField(Work, through='Assignment', related_name='assigned_workers')

    def __str__(self):
        return f"{self.name}, {self.role}, {self.availability}"
    




class Assignment(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='assignments')
    hours_worked = models.IntegerField(default=0)  # You can adjust this field based on your needs

    def __str__(self):
        return f"{self.worker.name} assigned to {self.work.work_name}"