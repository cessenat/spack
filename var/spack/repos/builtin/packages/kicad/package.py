# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Kicad(CMakePackage):
    """KiCad is an open source software suite for Electronic Design
    Automation (EDA). The programs handle Schematic Capture, and PCB
    Layout with Gerber output."""

    homepage = 'https://kicad.org'
    url = 'https://gitlab.com/kicad/code/kicad/-/archive/5.1.8/kicad-5.1.8.bz2'
    maintainers = ['aweits']

    version('6.0.5', sha256='fc77bf07a9b9e7bb889208f9741d21134ad398391085d10d3cf4afd9204507ab')
    version('5.1.9', sha256='631941d9a7cf7627e2831d5634d77627453ca04536e4972fc7ae4bf192a979d6')
    version('5.1.8', sha256='81ab6c167c982b2c90506134b0ee7ea5f9d61aec59856887892644dc9bbb9346')

    depends_on('wxwidgets')
    depends_on('python@3:', type=('build', 'run'))
    # py-wxpython needs work
    # depends_on('py-wxpython', type=('build', 'run'))
    depends_on('glew')
    depends_on('gl')
    depends_on('glm')
    depends_on('boost@1.56:')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on('oce+X11')
    depends_on('swig', type='build')
    depends_on('curl')
    depends_on('pkgconfig')
    depends_on('git', type=('build', 'run'))
    depends_on('ngspice')
    depends_on('hicolor-icon-theme', type=('build', 'run'))
    depends_on('adwaita-icon-theme', type=('build', 'run'))
    depends_on('gsettings-desktop-schemas', type=('build', 'run'))

    extends('python')

    resource_list = [
        # version, resource, sha256sum
        ('5.1.8', 'footprints', '8937b5ba0f67844ffaca40632bebe9c2f4f17fba446137434aa72363c55d7dd9'),
        ('5.1.8', 'packages3D', '81e64939e922742431284bb19d1ec274d6dc10fd238e5583ead21dc08876c221'),
        ('5.1.8', 'symbols', '98cedcca4d7ad6e3be96ec5a41f8f9b3414eae276bac1efdfd3f8871f0f8bc7e'),
        ('5.1.8', 'templates', 'd64ca82854e9780413447a3fa82a528b264d39f57d467fddfc78f919e7ed15c5'),
        ('5.1.9', 'footprints', 'a86fbe00fccd6da2d29687ec0c56a9c3cb6b9748ee8fd35c1625839168f28edc'),
        ('5.1.9', 'packages3D', '35a4888dabd2dedb0d49c3e84b0eebc97b306200510e818dad90d4bb1c9e3296'),
        ('5.1.9', 'symbols', '6741a7b01f14f1f5aae3155a554816516cf02ce7790074ba8462dee8091f8c2f'),
        ('5.1.9', 'templates', 'bacf93567f8efe87314762448bb69698c8ed387058c13868c051c91740014aac'),
        ('6.0.5', 'footprints', 'd3cf9eb72ebac152548c7dd595725827c5f7b52ee2e96fe951ed41637a178bb5'),
        ('6.0.5', 'packages3D', 'af10545c315474495e8be2137f25172d16103430133e91437cd4cf4f9d382436'),
        ('6.0.5', 'symbols', '2ae9c33975510c8ffd89f0ad66f119e18e82bcafd02002f7bd30bbd369a46435'),
        ('6.0.5', 'templates', 'd296e77b8106d772ef6a31747fa2bbece51dd7975573a39c865ed075ce3aa91a'),
    ]

    for ver, lib, checksum in resource_list:
        resource(when='@{0}'.format(ver),
                 name=lib,
                 url='https://gitlab.com/kicad/libraries/kicad-{0}/-/archive/{1}/kicad-{0}-{1}.tar.bz2'.format(lib, ver),
                 sha256=checksum,
                 destination='',
                 )

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path('XDG_DATA_DIRS', self.prefix.share)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path('XDG_DATA_DIRS', self.prefix.share)

    def setup_build_environment(self, env):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)

    def setup_run_environment(self, env):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)

    def cmake_args(self):
        args = []
        args.append('-DKICAD_SCRIPTING_PYTHON3=ON')
        args.append('-DKICAD_SCRIPTING_WXPYTHON=OFF')
        return args

    @run_after('install')
    def install_libraries(self):
        for ver, lib, checksum in self.resource_list:
            if self.spec.version == Version(ver):
                with working_dir('kicad-{0}-{1}'.format(lib, ver)):
                    args = std_cmake_args
                    cmake(*args)
                    make('install')
