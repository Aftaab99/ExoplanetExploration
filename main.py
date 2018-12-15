from flask import Flask, render_template, request, jsonify
import os
from EstimateDistance import calc_position, calc_period, calc_angle
import pandas as pd
from datetime import datetime
import numpy as np

app = Flask(__name__)

ASSETS_FOLDER = os.path.join(os.path.dirname(__file__), 'static/assets/')


@app.route('/', methods=['GET'])
def home():
	return render_template('index.html')


@app.route('/distance', methods=['POST'])
def distance():
	planet_name = request.form.get('PlanetName').strip()
	dataset_path = os.path.join(ASSETS_FOLDER, 'oec.csv')
	dataset = pd.read_csv(dataset_path)
	res = {'error': 1, 'distance': -1}
	for index, row in dataset.iterrows():
		if planet_name.lower() == row['PlanetIdentifier'].lower():
			if row['DistFromSunParsec'] is not None:
				res['error'] = 0
				res['distance'] = row['DistFromSunParsec']
			break
	return jsonify(res)


@app.route('/orbit_position_present', methods=['POST'])
def orbit_position_present():
	planet_name = request.form.get('PlanetName').strip()
	dataset_path = os.path.join(ASSETS_FOLDER, 'oec.csv')
	dataset = pd.read_csv(dataset_path)
	res = {'error': 1}
	for index, row in dataset.iterrows():
		if planet_name.lower() == row['PlanetIdentifier'].lower():
			# Converting AU to metre
			a = row['SemiMajorAxisAU'] * 1.496e+11
			ecc = row['Eccentricity']
			long_asc_node = row['AscendingNodeDeg']
			inc = row['InclinationDeg']
			arg_per = row['PeriastronDeg']
			period = row['PeriodDays']
			date_measured = datetime.strptime(row['LastUpdated'], '%d/%m/%y')
			mean_long = row['LongitudeDeg']

			orbital_elements = calc_position(a, ecc, long_asc_node, inc, arg_per, period, date_measured, mean_long)
			res['error'] = 0
			res['radius_vector'] = orbital_elements['radius_vector'] / 1.496e+11
			res['RA'] = orbital_elements['RA']
			res['DEC'] = orbital_elements['DEC']

			break
	return jsonify(res)


@app.route('/orbit_position_other', methods=['POST'])
def orbit_position_other():
	dataset_path = os.path.join(ASSETS_FOLDER, 'oec.csv')
	res = {'error': 1}
	try:
		a = float(request.form.get('semi-major-axis').strip()) * 1.496e+11
		ecc = float(request.form.get('eccentricity').strip())
		long_asc_node = float(request.form.get('ascending-node').strip())
		inc = float(request.form.get('inclination').strip())
		arg_per = float(request.form.get('periastron').strip())
		period = float(request.form.get('period').strip())
		date_measured = datetime.strptime(request.form.get('dates').strip(), '%d/%m/%y')
		mean_long = float(request.form.get('mean_long_degrees').strip())
		orbital_elements = calc_position(a, ecc, long_asc_node, inc, arg_per, period, date_measured, mean_long)
		res['error'] = 0
		res['radius_vector'] = orbital_elements['radius_vector'] / 1.496e+11
		res['RA'] = orbital_elements['RA']
		res['DEC'] = orbital_elements['DEC']
	except Exception as e:
		print(e)
	finally:
		return jsonify(res)


@app.route('/orbital_period', methods=['POST'])
def orbital_period():
	a = float(request.form.get('semi-major-axis').strip())
	slrmass = float(request.form.get('mass').strip())
	# Converting period to days
	res = {'orbital_period': calc_period(a, slrmass) * 365.25}
	return jsonify(res)


@app.route('/search_hints', methods=['GET'])
def search_hints():
	print('Request made')
	query = request.args.get('query')
	dataset_path = os.path.join(ASSETS_FOLDER, 'oec.csv')
	data = pd.read_csv(dataset_path)
	res = []
	for index, row in data.iterrows():
		if (row['PlanetIdentifier'].lower()).startswith(query.lower()):
			res.append(row['PlanetIdentifier'])
	return jsonify(res)


@app.route('/search_results', methods=['GET'])
def search_results_get():
	return render_template('search.html')


@app.route('/search_results', methods=['POST'])
def search_results():
	query = request.form.get('search-field')
	dataset_path = os.path.join(ASSETS_FOLDER, 'oec.csv')
	data = pd.read_csv(dataset_path)
	for index, row in data.iterrows():
		if (row['PlanetIdentifier'].lower()) == query.lower():
			pn = row['PlanetIdentifier']
			pt = row['TypeFlag']
			pm = validate_nan(row['PlanetaryMassJpt'])
			pr = validate_nan(row['RadiusJpt'])
			pp = validate_nan(row['PeriodDays'])
			pa = validate_nan(row['SemiMajorAxisAU'])
			pe = validate_nan(row['Eccentricity'])
			pk = validate_nan(row['SurfaceTempK'])

			if pt == 0:
				pt = 'Non binary(no known stellar binary companion)'
			elif pt == 1:
				pt = 'Circumbinary planet'
			elif pt == 2:
				pt = 'S-type binary'
			else:
				pt = 'Orphan planet(planet with no host star)'

			return render_template('search.html', planet_name=pn, planet_type=pt, planet_mass=pm, planet_radius=pr,
								   planet_period=pp, planet_sma=pa, planet_ecc=pe, planet_temp=pk)
	return render_template('not_found.html')


@app.route('/angle', methods=['POST'])
def angle():
	ra1 = list(map(float, request.form.get('ra_1').split(' ')))
	ra2 = list(map(float, request.form.get('ra_2').split(' ')))
	dec1 = list(map(float, request.form.get('dec_1').split(' ')))
	dec2 = list(map(float, request.form.get('dec_2').split(' ')))

	ra_1_d = ra1[0] * 15 + ra1[1] / 4 + ra1[2] / 240
	ra_2_d = ra2[0] * 15 + ra2[1] / 4 + ra2[2] / 240
	dec_1_d = dec1[0] + dec1[1] / 60 + dec1[2] / 3600
	dec_2_d = dec2[0] + dec2[1] / 60 + dec2[2] / 3600

	theta = calc_angle(ra_1_d, ra_2_d, dec_1_d, dec_2_d)
	return jsonify({'angle': theta})


def validate_nan(x):
	if np.isnan(x):
		return 'Not present in dataset'
	else:
		return x


if __name__ == '__main__':
	app.run(debug=True)
