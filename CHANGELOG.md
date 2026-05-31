# Changelog

All notable changes to the **Monokai Faded** theme are documented here.
This project adheres to [Semantic Versioning](https://semver.org/).

## [1.1.1] - 2026-05-31

### Changed
- Updated README badges (license, GitHub release, Marketplace installs).

## [1.1.0] - 2026-05-31

A large refinement pass focused on a consistent, neutral UI with color
reserved for *meaning*, plus coverage for many editor surfaces that newer
VS Code versions added since the original release.

### Added
- **Bracket pair colorization** — a 6-color depth rainbow drawn from the theme
  accents (pink/orange/yellow/green/cyan/purple), with red for unmatched brackets.
- **Semantic highlighting** enabled (`semanticHighlighting`).
- **Markdown styling** — headings, bold, italic, strikethrough, links, blockquotes,
  and list markers (previously unstyled).
- **Editor overview ruler** marks for find, errors, warnings, and git add/modify/delete.
- Styling for previously-unstyled surfaces: **Peek View**, **sticky scroll**,
  **breadcrumbs**, **command palette**, find/hover/suggest **widgets**, indent
  guides, word-highlight, menus, and assorted misc keys.
- **Search match borders/visibility** tuning and **diff-editor** inserted/removed
  backgrounds for readable text on changed lines.

### Changed
- **Neutral UI chrome** — selections, hover, focus ring, buttons, badges, sliders,
  and widget backgrounds are now neutral greys/translucent veils. **Blue is reserved
  for meaning**: links, git-modified, and unsaved (dirty) tabs.
- **Accent blue desaturated** (`#568AF2` → `#5C89D6`) to fit the faded palette.
- **Diff / git colors unified** across the diff editor, gutter, minimap, and overview
  ruler — added = lime `#B5D93F`, deleted = `#D13B2E`.
- **Terminal ANSI** palette aligned to the syntax colors; fixed an invisible
  "bright black" (dim text) color.
- **Bracket match** and the active **scope guide** now use orange; the bracket-pair
  glyphs use the depth rainbow.
- **Input/dropdown/checkbox** controls unified to a dark recessed style.
- Line numbers, indent guides, and tree/list selection retuned for consistency.

### Fixed
- Corrected a malformed color value (`tab.unfocusedActiveModifiedBorder`) that was
  invalid and silently ignored by VS Code.
- Fixed low-contrast white-on-light text in info/warning input-validation messages.

## [1.0.4] - 2020-03-24
### Changed
- Updated various element colors; minor fixes.

## [1.0.3] - 2020-03-17
### Changed
- Updates and bug fixes.

## [1.0.2] - 2020-03-15
### Changed
- Color and metadata updates.

## [1.0.1] - 2020-03-13
### Changed
- Early fixes following the initial release.

## [1.0.0] - 2020-03-12
### Added
- Initial release — a faded Monokai interface and syntax theme for VS Code,
  based on the original Monokai theme by Wimer Hazenberg.
