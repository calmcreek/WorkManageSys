from django.contrib import admin
from .models import Worker,Work,Role,WorkRoleRequirement, Assignment




# Register your models here.

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ("name", "role","availability")
    
admin.site.register(Role)
    

class WorkRoleRequirementInline(admin.TabularInline):
    model = WorkRoleRequirement
    extra = 1

# Define a custom admin class for the Work model
@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ("work_name", "work_ID", "priority", "workstatus")
    inlines = [WorkRoleRequirementInline]

    # Register the custom admin action
    actions = ['assign_workers_to_works']

    def assign_workers_to_works(self, request, queryset):
        queryset = queryset.order_by('priority')
        for work in queryset:
            # Perform assignment logic 
            # 1. Get available workers based on some criteria
            workers = Worker.objects.filter(
                role__in=work.roles_required.all(),
                availability='yes'
            ).order_by('-skill_level')

            workers_count = workers.count()
            required_workers_count = sum(work_req.number_of_workers_required for work_req in work.workrolerequirement_set.all())

            if workers_count < required_workers_count:
                self.message_user(request, f"Not enough available workers for '{work}'.")
                continue
            # 2. Assign workers to the work
            assigned_workers = workers[:required_workers_count]
            for worker in assigned_workers:
                # Create Assignment instances
                Assignment.objects.create(worker=worker, work=work)
                
                # Update worker availability
                worker.availability = 'no'
                worker.save()

            self.message_user(request, f"{len(assigned_workers)} workers assigned to '{work}'.")

            # You can update workstatus or any other necessary fields here
            work.workstatus = 'assigned'
            work.save()
            pass

    assign_workers_to_works.short_description = "Assign Workers to Works"
    

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    pass  