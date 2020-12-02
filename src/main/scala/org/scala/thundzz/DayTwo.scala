package org.scala.thundzz

import scala.io.Source
import scala.util.matching.Regex
import scala.util.{Failure, Try}

object DayTwo extends App {

  case class Input(fst: Int, snd: Int, char: Char, password: String)

  def parseRecord(line: String): Try[Input] = {
    val Pattern: Regex = "(\\d+)-(\\d+) (\\w): (\\w+)".r
    line match {
      case Pattern(fst, snd, char, password) => Try(Input(fst.toInt, snd.toInt, char(0), password))
      case _ => Failure(new Exception(s"Could not parse row $line"))
    }
  }

  def parseResource(resourcePath: String): Try[List[Input]] =
    Helpers.sequence(Source.fromResource(resourcePath).getLines.map(parseRecord).toList)

  def countCheck(input: Input): Boolean = {
    val counts = input.password.groupBy(identity).mapValues(_.length)
    val mini = input.fst
    val maxi = input.snd
    counts.getOrElse(input.char, 0) >= mini && counts.getOrElse(input.char, 0) <= maxi
  }

  def positionCheck(input: Input): Boolean = {
    val cnt = Seq(input.fst, input.snd)
      .map(_ - 1)
      .map(x => if (input.password(x) == input.char) 1 else 0)
      .sum
    cnt == 1
  }

  def solve(inputs: Seq[Input], solveFnct: Input => Boolean): Int = {
    inputs.count(solveFnct)
  }

  val inputs = parseResource("day_02/input.txt")
  println(inputs.map(inputs => solve(inputs, countCheck)))
  println(inputs.map(inputs => solve(inputs, positionCheck)))

}
