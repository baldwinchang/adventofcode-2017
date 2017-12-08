__author__ = 'Baldwin Chang'

"""
--- Day 8: I Heard You Like Registers ---

You receive a signal directly from the CPU. Because of your recent assistance with jump instructions, it would like you to compute the result of a series of unusual register instructions.

Each instruction consists of several parts: the register to modify, whether to increase or decrease that register's value, the amount by which to increase or decrease it, and a condition. If the condition fails, skip the instruction without modifying the register. The registers all start at 0. The instructions look like this:

b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10
These instructions would be processed as follows:

Because a starts at 0, it is not greater than 1, and so b is not modified.
a is increased by 1 (to 1) because b is less than 5 (it is 0).
c is decreased by -10 (to 10) because a is now greater than or equal to 1 (it is 1).
c is increased by -20 (to -10) because c is equal to 10.
After this process, the largest value in any register is 1.

You might also encounter <= (less than or equal to) or != (not equal to). However, the CPU doesn't have the bandwidth to tell you what all the registers are named, and leaves that to you to determine.

What is the largest value in any register after completing the instructions in your puzzle input?
"""

"""
--- Part Two ---

To be safe, the CPU also needs to know the highest value held in any register during this process so that it can decide how much memory to allocate to these operations. For example, in the above instructions, the highest value ever held was 10 (in register c after the third instruction was evaluated).
"""


class Instruction:

    def __init__(self, register_to_modify, operator, amount, comparison):
        self.register_to_modify = register_to_modify
        self.operator = operator
        self.amount = amount
        self.comparison = comparison

    def evaluate(self, registry):
        if registry.evaluate_comparison(self.comparison):
            registry_value = registry.get(self.register_to_modify)

            if self.operator == 'inc':
                registry.set(self.register_to_modify, registry_value + self.amount)
            elif self.operator == 'dec':
                registry.set(self.register_to_modify, registry_value - self.amount)

    @classmethod
    def from_input(cls, s):
        instruction, comparison = s.split(' if ')

        register_to_modify, operator, amount = instruction.split(' ')
        register_to_check, comparator, value = comparison.split(' ')

        return cls(register_to_modify, operator, int(amount), Comparison(register_to_check, comparator, int(value)))


class Comparison:

    def __init__(self, register_to_check, comparator, value):
        self.register_to_check = register_to_check
        self.comparator = comparator
        self.value = value


class Registry:

    def __init__(self):
        self._registry = dict()
        self.highest_value = None

    def get(self, block):
        rv = self._registry.get(block)
        # Insert block into registry
        if self._registry.get(block) is None:
            rv = self._registry[block] = 0
        return rv

    def set(self, block, value):
        self._registry[block] = value

        # Keep record of the highest value
        if self.highest_value is None or self.highest_value < value:
            self.highest_value = value

    def evaluate_comparison(self, comparison):
        register_value = self.get(comparison.register_to_check)

        if comparison.comparator == '==':
            return register_value == comparison.value
        elif comparison.comparator == '!=':
            return register_value != comparison.value
        elif comparison.comparator == '>=':
            return register_value >= comparison.value
        elif comparison.comparator == '<=':
            return register_value <= comparison.value
        elif comparison.comparator == '>':
            return register_value > comparison.value
        elif comparison.comparator == '<':
            return register_value < comparison.value

    def get_largest_value(self):
        return max(value for value in self._registry.values())


with open('puzzle_input.txt') as f:
    puzzle_input = f.read().split('\n')


instructions = [Instruction.from_input(line) for line in puzzle_input]
registry = Registry()

for instruction in instructions:
    instruction.evaluate(registry)

print(registry.get_largest_value(), registry.highest_value)