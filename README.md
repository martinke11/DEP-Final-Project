# DEP-Final-Project

Step 1: Use met_cleaning.py and read in MetObjects.csv output to csv named cleaned_data.csv


Step 2: Open met_schema.sql and run these lines at the top:
/*!40101 SET NAMES utf8 */;
/*!40101 SET SQL_MODE=''*/;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`met` /*!40100 DEFAULT CHARACTER SET latin1 */;
use met;



Step 3: Use insert_data_into_sql.py which already is set to read cleaned_data.csv run this file and 
        cleaned_met_data (cleaned_data.csv) will be its own table in met database.
        NOTE: Most likely you will need to install some packages, try running it and then paste the error
              message into ChatGPT and it will tell you what to do.



Step 4: Run the rest of the met_schema.sql script to finish building and populating normalized tables.
