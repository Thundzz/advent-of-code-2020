package org.scala.thundzz

import org.scala.thundzz.DayFive.toIndex
import org.scala.thundzz.DayFour.HeightValidationRule
import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers

class DayFiveSpec extends AnyFlatSpec with Matchers {

  "toIndex" should "of 1000110 should be 70 " in {
    val bsp = List(1, 0, 0, 0, 1, 1, 0)
    toIndex(128, bsp) should be(70)
  }

}
