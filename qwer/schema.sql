drop table if exists jobs;
create table jobs (
  id integer primary key autoincrement,
  status text not null,
  location text not null,
  'data' text
);