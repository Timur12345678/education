from django.db import models

# Create your models here.

class SiteUser(models.Model):
    last_name = models.CharField(max_length=200, blank=True)
    first_name = models.CharField(max_length=200, blank=True)
    middle_name = models.CharField(max_length=200, blank=True)
    iin = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    email = models.CharField(max_length=200, blank=True)
    password = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.last_name+ '' + self.phone


    class CourseCategory(models.Model):
        title = models.CharField(max_length=300)
        status = models.IntegerField(default=0)


        def __str__(self):
            return self.title


    class Course(models.Model):
        title= models.CharField(max_length=300)
        category = models.ForeignKey(CourseCategory, blank=True, on_delete=models.CASCADE())
        logo = models.ImageField(upload_to='upload', blank=True)
        lessons_count = models.IntegerField(default=0, blank=True)
        discription = models.TextField(blank=True)
        is_free = models.BooleanField(default=0)
        is_profession = models.BooleanField(default=0)
        course_type = models.IntegerField(default=0, blank=True)#0 =vidio, 1 =audio, 2=text, 3=offline. 4 = online.

        info1_text = models.CharField(blank=True)
        info1 = models.CharField(blank=True, max_length=300)

        info2 = models.CharField(blank=True, max_length=300)
        info2_text = models.CharField(blank=True)

        info3 = models.CharField(blank=True, max_length=300)
        info3_text = models.CharField(blank=True)

        info4 = models.CharField(blank=True, max_length=300)
        info4_text = models.CharField(blank=True)

        def __str__(self):
            return self.title


    class CourseItem(models.Model):
        title = models.CharField(max_length=300)
        video_link = models.CharField(max_length=300, blank=True)
        mini_description = models.TextField(blank=True)
        description = models.TextField(blank=True)
        video_minutes = models.IntegerField(default=0, blank=True)
        course = models.ForeignKey(Course, on_delete=models.CASCADE)
        task = models.TextField(blank=True)
        task_code = models.TextField(blank=True)



        description = models.TextField(blank=True)


        def __str__(self):
            return self.course.title + '' + self.title + '' + str(self.id)


    class CourseItemParagraph(models.Model):
        title = models.CharField(max_length=300, blank=True)
        video_link = models.CharField(max_length=300, blank=True)
        description1 = models.TextField(blank=True)
        description2= models.TextField(blank=True)
        description3 = models.TextField(blank=True)
        logo = models.ImageField(upload_to='upload',blank= True)
        course_item = models.ForeignKey(CourseItem, on_delete=models.CASCADE)

        def __str__(self):
            return self.course_item.title + '' + self.title
