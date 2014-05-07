import os

from ..utils import check_command
from ..utils import temporary_directory

this_dir = os.path.abspath(os.path.dirname(__file__))


def test_normative_case():
    # Build the normal packages and install them to a prefix for testing
    with temporary_directory() as temp_dir:
        build_dirs = os.path.join(temp_dir, 'build_dirs')
        install_dir = os.path.join(temp_dir, 'install')
        install_option = '-DCMAKE_INSTALL_PREFIX=' + install_dir
        fixture_dir = os.path.join(this_dir, 'fixtures', 'normative')
        # Build the package_resource_indexer and install it
        pri_build_dir = os.path.join(build_dirs, 'pri')
        os.makedirs(pri_build_dir)
        cmd = ['cmake', os.path.join(this_dir, '..', '..'), install_option]
        check_command(cmd, cwd=pri_build_dir)
        check_command(['make', 'install'], cwd=pri_build_dir)
        cpp = os.environ.get('CMAKE_PREFIX_PATH', '')
        if cpp and not cpp.endswith(':'):
            cpp += ':'
        cpp += install_dir
        # Build pkg1
        pkg1_build_dir = os.path.join(build_dirs, 'pkg1')
        os.makedirs(pkg1_build_dir)
        cmd = ['cmake', os.path.join(fixture_dir, 'pkg1'), install_option]
        check_command(cmd, cwd=pkg1_build_dir)
        check_command(['make', 'install'], cwd=pkg1_build_dir)
        # Build pkg2
        pkg2_build_dir = os.path.join(build_dirs, 'pkg2')
        os.makedirs(pkg2_build_dir)
        cmd = ['cmake', os.path.join(fixture_dir, 'pkg2'), install_option]
        check_command(cmd, cwd=pkg2_build_dir)
        check_command(['make', 'install'], cwd=pkg2_build_dir)

        # Now test the interface against the installed packages
        # Check for entry in packages
        resource_index = os.path.join(install_dir, 'share', 'resource_index')
        assert os.path.exists(resource_index), resource_index
        expected = sorted(['pkg1', 'pkg2'])
        actual = sorted(os.listdir(os.path.join(resource_index, 'packages')))
        assert expected == actual, (expected, actual)
        # Check for pkg1's "plugin" registry
        expected = ['pkg1']
        resource_dir = os.path.join(resource_index, 'plugin.rviz.display')
        actual = sorted(os.listdir(resource_dir))
        assert expected == actual, (expected, actual)
        marker_path = os.path.join(resource_dir, 'pkg1')
        with open(marker_path, 'r') as f:
            content = f.read()
            assert '../../pkg1/rviz_plugin.xml' in content, content
        referenced_file_path = os.path.join(
            os.path.dirname(marker_path), '..', '..', 'pkg1', 'rviz_plugin.xml')
        assert os.path.exists(referenced_file_path), referenced_file_path
        # Check pkg1's CONTENT_FILE example
        expected = ['pkg1']
        resource_dir = os.path.join(resource_index, 'test.content.file')
        actual = sorted(os.listdir(resource_dir))
        assert expected == actual, (expected, actual)
        marker_path = os.path.join(resource_dir, 'pkg1')
        with open(marker_path, 'r') as f:
            content = f.read()
            assert '#define TEST_DEFINE' in content, content
            assert '${TEST_CURLY_BRACES}' in content, content
            assert 'at symbol works' in content, content
