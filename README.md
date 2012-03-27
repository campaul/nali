# nali

**nali** is a programming language I created for fun. It is largely unfinished,
unstable, and unusable for any real tasks. It is a toy and nothing more.

## Basic Usage

You can perform basic math almost like you would on a calculator,

```
>> 2 + 3
5
```

**nali** uses message passing similar to Smalltalk, so be aware of order of
operations.

```
>> 2 + 3 * 5
25
>> 2 + (3 * 5)
17
```

Messages are identified by a leading period, with preceding whitespace being
optional. `+`,`-`,`*`,`/`, and `%` are just aliases to `.add`, `.sub`, `.mul`,
`.div`, and `.mod`.

```
>> 1 .add 2
3
>> 1.add 2.mul 3
9
```

In the last example, the integer 1 is passed the message `.add`, which returns
the `add` method belonging to it. This method is executed with the argument 2,
which returns the integer 3. This process continues until there are no more
terms remaining in the expression.

Parenthesis represent nested expressions, and can be used to enforce order of
operations or invoke methods that take no arguments. For example, if an object
`foo` had a method `bar` that took no arguments and returned 5:

```
>> foo .bar
[function]
>> (foo .bar)
5
```

## Defining Variables

Most objects execute with one argument, which is either a message or a symbol.
Note: functions are a special type of object that can execute with any numbers of
arguments. Symbols are used to define instance variables of an object, which can
then be accessed by sending the corresponding message.

```
>> foo :bar 5
>> foo .bar
5
```

There is always a reference to the current namespace called `def` which can be
used to define variables.

```
>> def :foo 3
>> foo
3
```

## Functions

Functions are created using literals, and resemble the lambda syntax of Python /
the code blocks of Smalltalk.

```
>> def :increment [|x| x + 1]
>> increment 3
4
```