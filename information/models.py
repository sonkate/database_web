from django.db import models
from django.core.validators import MaxValueValidator, RegexValidator


class Average(models.Model):
    ssn_trainee = models.OneToOneField('Mentorvaluatetrainee', models.CASCADE, db_column='SSN_trainee', primary_key=True)  # Field name made lowercase.
    averagescore = models.IntegerField(db_column='AverageScore', blank=True, null=True)  # Field name made lowercase.
    voteep2 = models.IntegerField(db_column='VoteEp2', blank=True, null=True)  # Field name made lowercase.
    voteep3 = models.IntegerField(db_column='VoteEp3', blank=True, null=True)  # Field name made lowercase.
    year = models.TextField(db_column='Year')  # Field name made lowercase. This field type is a guess.
    voteep4 = models.IntegerField(db_column='VoteEp4', blank=True, null=True)  # Field name made lowercase.
    voteep5 = models.IntegerField(db_column='VoteEp5', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'average'



class Company(models.Model):
    regex_cnumber = RegexValidator(regex='(C)[1-9][1-9][1-9]', message="Invalid C number")
    cnumber = models.CharField(db_column='Cnumber', primary_key=True, max_length=4, validators=[regex_cnumber])  #
    name = models.CharField(db_column='Name', max_length=30)  #
    address = models.CharField(db_column='Address', max_length=50, blank=True, null=True)  #
    phone = models.IntegerField(db_column='Phone', unique=True)  #
    edate = models.DateField(db_column='Edate', blank=True, null=True)  #

    class Meta:
        managed = False
        db_table = 'company'
    def __str__(self) -> str:
        return str(self.cnumber)

class Episode(models.Model):
    year = models.IntegerField(db_column='Year', primary_key=True)  #
    no = models.IntegerField(db_column='No', unique=True)  #
    datetime = models.DateTimeField(db_column='Datetime', blank=True, null=True)  #
    duration = models.TimeField(db_column='Duration', blank=True, null=True)  #

    class Meta:
        managed = False
        db_table = 'episode'
        unique_together = (('year', 'no'),)
    def __str__(self) -> str:
        return str(self.year)
    

class Group(models.Model):
    gname = models.CharField(db_column='Gname', primary_key=True, max_length=30)  #
    no_of_member = models.IntegerField(db_column='No_of_member', blank=True, null=True)  #
    guest = models.ForeignKey('Invitedguest', models.CASCADE, db_column='Guest_ID', blank=True, null=True)  #

    class Meta:
        managed = False
        db_table = 'group'
    def __str__(self):
        return str(self.gname)

class Groupsignaturesong(models.Model):
    gname = models.OneToOneField(Group, models.CASCADE, db_column='Gname', primary_key=True)  #
    song_name = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'groupsignaturesong'
        unique_together = (('gname', 'song_name'),)


class Guestsupportstage(models.Model):
    guest = models.ForeignKey('Invitedguest', models.CASCADE, db_column='Guest_ID', blank=True, null=True)  #
    year = models.OneToOneField('Stage', models.CASCADE, db_column='Year', primary_key=True)  #
    stage_no = models.ForeignKey('Stage', models.CASCADE, db_column='Stage_No', to_field='stage_no', related_name='StageNo')  #
    class Meta:
        managed = False
        db_table = 'guestsupportstage'
        unique_together = (('year', 'stage_no'),)


class Invitedguest(models.Model):
    guest_id = models.AutoField(db_column='Guest_ID', primary_key=True)  #

    class Meta:
        managed = False
        db_table = 'invitedguest'
    def __str__(self):
        return str(self.guest_id)

class Mc(models.Model):
    ssn = models.OneToOneField('Person', models.PROTECT, db_column='SSN', primary_key=True, unique=False)  #

    class Meta:
        managed = False
        db_table = 'mc'
    def __str__(self) -> str:
        return str(self.ssn)

class Mentor(models.Model):
    ssn = models.OneToOneField('Person',db_column='SSN', on_delete= models.PROTECT, primary_key=True, validators=[MaxValueValidator(999999999999)])  #

    class Meta:
        managed = False
        db_table = 'mentor'
    def __str__(self):
        return str(self.ssn)

class Mentorvaluatetrainee(models.Model):
    year = models.OneToOneField('Season', models.CASCADE, db_column='Year', primary_key=True)  #
    ssn_trainee = models.ForeignKey('Trainee', models.CASCADE, db_column='SSN_Trainee')  #
    ssn_mentor = models.ForeignKey(Mentor, models.CASCADE, db_column='SSN_Mentor')  #
    score = models.IntegerField(db_column='Score', blank=True, null=True)  #

    class Meta:
        managed = False
        db_table = 'mentorvaluatetrainee'
        unique_together = (('year', 'ssn_trainee', 'ssn_mentor'),)


class Person(models.Model):
    regex_ssn = RegexValidator(regex='[1-9][1-9][1-9][1-9][1-9][1-9][1-9][1-9][1-9][1-9][1-9][1-9]', message= "Invalid SSN")
    ssn = models.CharField(db_column='SSN', primary_key=True, validators=[regex_ssn], max_length=12)  #
    phone = models.CharField(db_column='Phone', unique=True, max_length=30)  #
    fname = models.CharField(db_column='Fname', max_length=20, blank=True, null=True)  #
    lname = models.CharField(db_column='Lname', max_length=20)  #
    address = models.CharField(db_column='Address', max_length=255, blank=True, null=True)  #

    class Meta:
        managed = False
        db_table = 'person'
    def __str__(self) -> str:
        return str(self.ssn)
    def full_name(self):
        return str(f'{self.fname} {self.lname}')

class Producer(models.Model):
    ssn = models.OneToOneField(Mentor, models.CASCADE, db_column='SSN', primary_key=True)  #

    class Meta:
        managed = False
        db_table = 'producer'
    def __str__(self) -> str:
        return str(self.ssn)

class Producerprogram(models.Model):
    program_name = models.CharField(db_column='Program_name', max_length=30,)  #
    ssn = models.OneToOneField(Producer, models.CASCADE, db_column='SSN')  #

    class Meta:
        managed = False
        db_table = 'producerprogram'
        unique_together = (('ssn', 'program_name'),)


class Season(models.Model):
    year = models.IntegerField(db_column='Year', primary_key=True)  # This field type is a guess.
    themesong = models.ForeignKey('Themesong', models.CASCADE, db_column='Themesong_ID', blank=True, null=True)  #
    mc_ssn = models.ForeignKey(Mc, models.CASCADE, db_column='MC_SSN', blank=True, null=True)  #
    location = models.CharField(db_column='Location', max_length=100)  #

    class Meta:
        managed = False
        db_table = 'season'
    def __str__(self) -> str:
        return str(self.year)

class Seasonmentor(models.Model):
    year = models.OneToOneField(Season, models.CASCADE, db_column='Year', primary_key=True)  #
    ssn_mentor = models.ForeignKey(Mentor, models.CASCADE, db_column='SSN_Mentor')  #

    class Meta:
        managed = False
        db_table = 'seasonmentor'
        unique_together = (('year', 'ssn_mentor'),)


class Seasontrainee(models.Model):
    year = models.OneToOneField(Season, models.CASCADE, db_column='Year', primary_key=True)  #
    ssn_trainee = models.ForeignKey('Trainee', models.CASCADE, db_column='SSN_Trainee')  #

    class Meta:
        managed = False
        db_table = 'seasontrainee'
        unique_together = (('year', 'ssn_trainee'),)


class Singer(models.Model):
    guest = models.ForeignKey(Invitedguest, models.CASCADE, db_column='Guest_ID', blank=True, null=True)  #
    ssn = models.OneToOneField(Mentor, models.CASCADE, db_column='SSN', primary_key=True)  #

    class Meta:
        managed = False
        db_table = 'singer'
    def __str__(self):
        return str(self.ssn)

class Singersignaturesong(models.Model):
    song_name = models.CharField(db_column='Song_name', max_length=30)  #
    ssn = models.OneToOneField(Singer, models.CASCADE, db_column='SSN', primary_key=True)  #

    class Meta:
        managed = False
        db_table = 'singersignaturesong'
        unique_together = (('ssn', 'song_name'),)


class Song(models.Model):
    number = models.AutoField(db_column='Number', primary_key=True)  #
    released_year = models.TextField(db_column='Released_year', blank=True, null=True)  # This field type is a guess.
    name = models.CharField(db_column='Name', max_length=30, blank=True, null=True)  #
    singer_ssn_fist_performed = models.ForeignKey(Singer, models.CASCADE, db_column='Singer_SSN_fist_performed', blank=True, null=True)  #

    class Meta:
        managed = False
        db_table = 'song'
    def __str__(self) -> str:
        return str(self.name)

class Songcomposedby(models.Model):
    composer_ssn = models.ForeignKey('Songwriter', models.CASCADE, db_column='composer_SSN')  #
    song = models.OneToOneField(Song, models.CASCADE, db_column='Song_ID', primary_key=True)  #

    class Meta:
        managed = False
        db_table = 'songcomposedby'
        unique_together = (('song', 'composer_ssn'),)
    def __str__(self) -> str:
        return str(self.song)

class Songwriter(models.Model):
    ssn = models.OneToOneField(Mentor, models.CASCADE, db_column='SSN', primary_key=True)  #

    class Meta:
        managed = False
        db_table = 'songwriter'
    def __str__(self) -> str:
        return str(self.ssn)
class Stage(models.Model):
    year = models.OneToOneField(Episode, models.CASCADE, db_column='Year', primary_key=True)  #
    ep_no = models.ForeignKey(Episode, models.CASCADE, db_column='Ep_No', related_name='EpisodeNo', to_field='no', )  #
    stage_no = models.IntegerField(db_column='Stage_No', unique=True)  #
    is_group = models.IntegerField(db_column='is_Group', blank=True, null=True)  #
    skill = models.IntegerField(db_column='Skill', blank=True, null=True)  #
    total_vote = models.IntegerField(db_column='Total_vote', blank=True, null=True)  #
    song = models.ForeignKey(Song, models.CASCADE, db_column='Song_ID', blank=True, null=True)  #

    class Meta:
        managed = False
        db_table = 'stage'
        unique_together = (('year', 'ep_no', 'stage_no'),)
    def __str__(self) -> str:
        return str(f'{self.year} ep_no: {self.ep_no}')

class Stageincludetrainee(models.Model):
    year = models.ForeignKey(Episode, models.CASCADE, db_column='Year', related_name='Year')  #
    ep_no = models.OneToOneField(Episode, models.CASCADE, db_column='Ep_No', primary_key=True, unique=True)  #
    stage_no = models.ForeignKey(Stage, models.CASCADE, db_column='Stage_No', to_field='stage_no')  #
    ssn_trainee = models.CharField(db_column='SSN_Trainee', max_length=12)  #
    role = models.IntegerField(db_column='Role', blank=True, null=True)  #
    no_of_vote = models.IntegerField(db_column='No_of_Vote', blank=True, null=True)  #

    class Meta:
        managed = False
        db_table = 'stageincludetrainee'
        unique_together = (('ep_no', 'year', 'stage_no', 'ssn_trainee'),)


class Themesong(models.Model):
    song = models.OneToOneField(Song, models.CASCADE, db_column='Song_ID', primary_key=True)  #

    class Meta:
        managed = False
        db_table = 'themesong'
    def __str__(self) -> str:
        return str(self.song)

class Trainee(models.Model):
    ssn = models.OneToOneField(Person, db_column='SSN', primary_key=True, to_field='ssn',on_delete=models.CASCADE)  #
    dob = models.DateField(db_column='DoB', blank=True, null=True)  #
    photo = models.TextField(db_column='Photo', blank=True, null=True)  #
    company = models.ForeignKey(Company, models.RESTRICT, db_column='Company_ID', blank=True, null=True)  #
    
    class Meta:
        managed = False
        db_table = 'trainee'
        
    def __str__(self) -> str:
        return str(self.ssn) 

    def full_name(self):
        return self.ssn.full_name()
    
