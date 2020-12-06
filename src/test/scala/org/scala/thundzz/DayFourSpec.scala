package org.scala.thundzz

import org.scala.thundzz.DayFour.HeightValidationRule
import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers

class DayFourSpec extends AnyFlatSpec with Matchers {

  "ParsingFunction" should "properly return all expected fields" in {
    val rawPassport =
      """
        |cid:223 byr:1927
        |hgt:177cm hcl:#602927 iyr:2016 pid:404183620
        |ecl:amb
        |eyr:2020""".stripMargin

    val expectedMap = Map(
      "cid" -> "223", "byr" -> "1927", "hgt" -> "177cm", "hcl" -> "#602927",
      "iyr" -> "2016", "pid" -> "404183620", "ecl" -> "amb", "eyr" -> "2020"
    )

    val parsedMap = DayFour.parsePassport(rawPassport)
    parsedMap should be(expectedMap)
  }

  "HeightValidationRule" should "expect 182cm to be valid" in {
    HeightValidationRule.check("182cm") should be(true)
  }
}
