package org.scala.thundzz

import org.scala.thundzz.DayTwo.Input
import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers

class DayTwoSpec extends AnyFlatSpec with Matchers {
  "countCheck" should "consider 1-3 a: abcde valid" in {
    val input = Input(1, 3, 'a', "abcde")
    DayTwo.countCheck(input) should be(true)
  }

  it should "consider 2-9 c: ccccccccc valid" in {
    val input = Input(2, 9, 'c', "ccccccccc")
    DayTwo.countCheck(input) should be(true)
  }

  it should "consider 1-3 b: cdefg invalid" in {
    val input = Input(1, 3, 'b', "cdefg")
    DayTwo.countCheck(input) should be(false)
  }

  "positionCheck" should "consider 1-3 a: abcde valid" in {
    val input = Input(1, 3, 'a', "abcde")
    DayTwo.positionCheck(input) should be(true)
  }

  it should "consider 2-9 c: ccccccccc invalid" in {
    val input = Input(2, 9, 'c', "ccccccccc")
    DayTwo.positionCheck(input) should be(false)
  }

  it should "consider 1-3 b: cdefg invalid" in {
    val input = Input(1, 3, 'b', "cdefg")
    DayTwo.positionCheck(input) should be(false)
  }

}
