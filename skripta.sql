-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema lov_stranica
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema lov_stranica
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `lov_stranica` DEFAULT CHARACTER SET utf8mb3 ;
USE `lov_stranica` ;

-- -----------------------------------------------------
-- Table `lov_stranica`.`admin`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `lov_stranica`.`admin` (
  `id_admin` INT NOT NULL AUTO_INCREMENT,
  `korisnicko` VARCHAR(45) NOT NULL,
  `ime` VARCHAR(45) NOT NULL,
  `prezime` VARCHAR(45) NOT NULL,
  `email` VARCHAR(50) NOT NULL,
  `sifra` VARCHAR(45) NOT NULL,
  `aktivan` TINYINT(1) NULL DEFAULT '0',
  PRIMARY KEY (`id_admin`))
ENGINE = InnoDB
AUTO_INCREMENT = 13
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `lov_stranica`.`oruzje`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `lov_stranica`.`oruzje` (
  `id_oruzje` INT NOT NULL AUTO_INCREMENT,
  `model` VARCHAR(45) NOT NULL,
  `opis` VARCHAR(5000) NOT NULL,
  `slika` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`id_oruzje`))
ENGINE = InnoDB
AUTO_INCREMENT = 8
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `lov_stranica`.`podrucje`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `lov_stranica`.`podrucje` (
  `id_podrucje` INT NOT NULL AUTO_INCREMENT,
  `naziv` VARCHAR(45) NOT NULL,
  `opis` VARCHAR(5000) NOT NULL,
  `slika` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`id_podrucje`))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `lov_stranica`.`vozilo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `lov_stranica`.`vozilo` (
  `id_vozila` INT NOT NULL AUTO_INCREMENT,
  `model` VARCHAR(45) NOT NULL,
  `opis` VARCHAR(5000) NULL DEFAULT NULL,
  `slika` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`id_vozila`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `lov_stranica`.`zivotinja`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `lov_stranica`.`zivotinja` (
  `id_zivotinja` INT NOT NULL AUTO_INCREMENT,
  `vrsta` VARCHAR(45) NOT NULL,
  `opis` VARCHAR(5000) NOT NULL,
  `slika` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`id_zivotinja`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `lov_stranica`.`zivotinja_has_podrucje`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `lov_stranica`.`zivotinja_has_podrucje` (
  `zivotinja_id_zivotinja` INT NOT NULL,
  `podrucje_id_podrucje` INT NOT NULL,
  PRIMARY KEY (`zivotinja_id_zivotinja`, `podrucje_id_podrucje`),
  INDEX `fk_zivotinja_has_podrucje_podrucje1_idx` (`podrucje_id_podrucje` ASC) VISIBLE,
  INDEX `fk_zivotinja_has_podrucje_zivotinja1_idx` (`zivotinja_id_zivotinja` ASC) VISIBLE,
  CONSTRAINT `fk_zivotinja_has_podrucje_podrucje1`
    FOREIGN KEY (`podrucje_id_podrucje`)
    REFERENCES `lov_stranica`.`podrucje` (`id_podrucje`),
  CONSTRAINT `fk_zivotinja_has_podrucje_zivotinja1`
    FOREIGN KEY (`zivotinja_id_zivotinja`)
    REFERENCES `lov_stranica`.`zivotinja` (`id_zivotinja`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
