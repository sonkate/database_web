create table company
(
    Cnumber varchar(4)  not null comment 'C[0-9][0-9][0-9]'
        primary key,
    Name    varchar(30) not null,
    Address varchar(50) null,
    Phone   varchar(30) not null,
    Edate   date        null,
    constraint COMPANY_pk
        unique (Phone)
);

create table episode
(
    Year     year     not null,
    No       int      not null comment '[1-5]',
    Datetime datetime null,
    Duration time     null,
    primary key (Year, No),
    constraint `check episode number`
        check ((`No` >= 1) and (`No` <= 5))
);

create table invitedguest
(
    Guest_ID int auto_increment
        primary key
);

create table `group`
(
    Gname        varchar(30) not null
        primary key,
    No_of_member int         null comment '[1, 20] ',
    Guest_ID     int         null,
    constraint Group_invitedguest_null_fk
        foreign key (Guest_ID) references invitedguest (Guest_ID),
    constraint `check number member`
        check ((`No_of_member` >= 1) and (`No_of_member` <= 20))
);

create table groupsignaturesong
(
    Gname     varchar(30) not null,
    song_name varchar(30) not null,
    primary key (Gname, song_name),
    constraint groupsignaturesong_group_null_fk
        foreign key (Gname) references `group` (Gname)
);

create table mentor
(
    SSN varchar(12) not null
        primary key
);

create table person
(
    SSN     varchar(12)  not null comment ' 12 digit number'
        primary key,
    Phone   varchar(30)  not null comment 'Unique and not null',
    Fname   varchar(20)  null,
    Lname   varchar(20)  not null,
    Address varchar(255) null,
    constraint Phone
        unique (Phone)
);

create table mc
(
    SSN varchar(12) not null comment '12 digit'
        primary key,
    constraint MC_person_null_fk
        foreign key (SSN) references person (SSN)
);

create table producer
(
    SSN varchar(12) not null comment 'SSN'
        primary key,
    constraint producer_mentor_null_fk
        foreign key (SSN) references mentor (SSN)
);

create table producerprogram
(
    Program_name varchar(30) not null,
    SSN          varchar(12) not null,
    primary key (SSN, Program_name),
    constraint ProducerProgram_producer_null_fk
        foreign key (SSN) references producer (SSN)
);

create table singer
(
    Guest_ID int         null,
    SSN      varchar(12) not null
        primary key,
    constraint SINGER_invitedguest_null_fk
        foreign key (Guest_ID) references invitedguest (Guest_ID),
    constraint SINGER_mentor_null_fk
        foreign key (SSN) references mentor (SSN)
);

create table singersignaturesong
(
    Song_name varchar(30) not null,
    SSN       varchar(12) not null,
    primary key (SSN, Song_name),
    constraint singersignaturesong_singer_null_fk
        foreign key (SSN) references singer (SSN)
);

create table song
(
    Number                    int auto_increment comment ' S[auto increment integer] '
        primary key,
    Released_year             year        null,
    Name                      varchar(30) null,
    Singer_SSN_fist_performed varchar(12) null,
    constraint Song_singer_null_fk
        foreign key (Singer_SSN_fist_performed) references singer (SSN)
);

create table songwriter
(
    SSN varchar(12) not null comment 'Mentor'
        primary key,
    constraint Songwriter_mentor_null_fk
        foreign key (SSN) references mentor (SSN)
);

create table songcomposedby
(
    composer_SSN varchar(12) not null comment 'SSN of Songwritter',
    Song_ID      int         not null,
    primary key (Song_ID, composer_SSN),
    constraint Songcomposedby_song_null_fk
        foreign key (Song_ID) references song (Number),
    constraint songcomposedby_songwriter_null_fk
        foreign key (composer_SSN) references songwriter (SSN)
);

create table stage
(
    Year       year       not null,
    Ep_No      int        not null,
    Stage_No   int        not null,
    is_Group   tinyint(1) null comment 'Yes: group stage, No: individual stage',
    Skill      int        null comment ' 1 – vocal, 2 – rap, 3 – dance, 4 – mixed (default value)',
    Total_vote int        null,
    Song_ID    int        null,
    primary key (Year, Ep_No, Stage_No),
    constraint Stage_episode_null_null_fk
        foreign key (Year, Ep_No) references episode (Year, No),
    constraint Stage_song_null_fk
        foreign key (Song_ID) references song (Number)
);

create table guestsupportstage
(
    Guest_ID int  null,
    Year     year not null,
    Ep_No    int  not null,
    Stage_No int  not null,
    primary key (Year, Ep_No, Stage_No),
    constraint GuestSupportStage_invitedguest_null_fk
        foreign key (Guest_ID) references invitedguest (Guest_ID),
    constraint GuestSupportStage_stage_null_null_null_fk
        foreign key (Year, Ep_No, Stage_No) references stage (Year, Ep_No, Stage_No)
);

create table stageincludetrainee
(
    Year        year        not null,
    Ep_No       int         not null,
    Stage_No    int         not null,
    SSN_Trainee varchar(12) not null,
    Role        int         null comment '1 – member (default), 2 – leader, 3 – center',
    No_of_Vote  int         null comment ' [0, 500]',
    primary key (Ep_No, Year, Stage_No, SSN_Trainee),
    constraint StageIncludeTrainee_stage_null_null_null_fk
        foreign key (Year, Ep_No, Stage_No) references stage (Year, Ep_No, Stage_No),
    constraint `check number of vote`
        check ((`No_of_Vote` >= 0) and (`No_of_Vote` <= 500))
);

create definer = root@localhost trigger ensure_final_stage
    after insert
    on stageincludetrainee
    for each row
