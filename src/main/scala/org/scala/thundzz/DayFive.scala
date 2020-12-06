package org.scala.thundzz

import scala.annotation.tailrec
import scala.io.Source

object DayFive extends App {

  case class SeatPosition(raw: String, row: List[Int], column: List[Int]) {
    def seatId: Int = {
      toIndex(math.pow(2, row.length).toInt, row) * 8 + toIndex(math.pow(2, column.length).toInt, column)
    }
  }

  def parse(resourcePath: String): Seq[SeatPosition] = {
    val toBit = (c: Char) => if (Set('F', 'L').contains(c)) 0 else 1
    Source.fromResource(resourcePath).getLines().map(line => {
      val row = line.slice(0, 7).map(toBit).toList
      val col = line.slice(7, line.length).map(toBit).toList
      SeatPosition(line, row, col)
    }).toList
  }

  def toIndex(size: Int, bsp: List[Int]): Int = {
    @tailrec
    def go(mini: Int, maxi: Int, mapping: List[Int]): Int = {
      val middle = (mini + maxi) / 2
      mapping match {
        case Nil => mini
        case 0 :: t => go(mini, middle, t)
        case 1 :: t => go(middle + 1, maxi, t)
      }
    }

    go(0, size - 1, bsp)
  }

  def findEmpty(seatIds: Seq[Int]): Option[Int] = {
    val emptySeats = (1 to seatIds.max).toSet.diff(seatIds.toSet)
    emptySeats.find(s => !emptySeats.contains(s - 1) && !emptySeats.contains(s + 1))
  }

  val seatPositions = parse("day_05/input.txt")
  val seatIds: Seq[Int] = seatPositions.map(_.seatId)
  println(seatIds.max)
  println(findEmpty(seatIds))
}

