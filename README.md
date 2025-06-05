# Mollang IDE

A complete IDE for the Mollang esoteric programming language with comprehensive syntax highlighting support.

## Features

- **Complete Syntax Highlighting**: Supports all Mollang language constructs
  - Variables (`몰`, `모올`, `모오올`, etc.)
  - Control flow keywords (`은?행`, `털!자`, `돌!자`, `짓!자`)
  - Jump keywords (`가!자`, `가자!`)
  - I/O operations (`루`, `루?`, `루!`, `아`)
  - Function names and calls
  - Heap memory operations
  - String I/O patterns
  - Arithmetic and logical operators

- **Customizable Keywords**: Add, edit, and delete custom keyword categories
- **Configuration Management**: Save and load keyword configurations
- **Dark Theme**: Optimized for comfortable coding
- **Line Numbers**: With current line highlighting
- **Test Code Templates**: Quick access to sample code

## Architecture

The project follows clean architecture principles with clear separation of concerns:

```
mollang_ide/
├── core/                   # Core business logic
│   ├── __init__.py
│   ├── keywords.py        # Keyword definitions and management
│   ├── highlighter.py     # Syntax highlighting logic
│   └── config.py          # Configuration save/load
├── components/            # UI components
│   ├── __init__.py
│   ├── editor.py          # Code editor with line numbers
│   ├── dialogs.py         # Keyword configuration dialogs
│   └── main_window.py     # Main application window
├── constants.py           # Application constants
├── main.py               # Application entry point
└── README.md
```

## Design Principles

This project follows **Frontend Design Guidelines** for maintainable code:

### 1. Readability
- **Named Constants**: All magic numbers replaced with descriptive constants
- **Abstracted Logic**: Complex interactions separated into dedicated components
- **Clear Conditionals**: Complex logic split into focused, single-responsibility components

### 2. Predictability  
- **Consistent Returns**: All similar functions use standardized return types
- **Single Responsibility**: Functions only perform actions implied by their names
- **Descriptive Names**: Unique, clear names that indicate specific functionality

### 3. Cohesion
- **Feature Organization**: Code organized by domain (core logic vs UI components)
- **Related Logic**: Constants and related functionality kept together
- **Focused Modules**: Each module has a well-defined, single purpose

### 4. Coupling
- **Scoped State**: State management broken into focused, specific managers
- **Composition over Inheritance**: Component composition eliminates props drilling
- **Minimal Dependencies**: Each module depends only on what it needs

## Usage

### Running the IDE

```bash
python main.py
```

### Basic Operations

1. **Writing Code**: Type Mollang code in the main editor
2. **Syntax Highlighting**: All language constructs are automatically highlighted
3. **Keyword Management**: Use "키워드 설정" to customize highlighting
4. **Save Configuration**: Use "설정 저장" to save your keyword setup
5. **Load Configuration**: Use "설정 불러오기" to restore saved settings
6. **Test Code**: Use "간단 테스트" or "전체 테스트" for sample code

### Keyboard Support

- Standard text editing shortcuts (Ctrl+A, Ctrl+C, Ctrl+V, etc.)
- Syntax highlighting updates automatically as you type
- Line numbers update dynamically

### Customization

The IDE supports full customization of syntax highlighting:

1. Open keyword configuration dialog
2. Add new categories and keywords
3. Choose custom colors for each category
4. Save configurations for future use

## Mollang Language Support

### Variables
- `몰` - Basic variable
- `모올`, `모오올`, `모오오올...` - Extended variables

### Control Flow
- `은?행` - Conditional execution
- `털!자`, `돌!자`, `짓!자` - Loop controls
- `가!자`, `가자!` - Jump statements

### I/O Operations
- `루` - Basic output
- `루?` - Input
- `루!` - Formatted output
- `아` - Character I/O

### Functions
- `뭵뤩`, `말랑`, `머리`, `무릎`, `망령`, `매립`, `무리`, `밀랍` - Function names

### Memory Operations
- `몰*모올` - Heap access
- `몰~모올` - Heap manipulation
- `&몰~모올` - Heap length calculation

### String Operations
- `몰~몰루?` - String input
- `몰~몰루` - String output

## Development

### Adding New Features

1. **Core Logic**: Add to appropriate module in `core/`
2. **UI Components**: Create new components in `components/`
3. **Constants**: Add configuration to `constants.py`
4. **Integration**: Wire components together in main window

### Code Style

- Follow the established architecture patterns
- Use type hints where appropriate
- Document complex logic with docstrings
- Follow the Frontend Design Guidelines for consistency

## Dependencies

- **PySide6**: Qt-based GUI framework
- **Python 3.7+**: Modern Python features

## License

This project is provided as-is for educational and research purposes.
