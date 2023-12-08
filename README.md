# EV Charge Station Optimizer

## Purpose

This project uses machine learning optimization techniques and the Google Maps API to find the ideal location for new electric vehicle charging infrastructure.

## Data Sources
Starting data points come from several sources:

#### [AAA EVs Out of Charge data](https://autoinsights.aaa.biz/products/evs-out-of-charge)
First, specifically targeting places where their customers have had to call for assistance due to an out-of-charge incident.

#### [EVRI eRoadMap](https://eroadmap.epri.com/)

An interactive map showing where electricity infrastructure is needed to accomodate full electrification of all vehicles by 2030. According to their [FAQ](https://eroadmap.epri.com/docs/eRoadMAP_FAQs_F_11172023.pdf):

> This tool reflects a combination of both high-confidence data sources and simulations of expected adoption. As EPRI gathers more and more data, the confidence in the
energy estimates at each hexagon will rise. It should also be noted that generally as one zooms in to smaller and smaller hexagons, the certainty will decrease as the data is
reliant on the behavior of fewer vehicles rather than an aggregated number"

#### Google Maps [Places](https://developers.google.com/maps/documentation/places/web-service/?apix=true) and [Routes](https://developers.google.com/maps/documentation/routes) APIs

#### [U.S. Dept of Energy Alternative Fuels Data Center](https://developer.nrel.gov/docs/transportation/alt-fuel-stations-v1/nearest/)

The AFDC has an [interactive map](https://afdc.energy.gov/fuels/electricity_locations.html#/find/route?fuel=ELEC&start=wenatchee,%20wa&end=spokane,%20wa) showing nearest stations along a route. This is also available via API so it can be referenced as a test validation for the results found above via Google Maps API.

## Getting Started

#### Installation of Python Packages

Uses [Poetry](https://python-poetry.org/docs/basic-usage/) for dependency management. See a good write-up to justify why I chose this on [Medium here](https://pub.towardsai.net/forget-pip-conda-requirements-txt-use-poetry-instead-and-thank-me-later-226a0bc38a56).