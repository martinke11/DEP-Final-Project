/*!40101 SET NAMES utf8 */;
/*!40101 SET SQL_MODE=''*/;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

SET SQL_SAFE_UPDATES = 0;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`met` /*!40100 DEFAULT CHARACTER SET latin1 */;
use met;

# removed object table, working straight from cleaned_met_data we can just rename this to objects
# and delete the columns we move to other tables

CREATE TABLE artists (
    artist_id INT AUTO_INCREMENT PRIMARY KEY,
    artist_role VARCHAR(255),
    artist_display_name VARCHAR(255) NOT NULL,
    artist_nationality VARCHAR(255),
    artist_begin_date BIGINT,
    artist_end_date BIGINT,
    is_female BIGINT
);

INSERT INTO artists (artist_role, artist_display_name, artist_nationality, artist_begin_date, artist_end_date, is_female)
SELECT artist_role, artist_display_name, artist_nationality, artist_begin_date, artist_end_date, is_female
FROM cleaned_met_data
GROUP BY artist_display_name;

ALTER TABLE cleaned_met_data
ADD COLUMN artist_id INT;

SET SQL_SAFE_UPDATES = 0;
UPDATE cleaned_met_data
SET artist_id = (SELECT artist_id
                 FROM artists
                 WHERE cleaned_met_data.artist_display_name = artists.artist_display_name);

CREATE INDEX idx_artist_id ON cleaned_met_data(artist_id);
CREATE INDEX idx_artist_id_on_artists ON artists(artist_id);


CREATE TABLE departments (
    department_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    department VARCHAR(255),
    accession_year BIGINT
);

INSERT INTO departments (department, accession_year)
SELECT DISTINCT department, accession_year
FROM cleaned_met_data;

ALTER TABLE cleaned_met_data
ADD COLUMN department_id BIGINT;

SET SQL_SAFE_UPDATES = 0;
UPDATE cleaned_met_data
SET department_id = (SELECT department_id
                     FROM departments
                     WHERE cleaned_met_data.department = departments.department
                     AND cleaned_met_data.accession_year = departments.accession_year);

SELECT department, COUNT(*) as object_count
FROM departments
GROUP BY department
ORDER BY object_count DESC;

CREATE INDEX idx_department_id ON cleaned_met_data(department_id);
CREATE INDEX idx_department_id_on_department ON department(department_id);

SELECT COUNT(*) AS number_of_objects
FROM cleaned_met_data cmd
JOIN departments d ON cmd.department_id = d.department_id
WHERE d.accession_year = 1970;


CREATE TABLE `period` (
    `period_id` BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `period` VARCHAR(255),
    `dynasty` VARCHAR(255),
    `reign` VARCHAR(255)
);

INSERT INTO period (period, dynasty, reign)
SELECT DISTINCT period, dynasty, reign
FROM cleaned_met_data;

ALTER TABLE cleaned_met_data
ADD COLUMN period_id BIGINT;

SET SQL_SAFE_UPDATES = 0;

UPDATE cleaned_met_data
SET period_id = (SELECT period_id
                     FROM period
                     WHERE cleaned_met_data.period = period.period
                     AND cleaned_met_data.dynasty = period.dynasty
                     AND cleaned_met_data.reign = period.reign);

CREATE INDEX idx_period_id ON cleaned_met_data(period_id);
CREATE INDEX idx_period_id_on_department ON period(period_id);

# got timeout error on credit line which may have to do with too many characters
CREATE TABLE `credit_line` (
    `credit_line_id` BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `credit_line` VARCHAR(1000)
);

INSERT INTO credit_line (credit_line)
SELECT DISTINCT credit_line
FROM cleaned_met_data;

ALTER TABLE cleaned_met_data
ADD COLUMN credit_line_id BIGINT;

SET SQL_SAFE_UPDATES = 0;

# Credit_line seems to be too big to do this needs more cleaning?
UPDATE cleaned_met_data
SET credit_line_id = (SELECT credit_line_id
                     FROM credit_line
                     WHERE cleaned_met_data.credit_line = credit_line.credit_line);



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

################### ignore this for now####################
CREATE TABLE `object_artist` (
    `object_id` BIGINT NOT NULL,
    `artist_id` BIGINT NOT NULL,
    PRIMARY KEY (`object_id`, `artist_id`),
    FOREIGN KEY (`object_id`) REFERENCES `object` (`object_id`) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (`artist_id`) REFERENCES `artists` (`artist_id`) ON DELETE CASCADE ON UPDATE CASCADE
);

###################################################


