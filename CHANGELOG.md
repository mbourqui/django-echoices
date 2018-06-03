# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.6.0] - 2018-06-03
### Removed
- Support for Django 1.9

### Fixed
- EChoice implements comparison methods instead of EOrderedChoice. Thus, field validators can be run, as the comparison
  is done on the EChoice.value property instead of the EChoice instance itself.
