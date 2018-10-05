#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `menzzasalma_langevin` package."""

import pytest

from click.testing import CliRunner

from Project1/Project1 import menzzasalma_langevin
from menzzasalma_langevin import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'menzzasalma_langevin.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output

def testDragForce(response):
    result = menzzasalma_langevin.dragForce(1,0.1) #testing simple multiplication
    assert result == 0.1
    result2 = menzzasalma_langevin.dragForce(1) #ensuring default value of input is accepted
    assert result2 == 1

def testRandomForce(response):
    result = menzzasalma_langevin.randomForce(0.5) #if temperature is 0.5 and default values accepted, var = 1 and std = 1
    assert result > -4 and result < 4 #with std of 1, normal distribution cenetered at zero should return a value between these bounds

def testIntegrator(response):
    result = menzzasalma_langevin.integrator(timeStep=1,velocity=0,position=0,temperature=0.5)
    assert result[0] < 4 #if initial velocity is zero, then the final velocity is timeStep * randomForce. timeStep is 1, and randomForce should still be less than 4 if T=0.5
    assert result[1] == 0 #the newPosition should be zero, as it starts at 0 and velocity is zero for the first timeStep 

def testParticleMotion(response):
    result = menzzasalma_langevin.particleMotion(1,1,0,0,300) #if the timeStep and timeTotal are equal, it will reach the max number of runs on the first go around, after adding just one set of items
    assert len(result) == 2
    result2 = menzzasalma_langevin.particleMotion(1,100,0,-1,300) #if the starting position is outside the bounds, it will notice after the first loop
    assert len(result2) == 2

