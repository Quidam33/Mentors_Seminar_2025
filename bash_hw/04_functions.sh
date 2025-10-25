#!/bin/bash

# Объявляем функции
hello_prefix() {
  echo "Hello, $1"
}

get_sum() {
  echo "$1 + $2 = $(($1+$2))"
}


# Вызываем функции

string="World"
hello_prefix "$string"

hello_prefix World
get_sum 2 3