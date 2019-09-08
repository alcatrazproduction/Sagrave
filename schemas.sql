SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
DROP TABLE IF EXISTS `carburant` ;
CREATE TABLE IF NOT EXISTS `carburant` (
  `id` INT(11) NOT NULL,
  `text_f` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`id`));
DROP TABLE IF EXISTS `t_cards` ;
CREATE TABLE IF NOT EXISTS `t_cards` (
  `id` VARCHAR(20) NOT NULL,
  `nom` VARCHAR(45) NULL DEFAULT NULL,
  `vehicule` VARCHAR(45) NULL DEFAULT NULL,
  `no_plaque` VARCHAR(45) NULL DEFAULT NULL,
  `code` VARCHAR(10) NULL DEFAULT NULL,
  `remarque` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`id`));
CREATE UNIQUE INDEX `id_UNIQUE` ON `t_cards` (`id` ASC) VISIBLE;
DROP TABLE IF EXISTS `t_tankdaten` ;
CREATE TABLE IF NOT EXISTS `t_tankdaten` (
  `M27` VARCHAR(150) NOT NULL COMMENT 'original',
  `WA` VARCHAR(6) NULL DEFAULT NULL,
  `STATION` INT(11) NULL DEFAULT NULL,
  `Type_Rec` INT(11) NULL DEFAULT NULL,
  `NTransaction` VARCHAR(4) NULL DEFAULT NULL,
  `BDate` DATE NULL DEFAULT NULL,
  `BTime` TIME NULL DEFAULT NULL,
  `BArt` VARCHAR(2) NULL DEFAULT NULL,
  `Carte` VARCHAR(20) NULL DEFAULT NULL,
  `IDNum` VARCHAR(6) NULL DEFAULT NULL,
  `Montant` FLOAT NULL DEFAULT NULL,
  `TermID` VARCHAR(4) NULL DEFAULT NULL,
  `KM` INT(11) NULL DEFAULT NULL,
  `Billets` FLOAT NULL DEFAULT NULL,
  `ColonneNum` INT(11) NULL DEFAULT NULL,
  `Carburant` INT(11) NULL DEFAULT NULL,
  `Prix` FLOAT NULL DEFAULT NULL,
  `Litres` FLOAT NULL DEFAULT NULL,
  `MontantAuto` FLOAT NULL DEFAULT NULL,
  `CodeFin` VARCHAR(2) NULL DEFAULT NULL,
  PRIMARY KEY (`M27`))i;
CREATE UNIQUE INDEX `M27_UNIQUE` ON `t_tankdaten` (`M27` ASC) VISIBLE;
DROP function IF EXISTS `sagrave_ouchy`.`calcul_total_card`;

DELIMITER $$
USE `sagrave_ouchy`$$
CREATE DEFINER=`root`@`localhost` FUNCTION `calcul_total_card`(card VARCHAR(20), ds DATE, df DATE ) RETURNS float
    DETERMINISTIC
BEGIN
DECLARE bDone INT;
DECLARE tot,val FLOAT;
DECLARE curs CURSOR FOR SELECT Litres FROM t_tankdaten WHERE Carte LIKE card AND BDate BETWEEN ds AND df;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET bDone = 1;
SET tot = 0;
SET bDone = 0;
OPEN curs;

  REPEAT
    FETCH curs INTO val;
    IF NOT bDone THEN
		SET tot = tot + val;
	END IF;
  UNTIL bDone END REPEAT;

  CLOSE curs;

RETURN tot;
END$$

DELIMITER ;

-- -----------------------------------------------------
-- function decode_memopass
-- -----------------------------------------------------

USE `sagrave_ouchy`;
DROP function IF EXISTS `sagrave_ouchy`.`decode_memopass`;

DELIMITER $$
USE `sagrave_ouchy`$$
CREATE DEFINER=`root`@`localhost` FUNCTION `decode_memopass`(iso varchar(20), wa varchar(6) ) RETURNS int(11)
    DETERMINISTIC
BEGIN
declare card VARCHAR(12);
IF MID(iso,1,6) LIKE wa THEN
	SET card = MID( iso, 7 ,12);
	RETURN CAST( card AS SIGNED INTEGER);
END IF;
RETURN -1;
END$$

DELIMITER ;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
