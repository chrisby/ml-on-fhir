import requests
from Patient import Patient
from os.path import join

class FHIRClient():
	def __init__(self, service_base_url: str):
		self.server_url = service_base_url

	def _check_status(self, status_code: int):
		return status_code == requests.codes.ok

	def _build_url(self, path: str, **query_params):
		base_url = join(self.server_url, path)
		if query_params:
			base_url += '?'

		for param in query_params.keys():
			base_url += '{}={}&'.format(param, query_params[param])
		return base_url

	def get_capability_statement(self):
		r = requests.get(self._build_url('metadata'))

		if self._check_status(r.status_code):
			return r.json()
		else:
			r.raise_for_status()

	def get_all_patients(self, max_count=100):
		r = requests.get(self._build_url('Patient', _count=max_count))

		if self._check_status(r.status_code):
			return [ Patient(d['resource']) for d in r.json()['entry'] ]
		else:
			r.raise_for_status()


