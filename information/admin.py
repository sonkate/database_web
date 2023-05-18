from django.contrib import admin
from .models import *
# Register your models here.

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('cnumber', 'name', 'address', 'phone', 'edate')

class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('year', 'no', 'datetime', 'duration')

class PersonAdmin(admin.ModelAdmin):
    list_display = ('ssn', 'phone', 'fname', 'lname', 'address')

class GroupAdmin(admin.ModelAdmin):
    list_display = ('gname', 'no_of_member', 'guest')
class InvitedguestAdmin(admin.ModelAdmin):
    list_display = ('guest_id',)
class GroupsignaturesongAdmin(admin.ModelAdmin):
    list_display = ('gname', 'song_name')
class SongAdmin(admin.ModelAdmin):
    list_display = ('number', 'released_year', 'name', 'singer_ssn_fist_performed')
class MentorAdmin(admin.ModelAdmin):
    list_display = ('ssn', )
class SingerAdmin(admin.ModelAdmin):
    list_display = ('ssn', 'guest')
class GuestsupportstageAdmin(admin.ModelAdmin):
    list_display = ('guest', )
class StageAdmin(admin.ModelAdmin):
    list_display = ('year', 'song', 'stage_no', 'is_group', 'skill', 'total_vote')
class GuestsupportstageAdmin(admin.ModelAdmin):
    list_display = ('year', 'guest', 'stage_no',)
class McAdmin(admin.ModelAdmin):
    list_display = ('ssn', )
class ThemesongAdmin(admin.ModelAdmin):
    list_display = ('song', )
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('year', 'themesong', 'mc_ssn', 'location')
class TraineeAdmin(admin.ModelAdmin):
    list_display = ('ssn', 'dob', 'photo', 'company', )
class MentorvaluatetraineeAdmin(admin.ModelAdmin):
    list_display = ('year', 'ssn_trainee', 'ssn_mentor', 'score')
class ProducerAdmin(admin.ModelAdmin):
    list_display = ('ssn',)
class SeasonmentorAdmin(admin.ModelAdmin):
    list_display = ('ssn_mentor', 'year')
class SeasontraineeAdmin(admin.ModelAdmin):
    list_display = ('ssn_trainee', 'year')
class SingersignaturesongAdmin(admin.ModelAdmin):
    list_display = ('ssn', 'song_name')
class SongcomposedbyAdmin(admin.ModelAdmin):
    list_display = ('composer_ssn', 'song')
class SongwriterAdmin(admin.ModelAdmin):
    list_display = ('ssn', )




admin.site.register(Company, CompanyAdmin)
admin.site.register(Episode, EpisodeAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Invitedguest,InvitedguestAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(Singer, SingerAdmin)
admin.site.register(Mentor, MentorAdmin)
admin.site.register(Groupsignaturesong, GroupsignaturesongAdmin)
admin.site.register(Stage, StageAdmin)
admin.site.register(Guestsupportstage, GuestsupportstageAdmin)
admin.site.register(Mc, McAdmin)
admin.site.register(Themesong, ThemesongAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Mentorvaluatetrainee, MentorvaluatetraineeAdmin)
admin.site.register(Trainee,TraineeAdmin)
admin.site.register(Producer,ProducerAdmin)
admin.site.register(Seasonmentor,SeasonmentorAdmin)
admin.site.register(Seasontrainee,SeasontraineeAdmin)
admin.site.register(Singersignaturesong,SingersignaturesongAdmin)
admin.site.register(Songcomposedby,SongcomposedbyAdmin)
admin.site.register(Songwriter,SongwriterAdmin)
