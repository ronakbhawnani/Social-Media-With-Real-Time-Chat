from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from groups.models import CustomGroup
from cloudinary_storage.storage import VideoMediaCloudinaryStorage
# from cloudinary_storage.validators import validate_video


User = settings.AUTH_USER_MODEL

# Create your models here.

class Post(models.Model):
	STATUSES = (
		('public', 'PUBLIC'),
		('friends', 'FRIENDS'),
		('only me', 'ONLY ME'),
	)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	shared_post = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
	group = models.ForeignKey(CustomGroup, on_delete=models.SET_NULL, null=True, blank=True)
	content = models.TextField()
	video = models.FileField(
		upload_to='post_video/%Y-%m-%d/',
		storage=VideoMediaCloudinaryStorage(),
		validators=[FileExtensionValidator(allowed_extensions=['mp4', 'webm', 'flv', 'mov', 'ogv' ,'3gp' ,'3g2' ,'wmv' , 'mpeg' ,'flv' ,'mkv' ,'avi'])],
		null=True,
		blank=True
	)
	likes = models.ManyToManyField(User, related_name='+')
	visibility = models.CharField(max_length=100, choices=STATUSES)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.pk} -- {self.user}'

	def get_absolute_url(self):
		return reverse('post_detail', kwargs={'pk': self.pk})

	@property
	def comment_count(self):
		reply_list = [comment.reply_set.all().count() for comment in self.comment_set.all()]
		return sum(reply_list) + len(reply_list)

class PostImage(models.Model):
	image = models.ImageField(upload_to='post_images/%Y-%m-%d/')
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.post.pk} -- {self.post.user}'

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	comment = models.TextField()
	likes = models.ManyToManyField(User, related_name='+')
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.user.username} comments on {self.post}'

	class Meta:
		ordering = ['-created',]

class Reply(models.Model):
	comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	reply = models.TextField()
	likes = models.ManyToManyField(User, related_name='+')
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.user.username} reply on {self.comment.user} comment on {self.comment.post.user} post'

	class Meta:
		ordering = ['-created',]



