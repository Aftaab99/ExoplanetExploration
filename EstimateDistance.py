from datetime import datetime
import math

"""
	Returns: Mean anamoly of the planet
	n is the daily motion of the planet= 360 * 1/T, where T is the orbital period(days)
	d is the number of days since measurements were
	l is the Longitude
	p is the periastron
	
"""


def calc_mean_anamoly(n, d, l, p):
	return n * d + l - p


def calc_true_anamoly(m, e):
	# Upto 3 terms only
	series = (2 * e - 0.25 * e ** 3) * math.sin(m) + (5 / 4) * e * e * math.sin(2 * m) + (13 / 12) * (
			e ** 3) * math.sin(3 * m)
	return m + series


def calc_position(semi_major_axis, eccentricty, long_asc_node, inclination, periastron, period, date_measurements,
				  mean_long):
	dele = (datetime(2013, 8, 16) - datetime(2000, 1, 1, hour=12)).days
	dpos = (datetime.utcnow() - date_measurements).days
	d = dpos - dele
	n = 360 / period

	mean_anamoly = calc_mean_anamoly(n, d, mean_long, periastron)
	mean_anamoly = mean_anamoly % 360
	true_anamoly = calc_true_anamoly(mean_anamoly, eccentricty)

	# distance of planet from host star at the current time
	radius_vector = semi_major_axis * (1 - eccentricty ** 2) / (1 + eccentricty * math.cos(true_anamoly))
	X = radius_vector * (math.cos(long_asc_node) * math.cos(true_anamoly + periastron - long_asc_node) - math.sin(
		long_asc_node) * math.sin(true_anamoly + periastron - long_asc_node) *
						 math.cos(inclination))
	Y = radius_vector * (math.sin(long_asc_node) * math.cos(true_anamoly + periastron - long_asc_node) + math.cos(
		long_asc_node) * math.sin(true_anamoly + periastron - long_asc_node) *
						 math.cos(inclination))
	Z = radius_vector * (math.sin(true_anamoly + periastron - long_asc_node) * math.sin(inclination))

	# Calculate X, Y, Z for earth
	n_e = 360 / 365.25
	mean_anamoly_e = calc_mean_anamoly(n_e, (datetime.utcnow() - datetime(2000, 1, 1, hour=12)).days, 100.46435,
									   102.94719)
	true_anamoly_e = calc_true_anamoly(mean_anamoly_e, 0.0167)
	X_e = radius_vector * math.cos(true_anamoly_e + 102.94719)
	Y_e = radius_vector * math.sin(true_anamoly_e + 102.94719)
	Z_e = 0

	X_hat = X - X_e
	Y_hat = Y - Y_e
	Z_hat = Z - Z_e

	Xq = X_hat
	Yq = Y_hat * math.cos(eccentricty) - Z_hat * math.sin(eccentricty)
	Zq = Z_hat * math.sin(eccentricty) - Z_hat * math.cos(eccentricty)

	RA = math.atan(Yq / Zq)
	if Xq < 0:
		RA += 180
	elif Xq > 0 and Yq < 0:
		RA += 360

	DEC = math.atan(Zq / (math.sqrt(Xq ** 2 + Yq ** 2)))

	# Expressed in hours
	RA = RA / 15

	# Converting to radians
	RA = RA * math.pi / 180
	DEC = DEC * math.pi / 180

	return {'radius_vector': radius_vector, 'RA': RA, 'DEC': DEC}


def calc_period(semi_major_axis, star_mass):
	return math.sqrt((semi_major_axis ** 3) / star_mass)

def calc_angle(ra1, ra2, dec1, dec2):
	return math.acos(math.sin(dec1)*math.sin(dec2) + math.cos(dec1)*math.cos(dec2)*math.cos(ra1-ra2))