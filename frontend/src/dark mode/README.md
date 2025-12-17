# Dark Mode Implementation

This folder contains all the dark mode functionality for the API Management System.

## Files

- **ThemeContext.js** - React context provider for theme management
  - Manages theme state (light/dark)
  - Persists theme preference in localStorage
  - Applies theme to document root via data-theme attribute

- **ThemeToggle.js** - Toggle switch component
  - Smooth animated toggle switch
  - Shows sun icon for light mode, moon icon for dark mode
  - Accessible with proper ARIA labels

- **ThemeToggle.css** - Styles for the toggle switch
  - Smooth transitions and animations
  - Theme-aware colors
  - Hover and focus states

## Color Scheme

### Light Mode
- Background: `#f5f5f5`
- Cards: `#ffffff`
- Text: `#333333`
- Accent: `#007bff`

### Dark Mode
- Background: `#1a1a1a`
- Cards: `#2d2d2d`
- Text: `#e0e0e0`
- Accent: `#007bff` (same)

## Usage

The theme is automatically applied when the app loads based on localStorage preference. Users can toggle between themes using the switch in the navbar.

## Features

✅ Theme persistence in localStorage
✅ Smooth transitions between themes
✅ CSS variables for easy theming
✅ WCAG AA compliant contrast ratios
✅ All components support dark mode
✅ Toast notifications support dark mode

