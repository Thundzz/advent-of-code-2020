package org.scala.thundzz

import scala.io.Source

object DayOne extends App {

  def solveFirst(numbers: Seq[Int]): Option[Long] = {
    val numbersSet = numbers.toSet
    numbers.view.map(n => {
      val rem = 2020 - n
      (numbersSet.contains(rem), n * rem)
    }).collectFirst({
      case (isValid, result) if isValid => result
    })
  }

  def solveSecondQuadratic(numbers: Seq[Int]): Option[Long] = {
    val numbersSet = numbers.toSet
    val filteredView = for {
      i <- numbers.view
      j <- numbers.view
      k = 2020 - i - j
      if numbersSet.contains(k)
    } yield i.toLong * j * k
    filteredView.headOption
  }

  def parseResource(resourcePath: String): List[Int] =
    Source.fromResource(resourcePath).getLines().map(_.toInt).toList

  val input = parseResource("day_01/input.txt")
  println(solveFirst(input))
  println(solveSecondQuadratic(input))

}
