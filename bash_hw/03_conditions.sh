#!/bin/bash

# Вводим число
read -p "Введите число: " number


# 1. Проверяем, является ли положительным/отрицательным/нулем
if (( number > 0 )); then
  echo "Число $number положительное"
elif (( number < 0 )); then
  echo "Число $number отрицательное"
else
  echo "Число $number равно нулю"
fi


# 2. Проведем подсчет от 1 до введенного числа (если положительное) 
if (( number > 0 )); then
  echo "Подсчет от 1 до $number:"
  i=1
  while (( i <= number )); do
    echo "$i"
    (( i++ ))
  done
fi