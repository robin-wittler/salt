# -*- coding: utf-8 -*-

# Import Salt Testing libs
from salttesting.helpers import (
    ensure_in_syspath,
    requires_network
)
ensure_in_syspath('../../')

# Import salt libs
import integration


class PillarModuleTest(integration.ModuleCase):
    '''
    Validate the pillar module
    '''
    def test_data(self):
        '''
        pillar.data
        '''
        grains = self.run_function('grains.items')
        pillar = self.run_function('pillar.data')
        self.assertEqual(pillar['os'], grains['os'])
        self.assertEqual(pillar['monty'], 'python')
        if grains['os'] == 'Fedora':
            self.assertEqual(pillar['class'], 'redhat')
        else:
            self.assertEqual(pillar['class'], 'other')

    @requires_network()
    def test_two_ext_pillar_sources_override(self):
        '''
        https://github.com/saltstack/salt/issues/12647
        '''

        self.assertEqual(
            self.run_function('pillar.data')['info'],
            'bar'
        )

    @requires_network()
    def test_two_ext_pillar_sources(self):
        '''
        https://github.com/saltstack/salt/issues/12647
        '''

        self.assertEqual(
            self.run_function('pillar.data')['abc'],
            'def'
        )

    def test_issue_5449_report_actual_file_roots_in_pillar(self):
        '''
        pillar['master']['file_roots'] is overwritten by the master
        in order to use the fileclient interface to read the pillar
        files. We should restore the actual file_roots when we send
        the pillar back to the minion.
        '''
        self.assertIn(
            integration.TMP_STATE_TREE,
            self.run_function('pillar.data')['master']['file_roots']['base']
        )

    def test_ext_cmd_yaml(self):
        '''
        pillar.data for ext_pillar cmd.yaml
        '''
        self.assertEqual(
                self.run_function('pillar.data')['ext_spam'], 'eggs'
                )

    def test_issue_5951_actual_file_roots_in_opts(self):
        self.assertIn(
            integration.TMP_STATE_TREE,
            self.run_function('pillar.data')['test_ext_pillar_opts']['file_roots']['base']
        )

if __name__ == '__main__':
    from integration import run_tests
    run_tests(PillarModuleTest)
