package org.scala.thundzz

import scala.util.{Failure, Success, Try}

object Helpers {
  def sequence[T](ts: List[Try[T]]): Try[List[T]] = {
    ts.partitionMap(_.toEither) match {
      case (Nil, rights) => Success(rights)
      case (firstLeft :: _, _) => Failure(firstLeft)
    }
  }
}
