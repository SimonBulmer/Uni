# Reference:
# https://www.w3schools.com/python 
# https://youtu.be/qwAFL1597eM?si=Fx9_Dc1Lfv9Oj5d- Python Tutorial for Beginners
# Planet and Moon Information taken from wikipedia - https://en.wikipedia.org/wiki/List_of_gravitationally_rounded_objects_of_the_Solar_System
# Skywatching - The Ultimate Guide to the Universe - David H.Levy (2006) - ISBN 0-00-220028-7
# The Heavens: Planets, Stars, Galaxies - The Leisure Circle Limited (1984)


class Moon:
    '''A class to store some common moons of the planets.
    Should I want to expand the class to contain other data I can easier do so.'''

    moons = []

    def __init__(self, name, planet):
        self.name = name
        self.planet = planet
        Moon.moons.append(self)

    def __str__(self):
        return self.name
    
    def create_moons():
        moon_data = {
            "Earth": ["Moon"],
            "Mars": ["Phobos", "Deimos"],
            "Jupiter": ["Io", "Europa", "Ganymede", "Callisto"],
            "Saturn": ["Titan", "Enceladus","Iapetus"],
            "Uranus": ["Titania", "Oberon", "Umbriel", "Ariel", "Miranda"],
            "Neptune": ["Triton","Nereid", "Proteus"]
        }

        for planet, moon_list in moon_data.items():
            for moon_name in moon_list:
                Moon(moon_name, planet)

