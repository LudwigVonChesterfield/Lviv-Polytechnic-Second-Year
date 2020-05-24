DROP DATABASE IF EXISTS noteWorthy;
CREATE DATABASE IF NOT EXISTS noteWorthy;
USE noteWorthy;
 
CREATE TABLE IF NOT EXISTS user (
  id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  username VARCHAR(32) NOT NULL,
  email VARCHAR(255) NOT NULL
);
 
CREATE TABLE IF NOT EXISTS tag (
  id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  color VARCHAR(45) NOT NULL,
  background VARCHAR(45) NOT NULL,
  priority INT NOT NULL,
  UNIQUE INDEX `tag_id_UNIQUE` (id ASC)
);
 
CREATE TABLE IF NOT EXISTS note (
  id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  content VARCHAR(512) NULL,
  created DATE NULL
);
 
CREATE TABLE IF NOT EXISTS note_group (
  id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  name VARCHAR(45) NOT NULL
);
 
CREATE TABLE IF NOT EXISTS permission (
  id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  note_id INT NULL,
  permission VARCHAR(45) NOT NULL,
  INDEX `note's id_idx` (`note_id` ASC),
  CONSTRAINT `note's id`
    FOREIGN KEY (`note_id`)
    REFERENCES note (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);
 
CREATE TABLE IF NOT EXISTS team (
  id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  name VARCHAR(32) NOT NULL,
  note_group_id INT NULL,
  INDEX `note_group's id_idx` (`note_group_id` ASC),
  CONSTRAINT `note_group's id_idx`
    FOREIGN KEY (`note_group_id`)
    REFERENCES note_group (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);
 
CREATE TABLE IF NOT EXISTS user_note_groups (
  id_note_groups INT NOT NULL,
  id_user INT NOT NULL,
  INDEX `user's id_idx` (`id_user` ASC),
  INDEX `note_group's id_idx` (`id_note_groups` ASC),
  CONSTRAINT `user's id`
    FOREIGN KEY (`id_user`)
    REFERENCES user (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `note_group's id`
    FOREIGN KEY (`id_note_groups`)
    REFERENCES note_group (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);
 
CREATE TABLE IF NOT EXISTS user_teams
(
  id_user INT NOT NULL,
  id_team INT NOT NULL,
  INDEX `user's id_idx` (`id_user` ASC),
  INDEX `team's id_idx` (`id_team` ASC),
  CONSTRAINT `user's id_teams`
    FOREIGN KEY (`id_user`)
    REFERENCES user (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `team's id`
    FOREIGN KEY (`id_team`)
    REFERENCES team (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);
 
CREATE TABLE IF NOT EXISTS user_notes
(
  id_user INT NOT NULL,
  id_note INT NOT NULL,
  INDEX `user's id_idx` (`id_user` ASC),
  INDEX `note's id_idx` (`id_note` ASC),
  CONSTRAINT `id_user_constr`
    FOREIGN KEY (`id_user`)
    REFERENCES user (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `id_note`
    FOREIGN KEY (`id_note`)
    REFERENCES note (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS note_tags
(
  note_id INT NULL,
  tag_id INT NULL,
  INDEX `note's id_idx` (`note_id` ASC),
  INDEX `tag's id_idx` (`tag_id` ASC),
  CONSTRAINT `note_id_tags`
    FOREIGN KEY (`note_id`)
    REFERENCES note (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `tag's id`
    FOREIGN KEY (`tag_id`)
    REFERENCES tag (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);
 
CREATE TABLE IF NOT EXISTS note_group_permissions
(
  note_group_id INT NULL,
  permission_id INT NULL,
  INDEX `note_group's id_idx` (`note_group_id` ASC),
  INDEX `permission's id_idx` (`permission_id` ASC),
  CONSTRAINT `note_group_id`
    FOREIGN KEY (`note_group_id`)
    REFERENCES note_group (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `permission's id`
    FOREIGN KEY (`permission_id`)
    REFERENCES permission (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS team_permissions
(
  team_id INT NULL,
  permission_id INT NULL,
  INDEX `team's id_idx` (`team_id` ASC),
  INDEX `permission's id_idx` (`permission_id` ASC),
  CONSTRAINT `team_id`
    FOREIGN KEY (`team_id`)
    REFERENCES team (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `permission's id_team`
    FOREIGN KEY (`permission_id`)
    REFERENCES permission (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);
 
CREATE TABLE IF NOT EXISTS user_permissions
(
  user_id INT NULL,
  permission_id INT NULL,
  INDEX `user's id_idx` (`user_id` ASC),
  INDEX `permission's id_idx` (`permission_id` ASC),
  CONSTRAINT `user's id_user_perms`
    FOREIGN KEY (`user_id`)
    REFERENCES user (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `permission_id_field`
    FOREIGN KEY (`permission_id`)
    REFERENCES permission (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);