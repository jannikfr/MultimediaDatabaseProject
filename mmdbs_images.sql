-- auto-generated definition
create table mmdbs_image
(
  id                    serial       not null
    constraint features_pkey
    primary key,
  path                  varchar(255) not null,
  classification        varchar(255),
  local_histogram       json,
  global_histogram      json,
  global_edge_histogram json
);