begin
    DECLARE count int default 0;
    set count = (SELECT count(stageincludetrainee.Stage_No) from stageincludetrainee
                 WHERE (stageincludetrainee.Year = new.Year )
                   AND (stageincludetrainee.Ep_No = new.Ep_No)
                   AND (stageincludetrainee.SSN_Trainee = new.SSN_Trainee)
                   AND (NEW.Ep_No = 5));
    if count > 2
    then
        signal SQLSTATE '45000' set message_text = 'This trainee must have at most one group';
    end if;
end;

create definer = root@localhost trigger ensure_group
    after insert
    on stageincludetrainee
    for each row
begin
    if exists((SELECT stageincludetrainee.Stage_No from stageincludetrainee
              WHERE (stageincludetrainee.Year = new.Year )
                AND (stageincludetrainee.Ep_No = new.Ep_No)
                AND (stageincludetrainee.SSN_Trainee = new.SSN_Trainee)
                AND (NEW.Ep_No = 2 OR NEW.Ep_No = 3 OR NEW.Ep_No = 4)))
        then
            signal SQLSTATE '45000' set message_text = 'This trainee must have at most one group';
    end if;
end;

create definer = root@localhost trigger sum_vote
    after insert
    on stageincludetrainee
    for each row
begin
    UPDATE stage SET Total_vote = (SELECT SUM(No_of_Vote) from stageincludetrainee
                                        WHERE stageincludetrainee.Year = NEW.Year
                                        AND stageincludetrainee.Ep_No = NEW.Ep_No
                                        AND stageincludetrainee.Stage_No = NEW.Stage_No)
        WHERE NEW.Year = Year AND NEW.Ep_No = Ep_No AND NEW.Stage_No = Stage_No;
end;

create definer = root@localhost trigger sum_vote_update
    after update
    on stageincludetrainee
    for each row
begin
    UPDATE stage SET Total_vote = (SELECT SUM(No_of_Vote) from stageincludetrainee
                                   WHERE stageincludetrainee.Year = NEW.Year
                                     AND stageincludetrainee.Ep_No = NEW.Ep_No
                                     AND stageincludetrainee.Stage_No = NEW.Stage_No)
    WHERE NEW.Year = Year AND NEW.Ep_No = Ep_No AND NEW.Stage_No = Stage_No;
end;

create table themesong
(
    Song_ID int not null
        primary key,
    constraint ThemeSong_song_null_fk
        foreign key (Song_ID) references song (Number)
);

create table season
(
    Year         year         not null
        primary key,
    Themesong_ID int          null,
    MC_SSN       varchar(12)  null,
    Location     varchar(100) not null,
    constraint Season_mc_null_fk
        foreign key (MC_SSN) references mc (SSN),
    constraint Season_themesong_null_fk
        foreign key (Themesong_ID) references themesong (Song_ID)
);

create table seasonmentor
(
    Year       year        not null,
    SSN_Mentor varchar(12) not null,
    primary key (Year, SSN_Mentor),
    constraint SeasonMentor_mentor_null_fk
        foreign key (SSN_Mentor) references mentor (SSN),
    constraint SeasonMentor_season_null_fk
        foreign key (Year) references season (Year)
);

create table trainee
(
    SSN        varchar(12) not null comment '12 digits'
        primary key,
    DoB        date        null,
    Photo      text        null comment 'url',
    Company_ID varchar(4)  null,
    constraint TRAINEE_company_null_fk
        foreign key (Company_ID) references company (Cnumber),
    constraint TRAINEE_person_null_fk
        foreign key (SSN) references person (SSN)
);

create table mentorvaluatetrainee
(
    Year        year        not null,
    SSN_Trainee varchar(12) not null,
    SSN_Mentor  varchar(12) not null,
    Score       int         null comment 'in range of [0-100]',
    primary key (Year, SSN_Trainee, SSN_Mentor),
    constraint MentorValuateTrainee_mentor_null_fk
        foreign key (SSN_Mentor) references mentor (SSN),
    constraint MentorValuateTrainee_season_null_fk
        foreign key (Year) references season (Year),
    constraint MentorValuateTrainee_trainee_null_fk
        foreign key (SSN_Trainee) references trainee (SSN),
    constraint check_name
        check ((`Score` >= 0) and (`Score` <= 100))
);

create table seasontrainee
(
    Year        year        not null,
    SSN_Trainee varchar(12) not null,
    primary key (Year, SSN_Trainee),
    constraint SeasonTrainee_season_null_fk
        foreign key (Year) references season (Year),
    constraint SeasonTrainee_trainee_null_fk
        foreign key (SSN_Trainee) references trainee (SSN)
);

create definer = root@localhost trigger debutNightCheck
    before insert
    on seasontrainee
    for each row
begin
    if exists(SELECT * from seasontrainee, stageincludetrainee
              WHERE (NEW.SSN_Trainee = seasontrainee.SSN_Trainee AND seasontrainee.Year < new.Year)
                AND NEW.SSN_Trainee IN (
                    SELECT seasontrainee.SSN_Trainee
                        from stageincludetrainee, seasontrainee
                            WHERE seasontrainee.SSN_Trainee = stageincludetrainee.SSN_Trainee
                            AND Ep_No = 5
                            AND seasontrainee.Year = stageincludetrainee.Year))
        then
        signal SQLSTATE '45000' set message_text = 'This trainee had taken part in The Debut Night before';
    end if;
end;

create definer = root@localhost trigger participate_time_counting
    before insert
    on seasontrainee
    for each row
begin
    DECLARE count int default 0;
    set count = (SELECT COUNT(SSN_Trainee) from seasontrainee WHERE NEW.SSN_Trainee = SSN_Trainee AND NEW.Year != YEAR);
    IF count > 2 then
        signal SQLSTATE '45000' set message_text = 'This trainee had participated 3 time!';
    end if;
end;


