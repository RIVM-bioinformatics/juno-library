# Changelog

## [2.2.1](https://github.com/RIVM-bioinformatics/juno-library/compare/v2.2.0...v2.2.1) (2024-07-26)


### Bug Fixes

* also enlist ref for juno mapping ([c6856d6](https://github.com/RIVM-bioinformatics/juno-library/commit/c6856d688e06329673f6d4e0197a39a2f4152766))

## [2.2.0](https://github.com/RIVM-bioinformatics/juno-library/compare/v2.1.3...v2.2.0) (2024-07-25)


### Features

* allow list as input type ([254e1c8](https://github.com/RIVM-bioinformatics/juno-library/commit/254e1c81234acfded7873cffe06e6f7cebcc3e41))


### Bug Fixes

* fix typing ([a135eb9](https://github.com/RIVM-bioinformatics/juno-library/commit/a135eb975d5b8bd93132752f4a34023c8ee35d3d))
* force tuple ([46c3608](https://github.com/RIVM-bioinformatics/juno-library/commit/46c3608fe70ad00c578d945c19371227084f5580))
* switch input_type to tuple ([f406df2](https://github.com/RIVM-bioinformatics/juno-library/commit/f406df298b376e4ea014e581ccbf9012e8350990))

## [2.1.3](https://github.com/RIVM-bioinformatics/juno-library/compare/v2.1.2...v2.1.3) (2024-02-09)


### Bug Fixes

* catch error if sample has multiple libraries ([cff035a](https://github.com/RIVM-bioinformatics/juno-library/commit/cff035a1dc16add72246ce39e3be530f67efa2d9))
* error message ([b66b9d5](https://github.com/RIVM-bioinformatics/juno-library/commit/b66b9d59efe501ee4fd41568e1d5fb444acf2495))
* parse illumina library correctly ([2fd54a7](https://github.com/RIVM-bioinformatics/juno-library/commit/2fd54a71c61b9a25b91cc6f774f901325ad33cb3))

## [2.1.2](https://github.com/RIVM-bioinformatics/juno-library/compare/v2.1.1...v2.1.2) (2024-01-25)


### Bug Fixes

* restrict snakemake to v7 ([393726c](https://github.com/RIVM-bioinformatics/juno-library/commit/393726cf12846990a8eac4f09c646ac19c431752))

## [2.1.0](https://github.com/RIVM-bioinformatics/juno-library/compare/v2.0.1...v2.1.0) (2023-07-04)


### Features

* add enlisting of bam and reference ([4ef4be6](https://github.com/RIVM-bioinformatics/juno-library/commit/4ef4be65946f3c89809ebebe7335c97ec88e5cf1))
* add vcf input files for mapping pipelines ([cf98af3](https://github.com/RIVM-bioinformatics/juno-library/commit/cf98af3e269fefa3e686b4dc64899e94324e58e0))
* include vcf in tests ([cdcef21](https://github.com/RIVM-bioinformatics/juno-library/commit/cdcef21103362e4f0e2ddc7d0880eed2e54bcef9))


### Bug Fixes

* correct vcf directory name ([6512211](https://github.com/RIVM-bioinformatics/juno-library/commit/6512211364dfaa0b88c7bddd1a667b0324ef7de3))
* Fix juno_metadata not existing ([9a478dd](https://github.com/RIVM-bioinformatics/juno-library/commit/9a478ddbff7a8414bc81594d1b393b2c928b214c))
* fix unit test ([ba8eee1](https://github.com/RIVM-bioinformatics/juno-library/commit/ba8eee1c8bc25b69fe7de93c52bd6ebaeeae3c50))
* include vcf in checks ([3e73986](https://github.com/RIVM-bioinformatics/juno-library/commit/3e73986a258578b72792ab6a918e8bb3b2857e96))

## [2.0.1](https://github.com/RIVM-bioinformatics/juno-library/compare/v2.0.0...v2.0.1) (2023-04-18)


### Bug Fixes

* Make sure library also works in python 3.8 ([fb9e7f6](https://github.com/RIVM-bioinformatics/juno-library/commit/fb9e7f6bc58f33c9ee8c58032b8abe1d4ccb4a57))

## [2.0.0](https://github.com/RIVM-bioinformatics/juno-library/compare/v1.0.1...v2.0.0) (2023-03-23)


### ⚠ BREAKING CHANGES

* Move snakemake args to dict

### Features

* Add no-containers flag ([9a5e33a](https://github.com/RIVM-bioinformatics/juno-library/commit/9a5e33ade44dd60a349521e7093704a186a5d213))


### Bug Fixes

* Make filepaths absolute ([375c661](https://github.com/RIVM-bioinformatics/juno-library/commit/375c661d85c1716a3f3b25be4ba37bd005add5eb))


### Code Refactoring

* Move snakemake args to dict ([afcd5d8](https://github.com/RIVM-bioinformatics/juno-library/commit/afcd5d8557b02d728bd8c49de4d76a27dec3b5da))


### Documentation

* Add docstrings to new functions ([fec95b9](https://github.com/RIVM-bioinformatics/juno-library/commit/fec95b9f7a4f1031802e54e7509c7bcfe3f53b1d))


### Dependencies

* Update dependencies ([74db4f5](https://github.com/RIVM-bioinformatics/juno-library/commit/74db4f573deeb1a2f094dc65df3e6599e3c3cdeb))

## [1.0.1](https://github.com/RIVM-bioinformatics/juno-library/compare/v1.0.0...v1.0.1) (2023-02-02)


### Features

* Add py.typed ([d49c3a6](https://github.com/RIVM-bioinformatics/juno-library/commit/d49c3a6c196f82edc9cfcfd058e69a55546d7712))

## [1.0.0](https://github.com/RIVM-bioinformatics/juno-library/compare/v1.0.0...v1.0.0) (2023-02-02)


### ⚠ BREAKING CHANGES

* Remove class abstraction in helper_functions

### Features

* Add checks in github actions ([ff6e986](https://github.com/RIVM-bioinformatics/juno-library/commit/ff6e9864220cff18cce43f0c4fa6b4dca20fe294))
* Add mypy checking ([754fe4d](https://github.com/RIVM-bioinformatics/juno-library/commit/754fe4de00c41b00229989d75a104cd9147ca389))
* Add release please ([47e317b](https://github.com/RIVM-bioinformatics/juno-library/commit/47e317b3b459d325e59014c5f2b5870df81fca93))
* Add run script ([739d9d1](https://github.com/RIVM-bioinformatics/juno-library/commit/739d9d1ec141751d813fa87f4981934fd203fddf))


### Bug Fixes

* Add extra kwargs functionality to RunSnakemake ([14ef3e7](https://github.com/RIVM-bioinformatics/juno-library/commit/14ef3e7e84f1fca0ad7f615c9d2106798d13be95))
* Add kw_only=True for inheritance ([c88f33c](https://github.com/RIVM-bioinformatics/juno-library/commit/c88f33cc5915d82f570c0e32f108612d38689265))
* Add openpyxl stubs to github action ([6080082](https://github.com/RIVM-bioinformatics/juno-library/commit/60800822d18f86b215c726e323a4d5ff234604fd))
* Add RunSnakemake to __init__.py ([a3b288b](https://github.com/RIVM-bioinformatics/juno-library/commit/a3b288b9bd112984fbd075020b420db4ac1397e6))
* Add type stubs to github action ([2e0b2db](https://github.com/RIVM-bioinformatics/juno-library/commit/2e0b2dba574e03803b806a231bc26518b06389a4))
* Change regex to string literal ([c156c64](https://github.com/RIVM-bioinformatics/juno-library/commit/c156c64bd1a60d0d8d48479ec1d763601de70f29))
* Fix github actions ([9ec06fb](https://github.com/RIVM-bioinformatics/juno-library/commit/9ec06fb86c5157a78e98cf05580bb5942a6806d2))
* Fix library tests ([64a5f2a](https://github.com/RIVM-bioinformatics/juno-library/commit/64a5f2a0cccf28fd2900b73009acc0f370f666c9))
* Fix main env and library_tests ([0f21c89](https://github.com/RIVM-bioinformatics/juno-library/commit/0f21c89377eef2ad9f8fcad11b05e99449e9e8a1))
* Fix mypy checks ([554c676](https://github.com/RIVM-bioinformatics/juno-library/commit/554c6768d5f2719e69879963740c42465bb84497))
* Fix previous commit ([07e6d1f](https://github.com/RIVM-bioinformatics/juno-library/commit/07e6d1ff30d3f3473c03d6ec1b02dbccc321f6fa))
* Fix previous commit install ([9299279](https://github.com/RIVM-bioinformatics/juno-library/commit/9299279c35b7f124d7ae2d73b5b97723b7be561b))
* Fix setuptools versions in env ([93f215a](https://github.com/RIVM-bioinformatics/juno-library/commit/93f215a1407de81327f603d70435976289533f1e))
* Fix the main conda env ([5eda41c](https://github.com/RIVM-bioinformatics/juno-library/commit/5eda41c3e21120c28a5b161fe46b73a8811f85c0))
* Fix unit tests for github actions ([0009194](https://github.com/RIVM-bioinformatics/juno-library/commit/00091944c26acf3c448a83f10b25995f187be0e8))
* Fix up module structure ([4c9adb1](https://github.com/RIVM-bioinformatics/juno-library/commit/4c9adb1d642128eaa1cb38376991fd5f0d97a52c))
* Remove conda env in github action ([3087ee4](https://github.com/RIVM-bioinformatics/juno-library/commit/3087ee4f44db73becaf6aec7daad49ae18bf8260))
* Remove stuff from github action ([9890d45](https://github.com/RIVM-bioinformatics/juno-library/commit/9890d45aa155b453f0141195bededc036014144c))
* Update env location in github workflow ([b6b8fec](https://github.com/RIVM-bioinformatics/juno-library/commit/b6b8fec4ba8b2cc489b967d73de054d1e3203e5d))
* Update mamba version ([3686131](https://github.com/RIVM-bioinformatics/juno-library/commit/3686131bb9f181087fe94e6ad160bc64cf9e9236))
* Use mamba in github action ([247947b](https://github.com/RIVM-bioinformatics/juno-library/commit/247947bd428f13e05a30ab637629eca01c6389c9))


### Code Refactoring

* Remove class abstraction in helper_functions ([0f7b045](https://github.com/RIVM-bioinformatics/juno-library/commit/0f7b045fdab85c1fbcfb01e46d76d030de91c9e3))


### Miscellaneous Chores

* release 1.0.0 ([9c0b8fa](https://github.com/RIVM-bioinformatics/juno-library/commit/9c0b8faf37fa0e2f3fc60f6478ee6bea540f9f17))

## [1.0.0](https://github.com/RIVM-bioinformatics/juno-library/compare/v0.2.9...v1.0.0) (2023-02-01)


### ⚠ BREAKING CHANGES

* Remove class abstraction in helper_functions

### Features

* Add checks in github actions ([ff6e986](https://github.com/RIVM-bioinformatics/juno-library/commit/ff6e9864220cff18cce43f0c4fa6b4dca20fe294))
* Add mypy checking ([754fe4d](https://github.com/RIVM-bioinformatics/juno-library/commit/754fe4de00c41b00229989d75a104cd9147ca389))
* Add release please ([47e317b](https://github.com/RIVM-bioinformatics/juno-library/commit/47e317b3b459d325e59014c5f2b5870df81fca93))
* Add run script ([739d9d1](https://github.com/RIVM-bioinformatics/juno-library/commit/739d9d1ec141751d813fa87f4981934fd203fddf))


### Bug Fixes

* Add extra kwargs functionality to RunSnakemake ([14ef3e7](https://github.com/RIVM-bioinformatics/juno-library/commit/14ef3e7e84f1fca0ad7f615c9d2106798d13be95))
* Add kw_only=True for inheritance ([c88f33c](https://github.com/RIVM-bioinformatics/juno-library/commit/c88f33cc5915d82f570c0e32f108612d38689265))
* Add openpyxl stubs to github action ([6080082](https://github.com/RIVM-bioinformatics/juno-library/commit/60800822d18f86b215c726e323a4d5ff234604fd))
* Add RunSnakemake to __init__.py ([a3b288b](https://github.com/RIVM-bioinformatics/juno-library/commit/a3b288b9bd112984fbd075020b420db4ac1397e6))
* Add type stubs to github action ([2e0b2db](https://github.com/RIVM-bioinformatics/juno-library/commit/2e0b2dba574e03803b806a231bc26518b06389a4))
* Change regex to string literal ([c156c64](https://github.com/RIVM-bioinformatics/juno-library/commit/c156c64bd1a60d0d8d48479ec1d763601de70f29))
* Fix github actions ([9ec06fb](https://github.com/RIVM-bioinformatics/juno-library/commit/9ec06fb86c5157a78e98cf05580bb5942a6806d2))
* Fix library tests ([64a5f2a](https://github.com/RIVM-bioinformatics/juno-library/commit/64a5f2a0cccf28fd2900b73009acc0f370f666c9))
* Fix main env and library_tests ([0f21c89](https://github.com/RIVM-bioinformatics/juno-library/commit/0f21c89377eef2ad9f8fcad11b05e99449e9e8a1))
* Fix mypy checks ([554c676](https://github.com/RIVM-bioinformatics/juno-library/commit/554c6768d5f2719e69879963740c42465bb84497))
* Fix previous commit ([07e6d1f](https://github.com/RIVM-bioinformatics/juno-library/commit/07e6d1ff30d3f3473c03d6ec1b02dbccc321f6fa))
* Fix previous commit install ([9299279](https://github.com/RIVM-bioinformatics/juno-library/commit/9299279c35b7f124d7ae2d73b5b97723b7be561b))
* Fix setuptools versions in env ([93f215a](https://github.com/RIVM-bioinformatics/juno-library/commit/93f215a1407de81327f603d70435976289533f1e))
* Fix the main conda env ([5eda41c](https://github.com/RIVM-bioinformatics/juno-library/commit/5eda41c3e21120c28a5b161fe46b73a8811f85c0))
* Fix unit tests for github actions ([0009194](https://github.com/RIVM-bioinformatics/juno-library/commit/00091944c26acf3c448a83f10b25995f187be0e8))
* Fix up module structure ([4c9adb1](https://github.com/RIVM-bioinformatics/juno-library/commit/4c9adb1d642128eaa1cb38376991fd5f0d97a52c))
* Remove conda env in github action ([3087ee4](https://github.com/RIVM-bioinformatics/juno-library/commit/3087ee4f44db73becaf6aec7daad49ae18bf8260))
* Remove stuff from github action ([9890d45](https://github.com/RIVM-bioinformatics/juno-library/commit/9890d45aa155b453f0141195bededc036014144c))
* Update env location in github workflow ([b6b8fec](https://github.com/RIVM-bioinformatics/juno-library/commit/b6b8fec4ba8b2cc489b967d73de054d1e3203e5d))
* Update mamba version ([3686131](https://github.com/RIVM-bioinformatics/juno-library/commit/3686131bb9f181087fe94e6ad160bc64cf9e9236))
* Use mamba in github action ([247947b](https://github.com/RIVM-bioinformatics/juno-library/commit/247947bd428f13e05a30ab637629eca01c6389c9))


### Code Refactoring

* Remove class abstraction in helper_functions ([0f7b045](https://github.com/RIVM-bioinformatics/juno-library/commit/0f7b045fdab85c1fbcfb01e46d76d030de91c9e3))
