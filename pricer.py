#!/usr/bin/env python3
"""
pricer.py - generates pricing data based on tables

Authors:
  Erick Brown

Copyright:
  2022, Erick Brown

Warranty:
  None - use this software at your own risk!
"""

import mdtable
import rpmath
       

def make_price_list(place_name, tables):
    """
    make_price_list - builds a price list for a specific place

    :param place_name:  The place for which a price list should be generated
    :type place_name: str
    :param tables:      The input tables containing the reference data
    :type tables: dict
    :return:            Returns a dict containing the price data
    :rtype: dict
    """

    place = tables['Places'].find('Name', place_name)
    if place is None:
        raise ValueError("Specified place ('" + place_name + "') was not found")

    override = tables['Availability Probability Overrides'].find(0, place_name)
    
    place_type = tables['Place Types'].find('Name', place['Type'])
    if place_type is None:
        raise ValueError(place_name + " type ('" + place['Type'] + "') was not found")