class Planet:
    '''This represents the planets in our solar system. It stores the name, mass, distance from the sun and the number of moons.
    It calculates mass relative to Earth and converts the distance from the Sun to miles and AU (Astronomical Units).
    The calculations were left in as the information I used from Wikipedia showed the distance in other units and included the relative earth mass.
    
    known_moons was added as an after thought. The brief states I should list the moons '''
    def __init__(self, name, mass, mass_exponent,distance_from_sun, known_moons):
        self.name = name
        self.mass = mass
        self.mass_exponent = mass_exponent 
        self.distance_from_sun = distance_from_sun
        self.known_moons = known_moons

    def get_moons(self):
        return [moon for moon in Moon.moons if moon.planet == self.name]
    
    def calculate_mass(self):
        mass = self.mass * (10 ** self.mass_exponent) 
        earth_mass = 5.972e24
        relative_mass = mass / earth_mass
        return relative_mass
    
    def display_mass(self):
            print(f"  {self.name} has a mass of {self.mass} x 10^{self.mass_exponent} kg ({self.calculate_mass():.3f} Earths).")

    # Using Wikipedia as a source I saw it mention Miles and AU in the table of distances from the Sun.
    def calculate_distance_from_sun(self):
        miles = self.distance_from_sun * 0.621371
        au = self.distance_from_sun / 149597870.7
        return [miles, au]

    def display_distance_from_sun(self):
        miles, au = self.calculate_distance_from_sun()
        print(f" {self.name} is {self.distance_from_sun:,} km from the Sun. This is the equivalent to {miles:,.2f} miles or {au:,.6f} AU (Astronomical Units)")

    def create_planets():
        
        mercury = Planet("Mercury", 3.302, 23, 57909175, 0)
        venus = Planet("Venus", 4.869, 24, 108208930, 0)
        earth = Planet("Earth", 5.972, 24, 149597890, 1)
        mars = Planet("Mars", 6.419, 23, 227936640, 2)
        jupiter = Planet("Jupiter", 1.898, 27, 778412010, 97)
        saturn = Planet("Saturn", 5.685, 26, 1426725400, 274)
        uranus = Planet("Uranus", 8.684, 25, 2870972200, 28)
        neptune = Planet("Neptune", 1.024, 26, 4498252900, 16)

        return [mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

class Queries:
    '''This handles input queries by checking for keywords in the user input and returning the requested information.'''
    def __init__(self, planets):
        self.planets = planets
        self.planet_dict = {p.name.lower(): p for p in planets}

    # This function displays all the planets and their information in a formatted manner. (I've used this before in other projects and like the way it looks.)
    def display_all_planet_info(self, planet=None):
        try:
            if planet:
                print(f"=" * 90)
                print(f"Planet Information: {planet.name}:")
                print(f"=" * 90)
                print(f"{'Name':<15} {'Mass (kg)':<30} {'Distance (km)':<30} {'Moons':>10}")
                print(f"-" * 90)
                mass_combined = f"{planet.mass} x 10^{planet.mass_exponent}"
                print(f"{planet.name:<15} {mass_combined:<30} {planet.distance_from_sun:<30,} {planet.known_moons:>10}")
                print(f"=" * 90)
            else:
                print(f"=" * 90)
                print(f"Planet Information:")
                print(f"=" * 90)
                print(f"{'Name':<15} {'Mass (kg)':<30} {'Distance (km)':<30} {'Moons':>10}")
                print(f"-" * 90)
                for planet in self.planets:
                    mass_combined = f"{planet.mass} x 10^{planet.mass_exponent}"
                    print(f"{planet.name:<15} {mass_combined:<30} {planet.distance_from_sun:<30,} {planet.known_moons:>10}")
                print(f"=" * 90)
        except Exception as e:
            print(f"Error retrieving planet information: {e}")

    def display_moon_info(self, planet):
        try:
            moon_count = planet.known_moons
            moons = planet.get_moons()
            no_of_moons = "moon" if moon_count == 1 else "moons"
            if moon_count == 0:
                print(f"{planet.name} doesn't have any {no_of_moons}.")
            elif planet.name == "Earth":
                print(f"{planet.name} has {moon_count} {no_of_moons}: We call it The {' '.join(str(m) for m in moons)}.")
            elif moon_count < 3:
                print(f"{planet.name} has {moon_count} {no_of_moons}: Their names are {' and '.join(str(m) for m in moons)}.")
            else:
                print(f"{planet.name} has {moon_count} {no_of_moons}: A selection of common names are {', '.join(str(m) for m in moons)}.")
        except Exception as e:
            print(f"Error retrieving moon information for {planet.name}: {e}")

    # Instead of creating a menu I opted to use keywords to determine what information is returned.
    def user_query(self, query):
        try:
            query = query.lower()
        
            if "quit" in query:
                return "quit"

            elif any (word in query for word in["show all","list all","display all", "list planets"]):
                self.display_all_planet_info()
                return

            for name in self.planet_dict:
                if name in query:
                    planet = self.planet_dict[name]

                    if any (word in query for word in["everything","info","details","notes"]):
                        self.display_all_planet_info(planet)
                        return
                    elif "mass" in query:
                        planet.display_mass()
                        return
                    elif "distance" in query:
                        planet.display_distance_from_sun()
                        return
                    elif "moon" in query:
                        self.display_moon_info(planet)
                        return
                    else:
                        print(f"Can you be more specific. What do you want to know about {planet.name}?")
                        return

            if "pluto" in query:
                print("Pluto is no longer classified as a planet in our solar system.")
                return

            print("I don't understand your query.")
        except Exception as e:
            print(f"An error occurred with your request: {e}.")

# Added the examples set in the Assessment Brief to help prompt users
def user_interface(planets):
    query = Queries(planets)
    print(f"=" * 40)
    print(f"Solar System Information")
    print(f"=" * 40)
    print(f"Example questions:")
    print(f"  - Tell me everything about Saturn")
    print(f"  - How massive is Neptune?")
    print(f"  - How many moons does Earth have?")
    print(f"  - Is Pluto in the list of planets?")
    print(f"  - Show all planets")
    print(f"=" * 40)
    print(f"  - Type Quit to exit the program\n")

    while True:
        user_input = input(": ")
        result = query.user_query(user_input)
        if result == "quit":
            break


if __name__ == "__main__":
    try:
        solar_system = Planet.create_planets()
        Moon.create_moons()
        user_interface(solar_system)
    except KeyboardInterrupt: # added this to handle Ctrl+C with a friendly message instead of Traceback message
        print("\nCtrl+C detected. Exiting...")