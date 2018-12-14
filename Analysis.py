import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

data_path = '/home/aftaab/Datasets/exoplanet/oec.csv'
dataset = pd.read_csv(data_path)
sns.set_style('whitegrid')


def dist_vs_method():
	plt.title('Discovery method vs distance from Sun', weight='bold')
	data = dataset[['DiscoveryMethod', 'DistFromSunParsec']]
	ax = sns.boxplot(x='DiscoveryMethod', y='DistFromSunParsec', palette='vlag', data=data)
	ax.set(xlabel='Discovery method', ylabel='Distance from Sun in Parsec')
	plt.show()


def star_mass_vs_method():
	plt.title('Discovery method vs mass of host star', weight='bold')
	data = dataset[['HostStarMassSlrMass', 'DiscoveryMethod']]
	ax = sns.swarmplot(y='HostStarMassSlrMass', x='DiscoveryMethod', data=data)
	ax.set(ylabel='Mass or host star(in solar mass)', xlabel='Discovery method')
	plt.show()


def planet_mass_vs_method():
	sns.set_style('white')
	plt.title('Discovery method vs Planet mass', weight='bold')
	data = dataset[['PlanetaryMassJpt', 'DiscoveryMethod']]
	ax = sns.swarmplot(y='PlanetaryMassJpt', x='DiscoveryMethod', data=data)
	ax.set(ylabel="Planetary mass(in relation to Jupyter's mass(Log Scale)", xlabel='Discovery method')
	ax.set_yscale('log')
	plt.show()

def year_of_discovery():
	sns.set_style('whitegrid')
	plt.title('Frequency of exoplanets discovered by year', weight='bold')
	data = dataset[['DiscoveryYear']].dropna()
	ax = sns.distplot(a=data, kde=False)
	ax.set(ylabel="Year", xlabel='Number of exoplanets discovered')
	plt.show()

