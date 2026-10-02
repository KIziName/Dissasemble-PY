## 🔍 disassemble-PY

Простой инструмент для просмотра байт-кода Python.  

Он компилирует указанный `.py`-файл и показывает, во что Python превращает ваш код перед выполнением.


## 📦 Что это?

Это лёгкая обёртка над встроенным модулем `dis`. Она помогает:

- понять, как работает интерпретатор CPython;
- находить «горячие» места в коде;
- отлаживать неочевидное поведение;
- изучать байт-код для самообразования.


## 🚀 Установка

1. Запустите
2. Напишите названия `.py`
3. Готовый байт-код

## Требования
- ***Python 3.7*** и выше

## Прммер кода (исходник + байт-код)
``` python
def greet(name):
    return f"Hello, {name}!"

print(greet("World"))
```
----

```
  1           0 LOAD_CONST               0 (<code object greet at 0x...>)
              2 LOAD_CONST               1 ('greet')
              4 MAKE_FUNCTION            0
              6 STORE_NAME               0 (greet)

  4           8 LOAD_NAME                1 (print)
             10 LOAD_NAME                0 (greet)
             12 LOAD_CONST               2 ('World')
             14 CALL_FUNCTION            1
             16 CALL_FUNCTION            1
             18 POP_TOP
             20 LOAD_CONST               3 (None)
             22 RETURN_VALUE
```

## 🔍 disassemble-PY

A simple tool for viewing Python bytecode.

It compiles a specified `.py` file and shows what Python turns your code into before execution.


## 📦 What is it?

Is a lightweight wrapper around the built-in `dis` module. It helps you:

- understand how the CPython interpreter works;
- find "hot spots" in your code;
- debug unexpected behavior;
- study bytecode for self‑education.


## 🚀 Installation

1. Run it.
2. Enter the name of the `.py` file.
3. Get the resulting bytecode.

## Requirements

- ***Python 3.7*** and above

## Example code (source + bytecode)
``` python
def greet(name):
    return f"Hello, {name}!"

print(greet("World"))
```
---

```
  1           0 LOAD_CONST               0 (<code object greet at 0x...>)
              2 LOAD_CONST               1 ('greet')
              4 MAKE_FUNCTION            0
              6 STORE_NAME               0 (greet)

  4           8 LOAD_NAME                1 (print)
             10 LOAD_NAME                0 (greet)
             12 LOAD_CONST               2 ('World')
             14 CALL_FUNCTION            1
             16 CALL_FUNCTION            1
             18 POP_TOP
             20 LOAD_CONST               3 (None)
             22 RETURN_VALUE
```
