/* James Houston
 * Container Orchestrator ©2017
 * create_orchestrator.sql
 * - This script will create the Container Orchestrator tables
 */
 
 /* This statement is used for selecting the Container Orchestrator database
  * Replace <DATABASE> with the database name and uncomment the line to run
  */
# USE <DATABASE>;

/* Create tables */
CREATE TABLE account (
  id SMALLINT NOT NULL AUTO_INCREMENT,
  username VARCHAR(25) NOT NULL,
  password VARCHAR(25) NOT NULL,
  PRIMARY KEY (id)
);
CREATE TABLE container (
  id VARCHAR(100) NOT NULL,
  imageName VARCHAR(100) NOT NULL,
  createdBy SMALLINT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (createdBy) REFERENCES account(id)
);


