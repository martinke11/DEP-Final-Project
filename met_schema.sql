/*!40101 SET NAMES utf8 */;
/*!40101 SET SQL_MODE=''*/;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


CREATE DATABASE /*!32312 IF NOT EXISTS*/`met` /*!40100 DEFAULT CHARACTER SET latin1 */;
use met;

# removed object date
CREATE TABLE `object` (
    `object_id` BIGINT NOT NULL,
	`artist_id` BIGINT,
	`department_id` BIGINT,
    `period_id` BIGINT,
    `geography_type_id` BIGINT,
    `is_highlight` INT,
    `is_timeline_work` INT,
    `is_public_domain` INT,
    `object_name` TEXT,
    `title` TEXT,
    `culture` TEXT,
    `object_begin_date` BIGINT,
    `object_end_date` BIGINT,
    `medium` TEXT,
    `dimensions` TEXT,
    `excavation` TEXT,
    PRIMARY KEY (`object_id`),
    FOREIGN KEY (`department_id`) REFERENCES `department` (`department_id`) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (`period_id`) REFERENCES `period` (`period_id`) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (`geography_type_id`) REFERENCES `geography` (`geography_type_id`) ON DELETE SET NULL ON UPDATE CASCADE
);

INSERT INTO object (object_id, is_highlight, is_timeline_work, is_public_domain, object_name, title, culture, object_begin_date, object_end_date, medium, dimensions, excavation)
SELECT object_id, is_highlight, is_timeline_work, is_public_domain, object_name, title, culture, object_begin_date, object_end_date, medium, dimensions, excavation
FROM cleaned_met_data;


CREATE TABLE `artists` (
    `artist_id` BIGINT NOT NULL AUTO_INCREMENT,
    `artist_role` TEXT,
    `artist_display_name` TEXT,
    `artist_nationality` TEXT,
    `artist_begin_date` BIGINT,
    `artist_end_date` BIGINT,
    `is_female` BIGINT,
    PRIMARY KEY (`artist_id`)
);
SHOW COLUMNS FROM cleaned_met_data;
INSERT INTO artists (artist_role, artist_display_name, artist_nationality, artist_begin_date, artist_end_date, is_female)
SELECT artist_role, artist_display_name, artist_nationality, artist_begin_date, artist_end_date, is_female
FROM cleaned_met_data;

DROP TABLE artists;




CREATE TABLE `object_artist` (
    `object_id` BIGINT NOT NULL,
    `artist_id` BIGINT NOT NULL,
    PRIMARY KEY (`object_id`, `artist_id`),
    FOREIGN KEY (`object_id`) REFERENCES `object` (`object_id`) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (`artist_id`) REFERENCES `artists` (`artist_id`) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE `department` (
    `department_id` BIGINT NOT NULL AUTO_INCREMENT,
    `department` TEXT,
    `accession_year` BIGINT,
	PRIMARY KEY (`department_id`)
);

INSERT INTO department (department, accession_year)
SELECT DISTINCT department, accession_year
FROM cleaned_met_data;


CREATE TABLE `period` (
    `period_id` BIGINT NOT NULL AUTO_INCREMENT,
    `period` TEXT,
    `dynasty` TEXT,
    `reign` TEXT,
    PRIMARY KEY (`period_id`)
);

INSERT INTO period (period, dynasty, reign)
SELECT DISTINCT period, dynasty, reign
FROM cleaned_met_data;

CREATE TABLE `credit_line` (
    `credit_line_id` BIGINT NOT NULL AUTO_INCREMENT,
    `credit_line` TEXT,
    PRIMARY KEY (`credit_line_id`)
);

INSERT INTO credit_line (credit_line)
SELECT DISTINCT credit_line
FROM cleaned_met_data;


CREATE TABLE `object_credit_line` (
    `object_id` BIGINT NOT NULL,
    `credit_line_id` BIGINT NOT NULL,
    PRIMARY KEY (`object_id`, `credit_line_id`),
    FOREIGN KEY (`object_id`) REFERENCES `object` (`object_id`) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (`credit_line_id`) REFERENCES `credit_line` (`credit_line_id`) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE `geography` (
	`geography_type_id` BIGINT AUTO_INCREMENT,
    `location_id` BIGINT,
    `geography_type` TEXT,
    `region_id` BIGINT,
    PRIMARY KEY (`geography_type_id`),
    FOREIGN KEY (`region_id`) REFERENCES `region` (`region_id`) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (`location_id`) REFERENCES `location` (`location_id`) ON DELETE SET NULL ON UPDATE CASCADE
);

INSERT INTO geography (geography_type)
SELECT DISTINCT geography_type
FROM cleaned_met_data;

CREATE TABLE `location` (
    `location_id` BIGINT NOT NULL AUTO_INCREMENT,
    `city` TEXT,
    `state` TEXT,
    `county` TEXT,
    `country` TEXT,
    PRIMARY KEY (`location_id`)
);

INSERT INTO location (city, state, county, country)
SELECT DISTINCT city, state, county, country
FROM cleaned_met_data;

CREATE TABLE `region` (
    `region_id` BIGINT NOT NULL AUTO_INCREMENT,
    `region` TEXT,
    `subregion` TEXT,
    `locale` TEXT,
    `locus` TEXT,
    `river` TEXT,
    PRIMARY KEY (`region_id`)
);

INSERT INTO region (region, subregion, locale, locus, river)
SELECT DISTINCT region, subregion, locale, locus, river
FROM cleaned_met_data;


