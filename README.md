# DEP-Final-Project

In this project we designed and implemented a comprehensive data schema using relational database management system (RDBMS) MySQL to streamline the organization of The Metropolitan Museum of Art’s extensive artwork database (500,000+ objects), enhancing data accessibility and integrity for varied analytical applications.

[Project Presentation](https://github.com/martinke11/DEP-Final-Project/blob/main/met_ppt.pdf)

Link to MetObject.csv (too big to commit to github): https://drive.google.com/file/d/1S7oVC6e0PW1r2-0uraRzGeE9vtlwODxO/view?usp=sharing

Step 1: Use met_cleaning.py and read in MetObjects.csv output to csv named cleaned_data_with_ids.csv


Step 2: Open met_schema.sql and run these lines at the top:
/*!40101 SET NAMES utf8 */;
/*!40101 SET SQL_MODE=''*/;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`met` /*!40100 DEFAULT CHARACTER SET latin1 */;
use met;


Step 3: Use insert_data_into_sql.py which already is set to read cleaned_data_with_ids.csv run this file and 
        cleaned_met_data_with_ids (cleaned_data_with_ids.csv) will be its own table in met database.


Step 4: Run the rest of the met_schema_final.sql script to finish building and populating normalized tables.
