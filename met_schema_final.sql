/*!40101 SET NAMES utf8 */;
/*!40101 SET SQL_MODE=''*/;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

SET SQL_SAFE_UPDATES = 0;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`met` /*!40100 DEFAULT CHARACTER SET latin1 */;
use met;

#CREATE OBJECTS TABLE:

CREATE TABLE `object` (
    `object_id` INT NOT NULL,
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

INSERT INTO object (object_id,department_id,period_id,geography_type_id,is_highlight, is_timeline_work, is_public_domain, object_name, title, culture, object_begin_date, object_end_date, `medium`, dimensions, excavation)
SELECT object_id,department_id,period_id,geography_id, is_highlight, is_timeline_work, is_public_domain, object_name, title, culture, object_begin_date, object_end_date, `medium`, dimensions, excavation
FROM cleaned_data_with_ids;

#CREATE ARTISTS TABLE

CREATE TABLE artist (
    artist_id INT PRIMARY KEY NOT NULL,
    artist_role VARCHAR(255),
    artist_display_name VARCHAR(255) NOT NULL,
    artist_nationality VARCHAR(255),
    artist_begin_date BIGINT,
    artist_end_date BIGINT,
    is_female BIGINT
);

INSERT INTO artist (artist_id,artist_role, artist_display_name, artist_nationality, artist_begin_date, artist_end_date, is_female)
SELECT artist_id, artist_role, artist_display_name, artist_nationality, artist_begin_date, artist_end_date, is_female
FROM cleaned_data_with_ids
WHERE artist_id != 0
GROUP BY artist_id;

CREATE INDEX idx_artist_id_on_artists ON artist(artist_id);

#CREATE OBJECT ARTIST MAPPING

CREATE TABLE `object_artist` (
    `object_id` INT NOT NULL,
    `artist_id` INT NOT NULL,
    PRIMARY KEY (`object_id`, `artist_id`),
    FOREIGN KEY (`object_id`) REFERENCES `object` (`object_id`) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (`artist_id`) REFERENCES `artist` (`artist_id`) ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT INTO object_artist (object_id, artist_id)
SELECT object_id, artist_id
FROM cleaned_data_with_ids
WHERE artist_id != 0
GROUP BY object_id, artist_id;

#CREATE DEPARTMENT TABLE

CREATE TABLE department (
    department_id BIGINT NOT NULL PRIMARY KEY,
    department VARCHAR(255),
    accession_year BIGINT
);

INSERT INTO department (department_id, department, accession_year)
SELECT department_id, department, accession_year
FROM cleaned_data_with_ids
WHERE department_id != 0
GROUP BY department_id;

CREATE INDEX idx_department_id ON object(department_id);
CREATE INDEX idx_department_id_on_department ON department(department_id);

#CREATE PERIOD TABLE

CREATE TABLE `period` (
    `period_id` BIGINT NOT NULL PRIMARY KEY,
    `period` VARCHAR(255),
    `dynasty` VARCHAR(255),
    `reign` VARCHAR(255)
);

INSERT INTO period (period_id, period, dynasty, reign)
SELECT period_id, period, dynasty, reign
FROM cleaned_data_with_ids
WHERE period_id != 0 and period !=''
GROUP BY period_id;

CREATE INDEX idx_period_id ON object(period_id);
CREATE INDEX idx_period_id_on_department ON period(period_id);

#CREATE CREDIT LINE TABLE

CREATE TABLE `credit_line` (
    `credit_line_id` BIGINT NOT NULL PRIMARY KEY,
    `credit_line` VARCHAR(1000)
);

INSERT INTO credit_line (credit_line_id, credit_line)
SELECT credit_line_id, credit_line
FROM cleaned_data_with_ids
WHERE credit_line_id != 0 and credit_line <> ''
GROUP BY credit_line_id;

#CREATE OBJECT CREDIT LINE MAPPING

CREATE TABLE `object_credit_line` (
    `object_id` INT NOT NULL,
    `credit_line_id` BIGINT NOT NULL,
    PRIMARY KEY (`object_id`, `credit_line_id`),
    FOREIGN KEY (`object_id`) REFERENCES `object` (`object_id`) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (`credit_line_id`) REFERENCES `credit_line` (`credit_line_id`) ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT INTO object_credit_line (object_id, credit_line_id)
SELECT object_id, credit_line_id
FROM cleaned_data_with_ids
WHERE credit_line_id != 0
GROUP BY object_id, credit_line_id;

#CREATE GEOGRAPHY TABLE

CREATE TABLE `geography` (
	`geography_type_id` BIGINT NOT NULL,
    `location_id` BIGINT,
    `geography_type` TEXT,
    `region_id` BIGINT,
    PRIMARY KEY (`geography_type_id`),
    FOREIGN KEY (`region_id`) REFERENCES `region` (`region_id`) ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (`location_id`) REFERENCES `location` (`location_id`) ON DELETE SET NULL ON UPDATE CASCADE
);

INSERT INTO geography (geography_type_id,location_id,geography_type,region_id)
SELECT geography_id,location_id, geography_type, region_id
FROM cleaned_data_with_ids
WHERE geography_id != 0 AND geography_id <> ''
GROUP BY geography_id;

#CREATE REGION TABLE

CREATE TABLE `region` (
    `region_id` BIGINT NOT NULL,
    `region` TEXT,
    `subregion` TEXT,
    `locale` TEXT,
    `locus` TEXT,
    `river` TEXT,
    PRIMARY KEY (`region_id`)
);

INSERT INTO region (region_id, region, subregion, locale, locus, river)
SELECT region_id, region, subregion, locale, locus, river
FROM cleaned_data_with_ids
WHERE region_id != 0 and region !=''
GROUP BY region_id;

#CREATE LOCATION TABLE

CREATE TABLE `location` (
    `location_id` BIGINT NOT NULL,
    `city` TEXT,
    `state` TEXT,
    `county` TEXT,
    `country` TEXT,
    PRIMARY KEY (`location_id`)
);

INSERT INTO location (location_id, city, state, county, country)
SELECT DISTINCT location_id, city, state, county, country
FROM cleaned_data_with_ids
WHERE location_id != 0
GROUP BY location_id;

