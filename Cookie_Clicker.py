"""
 -*- coding: utf-8 -*-
@Date    : 2022-04-18
@Author  : Utkarsh Bardia
Cookie Clicker Simulator
"""

# import user40_lbarkGzPKK_46 as cookie_clicker_testsuite
import poc_clicker_provided as provided
import simpleplot
import math
import random
import codeskulptor
codeskulptor.set_timeout(20)


# Constants
SIM_TIME = 10000000000.0

# -----------------------------------ClickerState Class-------------------


class ClickerState:

    """
    Simple class to keep track of the game state.
    """

    def __init__(self, total_cookies=0, current_cookies=0, current_seconds=0, current_cps=1):
        self._total_cookies = total_cookies
        self._current_cookies = current_cookies
        self._current_seconds = current_seconds
        self._current_cps = current_cps
        self._history = [(0.0, None, 0.0, 0.0)]

    def __str__(self):
        """
        Return human readable state
        """
        history_dict = {'total_cookies': self._total_cookies,
                        'current_cookies': self._current_cookies,
                        'current_seconds': self._current_seconds,
                        'current_cps': self._current_cps}
        string = ""
        for name, value in history_dict.items():
            string += name + ": " + str(value) + " "
        return string + str(self._history)

    def print_history(self):
        """
        human readable print history
        """
        history_dict = {'total_cookies': self._total_cookies,
                        'current_cookies': self._current_cookies,
                        'current_seconds': self._current_seconds,
                        'current_cps': self._current_cps}
        string = "\n----------------------------\n"
        for name, item in history_dict.items():
            space_length = 28 - len(str(name) + ": " + str(item))
            string += str(name) + ": " + str(item) + \
                "|".rjust(space_length) + "\n"
        return string + "----------------------------"

    def get_cookies(self):
        """
        Return current number of total_cookies 
        (not total number of total_cookies)

        Should return a float
        """
        return self._current_cookies

    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps

    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_seconds

    def get_history(self):
        """
        Return history list
        History list should be a list of tuples of the form:
        (time, item, cost of item, total total_cookies)
        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        history_copy = self._history[:]
        return history_copy

    def time_until(self, total_cookies):
        """
        Return time until you have the given number of total_cookies
        (could be 0.0 if you already have enough total_cookies)

        Should return a float with no fractional part
        """
        if self._current_cookies >= total_cookies:
            result = 0.0
        else:
            current_cookies = total_cookies - self._current_cookies
            result = math.ceil(current_cookies / self._current_cps)
        return result

    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time <= 0.0:
            return
        self._current_seconds += time  # time should increase
        # cookies made in given time
        self._current_cookies += time * self._current_cps
        # cookies made in given time
        self._total_cookies += time * self._current_cps

    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state
        Should do nothing if you cannot afford the item
        """
        if cost > self._current_cookies:
            return
        item = (self._current_seconds, item_name, cost, self._total_cookies)
        self._current_cookies -= cost
        self._current_cps += additional_cps
        self._history.append(item)

# -----------------------------------Simulation Functions-----------------


def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.

    1. Check the current time and break out of the loop if the duration has been passed.

    2. Call the strategy function with the appropriate arguments to determine 
    which item to purchase next. If the strategy function returns None, 
    you should break out of the loop, as that means no more items will be purchased.

    3. Determine how much time must elapse until it is possible to purchase the item. 
    If you would have to wait past the duration of the simulation to purchase the item, 
    you should end the simulation.

    4. Wait until that time.

    5. Buy the item.

    6. Update the build information.
    """
    if not strategy:
        return None
    build_info_clone = build_info.clone()
    clicker_state = ClickerState()
    while duration >= clicker_state.get_time():
        total_cookies = clicker_state.get_cookies()
        cps = clicker_state.get_cps()
        history = clicker_state.get_history()
        time_left = duration - clicker_state.get_time()
        item_to_buy = strategy(
            total_cookies, cps, history, time_left, build_info_clone)
        if item_to_buy is None:
            break
        secs_left_to_buy = clicker_state.time_until(
            build_info_clone.get_cost(item_to_buy))
        if duration < clicker_state.get_time() + secs_left_to_buy:
            break

        # 4. Wait until that time
        clicker_state.wait(secs_left_to_buy)
        # 5. Buy the item.
        clicker_state.buy_item(item_to_buy,
                               build_info_clone.get_cost(item_to_buy),
                               build_info_clone.get_cps(item_to_buy))
        # 6. Update the build information.
        build_info_clone.update_item(item_to_buy)

    clicker_state.wait(duration - clicker_state.get_time())

    return clicker_state


def strategy_cursor_broken(total_cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"


def strategy_none(total_cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None


def strategy_cheap(total_cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    # Check if I have enough money to purchase any item
    obj = ClickerState(total_cookies, 0, 0, cps)
    obj.wait(time_left)
    total_cookies += obj.get_cookies()
    cheapest = build_info.build_items()[0]
    for item in build_info.build_items():
        if total_cookies >= build_info.get_cost(item):
            cheapest = item
            break
        else:
            return None

    # Start searching for the cheapest item
    for item in build_info.build_items():
        if total_cookies >= build_info.get_cost(item) < build_info.get_cost(cheapest):
            cheapest = item

    return cheapest


def strategy_expensive(total_cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    obj = ClickerState(total_cookies, 0, 0, cps)
    obj.wait(time_left)
    total_cookies += obj.get_cookies()
    maximum = build_info.build_items()[0]
    for item in build_info.build_items():
        if total_cookies >= build_info.get_cost(item):
            maximum = item
            break
        else:
            return None

    # Start searching for the cheapest item
    for item in build_info.build_items():
        if total_cookies >= build_info.get_cost(item) > build_info.get_cost(maximum):
            maximum = item
    return maximum


def strategy_best(total_cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    # Find all items that are purchasable
    obj = ClickerState(total_cookies, 0, 0, cps)
    obj.wait(time_left)
    total_cookies += obj.get_cookies()
    purchasable_items = filter(
        lambda x: build_info.get_cost(x) < total_cookies, build_info.build_items())
    if not purchasable_items:
        item_to_buy = None
    else:
        item_to_buy = random.choice(purchasable_items)
    return item_to_buy


def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print("Chosen Strategy: " + strategy_name.upper() + "\n" + str(state))


def run():
    """
    Run the simulator.
    """
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Best", SIM_TIME, strategy_best)


run()
