# Reference:

# https://docs.pytest.org/en/stable/contents.html - pytest documentation
# https://docs.pytest.org/en/stable/reference/reference.html#capsys - Capturing output
# https://docs.pytest.org/en/stable/how-to/capture-stdout-stderr.html#captures
# https://stackoverflow.com/questions/70801967/fixture-not-found-pytest - How to use fixtures in pytest after receiving "E       fixture 'setup_solar_system' not found" error
# https://docs.pytest.org/en/stable/reference/reference.html#pytest.approx - Comparison of floating point numbers
# https://docs.pytest.org/en/stable/how-to/parametrize.html - parameterizing tests


import pytest
from solar_system import Planet, Moon, Queries

@pytest.fixture
def setup_solar_system():
    Moon.moons = []  # Added to reset the moons list as I found the moons_output test fails because it contains data from previous tests.
    planets = Planet.create_planets()
    Moon.create_moons()
    return planets

# Tests to ensure the correct information is displayed about Saturn
def test_query_moon_output(capsys, setup_solar_system):
    q = Queries(setup_solar_system)
    q.user_query("Tell me everything about Saturn?")
    out = capsys.readouterr().out
    assert "Saturn" in out
    assert "5.685 x 10^26" in out
    assert "1,426,725,400" in out
    assert "274" in out

def test_query_mass_output(capsys, setup_solar_system):
    q = Queries(setup_solar_system)
    q.user_query("How massive is Neptune?")
    out = capsys.readouterr().out
    assert "Neptune has a mass of" in out

# Tests the output of a question benig asked about Pluto
def test_query_pluto_output(capsys, setup_solar_system):
    q = Queries(setup_solar_system)
    q.user_query("Is Pluto in the list of planets?")
    out = capsys.readouterr().out
    assert "Pluto" in out

# Test for Pluto not being in the list of planets
def test_pluto_in_planets(setup_solar_system):
    assert not any(planet.name.lower() == "pluto" for planet in setup_solar_system)

# Does the Earth have 1 moon? And does it return the correct name?
def test_query_moons_output(setup_solar_system):
    earth = next(p for p in setup_solar_system if p.name == "Earth")
    moons = earth.get_moons()
    assert len(moons) == 1
    assert moons[0].name == "Moon"

# Malformed, whitespace, empty, 
@pytest.mark.parametrize("user_input", [
    "#$fcvdg%^",
    " ", 
    "",
    ])
def test_query_invalid_input(capsys, setup_solar_system, user_input):
    q = Queries(setup_solar_system)
    q.user_query(user_input)
    out = capsys.readouterr().out
    assert "I don't understand your query." in out

# Testing my calculation function for Miles and AU
def test_distance_conversion(setup_solar_system):
    earth = Planet("Earth", 5.972, 24, 149597890, 1)
    miles, au = earth.calculate_distance_from_sun()
    assert miles == pytest.approx(92955790.51)
    assert au == pytest.approx(1.000000)

