import math
from datetime import datetime


class SunPos:

    radius_of_earth = 6371  # km
    height_of_atmosphere_eff = 9  # km
    ratio = round(radius_of_earth / height_of_atmosphere_eff)
    earth_atmosphere = 1353  # kW/m²

    def __init__(
        self,
        moment: datetime = datetime.now(),
        location: tuple = (33.6, 10.8),
        timezone: int = 1,
        refraction: bool = False,
    ) -> None:
        self.time = moment.time()
        self.date = moment.date()
        self.timezone = timezone
        self.location = location
        self.refraction = refraction

    def getpos(self) -> tuple:
        # main calculation of sun posistion base on  John Clark Craig  code . see following link
        # https://levelup.gitconnected.com/python-sun-position-for-solar-energy-and-research-7a4ead801777

        # Extract the passed data
        year = self.date.year
        month = self.date.month
        day = self.date.day
        hour = self.time.hour
        minute = self.time.minute
        second = self.time.second
        timezone = self.timezone
        latitude, longitude = self.location

        # Math typing shortcuts
        rad, deg = math.radians, math.degrees
        sin, cos, tan = math.sin, math.cos, math.tan
        asin, atan2 = math.asin, math.atan2

        # Convert latitude and longitude to radians
        rlat = rad(latitude)
        rlon = rad(longitude)

        # Decimal hour of the day at Greenwich
        greenwichtime = hour - timezone + minute / 60 + second / 3600

        # Days from J2000, accurate from 1901 to 2099
        daynum = (
            367 * year
            - 7 * (year + (month + 9) // 12) // 4
            + 275 * month // 9
            + day
            - 730531.5
            + greenwichtime / 24
        )

        # Mean longitude of the sun
        mean_long = daynum * 0.01720279239 + 4.894967873  # Mean anomaly of the Sun
        mean_anom = daynum * 0.01720197034 + 6.240040768  # Ecliptic longitude of the sun
        eclip_long = (
            mean_long + 0.03342305518 * sin(mean_anom) + 0.0003490658504 * sin(2 * mean_anom)
        )

        # Obliquity of the ecliptic
        obliquity = 0.4090877234 - 0.000000006981317008 * daynum

        # Right ascension of the sun
        rasc = atan2(cos(obliquity) * sin(eclip_long), cos(eclip_long))

        # Declination of the sun
        decl = asin(sin(obliquity) * sin(eclip_long))

        # Local sidereal time
        sidereal = 4.894961213 + 6.300388099 * daynum + rlon

        # Hour angle of the sun
        hour_ang = sidereal - rasc  # Local elevation of the sun
        elevation = asin(sin(decl) * sin(rlat) + cos(decl) * cos(rlat) * cos(hour_ang))

        # Local azimuth of the sun
        azimuth = atan2(
            -cos(decl) * cos(rlat) * sin(hour_ang),
            sin(decl) - sin(rlat) * sin(elevation),
        )

        # Convert azimuth and elevation to degrees
        azimuth = self.into_range(deg(azimuth), 0, 360)
        elevation = self.into_range(deg(elevation), -180, 180)

        # Refraction correction (optional)
        if self.refraction:
            targ = rad((elevation + (10.3 / (elevation + 5.11))))
            elevation += (1.02 / tan(targ)) / 60

        # Return azimuth and elevation in degrees
        return azimuth, elevation

    def into_range(self, x, range_min, range_max):
        shiftedx = x - range_min
        delta = range_max - range_min
        return (((shiftedx % delta) + delta) % delta) + range_min

    # calculatin of air mass
    def amcalc(self, elevation: float) -> float:

        am = math.sqrt(
            math.pow(self.ratio * math.cos(math.radians(90 - elevation)), 2) + 2 * self.ratio + 1
        ) - self.ratio * math.cos(math.radians(90 - elevation))

        return am

    # calculation of sun intensity
    def solint(self, airmass: float) -> float:

        return 1.1 * self.earth_atmosphere * 0.7**airmass**0.678
