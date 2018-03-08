import unittest
from mkproject import project

class TestProjectScaffold(unittest.TestCase):
    def setUp(self):
        self.mock_project = (
                {'path': 'some/file', 'data': r'some file bytes'.encode()},
                {'path': 'some/other/file', 'data': r'other file bytes'.encode()}
        )
        self.project = project.ProjectScaffold()
        self.project.register_path(self.mock_project[0]['path'], self.mock_project[0]['data'])
        self.project.register_path(self.mock_project[1]['path'], self.mock_project[1]['data'])
    def test_projectscaffold_data(self):
        item = self.mock_project[0]
        data = self.project.data(item['path'])
        self.assertEqual(data, item['data'])
    def test_projectsccaffold_paths(self):
        expect = (self.mock_project[0]['path'], self.mock_project[1]['path'])
        paths = self.project.paths()
        self.assertTupleEqual(expect, paths)
    def test_projectscaffold_project(self):
        expect = tuple(self.mock_project)
        project = self.project.project()
        self.assertTupleEqual(expect, project)
