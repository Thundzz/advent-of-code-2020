package org.scala.thundzz

import scala.io.Source

object DayThree extends App {

  object Mountain {
    def fromResource(resourcePath: String): Mountain = {
      new Mountain(Source.fromResource(resourcePath).getLines().toList.map(_.toCharArray).toArray)
    }
  }

  class Mountain(grid: Array[Array[Char]]) {
    require(grid.length > 0)

    val height: Int = grid.length
    val width: Int = grid(0).length

    def hasTree(p: Position): Boolean = grid(p.i)(p.j % width) == '#'
  }

  case class Slope(di: Int, dj: Int)

  case class Position(i: Int, j: Int) {
    def after(iteration: Int, slope: Slope): Position =
      Position(i + iteration * slope.di, j + iteration * slope.dj)
  }

  def countTreeOccurences(mountain: Mountain, slope: Slope): Long = {
    val initialPosition = Position(0, 0)
    (1 until (mountain.height / slope.di))
      .map(x => initialPosition.after(x, slope))
      .count(mountain.hasTree)
  }

  val mountain = Mountain.fromResource("day_03/input.txt")
  val slopes: Seq[Slope] = Seq(Slope(1, 1), Slope(1, 3), Slope(1, 5), Slope(1, 7), Slope(2, 1))

  val treeOccurences = slopes.map(countTreeOccurences(mountain, _))
  println(treeOccurences)
  println(treeOccurences.product)

}
