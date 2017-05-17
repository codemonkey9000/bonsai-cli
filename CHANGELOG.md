# Changelog

## 0.8.9
### Added
- Add this change log.

### Removed
- Remove nose2 config file.

## 0.8.8
### Added
- Add missing help message for `bonsai train start --remote`.
- Add a short help command for `bonsai log`.

## 0.8.7
### Fixed
- Fix an issue where a project file was uploaded with its local absolute
path instead of a path relative to the project root.

## 0.8.6
### Added
- Add the `bonsai log` command.

## 0.8.5
### Fixed
- Fix an issue that could cause file not found errors when using the
`--project` option with the `bonsai create` and `bonsai push` commands.

## 0.8.6
### Added
- Add the `bonsai push` command.

### Deprecated
- The `bonsai load` command is now deprecated. Use `bonsai push` instead.
