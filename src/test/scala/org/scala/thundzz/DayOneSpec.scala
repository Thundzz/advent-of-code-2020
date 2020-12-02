package org.scala.thundzz

import org.scalatest.flatspec.AnyFlatSpec
import org.scalatest.matchers.should.Matchers

class DayOneSpec extends AnyFlatSpec with Matchers {
  "Part one example" should "have 514579 as solution" in {
    val exampleExpanseReport = Seq(1721, 979, 366, 299, 675, 1456)
    DayOne.solveFirst(exampleExpanseReport) should be(Some(514579))
  }

  "Part two example" should "have 241861950 as solution" in {
    val exampleExpanseReport = Seq(1721, 979, 366, 299, 675, 1456)
    DayOne.solveSecondQuadratic(exampleExpanseReport) should be(Some(241861950))
  }
}
