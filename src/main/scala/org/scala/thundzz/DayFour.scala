package org.scala.thundzz

import scala.io.Source
import scala.util.matching.Regex

object DayFour extends App {

  /**
   * Credit : this scala implementation was heavily inspired by @floh0's python solution for this problem.
   * https://github.com/floh0/advent-of-code-2020/blob/master/day4.py
   */

  sealed trait ValidationRule {
    def check(value: String): Boolean
  }

  case class BasicValidationRule(regex: Regex, isValid: String => Boolean) extends ValidationRule {
    def check(value: String): Boolean = regex.matches(value) && isValid(value)
  }

  case object HeightValidationRule extends ValidationRule {
    def check(value: String): Boolean = {
      val heightRegex = """^(\d+)(cm|in)$""".r
      heightRegex.findFirstMatchIn(value).exists(mat => {
        val value = mat.group(1).toInt
        val unit = mat.group(2)
        if (unit == "cm")
          value >= 150 && value <= 193
        else
          value >= 59 && value <= 76
      })
    }
  }

  def parsePassport(rawPassport: String): Map[String, String] = {
    val regex = "([a-z]{3}):([^\\n\\s]+)".r
    regex.findAllMatchIn(rawPassport)
      .map(matchOccurence => {
        matchOccurence.group(1) -> matchOccurence.group(2)
      }).toMap
  }

  def parsePassports(resourcePath: String): Seq[Map[String, String]] = {
    val rawPassports = Source.fromResource(resourcePath).getLines().mkString("\n").split("\n\n")
    rawPassports.map(parsePassport)
  }

  val mandatoryFields: Map[String, ValidationRule] = Map(
    "byr" -> BasicValidationRule("\\d+".r, year => 1920 <= year.toInt && year.toInt <= 2002),
    "iyr" -> BasicValidationRule("\\d+".r, year => 2010 <= year.toInt && year.toInt <= 2020),
    "eyr" -> BasicValidationRule("\\d+".r, year => 2020 <= year.toInt && year.toInt <= 2030),
    "hgt" -> HeightValidationRule,
    "hcl" -> BasicValidationRule("^#[0-9a-f]{6}$".r, _ => true),
    "ecl" -> BasicValidationRule("^(amb|blu|brn|gry|grn|hzl|oth)$".r, _ => true),
    "pid" -> BasicValidationRule("^\\d{9}$".r, _ => true)
  )

  def simpleValidation(passports: Seq[Map[String, String]]): Int = {
    passports.count(p => {
      val passportKeys = p.keys.toSet
      mandatoryFields.keys.forall(passportKeys.contains)
    })
  }

  def fullValidation(passports: Seq[Map[String, String]]): Int = {
    passports.count(p => {
      mandatoryFields.toSeq.forall({
        case (field, validationRule) => p.get(field).exists(validationRule.check)
      })
    })
  }

  val passports = parsePassports("day_04/input.txt")
  
  val simpleValidationCount = simpleValidation(passports)
  val fullValidationCount = fullValidation(passports)
  println(simpleValidationCount)
  println(fullValidationCount)

}

