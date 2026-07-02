from django.db import models
from django.utils.functional import cached_property

class Example(models.Model):
    name = models.CharField(max_length=32)
    timestamp = models.DateTimeField(auto_now_add=True)

class SubExample(models.Model):
    name = models.CharField(max_length=32)
    timestamp = models.DateTimeField(auto_now_add=True)
    example = models.ForeignKey("Example", null=True, on_delete=models.SET_NULL)

    # Also a Property - "Model Method" vs "Table Manger Method"
    @cached_property
    def disjoint_self(self):
        ## Muse use SubExample not self.objects.all or it converts to a Table Manager Method implicitly
        all_subexamples = SubExample.objects.all()
        all_subexamples.filter(name=self.name).delete()
        disjoint_examples = list(all_subexamples)
        return disjoint_examples
