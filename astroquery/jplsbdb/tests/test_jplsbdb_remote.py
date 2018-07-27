# Licensed under a 3-clause BSD style license - see LICENSE.rst

from astropy.tests.helper import remote_data
import astropy.units as u

from ... import jplsbdb


@remote_data
class TestSBDBClass:

    def test_id_types(self):
        sbdb1 = jplsbdb.SBDB.query('Mommert', id_type='search')
        sbdb2 = jplsbdb.SBDB.query('1998 QS55', id_type='desig')
        sbdb3 = jplsbdb.SBDB.query('2012893', id_type='spk')

        assert sbdb1['object']['fullname'] == '12893 Mommert (1998 QS55)'
        assert sbdb2['object']['fullname'] == '12893 Mommert (1998 QS55)'
        assert sbdb3['object']['fullname'] == '12893 Mommert (1998 QS55)'

    def test_name_search(self):
        sbdb = jplsbdb.SBDB.query('2014 AA1*', id_type='search',
                                  neo_only=True)
        assert sbdb['list']['pdes'] == ['2006 AN', '2014 AA17']

    def test_uri(self):
        sbdb = jplsbdb.SBDB.query('Mommert', id_type='search',
                                  get_uri=True)
        assert sbdb['query_uri'] == ('https://ssd-api.jpl.nasa.gov/sbdb.api'
                                     '?sstr=Mommert')

    def test_array_creation(self):
        sbdb = jplsbdb.SBDB.query('Apophis', id_type='search',
                                  close_approach=True)

        assert (sbdb['ca_data']['jd'].shape[0] > 0 and
                len(sbdb['ca_data']['jd'].shape) == 1)

    def test_units(self):
        sbdb = jplsbdb.SBDB.query('Apophis', id_type='search',
                                  close_approach=True)

        assert sbdb['orbit']['moid_jup'].bases[0] == u.au
        assert sbdb['orbit']['model_pars']['A2'].bases == [u.au, u.d]
        assert sbdb['orbit']['elements']['tp'].bases[0] == u.d
