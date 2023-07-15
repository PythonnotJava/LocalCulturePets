# I place the algorithm implementation of parts of core functions
from random import choice
from CommonConst import MIN_SINGLE_TALENT_ATTR_VALUE, MAX_SINGLE_TALENT_ATTR_VALUE
from typing import Generator

# If mode is True, ordinary modification will be performed, vice versa.
# The core idea of my algorithm :  every modification has a 50% chance of failure or success
# - The absolute value of each modification is between 0 and 5

# Returns the original, new and changed values of all atributes.
def changeTalents(talents: list[int], mode: bool = True) -> Generator:
    # Return the original, new and changed values of single attribute
    def single_change(cur_talent) -> tuple:
        if mode:
            talents_change = [0, 1, 2, 3, 4, 5, -1, -2, -3, -4, -5]
            _cur_talent = cur_talent + choice(talents_change)
            # Single attribut is reduced or unchanged
            if _cur_talent <= cur_talent:
                return cur_talent, max(MIN_SINGLE_TALENT_ATTR_VALUE, _cur_talent), \
                    max(MIN_SINGLE_TALENT_ATTR_VALUE, _cur_talent) - cur_talent
            # Single attribut is lift
            else:
                return cur_talent, min(MAX_SINGLE_TALENT_ATTR_VALUE, _cur_talent), \
                    min(MAX_SINGLE_TALENT_ATTR_VALUE, _cur_talent) - cur_talent
        else:
            talents_change = [1, 2, 3, 4, 5]
            _cur_talent = cur_talent + choice(talents_change)
            return cur_talent, min(MAX_SINGLE_TALENT_ATTR_VALUE, _cur_talent), \
                min(MAX_SINGLE_TALENT_ATTR_VALUE, _cur_talent) - cur_talent
    # It's a generator
    # Don't use multithread, remember! Remember! Remember!
    # Althrough it drives much more fast deal datas, these attributes are in order, it will lead to out of order input.
    return (single_change(_) for _ in talents)

__all__ = ['changeTalents']

# Conducting a test.
if __name__ == '__main__':
    change = changeTalents([122, 178, 198, 67, 49, 104, 122, 78], True)
    for i in range(8):
        print(next(change))
    for i in range(10):
        _change = 0
        change = changeTalents([122, 178, 198, 67, 49, 104, 122, 78], True)
        for j in range(8):
            print(next(change))
