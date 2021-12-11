create table if not exists users
(
    user_id    bigint                               not null
        constraint users_pk
            primary key,
    username   varchar,
    full_name  varchar,
    created_at timestamp  default CURRENT_TIMESTAMP not null,
    lang       varchar(2) default NULL::character varying
);

alter table users
    owner to soap;

create unique index if not exists users_telegram_id_uindex
    on users (user_id);

create table if not exists user_tests
(
    id              serial
        constraint user_tests_pk
            primary key,
    user_id         bigint,
    test_id         integer           not null,
    correct_answers integer default 0 not null,
    points          integer default 0 not null
);

alter table user_tests
    owner to soap;

create unique index if not exists user_tests_user_id_uindex
    on user_tests (user_id);

create table if not exists tests
(
    id     serial
        constraint tests_pk
            primary key,
    status integer default 0 not null,
    title  varchar
);

alter table tests
    owner to soap;

create table if not exists test_texts
(
    id          serial
        constraint test_texts_pk
            primary key,
    name        varchar,
    description varchar,
    lang        varchar(2),
    test_id     integer not null
);

alter table test_texts
    owner to soap;

create table if not exists questions
(
    id      serial
        constraint questions_pk
            primary key,
    test_id integer           not null,
    points  integer default 0 not null
);

alter table questions
    owner to soap;

create table if not exists question_texts
(
    id          serial
        constraint question_texts_pk
            primary key,
    question    varchar,
    lang        varchar(2),
    question_id integer not null
);

alter table question_texts
    owner to soap;

create table if not exists answers
(
    id          serial
        constraint answers_pk
            primary key,
    question_id integer               not null,
    is_true     boolean default false not null
);

alter table answers
    owner to soap;

create table if not exists answer_texts
(
    id          serial
        constraint answer_texts_pk
            primary key,
    answer_id   integer    not null,
    answer      varchar,
    description varchar,
    lang        varchar(2) not null
);

alter table answer_texts
    owner to soap;