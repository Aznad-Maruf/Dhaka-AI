drop table if exists Team;
drop table if exists Participant;
drop table if exists Leaderboard;


create table Team
(
    TeamName varchar(16) not null,
    Password varchar(400) not null,
    EmailAddress varchar(50),
    isVerified integer default 0,
    isAdmin integer default 0,
    DailyLimit integer default 0,
    primary key (TeamName)
);

create table Participant
(
	Name varchar(40),
	ContactNo varchar(15),
	Institution varchar(50),
	TeamName varchar(16),
	foreign key (TeamName) references Team(TeamName)
);

create table Leaderboard
(
  TeamName varchar(16),
	Accuracy double,
	SolutionPath varchar(150),
	foreign key (TeamName) references Team(TeamName)
);
