---
name: brand-guidelines
description: Applies visual design standards including brand colors, typography, spacing, and UI component styling to front-end applications. Use for web apps, websites, or any visual interface requiring consistent design system, color schemes, style guidelines, or brand identity.
---

# Brand Styling Guidelines

## Overview

Use this skill to access brand identity and style resources for any front-end development including web applications, websites, presentations, and visual interfaces.

**Keywords**: branding, corporate identity, visual identity, styling, brand colors, typography, visual formatting, visual design, presentation, web development, front-end, UI/UX, design system

## Brand Guidelines

### Colors

**Theme Colors (Primary Palette):**

- Dark 1: `#000000` (RGB: 0, 0, 0) - Primary text color
- Light 1: `#FFFFFF` (RGB: 255, 255, 255) - White backgrounds and text on dark
- Dark 2: `#1F497D` (RGB: 31, 73, 125) - Navy blue for emphasis
- Light 2: `#EEECE1` (RGB: 238, 236, 225) - Light cream/tan background

**Accent Colors:**

- Accent 1 (Blue): `#4F81BD` (RGB: 79, 129, 189) - Primary accent
- Accent 2 (Red): `#C0504D` (RGB: 192, 80, 77) - Secondary accent
- Accent 3 (Green): `#9BBB59` (RGB: 155, 187, 89) - Tertiary accent
- Accent 4 (Purple): `#8064A2` (RGB: 128, 100, 162) - Additional accent
- Accent 5 (Teal): `#4BACC6` (RGB: 75, 172, 198) - Additional accent
- Accent 6 (Orange): `#F79646` (RGB: 247, 150, 70) - Additional accent

**Frequently Used Colors:**

- Gold/Amber: `#BF9000` (RGB: 191, 144, 0) - Section headers, highlighted shapes
- Medium Gray: `#666666` (RGB: 102, 102, 102) - Secondary text
- Dark Magenta: `#741B47` (RGB: 116, 27, 71) - Accent shapes
- Dark Teal: `#134F5C` (RGB: 19, 79, 92) - Accent elements
- Brown: `#783F04` (RGB: 120, 63, 4) - Accent elements
- Dark Green: `#274E13` (RGB: 39, 78, 19) - Accent elements
- Gray: `#888888` (RGB: 136, 136, 136) - Subtle elements
- Dark Slate: `#454D4E` (RGB: 69, 77, 78) - Bullet points
- Link Blue: `#4A7DBA` (RGB: 74, 125, 186) - Hyperlinks
- Dark Cyan: `#005A6F` (RGB: 0, 90, 111) - Footer/accent elements

**Hyperlink Colors:**

- Hyperlink: `#0000FF` (RGB: 0, 0, 255)
- Followed Hyperlink: `#800080` (RGB: 128, 0, 128)

### Typography

- **Headings**: Arial (theme major font)
- **Body Text**: Calibri (primary body font)
- **Code/Monospace**: Source Code Pro Medium (with Courier New fallback)
- **Theme Minor Font**: Arial

## Features

### Smart Font Application

- Applies Arial font to headings and titles
- Applies Calibri font to body text and bullet points
- Applies Source Code Pro Medium to code blocks and technical content
- Automatically falls back to Courier New if Source Code Pro unavailable
- Preserves readability across all systems

### Text Styling

- Titles/Headings: Arial font, typically 28pt
- Body text: Calibri font, typically 14-16pt
- Code blocks: Source Code Pro Medium, monospaced
- Smart color selection based on background (dark text on light, white text on colored shapes)
- Preserves text hierarchy and formatting

### Shape and Accent Colors

- Primary accent shapes use Gold/Amber (`#BF9000`) with white text
- Non-text shapes use theme accent colors
- Cycles through blue, red, green, purple, teal, and orange accents
- Maintains visual interest while staying on-brand

## Technical Details

### Font Management

- Uses Arial for headings (system font, broadly available)
- Uses Calibri for body text (Office standard font)
- Uses Source Code Pro Medium for code (embedded in template)
- Provides automatic fallback to Courier New for monospace content
- For best results, ensure Calibri and Source Code Pro fonts are installed

### Color Application

- Uses RGB color values for precise brand matching
- Applied via python-pptx's RGBColor class
- Theme colors referenced via scheme color names (dk1, lt1, accent1, etc.)
- Maintains color fidelity across different systems

### Color Usage Guidelines

| Element Type | Recommended Color | RGB Value |
|-------------|------------------|-----------|
| Slide background | Light 1 (White) | #FFFFFF |
| Primary text | Dark 1 (Black) | #000000 |
| Section headers | Gold/Amber | #BF9000 |
| Code backgrounds | Light (no fill) with Dark 2 border | #1F497D |
| Accent shapes | Accent 1-6 | Various |
| Secondary text | Medium Gray | #666666 |
