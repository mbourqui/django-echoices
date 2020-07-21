# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [2.8.0] - 2020.07.21
## Added
- Support for Django 3.0


## [2.7.0] - 2020.07.21
## Changed
- Visibility of `EChoiceMeta`, now accessible at the same package level as the other enums

### Removed
- Support for Python 3.4
- Support for Django 1.10


## [2.6.0] - 2018.06.03
### Removed
- Support for Django 1.9

### Fixed
- EChoice implements comparison methods instead of EOrderedChoice. Thus, field validators can be run, as the comparison
  is done on the EChoice.value property instead of the EChoice instance itself.
